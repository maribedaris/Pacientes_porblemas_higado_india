# Template data science container - Notebooks

Project the notebooks. The naming convention is:

`[##.#]-[creator initials]-[short_description]-[yyyy_mm_dd].ipynb`

* `##.#` is the notebook number and version.
* `creator initials` are the initials of the person who created the notebook.
* `short_description` is a short `_` delimited description of the notebook.
* `yyyy_mm_dd` is the date the notebook was created.

Examples:

```text
01-jrz-data_exploration-2024_10_02.ipynb
02.1-jrz_data_raw_analysis-2024_10_08.ipynb
02.2-jrz_data_raw_analysis-2024_11_21.ipynb
```

## Folder structure

### Data

```text
data/
├── 01_raw/                   # Original data, without modifications
├── 02_intermediate/          # Data resulting from intermediate transformations
├── 03_primary/               # Data prepared for analysis and modeling
└── 04_reporting/             # Data and results prepared for reporting
```

### Notebooks

```text
notebooks/
├── 1-data                    # Data extraction and cleaning
├── 2-exploration             # Exploratory data analysis (EDA)
├── 3-analysis                # Statistical analysis and hypothesis testing
├── 4-feat_eng                # Feature engineering (creation, selection, and transformation)
├── 5-models                  # Model training, evaluation, and hyperparameter tuning
├── 6-interpretation          # Model interpretation
├── 7-deploy                  # Model packaging and deployment strategies
├── 8-reports                 # Storytelling, summaries, and analysis conclusions
└── notebook_template.ipynb
```
