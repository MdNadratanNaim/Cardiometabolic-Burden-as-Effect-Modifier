# BDHS Analysis Data Dictionary

## Purpose

This dictionary documents the full variable pipeline used in the analysis:

- **Part A** — raw BDHS codebook variables and their value labels, as encoded in `recode`.
- **Part B** — the final, analysis-ready variables actually used in the modeling pipeline, as encoded in `clean_recode`, together with the source variable(s) and the collapsing/derivation logic that produces each one.
- **Part C** — raw variables that are available (present in `recode`) but not mapped to any final `clean_recode` variable — kept for descriptive stats or sensitivity checks.
- **Part D** — variables from the original BDHS codebook that are **not available** in this extract at all.

Sample is restricted to currently married women (`S111A == 1`). BDHS's women's questionnaire frame is ever-married women by design; this is a further, deliberate restriction — several derived variables below (Partner occupation, Household Autonomy, IPV Attitude, Financial Decision-Making) require a co-resident husband to be defined, and aren't meaningful for widowed, divorced, or separated women. See `README.md` and `4. Exploratory Data Analysis.ipynb` for the full eligibility cascade.



---

## Part A — Raw Variable Codebook

### A1. Population / Identifiers

| Variable | Description | Codes |
|---|---|---|
| `S111A` | Current marital status | 1 = Currently married; 2 = Separated; 3 = Deserted; 4 = Divorced; 5 = Widowed |
| `V501` | Current marital status (alt. source) | 0 = Never married; 1 = Married; 2 = Living together; 3 = Widowed; 4 = Divorced; 5 = Not living together; 9 = Missing |
| `HV104` | Sex of household member | 1 = Male; 2 = Female; 9 = Missing |

### A2. Cardiometabolic Burden Components

| Variable | Description | Codes |
|---|---|---|
| `SB267` | Plasma glucose (mg/dL) | Continuous |
| `SB236` | Ever diagnosed with diabetes | 0 = No; 1 = Yes; 9 = Missing |
| `SB240` | Currently taking diabetes medication | 0 = No; 1 = Yes |
| `WBP24` | Final systolic blood pressure (mmHg) | Continuous |
| `WBP25` | Final diastolic blood pressure (mmHg) | Continuous |
| `WBP16` | Previously diagnosed with hypertension | 0 = No; 1 = Yes |
| `WBP19` | Currently taking BP medication | 0 = No; 1 = Yes |
| `HA40` | Body Mass Index (BMI) | Continuous |

*Note: the original codebook also lists `V445` as an alternate BMI source, but it was dropped in favor of `HA40` — obesity is computed from `HA40` only.*

*Note: dyslipidemia is not part of this burden score. BDHS's biomarker module collects anthropometry, blood pressure, and blood glucose (all listed above) but no lipid panel — a lipid panel needs venous blood and lab processing that the standard DHS biomarker round doesn't do. This is a data-availability constraint, not a scope choice: dyslipidemia was never an available component to include.*

### A3. Depression / Anxiety / Sleep

| Variable | Description | Codes |
|---|---|---|
| `MTH22` | PHQ-9 depression score (categorized) | 0 = 0–4 minimal; 1 = 5–9 mild; 2 = 10–14 moderate; 3 = 15–19 moderately severe; 4 = 20–27 severe |
| `MTH24` | GAD-7 anxiety score (categorized) | 0 = 0–4 minimal; 1 = 5–9 mild; 2 = 10–14 moderate; 3 = 15–21 severe |
| `MTH10` | Trouble falling/staying asleep, last 2 weeks | 0 = Never; 1 = Rarely; 2 = Often; 3 = Always; 7 = Refused; 8 = Don't know |

### A4. Socioeconomic Status — Education

| Variable | Description | Codes |
|---|---|---|
| `V133` | Education in single years | Continuous |
| `V149` | Educational attainment | 0 = No education; 1 = Incomplete primary; 2 = Complete primary; 3 = Incomplete secondary; 4 = Complete secondary; 5 = Higher; 9 = Missing |
| `V106` | Highest educational level | 0 = No education; 1 = Primary; 2 = Secondary; 3 = Higher |

### A5. Socioeconomic Status — Wealth

| Variable | Description | Codes |
|---|---|---|
| `V190` | Wealth index combined (categorical) | 1 = Poorest; 2 = Poorer; 3 = Middle; 4 = Richer; 5 = Richest |
| `V190A` | Wealth index combined, urban/rural clustered | Same as `V190` |
| `V191` | Wealth index factor score combined | Continuous |
| `V191A` | Wealth index factor score, urban/rural clustered | Continuous |

### A6. Socioeconomic Status — Occupation

| Variable | Description | Codes |
|---|---|---|
| `V714` | Respondent currently working | 0 = No; 1 = Yes |
| `V731` | Respondent worked in last 12 months | 0 = No; 1 = In the past year; 2 = Currently working; 3 = Has a job, on leave; 9 = Missing |
| `V716` | Respondent's occupation (detailed) | 0 = Not working; 11 = Land owner; 12 = Farmer; 13 = Agricultural worker; 14 = Fisherman; 15 = Poultry/cattle raising; 16 = Home-based manufacturing; 21 = Rickshaw driver/construction/boatman; 22 = Domestic servant; 23 = Non-agricultural worker; 31 = Skilled trade/driver/supervisor; 41 = Professional (doctor, lawyer, teacher, nurse…); 51 = Big businessman; 52 = Small business/trader; 61 = Unemployed/student; 62 = Retired; 96 = Others; 99998 = Don't know; 99999 = Missing |
| `V717` | Respondent's occupation (grouped) | 0 = Not working; 1 = Professional/technical/managerial; 2 = Clerical; 3 = Sales; 4 = Agricultural, self-employed; 5 = Agricultural, employee; 6 = Household/domestic; 7 = Services; 8 = Skilled manual; 9 = Unskilled manual |
| `V704` | Husband/partner's occupation (detailed) | Same code scheme as `V716` |
| `V705` | Husband/partner's occupation (grouped) | Same code scheme as `V717` |

### A7. Confounders — Age

| Variable | Description | Codes |
|---|---|---|
| `V012` | Respondent's current age (years) | Continuous, 15–49 |
| `V013` | Age in 5-year groups | 1 = 15–19; 2 = 20–24; 3 = 25–29; 4 = 30–34; 5 = 35–39; 6 = 40–44; 7 = 45–49 |

### A8. Confounders — Residence

| Variable | Description | Codes |
|---|---|---|
| `V024` | Division | 1 = Barishal; 2 = Chattogram; 3 = Dhaka; 4 = Khulna; 5 = Mymensingh; 6 = Rajshahi; 7 = Rangpur; 8 = Sylhet |
| `V025` | Type of place of residence | 1 = Urban; 2 = Rural |
| `V026` | De facto place of residence | 0 = Capital/large city; 1 = Small city; 2 = Town; 3 = Countryside; 9 = Missing |

### A9. Confounders — Marriage

| Variable | Description | Codes |
|---|---|---|
| `V511` | Age at first cohabitation | Continuous, 8–49 |
| `V513` | Cohabitation duration, grouped (years) | 0 = Never married; 1 = 0–4; 2 = 5–9; 3 = 10–14; 4 = 15–19; 5 = 20–24; 6 = 25–29; 7 = 30+ |

### A10. Confounders — Religion

| Variable | Description | Codes |
|---|---|---|
| `V130` | Religion | 1 = Islam; 2 = Hindu; 3 = Buddhist; 4 = Christianity; 96 = Others |

### A11. Confounders — Children Born

| Variable | Description | Codes |
|---|---|---|
| `V201` | Total children ever born | Continuous |
| `V212` | Age of respondent at first birth | Continuous |
| `V218` | Number of living children | Continuous, 0–20 |
| `V219` | Living children + current pregnancy | Continuous, 0–20 |

### A12. Confounders — Household Size

| Variable | Description | Codes |
|---|---|---|
| `V136` | Number of household members | Continuous |
| `V137` | Number of children age 5 and under in household | Continuous |
| `V138` | Number of eligible women in household | Continuous |

### A13. Confounders — Autonomy in Household Decisions

| Variable | Description | Codes |
|---|---|---|
| `V743A` | Decides on respondent's health care | 1 = Respondent alone; 2 = Respondent & husband jointly; 3 = Respondent & other person; 4 = Husband alone; 5 = Someone else; 6 = Other; 9 = Missing |
| `V743B` | Decides on large household purchases | Same code scheme as `V743A` |
| `V743D` | Decides on visits to family/relatives | Same code scheme as `V743A` |
| `V743F` | Decides what to do with money husband earns | Same code scheme as `V743A`, plus 7 = Husband/partner has no earnings |

`V743C` (daily-needs purchases) and `V743E` (food to cook) exist in the original codebook but are **not available** in this extract. `V743F`'s code 7 has no equivalent in `V743A`/`V743B`/`V743D` — it marks the item as not applicable rather than a lower level of autonomy (see Part B).

### A14. Confounders — Attitudes Toward Intimate Partner Violence

| Variable | Description | Codes |
|---|---|---|
| `V744A` | Beating justified: wife goes out without telling husband | 0 = No; 1 = Yes; 8 = Don't know; 9 = Missing |
| `V744B` | Beating justified: wife neglects children | Same code scheme |
| `V744C` | Beating justified: wife argues with husband | Same code scheme |
| `V744D` | Beating justified: wife refuses sex | Same code scheme |
| `V744E` | Beating justified: wife burns food | Same code scheme |

### A15. Confounders — Health Insurance & Media Exposure

| Variable | Description | Codes |
|---|---|---|
| `V481` | Covered by health insurance | 0 = No; 1 = Yes; 9 = Missing |
| `V157` | Frequency reads newspaper/magazine | 0 = Not at all; 1 = <1×/week; 2 = ≥1×/week; 3 = Almost daily; 9 = Missing |
| `V158` | Frequency listens to radio | Same code scheme |
| `V159` | Frequency watches TV | Same code scheme |
| `V171A` | Use of internet | 0 = Never; 1 = Yes, last 12 months; 2 = Yes, before last 12 months; 3 = Yes, timing unclear; 9 = Missing |

### A16. Contraceptive Use

| Variable | Description | Codes |
|---|---|---|
| `V312` | Current contraceptive method (detailed) | 0 = Not using; 1 = Pill; 2 = IUD; 3 = Injections; 4 = Diaphragm; 5 = Male condom; 6 = Female sterilization; 7 = Male sterilization; 8 = Periodic abstinence; 9 = Withdrawal; 10 = Other traditional; 11 = Implants/Norplant; 12 = Prolonged abstinence; 13 = LAM; 14 = Female condom; 15 = Foam/jelly; 16 = Emergency contraception; 17 = Other modern; 18 = SDM; 19–20 = Specific methods 1–2; 99 = Missing |
| `V313` | Current use by method type (simplified) | 0 = No method; 1 = Folkloric; 2 = Traditional; 3 = Modern; 9 = Missing |

### A17. Reproductive / Sexual Health

| Variable | Description | Codes |
|---|---|---|
| `V213` | Currently pregnant | 0 = No/unsure; 1 = Yes; 9 = Missing |
| `V226` | Time since last period (months, composite) | 0–400 continuous; 994 = In menopause; 995 = Before last pregnancy; 996 = Never menstruated; 997 = Inconsistent; 998 = Don't know; 999 = Missing |
| `V228` | Ever had a terminated pregnancy | 0 = No; 1 = Yes; 9 = Missing |
| `V536` | Recent sexual activity | 0 = Never had sex; 1 = Active in last 4 weeks; 2 = Not active — postpartum abstinence; 3 = Not active — other reason; 9 = Missing |

---

### A18. Survey Design

| Variable | Description | What it is used for |
|---|---|---|
| `CASEID` | Case Identification | Unique ID to identify individual |
| `V001` | Cluster number | Primary Sampling Unit (PSU) cluster identifier (Identical to `V021` — see Part B Survey Design; `V001` is retained here for the identity check but is not carried into the final analytic datasets) |
| `V005` | Individual sampling weight | Makes estimates representative of the target population |
| `V021` | Primary sampling unit | Accounts for clustering |
| `V022` | Sample stratum | Accounts for stratified sampling |

## Part B — Final Analysis Variables

Each row shows the analysis-ready variable (as it appears in `clean_recode`), its raw source variable(s), the collapsing/derivation logic, and the final category labels.

### Outcomes / Health Status

| Final variable | Source | Derivation | Final categories |
|---|---|---|---|
| **Depression** | `MTH22` | Pass-through of PHQ-9 severity band | 0 = 0–4 minimal; 1 = 5–9 mild; 2 = 10–14 moderate; 3 = 15–19 moderately severe; 4 = 20–27 severe |
| **Depression Binary** | `Depression` | Recoded: bands 0–1 (score <10) → 0; bands 2–4 (score ≥10) → 1, the standard PHQ-9 probable-case cutoff | 0 = No (score <10); 1 = Yes (score ≥10) |
| **Anxiety** | `MTH24` | Pass-through of GAD-7 severity band | 0 = 0–4 minimal; 1 = 5–9 mild; 2 = 10–14 moderate; 3 = 15–21 severe |
| **Anxiety Binary** | `Anxiety` | Recoded: bands 0–1 (score <10) → 0; bands 2–3 (score ≥10) → 1, the standard GAD-7 probable-case cutoff | 0 = No (score <10); 1 = Yes (score ≥10) |
| **Diabetes** | `SB267`, `SB236`, `SB240` | Flag = 1 if `SB267`≥126 OR `SB236`=Yes OR `SB240`=Yes; retained as its own column alongside the composite below | 0 = No; 1 = Yes |
| **Hypertension** | `WBP24`, `WBP25`, `WBP16`, `WBP19` | Flag = 1 if `WBP24`≥140 OR `WBP25`≥90 OR `WBP16`=Yes OR `WBP19`=Yes; retained as its own column alongside the composite below | 0 = No; 1 = Yes |
| **Obesity** | `HA40` | Flag = 1 if `HA40`≥3000; retained as its own column alongside the composite below | 0 = No; 1 = Yes |
| **Cardiometabolic Burden** | `Diabetes`, `Hypertension`, `Obesity` | Sum of the three binary flags above | 0 = None; 1 = One burden; 2 = Two burdens; 3 = Three burdens |
| **Cardiometabolic Burden Merged** | `Cardiometabolic Burden` | Collapsed: 0 and 1 kept as-is; 2 and 3 combined into a single "two or more" category, to thicken the top cell | 0 = None; 1 = One burden; 2 = Two or more burdens |
| **Cardiometabolic Burden Binary** | `Cardiometabolic Burden Merged` | Collapsed further: 0 → 0; 1 or 2 → 1 | 0 = No burden; 1 = Any burden |

### Socioeconomic Status

| Final variable | Source | Derivation | Final categories |
|---|---|---|---|
| **Socioeconomic Status** | `V190` (or `V190A`) | Pass-through of wealth quintile | 1 = Poorest; 2 = Poorer; 3 = Middle; 4 = Richer; 5 = Richest |

### Socioeconomic Confounders

| Final variable | Source | Derivation | Final categories |
|---|---|---|---|
| **Education** | `V106` | Pass-through of highest level attained | 0 = No education; 1 = Primary; 2 = Secondary; 3 = Higher |
| **Occupation** | `V714` | Pass-through | 0 = No; 1 = Yes |
| **Partner occupation** | `V705` | Collapsed: code 0 → "Not working"; codes 1–9 → "Working"; code 98 → "Don't know" (explicit category, not treated as missing) | 1 = Not working; 2 = Working; 3 = Don't know |

### Demographics / Confounders

*A **Marital status** variable is no longer part of the analytic pipeline: the eligibility filter now restricts the sample to currently married women (`S111A == 1`) directly, so the variable would be constant (zero variance) across the analytic sample and was dropped.*

| Final variable | Source | Derivation | Final categories |
|---|---|---|---|
| **Age** | `V013` | Collapsed from 7 five-year bands to 3: {1,2} → 15–24; {3,4} → 25–34; {5,6,7} → 35–49 | 1 = 15–24; 2 = 25–34; 3 = 35–49 |
| **Division** | `V024` | Pass-through | 1 = Barishal; 2 = Chattogram; 3 = Dhaka; 4 = Khulna; 5 = Mymensingh; 6 = Rajshahi; 7 = Rangpur; 8 = Sylhet |
| **Residence** | `V025` | Pass-through | 1 = Urban; 2 = Rural |
| **Religion** | `V130` | Collapsed: code 1 ("Islam") kept as-is; codes 2–96 (Hindu/Buddhist/Christianity/Others) collapsed together | 1 = Islam; 2 = Others |
| **Children** | `V201` | Pass-through for values 0–3, top-coded at 4 | 0 = No children; 1; 2; 3; 4 = 4 or more |
| **Family size** | `V136` | Collapsed at a threshold of 5 household members | 1 = Less than 5; 2 = 5 or more |
| **Age at first cohabitation** | `V511` | Collapsed from single years into 4 bands | 0 = <15; 1 = 15–24; 2 = 25–34; 3 = 35–49 |

### Household Autonomy & Attitudes

| Final variable | Source | Derivation | Final categories |
|---|---|---|---|
| **Household Autonomy** | `V743A`, `V743B`, `V743D` | For each item, recoded to 1 if the respondent has a say (raw codes 1–3: alone / jointly / with another person) or 0 if she does not (raw codes 4–6, 9); the three binary indicators are then summed. `V743F` (money husband earns) is deliberately **excluded** from this composite — see *Financial Decision-Making* below and the note under Part A13 | 0 = No autonomy; 1 = 1 decision; 2 = 2 decisions; 3 = 3 decisions |
| **Financial Decision-Making** | `V743F` | Kept as its own variable rather than merged into *Household Autonomy*, because raw code 7 ("Husband/partner has no earnings") marks the item as not applicable for ~1.3% of the sample, not a lower level of autonomy — merging it would force either an arbitrary denominator correction or an unjustified "no earnings = no autonomy" assumption. Recoded to 1 if the respondent has a say (codes 1–3), 0 if she does not (codes 4–6), 2 if there are no earnings to decide about (code 7). This mirrors DHS's own convention: the official "Participation in Decision Making" indicator and SDG Indicator 5.6.1 are both built from `V743A`/`V743B`/`V743D` only, with the money-earned item tracked as a separate empowerment dimension (DHS Guide to DHS Statistics; Kishor & Subaiya 2008, DHS Comparative Reports No. 20). Ambiguous causal role relative to Wealth (plausible confounder or plausible mediator — see `Supplementary Figure S1`) keeps it out of the primary adjustment set; tested together with IPV Attitude as a sensitivity addition in `6. Main Regression Analysis.ipynb`, Section 22, where neither changes the interaction finding | 0 = Husband/other decides; 1 = Respondent has a say; 2 = No earnings (N/A) |
| **IPV Attitude** | `V744A`–`V744E` | Recoded to a 3-level variable rather than binary, so "don't know" (raw code 8) gets its own category instead of being silently absorbed into "does not justify": **Justifies** (2) if any item = Yes; else **Uncertain** (1) if any item = Don't know; else **Rejects** (0). Extends DHS's own "any Yes wins" convention for this item with a second tier rather than collapsing don't-know into a numeric scale position. Not in the primary adjustment set — it's a DAG cause of Education and Mental Health but not of Wealth, so conditioning on Education (already in the model) already blocks its one backdoor path; tested alongside Financial Decision-Making as a sensitivity addition regardless (Section 22 above) | 0 = Rejects in all scenarios; 1 = Uncertain (Don't know, never affirms); 2 = Justifies in ≥1 scenario |

### Health Access / Media

| Final variable | Source | Derivation | Final categories |
|---|---|---|---|
| **Insurance** | `V481` | Pass-through. Present in the analysis data but excluded from the regression adjustment set: complete separation (0 of 16 insured women screen positive for either outcome) makes its coefficient a data artifact rather than a real estimate — see `6. Main Regression Analysis.ipynb`, Section 5 | 0 = No; 1 = Yes |
| **Mass Media** | `V171A`, `V159` | Combines internet use (`V171A`) and TV-watching frequency (`V159`): both 0 ("never") → 0; `V159` ∈ {1,2,3} (watches TV) and `V171A` = 0 → 1; `V171A` ∈ {1,2,3} (has used internet) and `V159` = 0 → 2; both non-zero → 3. Replaces the earlier internet-only variable | 0 = Neither; 1 = Television only; 2 = Internet only; 3 = Both television and internet |

### Reproductive Health

| Final variable | Source | Derivation | Final categories |
|---|---|---|---|
| **Contraceptive** | `V313` | Pass-through | 0 = No method; 1 = Folkloric method; 2 = Traditional method; 3 = Modern method |
| **Abortion** | `V228` | Pass-through | 0 = No; 1 = Yes |
| **Pregnant** | `V213` | Pass-through | 0 = No or unsure; 1 = Yes |
| **Menopause** | `V226` | Flag = 1 if `V226` == 994 ("In menopause"), else 0 | 0 = No; 1 = Yes |
| **Sexual activity** | `V536` | Collapsed: code 1 ("Active in last 4 weeks") → Active; codes 0, 2, 3 → Not active | 0 = Not active; 1 = Active |
| **Postpartum** | `V536` | Separate collapse of the same raw item: code 2 ("Not active — postpartum abstinence") → Yes; all other codes → No | 0 = No; 1 = Yes |

---

### Survey Design

Four survey-design variables are carried into the final analytic dataset (`depression-anxiety-dataset.csv`), alongside the substantive variables in the tables above. This single file replaced the earlier `depression_dataset.csv` / `anxiety_dataset.csv` pair — Depression and Anxiety (and their binary versions) are now columns of the same file, since both outcomes are measured on the same women:

| Final variable | Source | Role |
|---|---|---|
| **CASEID** | `CASEID` | Unique respondent identifier (record linkage / de-duplication, not entered as a model term) |
| **Sampling weight** | `V005` | Individual sampling weight, rescaled by dividing by 1,000,000 per DHS convention, so estimates are representative of the target population |
| **PSU** | `V021` | Primary sampling unit; accounts for clustering in variance estimation. `V001` ("Cluster number") is identical to `V021` (verified: `(V001==V021).mean() == 1.0`) and is therefore **not** carried into the final datasets — `PSU` is the single retained cluster identifier |
| **Stratum** | `V022` | Sample stratum; accounts for stratified sampling in variance estimation |

```markdown
                       BDHS sampling design
                              │
         ┌─────────────┬──────┴──────┬─────────────┐
         ▼             ▼             ▼             ▼
      CASEID        Weight          PSU         Stratum
      CASEID         V005          V021          V022
         │             │             │             │
         └─────────────┴──────┬──────┴─────────────┘
                               ▼
                   Survey-weighted regression
                (svyset: psu=PSU, strata=Stratum,
                       weight=Sampling weight)
```

---

## Part C — Raw Variables Retained but Not Mapped to a Final Analysis Variable

These are present in `recode` (available in the dataset) but are not directly used to build a `clean_recode` variable — likely kept for descriptive tables, alternate specifications, or sensitivity analysis:

`V020`, `V026`, `V501`, `HV104`, `V133`, `V149`, `V190A`, `V191`, `V191A`, `V731`, `V716`, `V717`, `V704`, `V513`, `V212`, `V218`, `V219`, `V137`, `V138`, `V157`, `V158`, `V312`, `MTH10`

*`V511` (age at first cohabitation) and `V159` (TV-watching frequency) were moved out of this list into Part B: `V511` now maps to **Age at first cohabitation**, and `V159` is now a joint source (with `V171A`) for **Mass Media**.*

- `V026` (de facto place of residence, 6-category) is superseded by the de jure `V025` (urban/rural) used for the final **Residence** variable, but is retained for a possible de facto vs. de jure sensitivity check.
- `V501` (marital status, alternate coding) is superseded by `S111A` as the eligibility-filter variable (see Purpose, above), but is retained for cross-checking the currently-married restriction against an independent marital-status item.

---

## Part D — Columns Not Available in This Extract

`V511A`, `V176`, `V485A`, `V485B`, `V743C`, `V743E`, `V463A`–`V463Z` (all smoking sub-items), `V463AA`, `V463AB`, `V464`, `V471A`–`V471I`, `V471CS`, `V472A`–`V472W`, `V472WA`–`V472WE`