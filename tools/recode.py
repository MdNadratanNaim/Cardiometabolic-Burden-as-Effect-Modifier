import html
import json
import uuid
import pandas as pd
from IPython.display import display, HTML


# ---------------------------------------------------------------------------
# Recode Dictionary
# ---------------------------------------------------------------------------

recode = {
    # --- Population ---
    "V020": {
        "name": "Type of sample or ever-married indicator",
        "value": {1: "Ever-married", 0: "All woman"},
    },
    "S111A": {
        "name": "Current marital status",
        "value": {1: "Currently married", 2: "Separated", 3: "Deserted", 4: "Divorced", 5: "Widowed"},
    },
    "V501": {
        "name": "Current marital status",
        "value": {0: "Never married", 1: "Married", 2: "Living together", 3: "Widowed", 4: "Divorced", 5: "Not living together", 9: "Missing"},
    },
    "HV104": {
        "name": "Sex of household member",
        "value": {1: "Male", 2: "Female", 9: "Missing"},
    },

    # --- Cardiometabolic burden: Diabetes ---
    "SB267": {"name": "Plasma glucose (mg/dL)", "value": None},
    "SB236": {
        "name": "Ever diagnosed with diabetes",
        "value": {0: "No", 1: "Yes", 9: "Missing"},
    },
    "SB240": {
        "name": "Currently taking medication for diabetes",
        "value": {0: "No", 1: "Yes", 9: "Missing"},
    },

    # --- Cardiometabolic burden: Hypertension ---
    "WBP24": {"name": "Final systolic blood pressure (mmHg)", "value": None},
    "WBP25": {"name": "Final diastolic blood pressure (mmHg)", "value": None},
    "WBP16": {
        "name": "Previously diagnosed with hypertension",
        "value": {0: "No", 1: "Yes"},
    },
    "WBP19": {
        "name": "Currently taking blood pressure medication",
        "value": {0: "No", 1: "Yes"},
    },

    # --- Cardiometabolic burden: Obesity ---
    "HA40": {"name": "Body Mass Index (BMI)", "value": None},

    # --- Depression / Anxiety ---
    "MTH22": {
        "name": "PHQ-9 depression score (categorized)",
        "value": {0: "0-4 (minimal)", 1: "5-9 (mild)", 2: "10-14 (moderate)", 3: "15-19 (moderately severe)", 4: "20-27 (severe)"},
    },
    "MTH24": {
        "name": "GAD-7 anxiety score (categorized)",
        "value": {0: "0-4 (minimal)", 1: "5-9 (mild)", 2: "10-14 (moderate)", 3: "15-21 (severe)"},
    },
    "MTH10": {
        "name": "Trouble falling/staying asleep, last 2 weeks",
        "value": {0: "Never", 1: "Rarely", 2: "Often", 3: "Always", 7: "Refused to answer", 8: "Don't know"},
    },

    # --- SES: Education ---
    "V133": {"name": "Education in single years", "value": None},
    "V149": {
        "name": "Educational attainment",
        "value": {0: "No education", 1: "Incomplete primary", 2: "Complete primary", 3: "Incomplete secondary", 4: "Complete secondary", 5: "Higher", 9: "Missing"},
    },
    "V106": {
        "name": "Highest educational level",
        "value": {0: "No education", 1: "Primary", 2: "Secondary", 3: "Higher"},
    },

    # --- SES: Wealth ---
    "V190": {
        "name": "Wealth index combined (categorical)",
        "value": {1: "Poorest", 2: "Poorer", 3: "Middle", 4: "Richer", 5: "Richest"},
    },
    "V190A": {
        "name": "Wealth index combined (categorical, urban/rural clustered)",
        "value": {1: "Poorest", 2: "Poorer", 3: "Middle", 4: "Richer", 5: "Richest"},
    },
    "V191": {"name": "Wealth index factor score combined", "value": None},
    "V191A": {"name": "Wealth index factor score combined (urban/rural clustered)", "value": None},

    # --- SES: Occupation ---
    "V714": {
        "name": "Respondent currently working",
        "value": {0: "No", 1: "Yes"},
    },
    "V731": {
        "name": "Respondent worked in last 12 months",
        "value": {0: "No", 1: "In the past year", 2: "Currently working", 3: "Have a job, but on leave last 7 days", 9: "Missing"},
    },
    "V716": {
        "name": "Respondent's occupation (detailed)",
        "value": {
            0: "Not working and didn't work in last 12 months",
            11: "Land Owner", 12: "Farmer", 13: "Agricultural Worker",
            14: "Fisherman", 15: "Poultry raising, Cattle raising",
            16: "Home-based Manufacturing (Handicraft, Food products)",
            21: "Rickshaw driver, Brick breaking, Road building, Construction worker, Boatman",
            22: "Domestic servant",
            23: "Non-agricultural worker (Factory worker, blue collar service)",
            31: "Carpenter, Mason, Bus/taxi driver, Construction supervisor, Seamstress",
            41: "Doctor, Lawyer, Dentist, Accountant, Teacher, Nurse, Family welfare visitor",
            51: "Big businessman", 52: "Small business/trader",
            61: "Unemployed/student", 62: "Retired", 96: "Others",
            99998: "Don't know", 99999: "Missing",
        },
    },
    "V717": {
        "name": "Respondent's occupation (grouped)",
        "value": {0: "Not working", 1: "Professional/technical/managerial", 2: "Clerical", 3: "Sales", 4: "Agricultural - self employed",
                   5: "Agricultural - employee", 6: "Household and domestic", 7: "Services", 8: "Skilled manual", 9: "Unskilled manual"},
    },
    "V704": {
        "name": "Husband/partner's occupation (detailed)",
        "value": {
            0: "Not working and didn't work in last 12 months",
            11: "Land Owner", 12: "Farmer", 13: "Agricultural Worker",
            14: "Fisherman", 15: "Poultry raising, Cattle raising",
            16: "Home-based Manufacturing (Handicraft, Food products)",
            21: "Rickshaw driver, Brick breaking, Road building, Construction worker, Boatman",
            22: "Domestic servant",
            23: "Non-agricultural worker (Factory worker, blue collar service)",
            31: "Carpenter, Mason, Bus/taxi driver, Construction supervisor, Seamstress",
            41: "Doctor, Lawyer, Dentist, Accountant, Teacher, Nurse, Family welfare visitor",
            51: "Big businessman", 52: "Small business/trader",
            61: "Unemployed/student", 62: "Retired", 96: "Others",
            99998: "Don't know", 99999: "Missing",
        },
    },
    "V705": {
        "name": "Husband/partner's occupation (grouped)",
        "value": {0: "Not working", 1: "Professional/technical/managerial", 2: "Clerical", 3: "Sales", 4: "Agricultural - self employed",
                   5: "Agricultural - employee", 6: "Household and domestic", 7: "Services", 8: "Skilled manual", 9: "Unskilled manual",
                   98: "Don't know"},
    },

    # --- Confounders: Age ---
    "V012": {"name": "Respondent's current age (years)", "value": None},
    "V013": {
        "name": "Age in 5-year groups",
        "value": {1: "15-19", 2: "20-24", 3: "25-29", 4: "30-34", 5: "35-39", 6: "40-44", 7: "45-49"},
    },

    # --- Confounders: Residence ---
    "V024": {
        "name": "Division",
        "value": {1: "Barishal", 2: "Chattogram", 3: "Dhaka", 4: "Khulna", 5: "Mymensingh", 6: "Rajshahi", 7: "Rangpur", 8: "Sylhet"},
    },
    "V025": {
        "name": "Type of place of residence",
        "value": {1: "Urban", 2: "Rural"},
    },
    "V026": {
        "name": "De facto place of residence",
        "value": {0: "Capital, large city", 1: "Small city", 2: "Town", 3: "Countryside", 9: "Missing"},
    },

    # --- Confounders: Marriage ---
    "V511": {"name": "Age at first cohabitation", "value": None},
    "V513": {
        "name": "Cohabitation duration, grouped (years)",
        "value": {0: "Never married", 1: "0-4", 2: "5-9", 3: "10-14", 4: "15-19", 5: "20-24", 6: "25-29", 7: "30+"},
    },

    # --- Confounders: Religion ---
    "V130": {
        "name": "Religion",
        "value": {1: "Islam", 2: "Hindu", 3: "Buddhist", 4: "Christianity", 96: "Others"},
    },

    # --- Confounders: Children born ---
    "V201": {"name": "Total children ever born", "value": None},
    "V212": {"name": "Age of respondent at first birth", "value": None},
    "V218": {"name": "Number of living children", "value": None},
    "V219": {"name": "Living children + current pregnancy", "value": None},

    # --- Confounders: Household size ---
    "V136": {"name": "Number of household members", "value": None},
    "V137": {"name": "Number of children age 5 and under in household", "value": None},
    "V138": {"name": "Number of eligible women in household", "value": None},

    # --- Confounders: Health insurance ---
    "V481": {
        "name": "Covered by health insurance",
        "value": {0: "No", 1: "Yes", 9: "Missing"},
    },

    # --- Confounders: Mass media exposure ---
    "V157": {
        "name": "Frequency of reading newspaper/magazine",
        "value": {0: "Not at all", 1: "Less than once a week", 2: "At least once a week", 3: "Almost every day", 9: "Missing"},
    },
    "V158": {
        "name": "Frequency of listening to radio",
        "value": {0: "Not at all", 1: "Less than once a week", 2: "At least once a week", 3: "Almost every day", 9: "Missing"},
    },
    "V159": {
        "name": "Frequency of watching television",
        "value": {0: "Not at all", 1: "Less than once a week", 2: "At least once a week", 3: "Almost every day", 9: "Missing"},
    },
    "V171A": {
        "name": "Use of internet",
        "value": {0: "Never", 1: "Yes, last 12 months", 2: "Yes, before last 12 months", 3: "Yes, can't establish when", 9: "Missing"},
    },

    # --- Confounders: Autonomy in household decision-making ---
    "V743A": {
        "name": "Person who decides on respondent's health care",
        "value": {1: "Respondent alone", 2: "Respondent & husband/partner jointly",
                   3: "Respondent and other person", 4: "Husband/partner alone",
                   5: "Someone else", 6: "Other", 9: "Missing"},
    },
    "V743B": {
        "name": "Person who decides on large household purchases",
        "value": {1: "Respondent alone", 2: "Respondent & husband/partner jointly",
                   3: "Respondent and other person", 4: "Husband/partner alone",
                   5: "Someone else", 6: "Other", 9: "Missing"},
    },
    "V743D": {
        "name": "Person who decides on visits to family/relatives",
        "value": {1: "Respondent alone", 2: "Respondent & husband/partner jointly",
                   3: "Respondent and other person", 4: "Husband/partner alone",
                   5: "Someone else", 6: "Other", 9: "Missing"},
    },
    "V743F": {
        "name": "Person who decides what to do with money husband earns",
        "value": {1: "Respondent alone", 2: "Respondent & husband/partner jointly",
                   3: "Respondent and other person", 4: "Husband/partner alone",
                   5: "Someone else", 7: "Husband/partner has no earnings", 6: "Other", 9: "Missing"},
    },

    # --- Confounders: Attitudes toward IPV (proxy for domestic violence exposure) ---
    "V744A": {
        "name": "Wife beating justified if she goes out without telling husband",
        "value": {0: "No", 1: "Yes", 8: "Don't know", 9: "Missing"},
    },
    "V744B": {
        "name": "Wife beating justified if she neglects the children",
        "value": {0: "No", 1: "Yes", 8: "Don't know", 9: "Missing"},
    },
    "V744C": {
        "name": "Wife beating justified if she argues with husband",
        "value": {0: "No", 1: "Yes", 8: "Don't know", 9: "Missing"},
    },
    "V744D": {
        "name": "Wife beating justified if she refuses to have sex with husband",
        "value": {0: "No", 1: "Yes", 8: "Don't know", 9: "Missing"},
    },
    "V744E": {
        "name": "Wife beating justified if she burns the food",
        "value": {0: "No", 1: "Yes", 8: "Don't know", 9: "Missing"},
    },

    # --- Confounders: Contraceptive Use ---
    "V312": {
        "name": "Current contraceptive method",
        "value": {0: "Not using", 1: "Pill", 2: "IUD", 3: "Injections", 4: "Diaphragm", 5: "Male condom", 6: "Female sterilization", 
                   7: "Male sterilization", 8: "Periodic abstinence", 9: "Withdrawal", 10: "Other traditional", 11: "Implants/Norplant", 
                   12: "Prolonged abstinence", 13: "Lactational amenorrhea (LAM)", 14: "Female condom", 15: "Foam or jelly", 
                   16: "Emergency contraception", 17: "Other modern method", 18: "Standard days method (SDM)", 19: "Specific method 1", 
                   20: "Specific method 2", 99:  "Missing"}
    },
    "V313": {
        "name": "Current use by method type (simplified/collapsed version)",
        "value": {0: "No method", 1: "Folkloric method", 2: "Traditional method", 3: "Modern method", 9: "Missing"}
    },

    # --- Sexual/Pregnancy ---
    "V213": {
        "name": "Currently pregnant",
        "value": {0: "No or unsure", 1: "Yes", 9: "Missing"}
    },
    "V226": {
        "name": "Time since last period (comp) (months)",
        "value": {"Continuous": "0:400", 994: "In menopause", 995: "Before last pregnancy", 
               996: "Never menstruated", 997: "Inconsistent", 998: "Don't know", 999: "Missing"}
    },
    "V228": {
        "name": "Ever had a terminated pregnancy",
        "value": {0: "No", 1: "Yes", 9: "Missing"}
    },
    "V536": {
        "name": "Recent sexual activity",
        "value": {0: "Never had sex", 1: "Active in last 4 weeks", 2: "Not active in last 4 weeks - postpartum abstinence", 
               3: "Not active in last 4 weeks - not postpartum abstinence", 9: "Missing"}
    },
}


clean_recode = {
    "Depression": {
        "name": "PHQ-9 depression score (categorized)",
        "value": {0: "0-4 (minimal)", 1: "5-9 (mild)", 2: "10-14 (moderate)", 3: "15-19 (moderately severe)", 
               4: "20-27 (severe)"},
    },
    "Anxiety": {
        "name": "GAD-7 anxiety score (categorized)",
        "value": {0: "0-4 (minimal)", 1: "5-9 (mild)", 2: "10-14 (moderate)", 3: "15-21 (severe)"},
    },
    "Depression Binary": {
        "name": "Probable depression (PHQ-9 >= 10)",
        "value": {0: "No", 1: "Yes"},
    },
    "Anxiety Binary": {
        "name": "Probable anxiety (GAD-7 >= 10)",
        "value": {0: "No", 1: "Yes"},
    },
    "Cardiometabolic Burden": {
        "name": "Cardiometabolic Burden",
        "value": {0: "None", 1: "One burden", 2: "Two burdens", 3: "Three burdens"}
    },
    "Cardiometabolic Burden Merged": {
        "name": "Cardiometabolic Burden",
        "value": {0: "None", 1: "One burden", 2: "Two or more burdens"}
    },
    "Cardiometabolic Burden Binary": {
        "name": "Cardiometabolic Burden",
        "value": {0: "No", 1: "Yes"}
    },
    "Diabetes": {
        "name": "Has Diabetes",
        "value": {0: "No", 1: "Yes"}
    },
    "Hypertension": {
        "name": "Has Hypertension",
        "value": {0: "No", 1: "Yes"}
    },
    "Obesity": {
        "name": "Has Obesity",
        "value": {0: "No", 1: "Yes"}
    },
    "Socioeconomic Status": {
        "name": "Socioeconomic Status (Wealth index combined)",
        "value": {1: "Poorest", 2: "Poorer", 3: "Middle", 4: "Richer", 5: "Richest"},
    },
    "Education": {
        "name": "Highest educational level",
        "value": {0: "No education", 1: "Primary", 2: "Secondary", 3: "Higher"},
    },
    "Occupation": {
        "name": "Respondent currently working",
        "value": {0: "No", 1: "Yes"},
    },
    "Partner occupation": {
        "name": "Husband/partner's occupation (grouped)",
        "value": {1: "Not working", 2: "Working", 3: "Don't know"},
    },
    "Age": {
        "name": "Age in 5-year groups",
        "value": {1: "15-24", 2: "25-34", 3: "35-49"},
    },
    "Age at first cohabitation": {
        "name": "Age at first cohabitation, grouped",
        "value": {0: "<15", 1: "15-24", 2: "25-34", 3: "35-49"},
    },
    "Division": {
        "name": "Division",
        "value": {1: "Barishal", 2: "Chattogram", 3: "Dhaka", 4: "Khulna", 5: "Mymensingh", 6: "Rajshahi", 7: "Rangpur", 8: "Sylhet"},
    },
    "Residence": {
        "name": "Type of place of residence",
        "value": {1: "Urban", 2: "Rural"},
    },
    "Religion": {
        "name": "Religion",
        "value": {1: "Islam", 2: "Others"},
    },
    "Children": {
        "name": "Total children ever born", 
        "value": {0: "No children", 1: 1, 2: 2, 3: 3, 4: "4 or more"}
    },
    "Family size": {
        "name": "Number of household members", 
        "value": {1: "Less than 5", 2: "5 or more"}
    },
    "Household Autonomy": {
        "name": "Autonomy in household decisions (health care, purchases, family visits)",
        "value": {0: "No autonomy", 1: "1 decision", 2: "2 decisions", 3: "3 decisions"}
    },
    "Financial Decision-Making": {
        "name": "Person who decides what to do with money husband earns",
        "value": {0: "Husband/other decides", 1: "Respondent has a say", 2: "No earnings (N/A)"},
    },
    "IPV Attitude": {
        "name": "Justification for Physical/Sexual/Emotional Abuse",
        "value": {0: "Rejects in all scenarios", 1: "Uncertain (Don't know, never affirms)", 2: "Justifies in \u22651 scenario"},
    },
    "Insurance": {
        "name": "Covered by health insurance",
        "value": {0: "No", 1: "Yes"},
    },
    "Mass Media": {
        "name": "Use of mass media",
        "value": {0: "Never", 1: "Only television", 2: "Only internet", 3: "Both television and internet"},
    },
    "Contraceptive": {
        "name": "Current contraceptive use by method type (simplified/collapsed version)",
        "value": {0: "No method", 1: "Folkloric method", 2: "Traditional method", 3: "Modern method"}
    },
    "Abortion": {
        "name": "Ever had a terminated pregnancy",
        "value": {0: "No", 1: "Yes"}
    },
    "Pregnant": {
        "name": "Currently pregnant",
        "value": {0: "No or unsure", 1: "Yes"}
    },
    "Menopause": {
        "name": "In menopause",
        "value": {0: "No", 1: "Yes"}
    },
    "Sexual activity": {
        "name": "Recent sexual activity",
        "value": {0: "Not Active", 1: "Active"}
    },
    "Postpartum": {
        "name": "Postpartum abstinence",
        "value": {0: "No", 1: "Yes"}
    },
}


# ---------------------------------------------------------------------------
# 1. BINARY COLUMNS (2 substantive categories, e.g. Yes/No)
# ---------------------------------------------------------------------------

binary_cols = [
    "V020",   # Type of sample / ever-married indicator
    "HV104",  # Sex of household member
    "SB236",  # Ever diagnosed with diabetes
    "SB240",  # Currently taking medication for diabetes
    "WBP16",  # Previously diagnosed with hypertension
    "WBP19",  # Currently taking blood pressure medication
    "V714",   # Respondent currently working
    "V025",   # Type of place of residence (Urban/Rural)
    "V481",   # Covered by health insurance
    "V744A",  # Wife beating justified: goes out without telling husband
    "V744B",  # Wife beating justified: neglects children
    "V744C",  # Wife beating justified: argues with husband
    "V744D",  # Wife beating justified: refuses sex
    "V744E",  # Wife beating justified: burns food
    "V228",   # Ever had a terminated pregnancy
]

# ---------------------------------------------------------------------------
# 2. ORDINAL COLUMNS (ordered categories -> safe to encode 0..k or keep as int)
# ---------------------------------------------------------------------------

ordinal_cols = [
    "MTH22",  # PHQ-9 depression score (categorized, 0=minimal -> 4=severe)
    "MTH24",  # GAD-7 anxiety score (categorized, 0=minimal -> 3=severe)
    "MTH10",  # Trouble falling/staying asleep (Never -> Always)
    "V149",   # Educational attainment (No education -> Higher)
    "V106",   # Highest educational level (No education -> Higher)
    "V190",   # Wealth index combined (Poorest -> Richest)
    "V190A",  # Wealth index combined, urban/rural clustered (Poorest -> Richest)
    "V013",   # Age in 5-year groups
    "V026",   # De facto place of residence (Capital -> Countryside) [ambiguous: reads as an urbanization gradient, but treat as nominal if that gradient isn't meaningful for your model]
    "V513",   # Cohabitation duration, grouped (years)
    "V157",   # Frequency of reading newspaper/magazine
    "V158",   # Frequency of listening to radio
    "V159",   # Frequency of watching television
    "V171A",  # Use of internet [ambiguous: "can't establish when" (code 3) breaks the recency order — consider recoding to binary ever-used/never-used instead]
]

# ---------------------------------------------------------------------------
# 3. NOMINAL / CATEGORICAL COLUMNS (unordered, >2 categories)
# ---------------------------------------------------------------------------

nominal_cols = [
    "S111A",  # Current marital status
    "V501",   # Current marital status
    "V731",   # Respondent worked in last 12 months
    "V716",   # Respondent's occupation (detailed) — high cardinality
    "V717",   # Respondent's occupation (grouped)
    "V704",   # Husband/partner's occupation (detailed) — high cardinality
    "V705",   # Husband/partner's occupation (grouped)
    "V024",   # Division (geographic)
    "V130",   # Religion
    "V743A",  # Decision-maker: respondent's health care
    "V743B",  # Decision-maker: large household purchases
    "V743D",  # Decision-maker: visits to family/relatives
    "V743F",  # Decision-maker: money husband earns
    "V312",   # Current contraceptive method — high cardinality
    "V313",   # Current use by method type (No/Folkloric/Traditional/Modern) [ambiguous: has a rough "modernity" order but categories aren't strictly nested — nominal is the safer default]
]

# ---------------------------------------------------------------------------
# 4. NUMERICAL - CONTINUOUS COLUMNS
# ---------------------------------------------------------------------------

numerical_continuous_cols = [
    "SB267",  # Plasma glucose (mg/dL)
    "WBP24",  # Final systolic blood pressure (mmHg)
    "WBP25",  # Final diastolic blood pressure (mmHg)
    "HA40",   # Body Mass Index (BMI)
    "V191",   # Wealth index factor score combined
    "V191A",  # Wealth index factor score combined, urban/rural clustered
]

# ---------------------------------------------------------------------------
# 5. NUMERICAL - DISCRETE / COUNT COLUMNS
# ---------------------------------------------------------------------------

numerical_discrete_cols = [
    "V133",  # Education in single years
    "V012",  # Respondent's current age (years)
    "V511",  # Age at first cohabitation
    "V201",  # Total children ever born
    "V212",  # Age of respondent at first birth
    "V218",  # Number of living children
    "V219",  # Living children + current pregnancy
    "V136",  # Number of household members
    "V137",  # Number of children age 5 and under in household
    "V138",  # Number of eligible women in household
]

# ---------------------------------------------------------------------------
# DOMAIN GROUPINGS (useful for feature-block analysis / grouped imputation)
# ---------------------------------------------------------------------------

domain_groups = {
    "population": ["V020", "S111A", "V501", "HV104"],
    "diabetes": ["SB267", "SB236", "SB240"],
    "hypertension": ["WBP24", "WBP25", "WBP16", "WBP19"],
    "obesity": ["HA40"],
    "mental_health": ["MTH22", "MTH24"],
    "ses_education": ["V133", "V149", "V106"],
    "ses_wealth": ["V190", "V190A", "V191", "V191A"],
    "ses_occupation": ["V714", "V731", "V716", "V717", "V704", "V705"],
    "age": ["V012", "V013"],
    "residence": ["V024", "V025", "V026"],
    "marriage": ["V511", "V513"],
    "religion": ["V130"],
    "children": ["V201", "V212", "V218", "V219"],
    "household_size": ["V136", "V137", "V138"],
    "health_insurance": ["V481"],
    "mass_media": ["V157", "V158", "V159", "V171A"],
    "autonomy": ["V743A", "V743B", "V743D"],
    "financial_decision": ["V743F"],
    "ipv_attitudes": ["V744A", "V744B", "V744C", "V744D", "V744E"],
    "contraception": ["V312", "V313"],
    "pregnancy_loss": ["V228"],
}


# ---------------------------------------------------------------------------
# Parse any recoded variable
# ---------------------------------------------------------------------------

def investigate_row(row: pd.Series, mapping: dict = clean_recode) -> pd.Series:
    """
    Recodes numeric values in a pandas DataFrame row/Series using a dictionary.
    
    Parameters:
        row (pd.Series): A single row from a DataFrame.
        mapping (dict): Lookup dictionary mapping column names to label dicts.
        
    Returns:
        pd.Series: A new Series with recoded values.
    """
    recoded = row.astype(object).copy()
    
    for col in recoded.index:
        if col in mapping:
            val_map = mapping[col]["value"]
            val = recoded[col]
            
            # Handle NaN values safely
            if pd.notna(val):
                # Convert float to int if needed (e.g., 2.0 -> 2) for dict lookup
                lookup_key = int(val) if isinstance(val, float) and val.is_integer() else val
                recoded[col] = val_map.get(lookup_key, val)
                
    return recoded


# ---------------------------------------------------------------------------
# Parse any recoded variable
# ---------------------------------------------------------------------------

def parse_recode(feature_name: str, max_height: int = 350, default_open: bool = True):
    """
    Parses a single variable recode dictionary and renders a collapsible, 
    eye-friendly HTML card in Jupyter Notebooks.
    """
    var = recode.get(feature_name, None) or clean_recode.get(feature_name, None)
    if not isinstance(var, dict):
        display(HTML("<div style='color: #a83232; padding: 8px;'>Invalid variable input (expected dict).</div>"))
        return

    var_name = html.escape(str(var.get("name", "Unknown Variable")))
    feature_name_clean = html.escape(str(feature_name))
    value_map = var.get("value")
    
    # Generate unique ID to prevent conflicts between multiple outputs
    uid = f"recode_{uuid.uuid4().hex[:8]}"
    open_attr = "open" if default_open else ""

    # Scoped CSS to hide default browser details marker
    scoped_style = f"""
    <style>
        #{uid}_details > summary::-webkit-details-marker {{ display: none; }}
        #{uid}_details > summary {{ list-style: none; outline: none; }}
    </style>
    """

    # --- Header Title Styled HTML Block ---
    header_title_html = f"""
    <div style="display: flex; align-items: center; gap: 10px; overflow: hidden; padding-right: 10px;">
        <span style="
            font-family: SFMono-Regular, Consolas, monospace;
            background-color: #fef3c7;
            color: #92400e;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
        ">{feature_name_clean}</span>
        <span style="font-size: 13.5px; font-weight: 600; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{var_name}</span>
    </div>
    """

    # --- Case 1: Continuous Variable (value is None) ---
    if value_map is None:
        html_code = f"""
        {scoped_style}
        <details id="{uid}_details" {open_attr} style="
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            border: 1px solid #e2dcd5;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            margin: 12px 0;
            max-width: 600px;
            overflow: hidden;
            background-color: #faf8f5;
        ">
            <summary style="
                background-color: #4a5568;
                color: #f7fafc;
                padding: 12px 16px;
                cursor: pointer;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <!-- Left Side: Styled Variable Badge & Name -->
                    {header_title_html}
                    
                    <!-- Right Side: Badge & Arrow -->
                    <div style="display: flex; align-items: center; gap: 12px; flex-shrink: 0;">
                        <span style="
                            background: #ed8936; 
                            color: #ffffff;
                            padding: 2px 8px; 
                            border-radius: 12px; 
                            font-size: 11px;
                            font-weight: 600;
                            letter-spacing: 0.3px;
                        ">Continuous Variable</span>
                        <span id="{uid}_arrow" style="
                            font-size: 11px; 
                            display: inline-block; 
                            transition: transform 0.2s ease-in-out;
                            transform: {'rotate(90deg)' if default_open else 'rotate(0deg)'};
                        ">▶</span>
                    </div>
                </div>
            </summary>
            <div style="padding: 16px; font-size: 13px; color: #718096; text-align: center; font-style: italic; border-top: 1px solid #e2dcd5;">
                No categorical value mappings available. Values represent direct continuous measurements.
            </div>
        </details>
        <script>
            document.getElementById('{uid}_details').addEventListener('toggle', function(e) {{
                document.getElementById('{uid}_arrow').style.transform = e.target.open ? 'rotate(90deg)' : 'rotate(0deg)';
            }});
        </script>
        """
        display(HTML(html_code))
        return

    # --- Case 2: Categorical Variable ---
    total_items = len(value_map)
    items = []
    
    exact_match_keywords = ["na", "n/a", "missing", "refused", "don't know", "dont know", "unknown"]
    partial_match_keywords = ["missing", "refused", "don't know", "dont know"]

    for k, v in value_map.items():
        label_str = html.escape(str(v))
        label_lower = label_str.lower().strip()
        
        is_missing = (
            label_lower in exact_match_keywords or
            any(kw in label_lower for kw in partial_match_keywords) or
            k in [99998, 99999, -1, -9]
        )
        items.append({"code": html.escape(str(k)), "label": label_str, "is_missing": is_missing})

    items_json = json.dumps(items)

    html_code = f"""
    {scoped_style}
    <details id="{uid}_details" {open_attr} style="
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        border: 1px solid #e2dcd5;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin: 12px 0;
        max-width: 600px;
        overflow: hidden;
        background-color: #ffffff;
    ">
        <!-- Collapsible Header -->
        <summary style="
            background-color: #4a5568;
            color: #f7fafc;
            padding: 12px 16px;
            cursor: pointer;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <!-- Left Side: Styled Variable Badge & Name -->
                {header_title_html}
                
                <!-- Right Side: Badge & Arrow -->
                <div style="display: flex; align-items: center; gap: 12px; flex-shrink: 0;">
                    <span style="
                        background: rgba(255, 255, 255, 0.18); 
                        color: #f7fafc;
                        padding: 2px 8px; 
                        border-radius: 12px; 
                        font-size: 11px;
                        font-weight: 500;
                        white-space: nowrap;
                    ">{total_items} categories</span>
                    <span id="{uid}_arrow" style="
                        font-size: 11px; 
                        display: inline-block; 
                        transition: transform 0.2s ease-in-out;
                        transform: {'rotate(90deg)' if default_open else 'rotate(0deg)'};
                    ">▶</span>
                </div>
            </div>
        </summary>

        <div style="border-top: 1px solid #e2dcd5;">
            <!-- Search Input -->
            <div style="padding: 10px 16px; background-color: #fcfbf9; border-bottom: 1px solid #eae5df;">
                <input type="text" id="{uid}_search" placeholder="Filter codes or labels..." style="
                    width: 100%;
                    box-sizing: border-box;
                    padding: 7px 12px;
                    border: 1px solid #e2dcd5;
                    border-radius: 5px;
                    font-size: 12px;
                    background-color: #ffffff;
                    color: #2d3748;
                    outline: none;
                " oninput="{uid}_filterData()" />
            </div>

            <!-- Scrollable Table Container -->
            <div style="max-height: {max_height}px; overflow-y: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 12.5px;">
                    <thead style="position: sticky; top: 0; background: #f4f1eb; z-index: 1; border-bottom: 1px solid #e2dcd5;">
                        <tr style="color: #4a5568; font-weight: 600;">
                            <th style="padding: 8px 16px; text-align: center; width: 90px;">Code</th>
                            <th style="padding: 8px 16px; text-align: left;">Category Label</th>
                        </tr>
                    </thead>
                    <tbody id="{uid}_tbody">
                        <!-- Populated dynamically via JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </details>

    <script>
    (function() {{
        // Arrow rotation logic
        document.getElementById('{uid}_details').addEventListener('toggle', function(e) {{
            document.getElementById('{uid}_arrow').style.transform = e.target.open ? 'rotate(90deg)' : 'rotate(0deg)';
        }});

        const rawData = {items_json};

        window['{uid}_filterData'] = function() {{
            const query = document.getElementById('{uid}_search').value.toLowerCase().trim();
            const filteredData = rawData.filter(item => 
                item.code.toLowerCase().includes(query) || 
                item.label.toLowerCase().includes(query)
            );
            render(filteredData);
        }};

        function render(data) {{
            const tbody = document.getElementById('{uid}_tbody');
            tbody.innerHTML = '';

            if (data.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="2" style="text-align: center; padding: 18px; color: #a0aec0; font-style: italic;">No matching categories found</td></tr>';
                return;
            }}

            data.forEach(item => {{
                const row = document.createElement('tr');
                row.style.borderBottom = '1px solid #f2eee9';

                const badgeStyle = item.is_missing 
                    ? 'background-color: #fde8e8; color: #9b2c2c; border: 1px solid #f8b4b4;' 
                    : 'background-color: #edf7ed; color: #2e6033; border: 1px solid #c6e7c7;';

                row.innerHTML = `
                    <td style="padding: 8px 16px; text-align: center;">
                        <span style="
                            font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
                            background-color: #fef3c7;
                            color: #92400e;
                            padding: 2px 8px;
                            border-radius: 4px;
                            font-size: 11px;
                            font-weight: 600;
                        ">${{item.code}}</span>
                    </td>
                    <td style="padding: 8px 16px;">
                        <span style="
                            display: inline-block; 
                            padding: 3px 10px; 
                            border-radius: 12px; 
                            font-weight: 500;
                            line-height: 1.3;
                            ${{badgeStyle}}
                        ">${{item.label}}</span>
                    </td>
                `;
                tbody.appendChild(row);
            }});
        }}

        render(rawData);
    }})();
    </script>
    """
    display(HTML(html_code))


# ---------------------------------------------------------------------------
# Parse all recoded variable
# ---------------------------------------------------------------------------

def parse_all_recodes(recodes: dict = recode, container_max_height: int = 400, inner_max_height: int = 280):
    """
    Parses a dictionary of multiple variable recodes and renders a robust, 
    searchable, and collapsible master viewer in Jupyter Notebooks.
    """
    if not isinstance(recodes, dict) or not recodes:
        display(HTML("<div style='color: #a83232; padding: 12px; border: 1px solid #f8b4b4; border-radius: 6px; background-color: #fde8e8;'>No valid recode dictionary provided.</div>"))
        return

    master_uid = f"master_{uuid.uuid4().hex[:8]}"
    
    exact_match_keywords = ["na", "n/a", "missing", "refused", "don't know", "dont know", "unknown"]
    partial_match_keywords = ["missing", "refused", "don't know", "dont know"]

    cards_html = []
    total_vars = len(recodes)

    for var_id, var_info in recodes.items():
        if not isinstance(var_info, dict):
            continue

        card_uid = f"card_{uuid.uuid4().hex[:8]}"
        var_name = html.escape(str(var_info.get("name", var_id)))
        var_id_clean = html.escape(str(var_id))
        value_map = var_info.get("value")
        
        # Build search index string
        search_terms = [var_id_clean.lower(), var_name.lower()]

        if value_map is None:  # Continuous Variable
            badge_html = """<span style="background: #ed8936; color: #ffffff; padding: 2px 8px; border-radius: 12px; font-size: 10.5px; font-weight: 600;">Continuous</span>"""
            body_content = """<div style="padding: 14px; font-size: 12.5px; color: #718096; text-align: center; font-style: italic; background-color: #faf8f5;">Continuous variable — no discrete value categories.</div>"""
        else:  # Categorical Variable
            cat_count = len(value_map)
            badge_html = f"""<span style="background: rgba(255, 255, 255, 0.18); color: #f7fafc; padding: 2px 8px; border-radius: 12px; font-size: 10.5px; font-weight: 500;">{cat_count} categories</span>"""
            
            rows_html = []
            for k, v in value_map.items():
                code_str = html.escape(str(k))
                label_str = html.escape(str(v))
                label_lower = label_str.lower().strip()
                
                search_terms.append(code_str.lower())
                search_terms.append(label_lower)

                is_missing = (
                    label_lower in exact_match_keywords or
                    any(kw in label_lower for kw in partial_match_keywords) or
                    k in [99998, 99999, -1, -9]
                )

                badge_style = "background-color: #fde8e8; color: #9b2c2c; border: 1px solid #f8b4b4;" if is_missing else "background-color: #edf7ed; color: #2e6033; border: 1px solid #c6e7c7;"

                rows_html.append(f"""
                <tr class="cat-row" data-cat-text="{code_str.lower()} {label_lower}" style="border-bottom: 1px solid #f2eee9;">
                    <td style="padding: 6px 12px; text-align: center;">
                        <span style="font-family: SFMono-Regular, Consolas, monospace; background-color: #fef3c7; color: #92400e; padding: 1px 6px; border-radius: 3px; font-size: 10.5px; font-weight: 600;">{code_str}</span>
                    </td>
                    <td style="padding: 6px 12px;">
                        <span style="display: inline-block; padding: 2px 8px; border-radius: 10px; font-weight: 500; line-height: 1.3; {badge_style}">{label_str}</span>
                    </td>
                </tr>
                """)

            body_content = f"""
            <div style="padding: 8px 12px; background-color: #fcfbf9; border-bottom: 1px solid #eae5df;">
                <input type="text" class="card-filter-{master_uid}" data-card-id="{card_uid}" placeholder="Filter categories for {var_id_clean}..." style="
                    width: 100%;
                    box-sizing: border-box;
                    padding: 6px 10px;
                    border: 1px solid #e2dcd5;
                    border-radius: 4px;
                    font-size: 11.5px;
                    background-color: #ffffff;
                    color: #2d3748;
                    outline: none;
                " />
            </div>
            <div style="max-height: {inner_max_height}px; overflow-y: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                    <thead style="position: sticky; top: 0; background: #f4f1eb; z-index: 1; border-bottom: 1px solid #e2dcd5;">
                        <tr style="color: #4a5568; font-weight: 600;">
                            <th style="padding: 7px 12px; text-align: center; width: 80px;">Code</th>
                            <th style="padding: 7px 12px; text-align: left;">Category Label</th>
                        </tr>
                    </thead>
                    <tbody id="{card_uid}_tbody">
                        {"".join(rows_html)}
                    </tbody>
                </table>
            </div>
            """

        search_index = " ".join(search_terms)

        card_html = f"""
        <div id="{card_uid}" class="recode-card-{master_uid}" data-search="{search_index}" style="
            border: 1px solid #e2dcd5; 
            border-radius: 7px; 
            overflow: hidden; 
            background-color: #ffffff; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            margin-bottom: 10px;
            flex-shrink: 0;
            min-height: 42px;
        ">
            <!-- Header Div -->
            <div class="card-header-{master_uid}" data-card-id="{card_uid}" style="
                background-color: #4a5568; 
                color: #f7fafc; 
                padding: 10px 14px; 
                cursor: pointer; 
                user-select: none;
                display: flex;
                justify-content: space-between;
                align-items: center;
                min-height: 22px;
            ">
                <div style="display: flex; align-items: center; gap: 10px; overflow: hidden; padding-right: 10px;">
                    <span style="
                        font-family: SFMono-Regular, Consolas, monospace;
                        background-color: #fef3c7;
                        color: #92400e;
                        padding: 2px 7px;
                        border-radius: 4px;
                        font-size: 11px;
                        font-weight: 700;
                        white-space: nowrap;
                    ">{var_id_clean}</span>
                    <span style="font-size: 13.5px; font-weight: 600; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{var_name}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px; flex-shrink: 0;">
                    {badge_html}
                    <span id="{card_uid}_arrow" style="font-size: 10px; display: inline-block; transition: transform 0.2s ease-in-out; transform: rotate(0deg);">▶</span>
                </div>
            </div>
            
            <!-- Collapsible Body Div -->
            <div id="{card_uid}_body" style="border-top: 1px solid #e2dcd5; display: none;">
                {body_content}
            </div>
        </div>
        """
        cards_html.append(card_html)

    full_html = f"""
    <style>
        #{master_uid}_container ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        #{master_uid}_container ::-webkit-scrollbar-track {{ background: #f1ede6; border-radius: 4px; }}
        #{master_uid}_container ::-webkit-scrollbar-thumb {{ background: #cbd5e0; border-radius: 4px; }}
        #{master_uid}_container ::-webkit-scrollbar-thumb:hover {{ background: #a0aec0; }}
    </style>

    <div id="{master_uid}_container" style="
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        border: 1px solid #e2dcd5;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin: 16px 0;
        max-width: 750px;
        overflow: hidden;
        background-color: #fcfbf9;
    ">
        <!-- Master Header -->
        <div style="
            background-color: #2d3748;
            color: #f7fafc;
            padding: 14px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="font-size: 15px; font-weight: 700; letter-spacing: 0.2px;">Dataset Recode Viewer</span>
            <span id="{master_uid}_counter" style="
                background: rgba(255, 255, 255, 0.15); 
                color: #e2e8f0;
                padding: 3px 10px; 
                border-radius: 12px; 
                font-size: 11.5px;
                font-weight: 500;
            ">{total_vars} / {total_vars} variables</span>
        </div>

        <!-- Master Toolbar -->
        <div style="
            padding: 10px 16px; 
            background-color: #f4f1eb; 
            border-bottom: 1px solid #e2dcd5;
            display: flex;
            gap: 10px;
            align-items: center;
        ">
            <input type="text" id="{master_uid}_master_search" placeholder="Search variables by ID, name, or category label..." style="
                flex: 1;
                box-sizing: border-box;
                padding: 8px 12px;
                border: 1px solid #cbd5e0;
                border-radius: 6px;
                font-size: 12.5px;
                background-color: #ffffff;
                color: #2d3748;
                outline: none;
            " />

            <button id="{master_uid}_btn_expand" style="
                background-color: #ffffff;
                border: 1px solid #cbd5e0;
                color: #4a5568;
                padding: 7px 11px;
                border-radius: 6px;
                font-size: 11.5px;
                font-weight: 600;
                cursor: pointer;
                white-space: nowrap;
            ">Expand All</button>

            <button id="{master_uid}_btn_collapse" style="
                background-color: #ffffff;
                border: 1px solid #cbd5e0;
                color: #4a5568;
                padding: 7px 11px;
                border-radius: 6px;
                font-size: 11.5px;
                font-weight: 600;
                cursor: pointer;
                white-space: nowrap;
            ">Collapse All</button>
        </div>

        <!-- Master Scrollable Card List (Block layout to prevent flex shrinking) -->
        <div id="{master_uid}_list" style="
            max-height: {container_max_height}px; 
            overflow-y: auto; 
            padding: 12px 12px 2px 12px;
            display: block;
        ">
            {"".join(cards_html)}
        </div>
    </div>

    <script>
    (function() {{
        const masterUid = "{master_uid}";
        const container = document.getElementById(masterUid + '_container');
        if (!container) return;
        
        const cards = container.querySelectorAll('.recode-card-' + masterUid);

        // Core Toggle Logic
        const toggleCard = function(cardId, forceState) {{
            const body = document.getElementById(cardId + '_body');
            const arrow = document.getElementById(cardId + '_arrow');
            if (!body) return;

            let shouldOpen = (typeof forceState !== 'undefined') ? forceState : (body.style.display === 'none');
            
            body.style.display = shouldOpen ? 'block' : 'none';
            if (arrow) {{
                arrow.style.transform = shouldOpen ? 'rotate(90deg)' : 'rotate(0deg)';
            }}
        }};

        // Attach Click to Headers
        const headers = container.querySelectorAll('.card-header-' + masterUid);
        headers.forEach(header => {{
            header.addEventListener('click', function() {{
                const cardId = this.getAttribute('data-card-id');
                toggleCard(cardId);
            }});
        }});

        // Attach Input to Card Internal Filters
        const cardFilters = container.querySelectorAll('.card-filter-' + masterUid);
        cardFilters.forEach(inputEl => {{
            inputEl.addEventListener('input', function() {{
                const cardId = this.getAttribute('data-card-id');
                const q = this.value.toLowerCase().trim();
                const tbody = document.getElementById(cardId + '_tbody');
                if (!tbody) return;

                const rows = tbody.querySelectorAll('.cat-row');
                rows.forEach(row => {{
                    const text = row.getAttribute('data-cat-text') || '';
                    row.style.display = (!q || text.includes(q)) ? '' : 'none';
                }});
            }});
        }});

        // Master Search Event
        const masterSearch = document.getElementById(masterUid + '_master_search');
        if (masterSearch) {{
            masterSearch.addEventListener('input', function() {{
                const q = this.value.toLowerCase().trim();
                let visibleCount = 0;

                cards.forEach(card => {{
                    const searchText = card.getAttribute('data-search') || '';
                    if (!q || searchText.includes(q)) {{
                        card.style.display = 'block';
                        visibleCount++;
                        if (q.length > 1 && searchText.includes(q)) {{
                            toggleCard(card.id, true);
                        }}
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});

                const counter = document.getElementById(masterUid + '_counter');
                if (counter) counter.textContent = visibleCount + ' / ' + cards.length + ' variables';
            }});
        }}

        // Expand All Event
        const btnExpand = document.getElementById(masterUid + '_btn_expand');
        if (btnExpand) {{
            btnExpand.addEventListener('click', function() {{
                cards.forEach(card => {{
                    if (card.style.display !== 'none') toggleCard(card.id, true);
                }});
            }});
        }}

        // Collapse All Event
        const btnCollapse = document.getElementById(masterUid + '_btn_collapse');
        if (btnCollapse) {{
            btnCollapse.addEventListener('click', function() {{
                cards.forEach(card => {{
                    if (card.style.display !== 'none') toggleCard(card.id, false);
                }});
            }});
        }}
    }})();
    </script>
    """
    display(HTML(full_html))