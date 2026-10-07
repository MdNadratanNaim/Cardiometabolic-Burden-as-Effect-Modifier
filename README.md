# Cardiometabolic Burden as an Effect Modifier

Do cardiometabolic factors — hypertension, obesity, and diabetes — modify the effect of
socioeconomic status on anxiety and depressive symptoms among currently married women in
Bangladesh?

This repository contains the full, reproducible analysis pipeline for a cross-sectional study
using the **Bangladesh Demographic and Health Survey (BDHS) 2022**. Wealth is the exposure,
cardiometabolic burden (a 0–3 count of diabetes, hypertension, and obesity) is the hypothesized
effect modifier, and depression (PHQ-9) and anxiety (GAD-7) are the outcomes. Notebook 6 models both
versions of each outcome, the ordinal severity bands and the binary screens (score >= 10).
Everything is written in Python.

## Repository structure

```
├── notebooks/
│   ├── 1. Dataset Creation.ipynb              # Merge raw BDHS recode files into one dataset
│   ├── 2. Feature Engineering.ipynb           # Eligibility filter, recoding, final analytic CSV
│   ├── 3. Basic Inspection.ipynb              # Read-only checks on the final dataset
│   ├── 4. Exploratory Data Analysis.ipynb     # Missingness, selection, design-based descriptives,
│   │                                          #   bivariate screening, sparsity, GVIF
│   ├── 5. Confounder Selection.ipynb          # DAG-based, candidate-by-candidate adjustment sets
│   └── 6. Main Regression Analysis.ipynb      # 24 design-based models: all screen-significant
│                                              #   covariates, every outcome x Burden data type (Wealth x Burden)
├── tools/
│   ├── recode.py                              # Variable metadata (recode, clean_recode) + helpers
│   ├── regression.py                          # Design-based logistic and proportional-odds models, see below
│   └── survey.py                              # Design-based estimators (SurveyDesign), see below
├── docs/
│   └── Dictionary.md                          # Full raw-to-final variable dictionary
├── resources/
│   ├── full_dataset.csv                       # Raw merged sample (all interviewed women)
│   ├── depression-anxiety-dataset.csv         # Final analytic sample, both outcomes (same women)
│   └── visuals/                               # DAGs and the STROBE attrition diagram
├── pyproject.toml
└── uv.lock
```

## Data source

BDHS 2022, sourced from the World Bank Microdata Library (catalog entry 6290). Source recode
files (`REC01`, `REC11`, `REC22`, `REC31`, `REC32`, `REC71`, `REC91`, `RECH2`, `RECMTH`) are
merged on `CASEID` in Notebook 1. Raw source files are not included in this repository; obtain
them directly from the DHS Program / World Bank Microdata Library.

## Study population and sample size

The sample is restricted to **currently married women** (`S111A == 1`). Starting from 30,078
eligible (ever-married) women, 1,541 are excluded for not being currently married, and a further
23,650 are excluded for incomplete cardiometabolic biomarker components (the biomarker module was
administered to only a sub-sample of respondents — see `docs/Dictionary.md` and Notebook 4 for
the missingness-structure check confirming this is design-based, not item non-response). This
yields a **final analytic sample of n = 4,887**, identical for the depression and anxiety models.
See `resources/visuals/Main/Figure-2 (Biomarker structural attrition flow).svg` for the full
STROBE-style attrition diagram. Notebook 4 compares the analytic sample with the excluded women
and checks that the survey weights are adequate for the sub-sampled modules.

## Reproducing the pipeline

```bash
uv sync                 # or: pip install -e .
jupyter lab notebooks/
```

Run the notebooks in numeric order. Notebooks 1 and 2 write/overwrite `resources/full_dataset.csv`
and the final analytic CSV; the later notebooks read that output and can be re-run independently
once Notebook 2 has produced current output. Notebook 4 re-derives every analysis variable from the
raw columns and asserts that it reproduces the analytic file exactly.

## Survey-design helpers (`tools/survey.py`)

The BDHS is a stratified, two-stage cluster sample, and `statsmodels` cannot express
stratification. `tools/survey.py` provides `SurveyDesign`, which implements the Taylor-linearised
variance that `survey::svydesign(nest = TRUE)` and Stata's `svyset` use:

```python
from tools.survey import SurveyDesign

design = SurveyDesign(weights=df["Sampling weight"], psu=df["PSU"], stratum=df["Stratum"])
design.prop(df["Anxiety Binary"] == 1)            # proportion, SE, logit 95% CI
design.glm_test(y, X, "binomial")                 # weighted logistic/linear fit + design-based Wald test
design.glm_test(y, X, "binomial", domain=mask)    # subpopulation, keeping the full design
```

It was checked once against R 4.3.3 / `survey` 4.2.1 on this project's data (proportions,
standard errors, logit CIs, subpopulation estimates and weighted-regression Wald tests agree to
about 1e-5 relative difference; the weighted rank test agrees with `svyranktest` to about three
significant figures). R is not a dependency of this repository, and the check is not repeated here.
The module covers binomial and Gaussian GLMs; the regression models of Notebook 6 build on it in
`tools/regression.py`.

## Regression models (`tools/regression.py`)

A weighted logistic model and a weighted proportional-odds (cumulative-logit) model, both with the
stratified, PSU-clustered linearised variance of `SurveyDesign`. Single coefficients use a t
distribution on the design degrees of freedom and joint tests an F(k, ddf) Wald test, as
`survey::svyglm` does. No likelihood-ratio test, AIC or BIC is offered: with unequal weights the
pseudo-likelihood has no valid reference distribution.

```python
from tools.regression import fit_logit, fit_ordinal_logit

fit = fit_ordinal_logit(df["Anxiety"], X, design, list(X.columns))   # y coded 0..J-1; X = slope columns
fit.table()                                  # OR, 95% CI and design-based p for every slope
fit.wald(["Wealth × Burden"])                # joint design-based Wald F test
fit.contrast({"Wealth": 1, "Wealth × Burden": 0.66})   # a linear combination, e.g. a simple slope
```

`fit_logit` reproduces `SurveyDesign.glm_test` to about 1e-13, and `fit_ordinal_logit` reproduces the
coefficients of `statsmodels`' `OrderedModel` (same weights) to about 1e-8; Notebook 6 repeats both
checks on every run. All 24 models of Notebook 6 were also refitted once in R 4.3.3 / `survey` 4.2.1
(`svyolr` for the ordinal models, `svyglm` with a quasibinomial family for the logistic ones): the
largest coefficient difference was 9e-5 and the largest relative difference in a standard error 2e-5
for the ordinal models, and 4e-12 and 1e-6 for the logistic ones. R is not a dependency of this
repository, and that check is not repeated here.

## Key documentation

- `docs/Dictionary.md` — every raw BDHS variable, its final analysis-ready form, and the exact
  derivation logic, cross-referenced against `tools/recode.py`.
- `resources/visuals/Main/Figure-1 (Conceptual DAG).svg` — the simplified exposure/modifier/
  outcome DAG used in the main text.
- `resources/visuals/Supplementary/Supplementary Figure S1 (Full DAG).tex` — the full theoretical
  DAG underlying confounder selection.
- `resources/visuals/Supplementary/Supplementary Figure S2 (Half DAG).svg` — inclusion/exclusion
  reasoning for the reproductive-health covariates (mediator/collider/proxy-confounder calls).

## Status

Data creation, feature engineering, inspection, exploratory analysis (Notebook 4) and confounder
selection (Notebook 5) are in place. Notebook 6 fits 24 design-based models: four outcome versions
x three Burden data types (0-3 count, 0-2 merged, binary) x without and with the Wealth x Burden
interaction. Every model for an outcome carries all variables that were significant in Notebook 4's
bivariate screen, so only the data type of a variable changes between models. Its own "What this
notebook does not settle" section lists what remains open: the covariates come from the screen rather
than from Notebook 5's DAG, and the proportional-odds assumption is untested.

## Requirements

Python >= 3.12 (see `pyproject.toml` for pinned dependencies).
