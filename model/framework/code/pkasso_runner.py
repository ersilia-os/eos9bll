"""Run pKasso in mixed mode and reduce its output to a fixed set of columns.

pKasso (https://github.com/bindresearch/pkasso, v0.6.4) predicts the protonation
states of a molecule over a pH scan and derives its macroscopic pKa values from them.
It is run here as published, in mixed mode: MolGpKa together with the Uni-pKa model
retrained by the authors, using cross-validation fold 2 (the single-fold model the
authors recommend), on CPU, with pKasso's default tautomer search.

The Uni-pKa checkpoint is read from model/checkpoints/fold_2/checkpoint_best.pt. Its
sha256 matches the one pKasso expects, so nothing is downloaded at run time. The
MolGpKa weights ship with the pkasso package.
"""

import sys

import numpy as np
from pkasso.main import pKasso
from rdkit import Chem

# pH grid of pKasso's `scan` command and `scan_pH` function: 0 to 14 in steps of 0.25.
# The macroscopic pKa values are estimated from this scan.
SCAN_PHS = np.arange(0.0, 14.0 + 0.0001, 0.25, dtype=np.float64)

# pH values at which the net charge is reported: stomach, upper and lower small
# intestine, and blood.
CHARGE_PHS = np.array([1.2, 4.5, 6.8, 7.4], dtype=np.float64)

# pKasso reports each macroscopic pKa under the charge q it leads to: the transition
# from charge q + 1 to charge q. The columns cover +4 -> +3 down to -3 -> -4.
PKA_CHARGES = [3, 2, 1, 0, -1, -2, -3, -4]

PKA_COLUMNS = [
    "pka_p4_p3",
    "pka_p3_p2",
    "pka_p2_p1",
    "pka_p1_0",
    "pka_0_m1",
    "pka_m1_m2",
    "pka_m2_m3",
    "pka_m3_m4",
]
CHARGE_COLUMNS = [
    "net_charge_ph1_2",
    "net_charge_ph4_5",
    "net_charge_ph6_8",
    "net_charge_ph7_4",
]
# Net charge first: it has a value for every molecule pKasso processes, whereas most
# pKa steps are empty for any given molecule, and Ersilia's checks expect the first
# output column to be filled.
COLUMNS = CHARGE_COLUMNS + PKA_COLUMNS

DECIMALS = 4


def model_options(model_dir):
    """Return pKasso's model mapping for mixed mode with Uni-pKa fold 2 on CPU."""
    return {
        "molgpka": {},
        "unipka": {"folds": 2, "gpu": False, "model_dir": str(model_dir)},
    }


def _too_many_sites(ap):
    """Return True if pKasso skipped the molecule for having too many sites.

    Above `total_max_sites` (25) candidate sites pKasso returns the input molecule
    unchanged, so its pKa list is empty and its "net charge" is only the input's
    formal charge. That is not a prediction, so the row is left empty.
    """
    for context in ap.predictor_contexts:
        sites = set(context.acid_map_ids) | set(context.base_map_ids)
        if len(sites) > ap.total_max_sites:
            return True
    return False


def predict_one(smiles, options):
    """Return the 12 output values for one SMILES, NaN where there is no value."""
    row = np.full(len(COLUMNS), np.nan)
    mol = Chem.MolFromSmiles(smiles) if smiles else None
    if mol is None or mol.GetNumAtoms() == 0:
        # pKasso raises on unreadable SMILES but accepts an empty one as a molecule
        # with no atoms and net charge 0; neither is a prediction.
        print(f"Not a molecule: {smiles!r}", file=sys.stderr)
        return row
    ap = pKasso(smiles, model=options)
    scan = ap.run_scan(pHs=SCAN_PHS)
    if _too_many_sites(ap):
        print(f"pKasso skipped {smiles}: more than {ap.total_max_sites} protonation sites", file=sys.stderr)
        return row

    # Net charge at the reported pH values, from the same protonation-state
    # predictions as the scan above: pKasso's own pH-dependent step, without
    # predicting again. This keeps the pKa values exactly those of the default scan.
    charges = ap._finalize_scan(ap._scan_pH(CHARGE_PHS)).net_charges
    row[: len(CHARGE_COLUMNS)] = charges

    for i, q in enumerate(PKA_CHARGES):
        if q in scan.pkas_macro:
            row[len(CHARGE_COLUMNS) + i] = scan.pkas_macro[q]
    return row


def predict(smiles_list, options):
    """Return an array with one row per SMILES, in input order."""
    rows = []
    for smiles in smiles_list:
        try:
            rows.append(predict_one(smiles, options))
        except Exception as error:  # an unreadable molecule must not stop the batch
            print(f"pKasso failed on {smiles}: {type(error).__name__}: {error}", file=sys.stderr)
            rows.append(np.full(len(COLUMNS), np.nan))
    return np.round(np.array(rows, dtype=np.float64), DECIMALS)
