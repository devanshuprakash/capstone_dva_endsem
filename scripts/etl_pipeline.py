"""
ETL Pipeline — Credit Risk & Loan Default Analysis
Standalone script version of notebooks/02_cleaning.ipynb
Run: python scripts/etl_pipeline.py
"""

import pandas as pd
import numpy as np
import os
import sys

RAW_PATH = 'data/raw/lending_club_loans.csv'
PROCESSED_PATH = 'data/processed/loans_cleaned.csv'

KEEP_COLS = [
    'loan_amnt', 'funded_amnt', 'term', 'int_rate', 'installment',
    'grade', 'sub_grade', 'emp_length', 'home_ownership', 'annual_inc',
    'verification_status', 'loan_status', 'purpose', 'addr_state',
    'dti', 'delinq_2yrs', 'fico_range_low', 'fico_range_high',
    'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc',
    'issue_d', 'earliest_cr_line'
]

DEFAULT_STATUSES = [
    'Charged Off', 'Default',
    'Does not meet the credit policy. Status:Charged Off'
]

COMPLETED_STATUSES = [
    'Fully Paid', 'Charged Off', 'Default',
    'Does not meet the credit policy. Status:Fully Paid',
    'Does not meet the credit policy. Status:Charged Off'
]


def load_raw(path):
    print(f'Loading: {path}')
    if not os.path.exists(path):
        print(f'ERROR: File not found at {path}')
        sys.exit(1)
    df = pd.read_csv(path, low_memory=False)
    print(f'Raw shape: {df.shape}')
    return df


def select_columns(df):
    cols = [c for c in KEEP_COLS if c in df.columns]
    df = df[cols].copy()
    print(f'After column selection: {df.shape}')
    return df


def filter_completed_loans(df):
    before = len(df)
    df = df[df['loan_status'].notna()]
    df = df[df['loan_status'].isin(COMPLETED_STATUSES)]
    print(f'Filtered to completed loans: {len(df):,} (dropped {before - len(df):,})')
    return df


def create_default_flag(df):
    df['default_flag'] = df['loan_status'].isin(DEFAULT_STATUSES).astype(int)
    print(f'Default rate: {df["default_flag"].mean():.2%}')
    return df


def fix_dtypes(df):
    if df['int_rate'].dtype == object:
        df['int_rate'] = df['int_rate'].str.replace('%', '').str.strip().astype(float)
    if df['revol_util'].dtype == object:
        df['revol_util'] = pd.to_numeric(df['revol_util'].str.replace('%', '').str.strip(), errors='coerce')
    if df['term'].dtype == object:
        df['term'] = df['term'].str.strip().str.extract(r'(\d+)').astype(float)
    if df['emp_length'].dtype == object:
        df['emp_length'] = df['emp_length'].str.extract(r'(\d+)').astype(float)
    df['issue_d'] = pd.to_datetime(df['issue_d'], format='%b-%Y', errors='coerce')
    df['earliest_cr_line'] = pd.to_datetime(df['earliest_cr_line'], format='%b-%Y', errors='coerce')
    print('Data types fixed')
    return df


def handle_missing(df):
    numeric_cols = ['annual_inc', 'dti', 'revol_util', 'emp_length',
                    'delinq_2yrs', 'open_acc', 'pub_rec', 'total_acc']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    cat_cols = ['home_ownership', 'verification_status', 'purpose']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    print(f'Missing values remaining: {df.isnull().sum().sum()}')
    return df


def treat_outliers(df):
    df['annual_inc'] = df['annual_inc'].clip(upper=df['annual_inc'].quantile(0.99))
    df['dti'] = df['dti'].clip(upper=df['dti'].quantile(0.99))
    print('Outliers capped at 99th percentile')
    return df


def standardise_categoricals(df):
    for col in ['grade', 'home_ownership', 'purpose', 'verification_status', 'addr_state']:
        if col in df.columns:
            df[col] = df[col].str.upper().str.strip()
    print('Categoricals standardised')
    return df


def engineer_features(df):
    df['fico_avg'] = (df['fico_range_low'] + df['fico_range_high']) / 2
    df['credit_age_years'] = ((df['issue_d'] - df['earliest_cr_line']).dt.days / 365).round(1).clip(lower=0)
    df['income_band'] = pd.cut(df['annual_inc'],
        bins=[0, 40000, 80000, 120000, float('inf')],
        labels=['Low', 'Medium', 'High', 'Very High'])
    df['dti_band'] = pd.cut(df['dti'],
        bins=[0, 10, 20, 30, float('inf')],
        labels=['Low', 'Moderate', 'High', 'Very High'])
    df['issue_year'] = df['issue_d'].dt.year
    df['issue_month'] = df['issue_d'].dt.month
    print('Features engineered: fico_avg, credit_age_years, income_band, dti_band, issue_year, issue_month')
    return df


def save_processed(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f'Saved to {path} — shape: {df.shape}')


def run():
    df = load_raw(RAW_PATH)
    df = select_columns(df)
    df = filter_completed_loans(df)
    df = create_default_flag(df)
    df = fix_dtypes(df)
    df = handle_missing(df)
    df = treat_outliers(df)
    df = standardise_categoricals(df)
    df = engineer_features(df)
    save_processed(df, PROCESSED_PATH)
    print('\nETL pipeline complete.')


if __name__ == '__main__':
    run()
