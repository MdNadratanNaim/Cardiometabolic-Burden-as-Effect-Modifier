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

## Still open (not addressed — flagged, not fixed)

- Sentinel-code exclusion (`SB267` 994/996, `HA40` 9999) was fixed in Notebook 2 in an earlier
  round; re-verified via full re-execution but not re-audited against the official BDHS 2022
  biomarker codebook for `SB267` specifically (it's a country-specific extended-module variable,
  not in the standard cross-country DHS recode manual). Worth a final manual check before
  submission — this needs the official codebook, not something resolvable from within this repo.

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

`Insurance`'s complete separation, flagged above as "not yet resolved," **is now resolved** —
see the session below.

---

## ✅ Resolved (this session)

A follow-up review (`BDHS_Review_Resolutions_and_Methods_Outline.md`) turned the R-integration
cross-check's open items into a concrete list. All of it is now implemented, executed, and
verified in both `5. Main Regression Analysis.ipynb` and `5. Main Regression Analysis (R).ipynb`,
plus a lighter pass over `4. Exploratory Data Analysis.ipynb`.

**Adjustment-set changes:**
- `Insurance` dropped from the primary covariate set entirely (11 covariates, not 12) — complete
  separation on both outcomes, confirmed harmless to drop (LR-test p-values move by ~0.01-0.02).
- `Partner occupation = Don't know` (depression) and `Wealth=Poorest x Burden_collapsed=2+`
  (anxiety, newly identified) are reported as "not estimable" rather than the spurious OR = 0.000
  complete separation produces, in both notebooks.
- `Financial Decision-Making` and `IPV Attitude` tested together as a 13-covariate sensitivity
  model (both notebooks, "extended covariate set" section) rather than left open — neither the
  interaction finding nor the EPV picture changes meaningfully, so both stay out of the primary
  11-covariate set per the DAG reasoning in Notebook 4 Section 5.1.

**New diagnostics added (Python notebook primarily; ported to R where it's a design-based
question rather than a Python-tooling gap):** goodness-of-fit (exploratory weighted
Hosmer-Lemeshow in Python; `estat gof` added to the Stata replication block as the validated
version), linearity of the Burden term, events-per-variable disclosure, multiple-testing
correction (two framings — pre-specified-primary-only vs. all four tests run), E-values for the
headline estimates, an outcome-cutoff sensitivity check (PHQ-9 >= 15), a sampling-weight range
check, and Cook's-distance influence diagnostics.

**Figures:** `Figure-1` updated to "n = 11 covariates". `Supplementary Figure S1 (Full DAG).tex`
— `Insurance` now styled dashed/grey like `MaritalStatus`, with its own footnote; a new
`FinancialDecisionMaking` node added with a dashed, undirected edge to `Wealth` (direction
deliberately unasserted — that's the ambiguity in question) and a solid edge to `MentalHealth`.
`Supplementary Figure S2 (Half DAG).svg` — `Financial decisions` added to the reproductive-health
taxonomy, styled as "Exclude from primary model" with an "Ambiguous — excluded" sub-label (neither
"Collider" nor "Mediator" cleanly applies, so it gets its own reason rather than being forced into
an existing bucket).

**A second, independent review** of the same repo raised five more points, checked against the
actual code rather than taken at face value:
- *"Ever-married vs. currently-married population"* — not a real inconsistency. BDHS's frame is
  ever-married by design (30,078); Notebook 2 has a deliberate, explicit "Selection of currently
  married Women" step narrowing to 28,537, load-bearing for several covariates (Partner
  occupation, Household Autonomy, IPV Attitude all require a co-resident husband). `README.md`
  already documented this correctly; `Dictionary.md` and Notebook 4 now state it explicitly too.
- *"Dyslipidemia missing from the burden score"* — confirmed via `tools/recode.py` (which maps
  every BDHS variable touched anywhere in the pipeline) that no lipid/cholesterol variable exists
  anywhere in the extract. BDHS's biomarker module doesn't collect a lipid panel. Documented in
  `Dictionary.md` Part A2 so this doesn't get re-flagged.
- Weighted prevalence with a design-aware CI, an eligible-vs-analytic-sample representativeness
  comparison (wealth/age/division), and a note on the ordinal-outcome-model extension were added
  to Notebook 4 as reasonable EDA completeness suggestions.
- Everything else in that review (R-as-authoritative, omnibus-test-before-simple-slopes, the
  Model 1c nesting fix, sparse-cell handling, bootstrap-as-cross-check-not-primary) matched what
  this session already implements.

---
