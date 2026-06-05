"""Limpieza y normalización del dataset unificado."""
import pandas as pd
import numpy as np


def clean_normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    initial = len(df)

    # Remove zero/negative salaries
    before = len(df)
    df = df[df['salary_usd'] > 0]
    print(f'  [Clean] Salarios >0: {before} -> {len(df)}')

    # Remove salary < 1000 USD (likely erroneous)
    before = len(df)
    df = df[df['salary_usd'] >= 1000]
    print(f'  [Clean] Salarios >=$1K: {before} -> {len(df)}')

    # Remove salary > 1M USD (extreme outliers)
    before = len(df)
    df = df[df['salary_usd'] <= 1000000]
    print(f'  [Clean] Salarios <=$1M: {before} -> {len(df)}')

    # Normalize role categories
    df['role_category'] = df['role_category'].fillna('Other Tech').str.strip()

    # Normalize experience levels
    df['experience_level'] = df['experience_level'].fillna('Unknown').str.strip().str.title()

    # Normalize employment types
    df['employment_type'] = df['employment_type'].fillna('Full-time').str.strip()

    # Fill missing company sizes
    df['company_size'] = df['company_size'].fillna('Medium')

    # Ensure year is int
    df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(2023).astype(int)

    # Drop duplicates (same source, title, salary, country)
    before = len(df)
    df = df.drop_duplicates(subset=['source', 'country', 'job_title', 'salary_usd'])
    print(f'  [Clean] Duplicados: {before} -> {len(df)}')

    # IQR outlier detection (informational)
    q1 = df['salary_usd'].quantile(0.25)
    q3 = df['salary_usd'].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = df[(df['salary_usd'] < lower) | (df['salary_usd'] > upper)]
    print(f'  [Clean] Outliers IQR: {len(outliers)} ({(len(outliers)/len(df)*100):.1f}%)')
    print(f'  [Clean] Rango IQR: ${lower:,.0f} - ${upper:,.0f}')

    # Stats
    print(f'  [Clean] Total final: {len(df)} registros')
    print(f'  [Clean] Salario USD: media=${df["salary_usd"].mean():,.0f} '
          f'mediana=${df["salary_usd"].median():,.0f}')
    print(f'  [Clean] Paises: {df["country"].nunique()}')
    print(f'  [Clean] Fuentes: {df["source"].nunique()}')
    print(f'  [Clean] Roles: {df["role_category"].nunique()}')

    return df
