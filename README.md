# Macroscopic pKa and Protonation States

Predicts whole-molecule (macroscopic) pKa values and the pH-dependent net charge of small molecules with pKasso from Bind Research. Site pKa predictions from MolGpKa and a Uni-pKa model retrained with IUPAC data are combined into populations of every protonation state. On six experimental benchmarks this mixed mode, with the single Uni-pKa fold run here on CPU, gives a mean absolute error of 0.61 pKa units. Validated only on small organic molecules; the input tautomer is kept for all states, and state populations are checked only qualitatively.

This model was incorporated on 2026-11-25.
Last packaged on 2026-11-27.

## Information
### Identifiers
- **Ersilia Identifier:** `eos9bll`
- **Slug:** `pkasso`

### Domain
- **Task:** `Annotation`
- **Subtask:** `Property calculation or prediction`
- **Biomedical Area:** `Any`
- **Target Organism:** `Any`
- **Tags:** `pKa`, `ADME`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `12`
- **Output Consistency:** `Fixed`
- **Interpretation:** Net charge at pH 1.2, 4.5, 6.8, 7.4, plus macroscopic pKa for each net-charge step from +4 to -4.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| net_charge_ph1_2 | float | high | Predicted average net charge at pH 1.2 derived from the predicted protonation states |
| net_charge_ph4_5 | float | high | Predicted average net charge at pH 4.5 derived from the predicted protonation states |
| net_charge_ph6_8 | float | high | Predicted average net charge at pH 6.8 derived from the predicted protonation states |
| net_charge_ph7_4 | float | high | Predicted average net charge at pH 7.4 derived from the predicted protonation states |
| pka_p4_p3 | float | high | Macroscopic pKa for the step from net charge +4 to +3 (empty if no such step is predicted) |
| pka_p3_p2 | float | high | Macroscopic pKa for the step from net charge +3 to +2 (empty if no such step is predicted) |
| pka_p2_p1 | float | high | Macroscopic pKa for the step from net charge +2 to +1 (empty if no such step is predicted) |
| pka_p1_0 | float | high | Macroscopic pKa for the step from net charge +1 to 0 (empty if no such step is predicted) |
| pka_0_m1 | float | high | Macroscopic pKa for the step from net charge 0 to -1 (empty if no such step is predicted) |
| pka_m1_m2 | float | high | Macroscopic pKa for the step from net charge -1 to -2 (empty if no such step is predicted) |

_10 of 12 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos9bll](https://hub.docker.com/r/ersiliaos/eos9bll)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos9bll.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos9bll.zip)
- **Apptainer**: [https://models-sif.s3.eu-north-1.amazonaws.com/eos9bll_v1.sif](https://models-sif.s3.eu-north-1.amazonaws.com/eos9bll_v1.sif)

### Resource Consumption
- **Model Size (Mb):** `546`
- **Environment Size (Mb):** `1735`
- **Image Size (Mb):** `927.87`

**Computational Performance (seconds):**
- 10 inputs: `33.75`
- 100 inputs: `-1`
- 10000 inputs: `-1`

### References
- **Source Code**: [https://github.com/bindresearch/pkasso](https://github.com/bindresearch/pkasso)
- **Publication**: [https://doi.org/10.26434/chemrxiv.15011954/v1](https://doi.org/10.26434/chemrxiv.15011954/v1)
- **Publication Type:** `Preprint`
- **Publication Year:** `2026`
- **Ersilia Contributor:** [TiagoJanela](https://github.com/TiagoJanela)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [Non-commercial](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos9bll
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos9bll
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
