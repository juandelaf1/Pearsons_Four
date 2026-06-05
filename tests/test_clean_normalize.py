import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from pipeline.clean_normalize import clean_normalize


def test_clean_normalize_removes_zero_salaries():
    df = pd.DataFrame({
        'salary_usd': [0, 50000, -100, 75000],
        'country': ['US', 'ES', 'GB', 'DE'],
        'source': ['A', 'B', 'C', 'D'],
        'job_title': ['a', 'b', 'c', 'd'],
        'role_category': ['DS', 'DE', 'DA', 'ML'],
        'experience_level': ['Senior', 'Mid', 'Entry', 'Senior'],
        'employment_type': ['FT', 'FT', 'FT', 'FT'],
        'company_size': ['L', 'M', 'S', 'M'],
        'year': [2023, 2024, 2023, 2024],
    })
    result = clean_normalize(df)
    assert len(result) == 2
    assert result['salary_usd'].min() > 0


def test_clean_normalize_fills_missing_fields():
    df = pd.DataFrame({
        'salary_usd': [50000, 75000],
        'country': ['US', 'ES'],
        'source': ['A', 'B'],
        'job_title': ['a', 'b'],
        'role_category': [np.nan, 'DE'],
        'experience_level': [np.nan, 'Senior'],
        'employment_type': [np.nan, 'FT'],
        'company_size': [np.nan, 'M'],
        'year': [np.nan, 2024],
    })
    result = clean_normalize(df)
    assert result['role_category'].iloc[0] == 'Other Tech'
    assert result['experience_level'].iloc[0] == 'Unknown'
    assert result['employment_type'].iloc[0] == 'Full-time'
    assert result['company_size'].iloc[0] == 'Medium'
    assert result['year'].iloc[0] == 2023


def test_clean_normalize_deduplicates():
    df = pd.DataFrame({
        'salary_usd': [50000, 50000, 75000],
        'country': ['US', 'US', 'ES'],
        'source': ['A', 'A', 'B'],
        'job_title': ['a', 'a', 'b'],
        'role_category': ['DS', 'DS', 'DE'],
        'experience_level': ['Senior', 'Senior', 'Mid'],
        'employment_type': ['FT', 'FT', 'FT'],
        'company_size': ['L', 'L', 'M'],
        'year': [2023, 2023, 2024],
    })
    result = clean_normalize(df)
    assert len(result) == 2
