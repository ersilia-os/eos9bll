# imports
import os
import sys

import numpy as np
from ersilia_pack_utils.core import read_smiles, write_out

# current file directory, and the checkpoints folder
root = os.path.dirname(os.path.abspath(__file__))
checkpoints = os.path.abspath(os.path.join(root, "..", "..", "checkpoints"))

sys.path.insert(0, root)
from pkasso_runner import COLUMNS, model_options, predict  # noqa: E402

# small molecule used to load the Uni-pKa model once, in load_tool()
WARMUP_SMILES = "CC(=O)O"


# load the model once: pKasso keeps the Uni-pKa model in memory for the rest of the
# process, so it is loaded here rather than on the first molecule of a batch.
# When served, Ersilia calls this once and keeps the result in memory between batches.
def load_tool():
    options = model_options(checkpoints)
    predict([WARMUP_SMILES], options)
    return options


# run the model on one batch: read the input file, predict, write the output file.
def run_tool(model, input_file, output_file):
    # read SMILES from the input file
    _, smiles_list = read_smiles(input_file)

    # run pKasso on each molecule; a molecule it cannot process gets an empty row
    outputs = predict(smiles_list, model)

    # check input and output have the same length
    assert len(smiles_list) == len(outputs)

    # missing values as None: blank cells in a .csv output, as in Ersilia's own output,
    # and NaN in a .bin output
    outputs = [[None if np.isnan(v) else float(v) for v in row] for row in outputs]

    # write the output file
    write_out(outputs, COLUMNS, output_file, np.float32)


if __name__ == "__main__":
    # parse arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    run_tool(load_tool(), input_file, output_file)
