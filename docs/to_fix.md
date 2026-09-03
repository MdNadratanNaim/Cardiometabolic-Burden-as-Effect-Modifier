## 🟠 Stale report artifacts — a recurring pattern across 3 separate deliverables

The pipeline has clearly evolved (ever-married → currently-married; n=5,137 → n=4,891), but several report-facing artifacts were never regenerated to match:

| Artifact | Says | Actual pipeline | 
|---|---|---|
| `Figure-2 (Biomarker structural attrition flow).svg` — the STROBE diagram | n=30,078 → n=5,137 final, single exclusion step | n=28,537 currently-married → n=4,891 final; missing the entire "not currently married" exclusion step (~1,541 women) entirely |
| `Figure-1 (Conceptual DAG).svg` | "**n = 13 covariates**" | The actual GVIF-validated adjustment set in Notebook 4 has **12** covariates (confirmed by counting `candidate_covariates` in the code, and the notebook's own text says "12-covariate" twice) |

Given three independent artifacts are stale in the same direction (pre-dating the currently-married restriction), I'd treat "regenerate all publication figures/metadata after the last pipeline change" as a checklist item before submission, not a one-off fix.

Related: `Supplementary Figure S1 (Full DAG).tex` still contains a `MaritalStatus` node with edges into Wealth/Burden/MentalHealth/Education, even though Marital status is now dropped from the analysis entirely (constant under the currently-married filter). Worth an explicit note in the figure or methods that this is controlled by design rather than by adjustment.

---

## 🟡 Dictionary.md completeness gaps

- **`V501`** and **`V026`** are documented in Part A (raw codebook) and present in `full_dataset.csv`, but appear in *none* of Part B (mapped), Part C (retained-unmapped), or Part D (unavailable) — falling through the dictionary's own stated four-way partition.
- **Grammar-level drift**: `recode.py`'s `clean_recode["Cardiometabolic Burden"]` uses "Two burden"/"Three burden" (singular); Dictionary.md uses "Two burdens"/"Three burdens." Trivial, but a sign the two weren't updated in lockstep.
- **Missing Survey design**: The survey design section of the d`ictionary.md` file is not showing all the weights.

---

## 🟡 Notebook/pipeline hygiene

- **Notebook 3 ("Basic Inspection") isn't just inspection** — it performs the Religion mode-imputation and **overwrites** `depression_dataset.csv`/`anxiety_dataset.csv`. A reader (or a re-run of just Notebook 2) would reasonably assume "Basic Inspection" is read-only; the actual data-mutation step is hidden one notebook downstream of where it's described as happening.
- **Stale variable naming**: Notebook 1 still names its marital-status column bundle `evermarried_cols`, a leftover from the pre-currently-married-only design. Harmless functionally, but confusing to a reader tracing the eligibility logic.
- `README.md` is completely empty — for a repo that's cited as the public companion to a journal submission, this is the first thing a reviewer or reader will hit.

