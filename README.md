# Cardiometabolic Burden as an Effect Modifier

Do cardiometabolic factors — hypertension, obesity, and diabetes — modify the effect of
socioeconomic status on anxiety and depressive symptoms among currently married women in
Bangladesh?

This repository contains the full, reproducible analysis pipeline for a cross-sectional study
using the **Bangladesh Demographic and Health Survey (BDHS) 2022**. Wealth is the exposure,
cardiometabolic burden (a 0–3 count of diabetes, hypertension, and obesity) is the hypothesized
effect modifier, and depression (PHQ-9) and anxiety (GAD-7) are the outcomes, analyzed as two
parallel survey-weighted logistic regression models.

## Repository structure

```
├── notebooks/
│   ├── .Rprofile                              # Activates renv for R kernel launches (see below)
│   ├── 1. Dataset Creation.ipynb              # Merge raw BDHS recode files into one dataset
│   ├── 2. Feature Engineering.ipynb           # Eligibility filter, recoding, final analytic CSVs
│   ├── 3. Basic Inspection.ipynb              # Read-only checks on the final datasets
│   ├── 4. Exploratory Data Analysis.ipynb     # Missingness structure, GVIF, descriptive summary
│   ├── 5. Main Regression Analysis.ipynb      # Python: model-building, sparse-cell diagnostics
│   └── 5. Main Regression Analysis (R).ipynb  # R: design-based inference (survey::svyglm)
├── tools/
│   └── recode.py                          # Variable metadata (recode, clean_recode) + helpers
├── docs/
│   ├── Dictionary.md                      # Full raw-to-final variable dictionary
│   └── to_fix.md                          # Running audit trail of issues found/resolved
├── resources/
│   ├── full_dataset.csv                   # Raw merged sample (all interviewed women)
│   ├── depression_dataset.csv             # Final analytic sample, depression outcome
│   ├── anxiety_dataset.csv                # Final analytic sample, anxiety outcome
│   └── visuals/                           # DAGs and the STROBE attrition diagram
├── renv/                                  # renv's own bookkeeping (activate.R, settings.json)
├── renv.lock                               # Pinned R package versions -- the "uv.lock" of R
├── DESCRIPTION                             # Explicit R dependency list -- the "pyproject.toml" of R
├── .Rprofile                               # Activates renv when R starts at the repo root
└── pyproject.toml
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
STROBE-style attrition diagram.

## Reproducing the pipeline

```bash
uv sync                 # or: pip install -e .
jupyter lab notebooks/
```

Run the Python notebooks in numeric order (1 → 4), then either `5. Main Regression Analysis.ipynb`
(Python) or `5. Main Regression Analysis (R).ipynb` (R) — they're independent of each other and
both read the same final analytic CSVs. Notebooks 1 and 2 write/overwrite `resources/full_dataset.csv`
and the two final analytic CSVs; Notebooks 3, 4, and both Notebook 5 variants are read-only and can
be re-run independently once Notebook 2 has produced current output.

### Setting up R (the `renv` equivalent of `uv sync`)

R dependencies are pinned in `renv.lock`, the same role `uv.lock` plays for Python. From the repo
root:

```r
install.packages("renv")   # one-time, if renv itself isn't installed yet
renv::restore()             # installs the exact pinned package versions from renv.lock
```

Then register the R kernel with Jupyter (also one-time):

```r
IRkernel::installspec(name = "ir", displayname = "R")
```

`renv::restore()` reads `renv.lock` and installs into a project-local library at `renv/library/`
(analogous to `.venv/`) — it does not touch any other R project on the machine. `renv/library/`
is git-ignored, same as `.venv/`; only `renv.lock`, `renv/activate.R`, and `renv/settings.json`
are committed. `.Rprofile` (both at the repo root and inside `notebooks/`, since Jupyter launches
the R kernel with its working directory set to wherever the `.ipynb` lives) auto-activates the
project library every time R starts in this project — no manual `renv::load()` needed day to day.

To add a new R package: `renv::install("packagename")` then `renv::snapshot()` to update the
lockfile, exactly like `uv add packagename`.

## Key documentation

- `docs/Dictionary.md` — every raw BDHS variable, its final analysis-ready form, and the exact
  derivation logic, cross-referenced against `tools/recode.py`.
- `docs/to_fix.md` — running audit trail of issues found and resolved across review sessions.
- `resources/visuals/Main/Figure-1 (Conceptual DAG).svg` — the simplified exposure/modifier/
  outcome DAG used in the main text.
- `resources/visuals/Supplementary/Supplementary Figure S1 (Full DAG).tex` — the full theoretical
  DAG underlying confounder selection for the 12-covariate GVIF-validated adjustment set.
- `resources/visuals/Supplementary/Supplementary Figure S2 (Half DAG).svg` — inclusion/exclusion
  reasoning for the reproductive-health covariates (mediator/collider/proxy-confounder calls).

## Python + R

This project is polyglot by design: Python (`pandas`, `statsmodels`) handles data creation,
feature engineering, and exploratory model-building; R (`survey`) handles the final regression
inference, since `statsmodels` has no equivalent to a stratified-multistage survey design object.
Both live in `notebooks/` as Jupyter notebooks — the R ones run on the `ir` kernel (`IRkernel`),
installed alongside the Python kernel so both notebook types open and execute the same way.

**R dependencies** are pinned in `renv.lock` (see "Setting up R" above) — 31 packages total,
headlined by `survey` (4.2-1) and `IRkernel` (1.3.2) on R 4.3.3. `IRkernel` is tracked as a real
project dependency, not just a system convenience: `renv` inferred it directly from the R
notebook's Jupyter kernel metadata, since without it the notebook can't execute at all. (`renv`
was bootstrapped in this environment by installing R 4.3.3 and the packages above via `apt`, then
running `renv::hydrate()` to link them into a project-local library and `renv::snapshot()` to
lock exact versions — an offline-friendly path used only because this sandbox has no CRAN access.
On a normal machine, `renv::restore()` alone is sufficient; see "Setting up R" above.)

**Why both, rather than migrating fully to R:** point estimates (odds ratios) are identical
regardless of language — both maximize the same weighted pseudo-likelihood. What differs is the
variance estimator: `statsmodels`' cluster-robust covariance is explicitly flagged by the library
itself as *"not fully supported"* when combined with weights, and has no way to express
stratification at all. R's `svydesign(id=~PSU, strata=~Stratum, weights=~Sampling.weight,
nest=TRUE)` does both correctly. Cross-checking the two languages against each other on this
project already caught two real issues once (see `docs/to_fix.md`): an invalid non-nested model
comparison that `statsmodels` didn't flag but R's `anova.svyglm` refused to run, and a
completely-separated covariate category (`Insurance = Yes`, 0 events in both outcomes) that
needed a systematic check to surface.

## Status

Data creation, feature engineering, exploratory analysis, and the main survey-weighted logistic
regression (wealth × cardiometabolic burden interaction, both Python and R versions) are
complete. Two known open items before manuscript-ready numbers: the `Insurance` separation issue
above, and confirming the PHQ-9/GAD-7 ≥10 binarization cutoff is the intended one (see
`5. Main Regression Analysis.ipynb`, Section 2).

## Requirements

Python ≥ 3.12 (see `pyproject.toml` for pinned dependencies) and R ≥ 4.3 with the `survey`
package (see "Python + R" above).
