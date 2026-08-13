### Population

- **Ever-married = 1 if**
    - `V020` == 1
- **Current marital status**
    - `S111A`
        - 1 == Currently married
        - 2 == Seperated
        - 3 == Deserted
        - 4 == Divorced
        - 5 == Widowed
    - `V501`
        - 0 == Never married
        - 1 == Married
        - 2 == Living together
        - 3 == Widowed
        - 4 == Divorced
        - 5 == Not living together
        - 9 == Missing

- **Sex of household member [`BDPR81SV`]**
    - `HV104`
        - 1 == Male
        - 2 == Female
        - 9 == Missing

---

### Cardiometabolic Burden [`BDPR81SV`]

#### 1. Diabetes (WHO Standard)

- **Diabetes = 1 if**
    - `SB267` >= 126            [ Plasma glucose (mg/dL) ]
    - OR `SB236` == Yes         [ Ever diagnosed with diabetes ]
    - OR `SB240` == Yes         [ Currently taking medication ]

#### 2. Hypertension (WHO Standard)

- **Hypertension = 1 if**
    - `WBP24` >= 140            [ Final systolic BP ]
    - OR `WBP25` >= 90          [ Final diastolic BP ]
    - OR `WBP16` = Yes          [ Previously diagnosed hypertension ]
    - OR `WBP19` = Yes          [ Taking BP medication ]

#### 3. Obesity (WHO Standard)

- **Obesity = 1 if**
    - `V445` or `HA40` >= 30              [ BMI ]

#### 4. Cardiometabolic burden
- 0 = none
- 1 = one condition
- 2 = two conditions
- 3 = three conditions

---

### Depression / Anxiety

#### Depression

- **PHQ-9 Score**
    - `MTH22`
        - 0 to 4 == 0
        - 5 to 9 == 1
        - 10 to 14 == 2
        - 15 to 19 == 3
        - 20 to 27 == 4

#### Anxiety

- **GAD-7 Score**
    - `MTH24`
        - 0 to 4 == 0
        - 5 to 9 == 1
        - 10 to 14 == 2
        - 15 to 21 == 3

---

### Socioeconomic Position (SEP) — Composite Index

#### 1. Education

- **Education in single years (Continuous)** 
    - `V133`
- **Educational attainment**
    - `V149`
        - 0 == No education
        - 1 == Incomplete primary
        - 2 == Complete primary
        - 3 == Incomplete secondary
        - 4 == Complete secondary
        - 5 == Higher
        - 9 == Missing
- **Highest educational level**
    - `V106`
        - 0 == No education
        - 1 == Primary
        - 2 == Secondary
        - 3 == Higher

#### 2. Wealth / Household Wealth

- **Wealth index factor score combined (Continuous)**
    - `V191`    or  `V191A` (urban/rural clustering separately)
        — household-level, identical to `HV271` in RECH2.dta
- **Wealth index combined (categorical):**
    - `V190`    or  `V190A` (urban/rural clustering separately)
        — household-level, identical to `HV270` in RECH2.dta
        - 1 == Poorest
        - 2 == Poorer
        - 3 == Middle
        - 4 == Richer
        - 5 == Richest

#### 3. Occupation

- **Respondent currently working**
    - `V714`
        - 0 == No
        - 1 == Yes
- **Respondent worked in last 12 months**
    - `V731`
        - 0 == No
        - 1 == In the past year
        - 2 == Currently working
        - 3 == Have a job, but on leave last 7 days
        - 9 == Missing
- **Respondent's occupation**
    - `V716`
        - 0 == Not working and didn't work in last 12 months
        - 11 == Land Owner
        - 12 == Farmer
        - 13 == Agricultural Worker
        - 14 == Fisherman
        - 15 == Poultry raising, Cattle raising
        - 16 == Home-based Manufacturing (Handicraft, Food products)
        - 21 == Rickshaw driver, Brick breaking, Road building, Construction worker, Boa
        - 22 == Domestic servant
        - 23 == Non-agricultural worker (Factory worker, blue collar service)
        - 31 == Carpenter, Masson, Bus/taxi driver, Construction supervisor, Seamstresse
        - 41 == Doctor, Lawyer, Dentist, Accountant, Teacher, Nurse, Family welfare visi
        - 51 == Big businessman
        - 52 == Small business/trader
        - 61 == Unemployed/student
        - 62 == Retired
        - 96 == Others
        - 99998 == Don't know
        - 99999 == Missing
- **Respondent's occupation (grouped)** 
    - `V717`
        - 0 == Not working
        - 1 == Professional/technical/managerial
        - 2 == Clerical
        - 3 == Sales
        - 4 == Agricultural – self employed
        - 5 == Agricultural – employee
        - 6 == Household and domestic
        - 7 == Services
        - 8 == Skilled manual
        - 9 == Unskilled manual
- **Husband/partner's occupation**
    - `V704`
        - 0 == Not working and didn't work in last 12 months
        - 11 == Land Owner
        - 12 == Farmer
        - 13 == Agricultural Worker
        - 14 == Fisherman
        - 15 == Poultry raising, Cattle raising
        - 16 == Home-based Manufacturing (Handicraft, Food products)
        - 21 == Rickshaw driver, Brick breaking, Road building, Construction worker, Boa
        - 22 == Domestic servant
        - 23 == Non-agricultural worker (Factory worker, blue collar service)
        - 31 == Carpenter, Masson, Bus/taxi driver, Construction supervisor, Seamstresse
        - 41 == Doctor, Lawyer, Dentist, Accountant, Teacher, Nurse, Family welfare visi
        - 51 == Big businessman
        - 52 == Small business/trader
        - 61 == Unemployed/student
        - 62 == Retired
        - 96 == Others
        - 99998 == Don't know
        - 99999 == Missing
- **Husband/partner's occupation (grouped):** 
    - `V705`
        - 0 == Not working
        - 1 == Professional/technical/managerial
        - 2 == Clerical
        - 3 == Sales
        - 4 == Agricultural – self employed
        - 5 == Agricultural – employee
        - 6 == Household and domestic
        - 7 == Services
        - 8 == Skilled manual
        - 9 == Unskilled manual

### Confounders

#### Age

- **Respondent's current age**
    - `V012`
        - 15:49 
- **Age in 5-year groups**
    - `V013`
        - 1 == 15-19
        - 2 == 20-24
        - 3 == 25-29
        - 4 == 30-34
        - 5 == 35-39
        - 6 == 40-44
        - 7 == 45-49

#### Residence

- **Division**
    - `V024`
        - 1 == Barishal
        - 2 == Chattogram
        - 3 == Dhaka
        - 4 == Khulna
        - 5 == Mymensingh
        - 6 == Rajshahi
        - 7 == Rangpur
        - 8 == Sylhet
- **Type of place of residence**
    - `V025`
        - 1 == Urban
        - 2 == Rural
- **De facto place of residence**
    - `V026`
        - 0 == Capital, large city
        - 1 == Small city
        - 2 == Town
        - 3 == Countryside
        - 9 == Missing

#### Marriage

- **Age at first cohabitation**
    - `V511`
        - 8:49
- **Age at current cohabitation**
    - `V511A`   **[ NA ]**
        - 8:49
- **Cohabitation duration (grouped)**
    - `V513`
        - 0 == Never married
        - 1 == 0-4
        - 2 == 5-9
        - 3 == 10-14
        - 4 == 15-19
        - 5 == 20-24
        - 6 == 25-29
        - 7 == 30+

#### Religion

- `V130`
    - 1 == Islam
    - 2 == Hindu
    - 3 == Christian
    - 4 == Other

#### Smoking

- **Smokes cigarettes (or anything related)**
    - `V463A` to `V463Z`   **[ NA ]**
        - 0 == No
        - 1 == Yes
        - 9 == Missing
- **Frequency smokes cigarettes**
    - `V463AA`   **[ NA ]**
        - 0 == Does not smoke
        - 1 == Everyday
        - 2 == Someday
        - 9 == Missing
- **Frequency currently uses other type of tob**
    - `V463AB`   **[ NA ]**
        - 0 == Does not smoke
        - 1 == Everyday
        - 2 == Someday
        - 9 == Missing
- **Number of cigarettes in last 24 hours**
    - `V464`   **[ NA ]**
        - 0:79
        - 80+
        - 98 == Don't know
        - 99 == Missing
        
#### Children born

- **Total children ever born**
    - `V201`
        - 0:20
- **Age of respondent at 1st birth**
    - `V212`
        - 10:49
- **Number of living children**
    - `V218`
        - 0:20  
- **Living children + current pregnancy**
    - `V219`
        - 0:20

#### Household size

- **Number of household members**
    - `V136`
- **Number of children 5 and under in household**
    - `V137`
- **Number of eligible women in household**
    - `V138`

#### Autonomy in household decision

- **Person who decides on respondent's health care**
    - `V743A`
        - 1 == Respondent alone
        - 2 == Respondent & husband/partner jointly
        - 3 == Respondent and other person
        - 4 == Husband/partner alone
        - 5 == Someone else
        - 6 == Other
        - 9 == Missing
- **Person who decides on large household purchases**
    - `V743B`
        - Same as above
- **Person who decides on household purchases for daily needs**
    - `V743C`   **[ NA ]**
        - Same as above
- **Person who decides on visits to family/relatives**
    - `V743D` 
        - Same as above
- **Person who decides on food to be cooked each day**
    - `V743E`   **[ NA ]**
        - Same as above
- **Person who decides on what to do with money husband earns**
    - `V743F`
        - Same as above

#### Food insucurity

- **Woman had tinned, powdered or fresh milk (& similar)**
    - `V471A` to `V471I`   **[ NA ]**
        - 0 == No
        - 1 == Yes
        - 2 == Don't know
        - 9 == Missing
- **Woman other liquid - sweetened**
    - `V471CS`   **[ NA ]**
        - Same as above
- **Woman had other vegetables (& similar)**
    - `V472A` to `V472W`   **[ NA ]**
        - Same as above
- **Woman had CS foods**
    - `V472WA` to `V472WE`   **[ NA ]**
        - Same as above

#### Physical/Sexual/Emotional Abuse

- **Beating justified if wife goes out without telling husband**
    - `V744A`
        - 0 == No
        - 1 == Yes
        - 8 == Don't know
        - 9 == Missing
- **Beating justified if wife neglects the children**
    - `V744B`
        - Same as above
- **Beating justified if wife argues with husband**
    - `V744C`
        - Same as above
- **Beating justified if wife refuses to have sex with husband**
    - `V744D`
        - Same as above
- **Beating justified if wife burns the food**
    - `V744E`
        - Same as above

#### Sleep Quality

- **Last 2 weeks: trouble falling asleep or sleepin**
    - `MTH10`
        - 0 == Never
        - 1 == Rarely
        - 2 == Often
        - 3 == Always
        - 7 == Refused to answer
        - 8 == Don't know

#### Self-rated health

- **Self reported health status**
    - `V176`   **[ NA ]**
        - 1 == Very good
        - 2 == Good
        - 3 == Moderate
        - 4 == Bad
        - 5 == Very bad

#### Health insurance

- **Covered by health insurance**
    - `V481`
        - 0 == No
        - 1 == Yes
        - 9 == Missing

#### Mass Media Exposure

- **Frequency of reading newspaper/magazine**
    - `V157`
        - 0 == Not at all
        - 1 == Less than once a week
        - 2 == At least once a week
        - 3 == Almost every day
        - 9 == Missing
- **Frequency of listening to radio**
    - `V158`
        - Same as above
- **Frequency of watching television**
    - `V159`
        - Same as above
- **Use of internet**
    - `V171A`
        - 0 == Never
        - 1 == Yes, last 12 months
        - 2 == Yes, before last 12 months
        - 3 == Yes, can't establish when
        - 9 == Missing

#### Alcohol

- **Number of days respondent drank alcoholic**
    - `V485A`   **[ NA ]**
        - 0 == Did not have even one drink
        - 1:31  
        - 95 == Every day/almost every day
        - 96 == Never have consumed alcohol
        - 99 == Missing
- **Number of alcoholic drinks per day**
    - `V485B`   **[ NA ]**
        - 1:39
        - 40 == 40+
        - 99 == Missing

#### Contraceptive Use

- **Current contraceptive method** 
    - `V312`
        - 0 == Not using
        - 1 == Pill
        - 2 == IUD
        - 3 == Injections
        - 4 == Diaphragm
        - 5 == Male condom
        - 6 == Female sterilization
        - 7 == Male sterilization
        - 8 == Periodic abstinence
        - 9 == Withdrawal
        - 10 == Other traditional
        - 11 == Implants/Norplant
        - 12 == Prolonged abstinence
        - 13 == Lactational amenorrhea (LAM)
        - 14 == Female condom
        - 15 == Foam or jelly
        - 16 == Emergency contraception
        - 17 == Other modern method
        - 18 == Standard days method (SDM)
        - 19 == Specific method 1
        - 20 == Specific method 2
        - 99 == Missing

- **Current use by method type (simplified/collapsed version)**
    - `V313`
        - 0 == No method
        - 1 == Folkloric method
        - 2 == Traditional method
        - 3 == Modern method
        - 9 == Missing

#### Miscarriage/Abortion

- **Ever had a terminated pregnancy**
    - `V228`
        - 0 == No
        - 1 == Yes
        - 9 == Missing

---

### Columns Not Available

['V511A', 'V176', 'V485A', 'V485B', 'V743C', 'V743E', 'V463A', 'V463B', 'V463C', 'V463D', 'V463E', 'V463F', 'V463G', 'V463H', 'V463I', 'V463J', 'V463K', 'V463L', 'V463X', 'V463Z', 'V463AA', 'V463AB', 'V464', 'V471A', 'V471B', 'V471C', 'V471D', 'V471E', 'V471F', 'V471G', 'V471H', 'V471I', 'V471CS', 'V472A', 'V472B', 'V472C', 'V472D', 'V472E', 'V472F', 'V472G', 'V472H', 'V472I', 'V472J', 'V472K', 'V472L', 'V472M', 'V472N', 'V472O', 'V472P', 'V472Q', 'V472R', 'V472S', 'V472T', 'V472U', 'V472V', 'V472W', 'V472WA', 'V472WB', 'V472WC', 'V472WD', 'V472WE']
