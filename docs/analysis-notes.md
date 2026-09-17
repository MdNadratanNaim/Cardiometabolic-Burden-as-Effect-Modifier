# Analysis Notes: Resolution Log & Methods Outline

Working notes from the review-resolution pass on this repo. This is where the *process*
commentary lives — what was decided, why, and what it would look like written up for a
manuscript — kept out of the notebooks themselves so those stay readable as "what we did and what
it means" rather than "what we changed and when." For the underlying analysis, read the notebooks;
for why they look the way they do, read this.

---

## 1. What prompted this pass

Two independent reviews of the repo (both against the state before this pass — 12-covariate
adjustment set, `Insurance` and `Financial Decision-Making` still unresolved) converged on largely
the same verdict: the Python → R progression is conceptually sound and should ship, but a specific
list of items needed resolving before the numbers were manuscript-ready. Section 3 below is that
list, resolved.

Two researcher decisions were needed before any of it could be implemented, since both change
numbers throughout the notebooks:

- **`Financial Decision-Making`'s adjustment-set status.** Resolved as: test it *together* with
  `IPV Attitude` as a single combined sensitivity model (13 covariates: the primary 11 + both),
  compared against the primary 11-covariate model — not three separate models, not folded into
  the primary set.
- **Scope: wealth-focal only, or also build an education-focal branch** (Education × Burden,
  Wealth as covariate)? Resolved as **wealth-focal only**. Operationally, "Socioeconomic Status"
  in this codebase already *is* the wealth index (that's how the column is named and coded
  throughout); Education stays a covariate/confounder, not a second parallel exposure. An
  education-focal branch would be a natural extension — structurally a copy of Notebook 5 with
  Wealth and Education's roles swapped — but isn't part of this round.

## 2. Two claims from the second review, checked against the actual repo

Reviews are useful precisely because they catch things — but a review is itself a claim to verify,
not something to implement on faith. Both of the substantive-sounding claims below turned out to
be non-issues once checked against the code, not the review's paraphrase of it:

**"Population says ever-married, code uses currently-married."** Checked `README.md`,
`tools/recode.py`, and Notebook 2 directly. BDHS's women's questionnaire frame is ever-married by
design (30,078 women) — `V020` in `recode.py` literally labels this "Type of sample or ever-married
indicator." Notebook 2 has an explicit, clearly-labeled "Selection of currently married Women" step
(`S111A == 1`) narrowing to 28,537, and it's load-bearing: Notebook 4 shows this same filter is what
resolved the earlier `Autonomy` silent-zero bug and the `Marital status`/`Partner occupation`
collinearity, since Partner occupation, Household Autonomy, and IPV Attitude all require a
co-resident husband to be defined in the first place. Re-including widowed/divorced/separated women
would reopen both. `README.md` already documented the cascade correctly; this pass added the same
clarification to `Dictionary.md` and Notebook 4's intro so it stops being a plausible-sounding but
incorrect thing to flag.

**"Dyslipidemia missing from the burden score."** Checked `tools/recode.py` — the single file that
maps every BDHS variable touched anywhere in this pipeline — for any lipid/cholesterol-related
variable. There isn't one. The three components used (diabetes via glucose + diagnosis +
medication; hypertension via blood pressure + diagnosis + medication; obesity via BMI) are exactly
BDHS's standard biomarker module. A lipid panel needs venous blood and lab processing that standard
DHS biomarker rounds don't do. This is a data-availability fact, not a scope decision — now stated
as such in `Dictionary.md` Part A2.

The rest of that review's 20 points either matched what this pass already implements (R as the
authoritative inferential source, the omnibus-test-before-simple-slopes framing, the Model 1c
nesting fix, sparse-cell handling, bootstrap as a cross-check rather than the primary method) or
were reasonable-but-optional EDA completeness suggestions (weighted prevalence with a design-aware
CI, an eligible-vs-analytic-sample comparison, noting an ordinal-outcome model as a possible future
extension) — the cheap ones went into Notebook 4; the ordinal model is flagged as available future
work rather than built unasked, since it's a real separate modeling effort, not an EDA addition.

## 3. Resolution log

Each item: what it was, what was done, and the verified result.

| # | Item | Resolution |
|---|---|---|
| 1 | `Insurance` complete separation (0/16 insured women screen positive, either outcome) | Dropped from the primary covariate set (11, not 12). Passes GVIF cleanly (Notebook 4) — confirmed this is a separation problem, not a collinearity one; GVIF can't catch the former. |
| 2 | `Partner occupation = Don't know` (n=8, depression) | Kept as a 3-level variable (dropping it discards real covariate information for those 8 women); its own coefficient reported as "not estimable" rather than the spurious OR = 0.000, in both notebooks. |
| 3 | New zero-event interaction cell: Anxiety, `Wealth=Poorest × Burden_collapsed=2+` (n=27) | Same treatment as #2 — reported "not estimable," found via a new interaction-cell-level zero-event check (Notebook 5 Python §6, R §4) that generalizes the covariate-level check to interaction cells specifically. |
| 4 | Goodness-of-fit | Exploratory weighted Hosmer-Lemeshow-style test added (Python §14) — design-naive, flagged as such. `estat gof` (Archer & Lemeshow 2006) added to the Stata replication block as the validated design-based version; no attempt to hand-roll a design-adjusted GOF test in Python or R. |
| 5 | Linearity of the Burden term | Categorical-vs-linear LR test added in both notebooks. No evidence against linearity for either outcome — supports using linear Burden as the primary specification rather than treating it as only a fix for the sparse-cell problem. |
| 6 | Events-per-variable disclosure | Added for M1/M2, both outcomes: ~6-7 EPV, below the conventional 10-EPV rule of thumb. Stated explicitly as the reason the omnibus LR test, not individual interaction coefficients, is the primary evidence for effect modification. |
| 7 | Multiple-testing correction | Two framings computed: primary-only (2 linear-interaction tests) and all-four (+ the 2 collapsed-Burden sensitivity tests). Under the honest framing (all four, since the collapsed coding was chosen after the linear one came up short), depression's collapsed-interaction p-value moves from ~0.02-0.03 to ~0.07-0.13 depending on language and method — no longer conventionally significant. Reported as suggestive, not confirmed. |
| 8 | E-values | Computed for the two headline main-effect estimates (~3.5, moderately robust to unmeasured confounding) and the driving interaction term (point estimate E-value is misleadingly large due to the sparse cell; the CI-limit version, ~7.3, is the honest one). |
| 9 | Outcome-cutoff sensitivity (PHQ-9 ≥15) | Refit at the stricter cutoff. Only 62 events (EPV ~1.7) — too sparse to confirm or overturn the ≥10 finding either way. Framed as a stated limitation of the ≥10 cutoff choice, not as a null result. |
| 10 | Weight trimming/calibration | Range disclosed (43x spread, min/max/mean), consistent with a normalized DHS weight and with Notebook 4's existing Kish design-effect check. No trimming applied. |
| 11 | Influential observations | Cook's distance computed for Depression M2 (Python only — a data-influence property that doesn't depend on the SE method, so not duplicated in R). Max D = 0.044, nowhere near the ~1 threshold that would indicate a single point distorting the fit; the highest-leverage cases are exactly the rare covariate/outcome combination driving the interaction finding, which is expected, not a data problem. |

## 4. Methods section outline

Structure for the manuscript's Methods section, reflecting the final decisions above. Written as
an outline with the specific numbers/citations to use, not full prose — the actual writing is a
separate task.

**2.1 Study design and data source**
Cross-sectional analysis of BDHS 2022 (World Bank Microdata Library, catalog 6290).

**2.2 Study population**
Ever-married women 15-49 are BDHS's sampling frame for the individual woman's questionnaire
(n=30,078 eligible). Restricted to currently married women (`S111A == 1`, n=28,537) because several
covariates (partner's occupation, household decision-making autonomy, attitudes toward
partner violence) are only defined relative to a co-resident husband. Further restricted to women
with complete cardiometabolic biomarker data (final analytic n=4,887) — state explicitly that this
is a structural sub-sample (the biomarker module was fielded to a subset by design), not
item-level non-response, citing the missingness-structure check in Notebook 4 §2.

**2.3 Exposure: socioeconomic status**
Wealth index (BDHS `V190`/`V190A`), 5 categories, Richest as reference. Education is treated as a
covariate in the adjustment set, not a second exposure — state this explicitly to avoid the
common reader assumption that "SEP" implies a composite or a parallel-models design.

**2.4 Effect modifier: cardiometabolic burden**
Composite count (0-3) of diabetes (glucose ≥126 mg/dL, self-reported diagnosis, or current
medication), hypertension (systolic ≥140 or diastolic ≥90 mmHg, self-reported diagnosis, or
current medication), and obesity (BMI ≥30). State explicitly that dyslipidemia is not part of this
construct because BDHS's biomarker module does not include a lipid panel — a data-availability
constraint, not a modeling choice.

**2.5 Outcomes**
Probable depression: PHQ-9 ≥10 (Kroenke, Spitzer & Williams, 2001, *J Gen Intern Med*). Probable
anxiety: GAD-7 ≥10 (Spitzer, Kroenke, Williams & Löwe, 2006, *Arch Intern Med*). State the cutoff
as a specified choice with a sensitivity check at a stricter threshold (PHQ-9 ≥15), and note the
sensitivity check was underpowered (n=62 events) rather than a confirming or disconfirming result.

**2.6 Covariates and confounder selection**
Theory-driven selection via a directed acyclic graph (Supplementary Figure S1), not
stepwise/data-driven methods. Primary adjustment set (11): Education, Occupation, Partner
occupation, Age, Division, Residence, Religion, number of children, household size, household
decision-making autonomy, internet use. Two exclusions from what a naive DAG reading might
suggest, both justified: `Marital status` is constant by construction under the currently-married
restriction (Supplementary Figure S1 footnote); `Insurance`, despite a theoretically valid
confounder role, is completely separated from both outcomes (0/16 insured women screen positive)
and is excluded from the fitted models on that basis alone (Figure S1 footnote), not because it
fails the DAG or the multicollinearity check.

**2.7 Statistical analysis**
Survey-weighted logistic regression via R's `survey` package (`svydesign` with PSU, stratum, and
sampling weight; `svyglm`, `family = quasibinomial`), the design-based source for all reported
standard errors, confidence intervals, and p-values. Python (`statsmodels`) served as the
model-development and diagnostic environment; a cluster-robust-by-PSU approximation there (lacking
stratification) was cross-checked against a stratified cluster bootstrap and against R, with point
estimates matching closely and standard errors/p-values taken from R as authoritative.

Nested model comparisons via design-based likelihood-ratio tests (`anova(..., method="LRT")`).
Burden entered as linear (primary) and as a collapsed 0/1/2+ category (sensitivity, since one
Wealth × Burden cell has n=1 in the fully categorical coding) — state that the linear-vs-categorical
choice was itself checked (§2.7.1) and not just a sparse-cell workaround.

**2.7.1 Model diagnostics**
Report: zero-event checks at both the covariate and interaction-cell level; linearity of the
Burden term (categorical-vs-linear LRT); events-per-variable (~6-7 for the primary interaction
models); goodness-of-fit (design-naive in Python/R, Stata `estat gof` as the validated version);
Cook's distance for influential observations; sampling weight range.

**2.7.2 Multiple comparisons**
State both tests run per outcome (linear and collapsed Burden interaction) as a single family of
four tests across both outcomes, corrected via Bonferroni and Benjamini-Hochberg — report which
findings survive correction, explicitly, rather than reporting only the uncorrected values.

**2.7.3 Effect modification interpretation**
Omnibus likelihood-ratio test as the primary evidence for effect modification; simple slopes
(wealth OR at each burden level, delta method on the interaction model's own covariance) as the
follow-up interpretation step, reported and interpreted only when the omnibus test supports it.

**2.7.4 Sensitivity analyses**
(a) Collapsed vs. linear Burden coding (§2.7 above). (b) Extended adjustment set adding `Financial
Decision-Making` and `IPV Attitude` together (13 covariates) — state the DAG rationale for their
exclusion from the primary set (ambiguous confounder-vs-mediator role for the former; a backdoor
path already blocked by adjusting for Education, for the latter) and report that neither the
interaction finding nor its magnitude changes meaningfully with both added. (c) Outcome-cutoff
sensitivity (PHQ-9 ≥15). (d) E-values for the headline estimates, as a bounding exercise for
unmeasured confounding rather than a formal test.

**2.8 Software**
Python 3.12 (`pandas`, `statsmodels`, `patsy`) for data preparation, model development, and
diagnostics; R 4.3+ (`survey`) for final inferential statistics; Stata (`svy: logit`, `estat gof`)
for the validated design-based goodness-of-fit test only.

## 5. Results-section numbers (R, design-based — cite these, not Python's)

| | Depression | Anxiety |
|---|---|---|
| N | 4,887 | 4,887 |
| Probable cases (≥10 cutoff) | 235 (4.8%) | 221 (4.5%) |
| Linear Wealth × Burden interaction, χ²(4) | 6.10, p=0.308 | 5.70, p=0.276 |
| Collapsed Wealth × Burden interaction, χ²(8) | 18.60, p=0.030 | 8.37, p=0.349 |
| EPV (primary interaction model) | 6.53 | 6.14 |
| Collapsed-interaction p, all-four-test correction (Bonferroni / BH) | 0.121 / 0.121 | 1.00 / 0.349 |
| Extended-set (+FDM+IPV) collapsed interaction, χ²(8) | 18.20, p=0.035 | 8.26, p=0.357 |

Depression's driving term: Wealth=Richer × Burden(2+), OR = 0.029 [0.003, 0.256] in the primary
11-covariate model (R) — matches Python's cluster-robust version (OR = 0.028) almost exactly, and
barely moves in the extended (+FDM+IPV) set either (OR = 0.030 [0.003, 0.260]). E-value for this
term's confidence limit: ~7.3.
