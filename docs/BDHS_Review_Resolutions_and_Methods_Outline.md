# BDHS Wealth × Cardiometabolic Burden Study — Review Response & Revised Methods Outline

*Audited against the live repo (`MdNadratanNaim/Cardiometabolic-Burden-as-Effect-Modifier`, current
`main`, cloned 2026-09-15). Every number below is computed directly from
`resources/depression_dataset.csv` / `anxiety_dataset.csv`, using the exact model formulas from
`5. Main Regression Analysis.ipynb` — my reproduction matched its stored outputs (LR statistics,
odds ratios, p-values) to 4 decimal places before I extended anything, so the new numbers sit on
the same footing as the notebook's own.*

## How the two reviews line up against the current repo

Both reviews are solid, but neither reflects what's actually in the notebooks right now — several
things they ask for are already built, and one thing neither could see (because it wasn't in front
of them) turns out to be the biggest open item of all.

**Already done — no action needed:**

| Review ask | Where it already lives |
|---|---|
| Formal likelihood-ratio test for the interaction | Notebook 5, §6/§9 — "LR test, ... Model 1 vs Model 2" |
| Simple slopes / marginal effects at each Burden level | Notebook 5, §7 — "Simple slopes: wealth OR at each level of cardiometabolic burden" |
| Invalid non-nested model comparison | Already fixed — Model 1c added as the correct nested comparator for Model 3 |
| Missingness structure (item vs. structural), Kish deff | Notebook 4, §1–2 — both reviews praised this and it's genuinely solid |

**Genuinely open, confirmed by direct inspection of the current data — resolved in Part 1 below:**
GOF, EPV disclosure, linearity, E-values, multiple testing, outcome-cutoff sensitivity, the
Insurance separation, weight range, influence diagnostics.

**Something neither review saw:** your own established analytic plan calls for two parallel
moderator model pairs — wealth-focal *and* education-focal. Notebook 5 (both languages) currently
runs the wealth-focal branch only; Education appears as one of the 12 covariates, not as its own
focal SEP × Burden interaction. That's flagged as a scope decision in Part 3.

*(One housekeeping note: my running project notes said Insurance had already been dropped from the
model and that an R-side zero-event check already existed. Neither is true of the actual repo —
`docs/to_fix.md` itself says the Insurance decision is still open, and the R notebook's §4 doesn't
have that check. I've corrected my notes to match what's actually there.)*

---

## Part 1 — Resolving the confirmed-open items

### 1. Insurance complete separation — recommend dropping it from the primary adjustment set

`Insurance = Yes` (n=16, 0.3% of the sample) has zero outcome events for **both** Depression and
Anxiety — the most severe form of separation there is. `docs/to_fix.md` correctly flags this as
unresolved and offers two paths: drop it, or refit with Firth's penalized likelihood.

I ran the comparison directly. Dropping Insurance from Depression Model 1/2 changes essentially
nothing:

| | With Insurance | Without Insurance |
|---|---|---|
| M1 vs M2 LRT (linear interaction) | χ²(4)=6.25, p=0.1816 | χ²(4)=6.05, p=0.1951 |
| Key term: Wealth=Poorer(2) OR (vs Richest) | 2.042 | 2.047 |

Given that, plus Insurance's marginal theoretical role (a background health-access covariate, not
one of the core wealth→mental-health mechanisms) and the precedent you already set for exactly this
situation (`MaritalStatus` got dropped and styled dashed/grey in the Supplementary DAG with a
footnote), I'd mirror that treatment rather than reach for Firth: combining Firth with the survey
design is genuinely nonstandard territory (your own to_fix.md already flags this), and here it buys
nothing empirically.

**Concrete steps:**
- Drop `Insurance` from `covariate_cols` in both Notebook 5 variants → adjustment set becomes 11
  covariates.
- Style the `Insurance` node in `Supplementary Figure S1 (Full DAG).tex` dashed/grey with a `†`
  footnote reading something like: *"Excluded due to empirical complete separation (Insurance=Yes,
  n=16, zero events in both outcomes), not a design-based exclusion like MaritalStatus."*
- Keep the existing Python zero-event check (§4) as a **diagnostic-only** cell that runs on the
  *full* 12-covariate set, so the separation is documented even though Insurance isn't in the fitted
  models — this is useful evidence for a reviewer who asks "did you check for separation."
- Update `Figure-1`'s `<desc>` and label, and `docs/Dictionary.md`, to say 11 covariates.

### 2. Partner-occupation "Don't know" separation (Depression only) — keep the category, suppress the coefficient

`Partner occupation = Don't know` (n=8) has zero Depression events — but not zero Anxiety events,
so it's a Depression-specific issue. This one is more consequential to fix by *dropping* the
category, because you've already established a clear principle elsewhere in this project (IPV
attitude's 3-level treatment) that "don't know" is a real answer, not something to silently merge
away. I checked what merging it into "Not working" would do — it resolves the separation cleanly
(model converges, 37 params instead of 38) — but that's exactly the move your own IPV-attitude
precedent argues against, so I wouldn't recommend it as the default.

**Recommended fix:** keep the 3-level `Partner occupation` variable as-is in the design matrix (its
presence still lets the other 8 women's data inform every *other* covariate in the model), but treat
that one coefficient as structurally non-identifiable and **don't report it**. Concretely: in the
odds-ratio table you put in the manuscript, replace that row's OR/CI with "not estimable (complete
separation, n=8)" instead of the literal `0.000 [0.000, 0.000]` `statsmodels` returns — that number
is not a real effect estimate and could be misread as a dramatic protective association if left in
a table as-is.

### 3. New finding: a second, undetected separation cell (Anxiety, Model 3)

The existing zero-event check (`check_zero_event_cells`, Notebook 5 §4) only tests the 12 marginal
covariates — it can't catch separation *inside* the Wealth × Burden interaction itself, which is a
different place for the same failure mode to show up. I checked, and there is one:

**Anxiety, `Wealth = Poorest × Burden_collapsed = 2` (i.e. "2+ conditions"): n=27, zero anxiety
events.** That's exactly the cell producing the `0.000 [0.000, 0.000]` interaction term you'll see
if you look at the full Anxiety Model 3 output (row `C(Q("Socioeconomic Status"))[T.1]:Q("Burden_collapsed")[T.2]`)
— it wasn't caught before because nothing was looking at interaction cells specifically.

Practical impact is limited (Anxiety's collapsed-Burden LRT was already non-significant overall,
p=0.3929), but the fix is cheap and worth having for the next dataset refresh or outcome you add.
Drop-in extension for Notebook 5 §4:

```python
def check_zero_event_interaction_cells(df, outcome_col, moderator_col, burden_col):
    """Zero-event check for the moderator x exposure CELLS themselves -- catches
    separation in the interaction term that the marginal per-covariate check can't see."""
    flagged = []
    ct_n = pd.crosstab(df[moderator_col], df[burden_col])
    ct_events = pd.crosstab(df[moderator_col], df[burden_col], df[outcome_col], aggfunc='sum').fillna(0)
    for wealth in ct_n.index:
        for burden in ct_n.columns:
            n = ct_n.loc[wealth, burden]
            if n > 0 and ct_events.loc[wealth, burden] == 0:
                flagged.append((wealth, burden, int(n)))
    return flagged

for label, df, outcome in [('Depression', dep, 'Depression_binary'), ('Anxiety', anx, 'Anxiety_binary')]:
    flags = check_zero_event_interaction_cells(df, outcome, 'Socioeconomic Status', 'Burden_collapsed')
    print(f'{label}: Wealth x Burden_collapsed cells with zero events:')
    for wealth, burden, n in flags:
        print(f'  Wealth={wealth}, Burden_collapsed={burden} (n={n}) -- term not identifiable')
    if not flags:
        print('  none')
```
Result: Depression has none; Anxiety flags exactly the cell above. Same reporting fix as item 2 —
suppress that one interaction term in the reported table rather than quoting `0.000`.

### 4. Goodness-of-fit

Nothing implements this yet anywhere in the repo — both reviews are right that it's missing. I ran
an exploratory weighted Hosmer-Lemeshow-style check in Python (design-naive, same caveat as the
rest of the Python notebook):

```python
def weighted_hl_test(res, data, outcome_col, weight_col='Sampling weight', g=10):
    yhat = res.predict(data)
    d = pd.DataFrame({'y': data[outcome_col].values, 'yhat': yhat, 'w': data[weight_col].values})
    d['decile'] = pd.qcut(d['yhat'], q=g, duplicates='drop')
    grp = d.groupby('decile', observed=True)
    obs1 = grp.apply(lambda x: np.sum(x['y']*x['w']), include_groups=False)
    exp1 = grp.apply(lambda x: np.sum(x['yhat']*x['w']), include_groups=False)
    n_w = grp['w'].sum(); obs0, exp0 = n_w - obs1, n_w - exp1
    stat = np.sum((obs1-exp1)**2/exp1 + (obs0-exp0)**2/exp0)
    dfree = len(grp) - 2
    return stat, dfree, stats.chi2.sf(stat, dfree)
```

| Model | χ² | df | p | Verdict |
|---|---|---|---|---|
| Depression M2 | 8.69 | 8 | 0.3695 | No evidence of poor fit |
| Anxiety M2 | 12.05 | 8 | 0.1488 | No evidence of poor fit |

For the **submission-grade** version, don't hand-roll the survey-design-adjusted version in either
language — Stata already has the validated Archer & Lemeshow (2006) test built in as a single
post-estimation command, and you already use Stata as an option:

```stata
svyset psu [pw=sampling_weight], strata(stratum)
svy: logit depression_binary i.ses##c.burden_num i.education i.occupation ...
estat gof
```
`estat gof` after `svy: logit` *is* the Archer-Lemeshow test — no custom implementation needed.
Add one line each to the Stata block in Notebook 5 §11, and a sentence in Methods citing Archer &
Lemeshow (2006).

### 5. Linearity of the logit

Age, Education, and every other covariate in this model are already **categorical**
(`C(Q("Age"))` etc.) — a linear-logit assumption doesn't apply to them at all, since a categorical
term gets a free parameter per level and can't misspecify a functional form. Box-Tidwell/splines,
as both reviews suggest for "Age," would be solving a problem this model doesn't have.

The one term that *is* entered continuously is `Burden_num` (0–3, linear) — that's the actual place
a linearity assumption is being made, and it's central to the interaction you're testing. I checked
it directly: fit Burden as a free 4-level factor (no linearity assumption) in the no-interaction
model and compared by LRT against the linear specification.

```python
dep['Burden_cat4'] = pd.Categorical(dep['Cardiometabolic Burden'].astype(int), categories=[0,1,2,3])
f_cat4 = f'Depression_binary ~ C(Q("Socioeconomic Status")) + C(Q("Burden_cat4")) + {covariate_formula}'
res_cat4 = fit_svy_logit(f_cat4, dep)
stat, df_diff, p = lr_test(res_dep_m1, res_cat4)   # res_dep_m1 already uses linear Burden_num
```

| Outcome | χ² | df | p | Verdict |
|---|---|---|---|---|
| Depression | 2.53 | 2 | 0.2816 | No evidence against linearity |
| Anxiety | 0.51 | 2 | 0.7767 | No evidence against linearity |

The free-form category ORs for Depression (vs. Burden=0: 0.738, 0.996, 1.190 for Burden 1/2/3)
don't show any sharp non-monotonic jump either — a mild, roughly linear-ish trend. This is a real
positive result worth a line in Methods: it substantively supports treating Burden as linear in the
primary model, on top of the Model 2-vs-3 comparison you already have as a sensitivity check on the
same question.

### 6. Events Per Variable (EPV)

Exact counts, refitting the actual models:

| Model | Events | Predictor params (excl. intercept) | EPV |
|---|---|---|---|
| Depression M1 (main effects) | 235 | 33 | 7.12 |
| Depression M2 (primary, + interaction) | 235 | 37 | **6.35** |
| Anxiety M1 (main effects) | 221 | 33 | 6.70 |
| Anxiety M2 (primary, + interaction) | 221 | 37 | **5.97** |

This matches Review 2's estimate almost exactly. Below the conventional EPV≥10 rule of thumb, and
worth disclosing explicitly rather than leaving a reviewer to compute it themselves — but I wouldn't
trim covariates just to raise this number, since your adjustment set is DAG-derived and theory-driven
(dropping something to hit an arbitrary EPV threshold would be the "stepwise/data-driven" selection
you deliberately avoided). The honest move is to state the EPV, cite it as a real limitation of a
~4.8%-prevalence outcome in a moderation design, and note that the GVIF check already ruled out
collinearity as a *separate* source of instability — EPV and multicollinearity are different risks
and you've now checked both.

### 7. Multiple testing correction

You're testing the Wealth × Burden interaction across 2 outcomes, in 2 parameterizations each
(linear = primary, collapsed = sensitivity) = 4 LRTs total, one of which (Depression, collapsed) is
significant at p=0.0166. I applied both Bonferroni and Benjamini-Hochberg FDR under two different
definitions of "the family being corrected for," using `statsmodels.stats.multitest.multipletests`:

```python
from statsmodels.stats.multitest import multipletests
primary = [0.1816, 0.2195]                    # Depression, Anxiety -- linear (pre-specified primary)
all_four = [0.1816, 0.2195, 0.0166, 0.3929]   # + Depression, Anxiety -- collapsed (sensitivity)
multipletests(primary,  method='bonferroni'); multipletests(primary,  method='fdr_bh')
multipletests(all_four, method='bonferroni'); multipletests(all_four, method='fdr_bh')
```

| Framing | Depression (linear) | Anxiety (linear) | Depression (collapsed) | Anxiety (collapsed) |
|---|---|---|---|---|
| Raw p | 0.1816 | 0.2195 | 0.0166 | 0.3929 |
| **A: family = 2 primary tests only** — Bonferroni | 0.3632 | 0.4390 | — | — |
| **A** — BH-FDR | 0.2195 | 0.2195 | — | — |
| **B: family = all 4 tests** — Bonferroni | 0.7264 | 0.8780 | **0.0664** | 1.0000 |
| **B** — BH-FDR | 0.2927 | 0.2927 | **0.0664** | 0.3929 |

This is the one place where the framing genuinely changes the story. Under Framing A — the 2
linear tests are the pre-specified primary hypotheses, and the collapsed model is a sensitivity
check on functional form, not a separate confirmatory test — correction is close to moot, since
neither primary test reaches significance anyway. Under Framing B — treat all four
outcome-by-parameterization combinations as one family — the Depression-collapsed finding no
longer survives (0.0664).

**Recommendation:** report Framing A's logic explicitly in Methods (Model 2/linear is pre-specified
primary; Model 3/collapsed is a pre-planned sensitivity check on the linearity assumption, not an
additional hypothesis test), and in Results, present the Depression-collapsed finding as
hypothesis-generating rather than confirmed — something like *"uncorrected for the additional
model-specification comparison this entailed."* That's honest either way the reviewer wants to
think about it, without quietly picking the framing that looks best.

### 8. E-values

Using the Ding & VanderWeele (2016) formula (OR as a reasonable stand-in for RR given <15%
prevalence in both outcomes):

```python
def e_value(estimate, ci_bound=None):
    def _ev(rr):
        rr = 1/rr if rr < 1 else rr
        return rr + np.sqrt(rr * (rr - 1))
    return _ev(estimate), (_ev(ci_bound) if ci_bound is not None else None)
```

| Finding | OR [95% CI] | E-value (point) | E-value (CI limit) |
|---|---|---|---|
| Wealth=Poorer vs Richest, Depression @ Burden=0 | 2.042 [1.084, 3.844] | 3.50 | 1.39 |
| Age 35–49 vs 15–24, Depression | 2.020 [1.179, 3.462] | 3.46 | 1.64 |
| Wealth=Richer × Burden(2+), Depression interaction | 0.028 [0.003, 0.250] | 70.93 | 7.46 |

Report E-values for the first two — well-populated, stable estimates where "how big a confounder
would it take to explain this away" is a meaningful question. I'd be cautious about headlining the
third: an E-value of ~71 sounds impressively robust, but that OR comes from one of the thinner
interaction cells discussed in §4 above (`Wealth=Poorest × Burden=3` has n=1 uncollapsed), so the
huge E-value is really a symptom of an extreme, less-stable point estimate rather than genuine
robustness to confounding. Apply E-values to your headline *simple-slope* findings, not to the raw
sparse-cell interaction terms.

### 9. Outcome-binarization sensitivity (PHQ-9 ≥15 cutoff)

Ran it directly — re-dichotomizing at the moderately-severe+ threshold and refitting:

| | Primary (≥10 cutoff) | Sensitivity (≥15 cutoff) |
|---|---|---|
| Probable-depression cases | 235 | 62 |
| M1 vs M2 LRT | χ²(4)=6.25, p=0.1816 | χ²(4)=7.95, p=0.0934 |

Same qualitative conclusion (not significant at either cutoff), and if anything trending a little
stronger at the stricter threshold — directionally reassuring. But be careful not to oversell this:
at 62 events over 37 parameters, EPV drops to ~1.7, far below even the primary model's already-low
6.35, so this comparison is underpowered on its own terms. Report it as "directionally consistent,"
not as independent confirmation.

### 10. Weight trimming / calibration

Checked the actual weight distribution: min 0.091, max 3.892, mean 0.993 (max/min ≈ 42.7). That
range looks wide in isolation, but the Kish design effect you already computed in Notebook 4
(1.253) is unremarkable for a stratified multistage DHS design — a genuinely problematic weight
distribution would show up as a much larger deff. Nothing here indicates trimming is needed; a
one-line note in Methods ("no weight trimming was applied; the design effect of 1.25 indicated
unequal weighting was not extreme") closes this out without more work.

### 11. Influential observations

Computed GLM Cook's distance for Depression Model 2 (`res.get_influence().cooks_distance`):

- Max Cook's D = 0.043 — far below the conventional concern threshold (~1).
- The 4/n screening rule flags 213/4,887 women, but that heuristic is known to over-flag at this
  sample size and isn't informative on its own.
- The highest-Cook's-D cases are ordinary profiles (wealthy women with moderate burden and
  depression — a genuinely less-common combination in the data, hence a bit more "surprising" to
  the model) — **not** the known separated categories (Insurance, Partner-occupation=Don't know).

No individual observation is driving the interaction estimates. This is a clean result to state in
Methods/Supplement as evidence the model isn't being pulled around by a handful of respondents —
separately from, and in addition to, the sparse-*cell* issues already identified above, which are a
different (aggregate, not single-observation) kind of instability.

---

## Part 2 — Corrections carried into `docs/to_fix.md` framing

Everything above should probably become new entries in `docs/to_fix.md` under a "GOF / EPV /
multiple-testing / sensitivity-analysis audit" pass, following the same Resolved / Still-open
structure the file already uses. I'd suggest:
- **Resolved this pass:** items 4–11 above (GOF, linearity, EPV disclosure, multiple testing,
  E-values, outcome-cutoff sensitivity, weight check, influence check).
- **Resolved this pass, pending your DAG sign-off:** items 1–3 (Insurance dropped, Partner-occ-DK
  suppressed, new Anxiety interaction-cell suppressed) — these are my recommendations, not yet
  applied to the notebooks.

---

## Part 3 — Two decisions that are genuinely yours to make

I can implement either direction once you confirm; I didn't want to bake a guess into "final"
notebook code or the Methods outline below without flagging the reasoning first.

### A. `Financial Decision-Making` — confounder, mediator, or sensitivity-only?

`docs/to_fix.md` and Notebook 4 §5.1 both flag this as open, and it's consequential: whichever way
it goes changes every model in Notebook 5. Your `Supplementary Figure S2` already has a working
taxonomy for exactly this kind of call (Proxy confounder / Confounds burden / Collider–exclude /
Mediator–exclude), so I'd slot this variable into that same framework rather than inventing new
criteria:

- **The case for treating it like `Household Autonomy` (include as a confounder):** it was only
  split out from that composite for a *measurement* reason (the "no earnings" category for ~1.3% of
  women, per `Dictionary.md`), not a causal-role reason. If the other three autonomy items are
  accepted as confounders of Wealth → Mental Health, this one is conceptually a sibling of them, and
  treating it differently needs its own causal argument.
- **The case for sensitivity-only (my provisional lean):** this item is specifically about the
  respondent's say over money *her husband* earns — closer to a downstream manifestation of the
  household's economic/employment structure than to general decision-making norms. If wealth shapes
  how a husband's income is structured (salaried vs. informal vs. business), which in turn shapes
  who gets a say in decisions about it, adjusting for it could partially block the very pathway
  you're testing (mediator-adjustment bias) — a costlier error than leaving a weak confounder out
  and disclosing it as a limitation.

I lean toward the second reading given the tighter link to income structure specifically, but this
is a judgment call about a causal story only you can finalize. **Recommended action either way:**
add it to `Supplementary Figure S2`'s taxonomy with an explicit label and one-line justification,
the same way `Abortion history` already got labeled "Mediator – exclude."

### B. Scope: wealth-focal only, or build out the education-focal branch too?

Your established analytic plan (two parallel moderator model pairs, wealth-focal and
education-focal, per the project brief) isn't fully reflected in the current repo — Notebook 5
(Python and R) only implements the wealth-focal side; Education sits inside the 12-covariate
adjustment set rather than as its own SEP × Burden interaction with Wealth demoted to a covariate.
Neither review flagged this since they were only shown the wealth-focal notebooks. This doesn't
block finishing the wealth-focal manuscript, but it does affect how confidently the Methods section
below can describe "two SEP indicators, tested in parallel" — right now that's true of the *plan*,
not yet of the *repo*. Worth a quick decision: finish education-focal as originally planned (I can
build it — it's a structural copy of Notebook 5 with Wealth and Education swapping roles), or
scope the current manuscript to wealth-only and note education-focal as future work.

---

## Part 4 — Revised Methods section outline

Structured per STROBE (cross-sectional) and Aiken & West (moderation reporting), matching your
established documentation conventions. Bracketed notes mark where a Part 3 decision changes the
wording.

**2.1 Study design and data source**
- Cross-sectional secondary analysis of BDHS 2022 (World Bank Microdata Library, catalog 6290)
- Recode files merged on `CASEID`: REC01, REC11, REC22, REC31, REC32, REC71, REC91, RECH2, RECMTH

**2.2 Study population, eligibility, and sample size**
- Eligibility: currently married women (`S111A == 1`)
- Attrition cascade: 30,078 eligible ever-married women → 1,541 excluded (not currently married) →
  28,537 → 23,650 excluded (incomplete cardiometabolic biomarker components) → final analytic
  n = 4,887 (identical for both outcomes)
- Explicit statement that Depression/Anxiety, Occupation, Insurance, and IPV-attitude items were
  collected in the *same* extended biomarker sub-module as the cardiometabolic components — this is
  the note Notebook 4's Finding A was flagging for whoever wrote this section; it belongs here.
- Reference Figure 2 (STROBE attrition diagram)

**2.3 Outcome ascertainment**
- PHQ-9 (depression) and GAD-7 (anxiety), administered as part of the extended module
- Binarization: PHQ-9 ≥10 = probable depression (Kroenke, Spitzer & Williams, 2001); GAD-7 ≥10 =
  probable anxiety (Spitzer, Kroenke, Williams & Löwe, 2006) — state as a documented analytic
  choice, not the only defensible one
- Sensitivity analysis at PHQ-9 ≥15 (moderately-severe+): consistent direction, underpowered
  (62 events) — reported as directionally supportive, not confirmatory

**2.4 Exposure and effect-modifier definitions**
- Wealth index (`V190`, DHS composite quintiles) — primary SEP indicator [+ Education as a second,
  parallel SEP indicator, pending the Part 3-B scope decision]
- Cardiometabolic burden: 0–3 count — Diabetes (glucose ≥126 mg/dL OR diagnosed OR on medication),
  Hypertension (SBP≥140 OR DBP≥90 OR diagnosed OR on medication), Obesity (BMI≥30)

**2.5 Covariates and confounder selection**
- DAG-based, theory-driven selection (Figure 1; Supplementary Figure S1), not stepwise/data-driven
- 11-covariate GVIF-validated adjustment set (Education, Occupation, Partner occupation, Age,
  Division, Residence, Religion, Children, Family size, Household Autonomy, Internet) — *Insurance
  removed per Part 1 item 1, pending your confirmation*
- Reproductive-health block handled via Supplementary Figure S2's confounder/mediator/collider
  taxonomy (e.g., Contraceptive use retained as proxy confounder, Abortion history excluded as a
  mediator)
- `Financial Decision-Making`: [status pending Part 3-A — describe as sensitivity-only variable, or
  fold into the primary set, once decided]

**2.6 Missing data**
- Missingness in the extended-module block (biomarkers, depression/anxiety, occupation, insurance,
  IPV-attitude items) is 100% explained by sub-sample module assignment, not item-level
  nonresponse — verified empirically (Notebook 4 §2)
- Explicit assumption statement: complete-case analysis is appropriate here because missingness is
  generated by survey design (module assignment), satisfying a missing-by-design/MCAR-conditional-
  on-design argument rather than requiring multiple imputation (STROBE item 13)
- Trivial exception: the single "missing" Religion case was a valid `V130==96` ("Others") response,
  not true missingness, after correcting the `religion()` recode function

**2.7 Statistical analysis**
- *2.7.1 Descriptive and bivariate screening* — design-naive Pearson χ² / Spearman / Kruskal-Wallis
  for initial screening; final reported bivariate statistics deferred to R (Rao-Scott χ²)
- *2.7.2 Survey design and weighting* — PSU (`V021`), Stratum (`V022`), sampling weight (`V005`,
  rescaled ÷1,000,000); `svydesign(id=~PSU, strata=~Stratum, weights=~Sampling.weight, nest=TRUE)`
  in R for final inference; Python/`statsmodels` cluster-robust SEs and a stratified cluster
  bootstrap (PSUs resampled within stratum) as an exploratory cross-check, since `statsmodels` has
  no native stratified-multistage variance estimator
- *2.7.3 Interaction-modeling strategy* — nested Model 1 (main effects) → Model 2 (+ Wealth ×
  Burden, linear, primary) → Model 3 (+ Wealth × Burden, collapsed 0/1/2+, sensitivity), motivated
  by the `Wealth=Poorest × Burden=3` sparse cell (n=1); omnibus likelihood-ratio test interpreted
  before any individual coefficient; simple slopes (delta method) reported only if the omnibus test
  is significant
- *2.7.4 Handling of non-identifiable terms* — Insurance dropped from the adjustment set
  (complete separation, empirically confirmed not to alter substantive conclusions); Partner
  occupation="Don't know" (Depression) and Wealth=Poorest×Burden(2+) (Anxiety, Model 3) retained in
  the design matrix but reported as "not estimable" rather than as numeric ORs
- *2.7.5 Model diagnostics* — GVIF (Fox & Monette, 1992; threshold ≈2 on GVIF^(1/2·Df)); linearity
  of Burden's functional form (categorical-vs-linear LRT, both outcomes n.s.); goodness-of-fit
  (Archer & Lemeshow, 2006, via Stata `estat gof`); influence diagnostics (Cook's distance, GLM)
- *2.7.6 Events-per-variable disclosure* — EPV 6.35 (Depression) / 5.97 (Anxiety) for the primary
  interaction model, stated as a limitation of a design-based adjustment set applied to an outcome
  with ~4.8% prevalence
- *2.7.7 Sensitivity analyses* — Model 3 (collapsed Burden); Insurance-dropped refit; PHQ-9 ≥15
  cutoff [+ Financial-Decision-Making-included refit, pending Part 3-A]
- *2.7.8 Multiple comparisons* — two pre-specified primary tests (linear interaction × 2 outcomes);
  the collapsed-Burden sensitivity result for Depression reported as hypothesis-generating, noting
  it would not survive correction if treated as part of a four-test family

**2.8 Quantitative bias assessment**
- E-values (Ding & VanderWeele, 2016) reported for the primary simple-slope findings, not for
  sparse-cell interaction terms

**2.9 Software**
- Python (`pandas`, `statsmodels`) for data preparation and exploratory modeling; R (`survey`
  4.2-1) and/or Stata for final design-based inference and goodness-of-fit; versions per
  `pyproject.toml` / `renv.lock` / `DESCRIPTION`
