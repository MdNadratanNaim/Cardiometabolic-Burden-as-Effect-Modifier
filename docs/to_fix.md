## ✅ Resolved

All items below were open as of the last review pass and are now fixed, verified against a real
end-to-end execution of Notebooks 2–4 (zero errors).

### Stale report artifacts

- **`Figure-2 (Biomarker structural attrition flow).svg`** — regenerated as a 4-step flow with
  current numbers: 30,078 eligible → −1,541 (5%) not currently married → 28,537 → −23,650 (83%)
  incomplete biomarkers → **final n = 4,887**. The previously-missing "not currently married"
  exclusion step is now shown explicitly.
- **`Figure-1 (Conceptual DAG).svg`** — "n = 13 covariates" corrected to "n = 12 covariates" in
  both the label and the `<desc>`, matching the GVIF-validated adjustment set in Notebook 4.
- **`Supplementary Figure S1 (Full DAG).tex`** — `MaritalStatus` node now styled dashed/grey with
  an asterisk, plus a caption note: "Controlled by design, not by adjustment: sample eligibility
  is restricted to currently married women, so MaritalStatus is constant in the analytic data and
  is excluded from all fitted models." Compiles cleanly with `pdflatex` (verified).

### Dictionary.md completeness gaps

- **`V501` and `V026`** added to Part C, each with a one-line note on why it's retained but
  unmapped. (`V501` vs. `S111A` agreement was verified empirically: 100% concordant.)
- **Grammar drift** — `recode.py`'s `clean_recode["Cardiometabolic Burden"]` now uses "Two
  burdens"/"Three burdens" (plural), matching `Dictionary.md`.
- **Missing Survey design weights** — the Part B Survey Design section and diagram now show all
  four variables actually retained in the final analytic datasets (`CASEID`, `Sampling weight`,
  `PSU`, `Stratum`), replacing the stale `Cluster`/`V001` reference. A note was added to Part A18
  cross-referencing that `V001` is verified identical to `V021` but is not carried into the final
  CSVs.
- Fixed "Survery Design" → "Survey Design" typo.

### Notebook/pipeline hygiene

- **Notebook 3** no longer performs any data mutation — the Religion mode-imputation step was
  removed entirely as a downstream consequence of the `religion()` fix (code 96 is now correctly
  routed to "Others" rather than treated as missing, so there is nothing left to impute).
  Confirmed via fresh execution: `Religion` missingness = 0 in both datasets.
- **Notebook 1** — `evermarried_cols` renamed to `marital_status_cols` (and its one usage
  updated); adjacent typos `marrage_cols` → `marriage_cols` and `alcohol_coils` → `alcohol_cols`
  fixed while in the same cell.
- **`README.md`** — was empty, now has a full overview, repo structure, data source, sample-size/
  attrition summary, reproduction steps, and status section.
- **Bonus fix (found during verification, not in the original list):** Notebook 4's "Summary of
  Findings" cell still said "Sample size dropped from 5,137 to 4,891... except the single
  previously-imputed Religion case" — stale on both counts after the sentinel-code and Religion
  fixes. Updated to state the current, correct cascade (30,078 → 4,887) and the corrected
  Religion-96 finding.

---

## Still open (not addressed in this pass — flagged, not fixed)

- Finding A in Notebook 4's summary ("Documentation note only — confirm §2.7 covers this")
  references a section number that doesn't exist in this notebook. Left as-is since it may refer
  to a manuscript section outside this repo — worth confirming with whoever is drafting Methods.
- Sentinel-code exclusion (`SB267` 994/996, `HA40` 9999) was fixed in Notebook 2 in the prior
  round; re-verified here via full re-execution but not re-audited against the official BDHS 2022
  biomarker codebook for `SB267` specifically (it's a country-specific extended-module variable,
  not in the standard cross-country DHS recode manual). Worth a final manual check before
  submission.
- `Wealth=Poorest × Burden=3` thin interaction cell (Notebook 4, Finding D) — still open, DAG
  decision on `Financial Decision-Making`'s place in the adjustment set — still open.

---

## R integration (this session)

R 4.3.3 + `survey` 4.2-1 + IRkernel 1.3.2 installed and registered as a genuine Jupyter kernel
(`ir`), alongside the existing Python kernel. `5. Main Regression Analysis (R).ipynb` replicates
the Python regression notebook using `svydesign(id=~PSU, strata=~Stratum, weights=~Sampling.weight,
nest=TRUE)` + `svyglm(family=quasibinomial())` -- genuine design-based inference, not the
cluster-only approximation `statsmodels` provides.

**Two real issues this cross-check surfaced, both now fixed in both notebooks:**

1. **Invalid non-nested model comparison.** The original "Model 1 vs Model 3" test compared
   models using different parameterizations of Burden (linear vs. collapsed categorical) via a
   plain deviance-difference test. `statsmodels` didn't flag this as invalid; R's
   `survey::anova.svyglm` refused outright ("models not nested"). Fixed in both notebooks by
   adding **Model 1c** (main effects with `Burden_collapsed`, matching Model 3's parameterization)
   as the correct nested comparator.
2. **`Insurance = Yes` is completely separated from both outcomes** (0 events out of 16 women,
   for both Depression and Anxiety) -- not merely sparse like `Partner occupation = Don't know`,
   but structurally non-identifiable via standard MLE in either language. Both notebooks now
   include an explicit zero-event covariate check that surfaces this. **Not yet resolved** --
   options are dropping Insurance from the adjustment set, or refitting with Firth's
   penalized-likelihood logistic regression (R: `logistf`, though combining it with `svydesign`
   is nonstandard and would need its own methodological justification).

**Cross-validation result:** point estimates matched closely between languages (e.g. the
`Wealth=Richer x Burden(2+)` term: OR = 0.028 in both). Qualitative conclusions were identical
after the fix: Depression shows a significant collapsed-Burden interaction (R: p = 0.028; Python:
p = 0.017) but not a linear one (R: p = 0.292; Python: p = 0.182); Anxiety shows no interaction
in either coding. R's p-values are consistently a bit higher/more conservative than Python's,
consistent with properly incorporating stratification rather than clustering alone.
