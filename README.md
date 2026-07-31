# DR Layout Enrichment Cues

Official implementation of the paper

**Enriching Dimensionality Reduction with Distortion Cues**

(Computers & Graphics, 2026)

---

## Overview

Dimensionality Reduction (DR) techniques such as **t-SNE** and **UMAP** are widely used for visualizing high-dimensional data. However, the resulting low-dimensional layouts often introduce distortions that can lead to misleading interpretations.

This repository contains the implementation of the geometry-based layout enrichment methodology proposed in the paper. Instead of modifying the dimensionality reduction algorithm itself, the proposed method enriches existing DR layouts with geometric cues derived from the original high-dimensional space, allowing users to better interpret projection distortions and relationships between data samples. :contentReference[oaicite:0]{index=0}

The repository includes:
- the source code for the proposed methodology,
- the datasets or dataset-loading procedures used in the experiments,
- notebooks for interactive exploration and complete experimental analysis,
- and a parameter-free script for reproducing the representative result selected for the replicability evaluation.


---

## Main Features

- Geometry-based layout enrichment for dimensionality reduction visualizations
- Delaunay triangulation-based interpolation
- Distortion cue visualization
- Sensitivity and rank-shift analysis
- Support for multiple dimensionality reduction techniques (e.g., t-SNE and UMAP)
- Reproducible notebooks used in the paper for complete results
- Reproducibility script for Figure 5

## Representative Result for Replicability Evaluation

**Figure 5** of the paper was selected as the representative result for the replicability evaluation.

The representative result can be reproduced using the parameter-free script:

```text
script_figure_5.py
```

After installing the dependencies, run the following command from the repository root:

```bash
poetry run python script_figure_5.py
```
The generated figure is saved to:

```bash
outputs/figure_5.png
```

---

## Repository Structure

```text
dr_layout_enrichment_cues/
│
├── datasets/                          # Example datasets used in the experiments
├── results/Figure_5/                           # Generated figures and results
│
├── src/
│   └── distortion_cues/               # Core implementation of the proposed method
│       ├── ...
│
├── script_figure_5.py                 # Reproduces representative Figure 5
├── main_projection_analysis.ipynb     # Main notebook reproducing the methodology
├── sensitivity_and_ranks_shift_analysis.ipynb
│                                      # Robustness and sensitivity analysis
├── plots.ipynb                        # Figure generation
│
├── config.py                          # Project configuration
├── pyproject.toml                     # Poetry dependencies
├── README.md
├── submission_info.txt                # Replicability submission information
├── LICENSE                            # Software license
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<username>/dr_layout_enrichment_cues.git

cd dr_layout_enrichment_cues
```

Install the dependencies

```bash
poetry install
```

Activate the virtual environment

```bash
poetry shell
```

```bash
poetry run python script_figure_5.py
```

Launch Jupyter

```bash
jupyter notebook
```

---

## Running the Experiments

The experiments presented in the paper can be reproduced using the provided notebooks.

### Main analysis

```text
main_projection_analysis.ipynb
```

Runs the complete pipeline, including

- loading datasets,
- dimensionality reduction,
- construction of Delaunay triangulation,
- computation of distortion cues,
- layout enrichment,
- visualization.

### Sensitivity Analysis

```text
sensitivity_and_ranks_shift_analysis.ipynb
```

Contains the robustness experiments presented in the supplementary material, including sensitivity and rank-shift analyses.

### Plot Generation

```text
plots.ipynb
```

Generates the figures used throughout the paper.

---

## Reproducing the Paper

Running the notebooks in the following order reproduces the analyses presented in the paper:

1. `main_projection_analysis.ipynb`
2. `sensitivity_and_ranks_shift_analysis.ipynb`
3. `plots.ipynb`

---

## Package Organization

The core implementation is located in

```text
src/distortion_cues/
```

This package contains the reusable implementation of the proposed methodology, including functions for

- Delaunay triangulation
- edge interpolation
- distortion computation
- visualization utilities
- helper functions

The notebooks mainly orchestrate experiments while the implementation resides inside the package.

---

## Data Availability

The datasets required for the experiments are located under:

```text
datasets/
```

## Requirements

- Python 3.12
- Poetry
- Jupyter Notebook or JupyterLab

## Tested Environment

The representative reproduction procedure was tested using:

- **Operating system:** Windows 11
- **Python version:** Python 3.12
- **Hardware:** CPU only
- **GPU:** Not required
- **Specialized hardware:** Not required

To check the installed Poetry version, run:

```bash
poetry --version
```

---

## Citation

If you use this code in your research, please cite:

```bibtex
Citation will be added after publication.
```

---

## License
