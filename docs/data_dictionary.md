# Data Dictionary — Lending Club Loan Dataset

## Source
Lending Club Loan Data via Kaggle  
Direct link: https://www.kaggle.com/datasets/wordsforthewise/lending-club

## Dataset Overview
- **Rows:** ~2.2M loan records
- **Columns:** 150+
- **Period:** 2007–2018
- **Grain:** One row per loan

## Key Columns Used in Analysis

| Column | Type | Description |
|--------|------|-------------|
| `loan_amnt` | Numeric | The listed amount of the loan applied for by the borrower |
| `funded_amnt` | Numeric | The total amount committed to that loan at that point in time |
| `term` | Categorical | Number of payments on the loan — 36 or 60 months |
| `int_rate` | Numeric | Interest rate on the loan (%) |
| `installment` | Numeric | Monthly payment owed by the borrower |
| `grade` | Categorical | LC assigned loan grade (A–G) |
| `sub_grade` | Categorical | LC assigned loan subgrade |
| `emp_length` | Categorical | Employment length in years (0–10+) |
| `home_ownership` | Categorical | Home ownership status — RENT, OWN, MORTGAGE |
| `annual_inc` | Numeric | Self-reported annual income of the borrower |
| `verification_status` | Categorical | Whether income was verified by LC |
| `loan_status` | Categorical | Current status of the loan — **target variable for default flag** |
| `purpose` | Categorical | Category provided by the borrower for the loan request |
| `addr_state` | Categorical | State provided by the borrower |
| `dti` | Numeric | Debt-to-income ratio |
| `delinq_2yrs` | Numeric | Number of 30+ days past-due incidences in past 2 years |
| `fico_range_low` | Numeric | Lower boundary of FICO score range |
| `fico_range_high` | Numeric | Upper boundary of FICO score range |
| `open_acc` | Numeric | Number of open credit lines in borrower's credit file |
| `pub_rec` | Numeric | Number of derogatory public records |
| `revol_bal` | Numeric | Total credit revolving balance |
| `revol_util` | Numeric | Revolving line utilization rate (%) |
| `total_acc` | Numeric | Total number of credit lines in borrower's credit file |
| `issue_d` | Date | Month the loan was funded |
| `earliest_cr_line` | Date | Month borrower's earliest credit line was opened |

## Derived / Engineered Columns

| Column | Description |
|--------|-------------|
| `default_flag` | Binary: 1 if loan_status is 'Charged Off' or 'Default', else 0 |
| `fico_avg` | Average of fico_range_low and fico_range_high |
| `credit_age_years` | Years between earliest_cr_line and issue_d |
| `income_band` | Binned annual_inc into Low / Medium / High / Very High |
| `dti_band` | Binned dti into Low / Moderate / High / Very High |
