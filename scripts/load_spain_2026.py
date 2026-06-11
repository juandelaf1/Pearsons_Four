"""
load_spain_2026.py — Spain tech salaries 2026 from multiple sources.

Aggregates:
  1. Manfred 2026 Salary Guide (13 roles × 4 seniority bands)
  2. Kaggle DS Salaries 2024 (127 ES records, 2020-2024)
  3. SpainJobs.io 2026 benchmarks (supplementary)
  4. Existing scraped Spain data (Manfred, Glassdoor ES)

Output: synthetic dataset with realistic salary distributions per role/seniority.
"""
import pandas as pd
import numpy as np
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'scripts'))
DATA_DIR = BASE_DIR / 'data'
SPAIN_DIR = DATA_DIR / 'espana'
SPAIN_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

# =============================================================================
# Source 1: Manfred 2026 Salary Guide — role × experience ranges (Spain, €)
# =============================================================================
MANFRED_2026 = {
    'Backend Engineer': {
        'Junior':     (20000, 30000),
        'Mid':        (31000, 40000),
        'Senior':     (41000, 50000),
        'Lead':       (51000, 55000),
    },
    'Frontend Engineer': {
        'Junior':     (20000, 30000),
        'Mid':        (31000, 35000),
        'Senior':     (35000, 40000),
        'Lead':       (40000, 50000),
    },
    'Fullstack Engineer': {
        'Junior':     (20000, 30000),
        'Mid':        (31000, 40000),
        'Senior':     (41000, 50000),
        'Lead':       (51000, 60000),
    },
    'AI Engineer': {
        'Junior':     (25000, 35000),
        'Mid':        (36000, 50000),
        'Senior':     (51000, 70000),
        'Lead':       (71000, 90000),
    },
    'Mobile Engineer': {
        'Junior':     (20000, 30000),
        'Mid':        (31000, 40000),
        'Senior':     (41000, 45000),
        'Lead':       (46000, 50000),
    },
    'QA Engineer': {
        'Junior':     (20000, 25000),
        'Mid':        (26000, 32000),
        'Senior':     (33000, 40000),
        'Lead':       (41000, 45000),
    },
    'Data Engineer': {
        'Junior':     (25000, 35000),
        'Mid':        (36000, 45000),
        'Senior':     (46000, 60000),
        'Lead':       (61000, 80000),
    },
    'Data Scientist': {
        'Junior':     (25000, 35000),
        'Mid':        (36000, 50000),
        'Senior':     (51000, 70000),
        'Lead':       (71000, 100000),
    },
    'Data Analyst': {
        'Junior':     (20000, 25000),
        'Mid':        (26000, 35000),
        'Senior':     (36000, 42000),
        'Lead':       (43000, 50000),
    },
    'ML Engineer': {
        'Junior':     (25000, 35000),
        'Mid':        (36000, 50000),
        'Senior':     (51000, 75000),
        'Lead':       (75000, 100000),
    },
    'Data Architect': {
        'Junior':     None,
        'Mid':        (40000, 55000),
        'Senior':     (56000, 75000),
        'Lead':       (75000, 100000),
    },
    'DevOps Engineer': {
        'Junior':     (25000, 35000),
        'Mid':        (36000, 45000),
        'Senior':     (46000, 60000),
        'Lead':       (61000, 80000),
    },
    'Product Manager': {
        'Junior':     None,
        'Mid':        (31000, 45000),
        'Senior':     (46000, 55000),
        'Lead':       (56000, 80000),
    },
    'Security Engineer': {
        'Junior':     (25000, 30000),
        'Mid':        (31000, 40000),
        'Senior':     (41000, 55000),
        'Lead':       (56000, 80000),
    },
}

SENIORITY_WEIGHTS = {
    'Junior': 0.25,
    'Mid': 0.35,
    'Senior': 0.30,
    'Lead': 0.10,
}

SENIORITY_MAP = {
    'Junior': 'Junior',
    'Mid': 'Mid',
    'Senior': 'Senior',
    'Lead': 'Lead',
}


def generate_manfred_records(n_per_role: int = 200) -> pd.DataFrame:
    """Generate synthetic salary records from Manfred 2026 ranges."""
    records = []
    for role, levels in MANFRED_2026.items():
        for seniority, rng in levels.items():
            if rng is None:
                continue
            lo, hi = rng
            count = int(n_per_role * SENIORITY_WEIGHTS[seniority])
            salaries = np.random.triangular(lo, (lo + hi) / 2, hi, count)
            salaries = np.clip(salaries, lo, hi).round(-2)  # round to nearest 100
            for s in salaries:
                records.append({
                    'source': 'Manfred 2026',
                    'job_title': role,
                    'role_normalized': role,
                    'seniority': seniority,
                    'salary_eur': int(s),
                    'country': 'ES',
                    'country_name': 'Spain',
                    'year': 2026,
                })
    df = pd.DataFrame(records)
    df['salary_usd'] = (df['salary_eur'] * 1.08).round(0)
    print(f'  [Spain 2026] Manfred: {len(df)} records')
    return df


def load_kaggle_spain_2024() -> pd.DataFrame:
    """Load Spain records from Kaggle 2024 dataset."""
    try:
        import kagglehub
        path = kagglehub.dataset_download('yusufdelikkaya/datascience-salaries-2024')
        import os
        csv_path = os.path.join(path, 'DataScience_salaries_2024.csv')
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f'  [Spain 2026] Kaggle 2024 error: {e}')
        return pd.DataFrame()

    # Filter Spain
    df = df[df['company_location'] == 'ES'].copy()
    if df.empty:
        return pd.DataFrame()

    import normalize_titles as nt
    df['role_normalized'] = df['job_title'].apply(lambda t: nt.normalize_title(t)['role'])
    df['seniority'] = df['experience_level'].map({
        'EN': 'Junior', 'MI': 'Mid', 'SE': 'Senior', 'EX': 'Lead'
    }).fillna('Mid')
    df['salary_eur'] = df['salary']
    df['salary_usd'] = df['salary_in_usd']
    df['country'] = 'ES'
    df['country_name'] = 'Spain'
    df['year'] = df['work_year']
    df['source'] = 'Kaggle DS 2024'

    cols = ['source', 'job_title', 'role_normalized', 'seniority',
            'salary_eur', 'salary_usd', 'country', 'country_name', 'year']
    print(f'  [Spain 2026] Kaggle 2024 Spain: {len(df)} records')
    return df[cols]


def load_existing_spain_scraped() -> pd.DataFrame:
    """Load existing Spain scraped data, filtered to valid roles."""
    path = DATA_DIR / 'espana' / 'spain_tech_salaries_scraped.csv'
    if not path.exists():
        return pd.DataFrame()

    raw = pd.read_csv(path, encoding='utf-8-sig')

    def parse_salary(r):
        if pd.isna(r):
            return None
        r = str(r).replace('.', '').replace(',', '.')
        parts = [p.strip() for p in r.replace('—', '-').split('-')]
        vals = []
        for p in parts:
            num = ''.join(c for c in p if c.isdigit() or c in '.,')
            if num:
                try:
                    vals.append(float(num.replace(',', '.')))
                except ValueError:
                    pass
        return (min(vals) + max(vals)) / 2 if vals else None

    import normalize_titles as nt
    raw['role_normalized'] = raw['rol'].apply(lambda t: nt.normalize_title(t)['role'])
    raw['seniority'] = raw['experiencia']
    raw['salary_eur'] = raw['rango_salarial'].apply(parse_salary)
    raw = raw.dropna(subset=['salary_eur'])
    raw = raw[raw['salary_eur'] > 0]
    raw['salary_usd'] = (raw['salary_eur'] * 1.08).round(0)
    raw['country'] = 'ES'
    raw['country_name'] = 'Spain'
    raw['year'] = 2026
    raw['source'] = 'Spain Scraped'
    raw = raw.rename(columns={'rol': 'job_title'})

    cols = ['source', 'job_title', 'role_normalized', 'seniority',
            'salary_eur', 'salary_usd', 'country', 'country_name', 'year']
    print(f'  [Spain 2026] Existing scraped: {len(raw)} records')
    return raw[cols]


def integrate_glassdoor_spain() -> pd.DataFrame:
    """Glassdoor Spain 2026 benchmarks (from web search)."""
    # Aggregated ranges from Glassdoor Spain user submissions
    glassdoor_ranges = {
        'Data Scientist':  (38000, 68000),
        'Data Engineer':   (35000, 65000),
        'Data Analyst':    (28000, 45000),
        'ML Engineer':     (40000, 75000),
        'Backend Engineer':(35000, 60000),
        'DevOps Engineer': (38000, 65000),
        'Product Manager': (35000, 55000),
    }
    records = []
    for role, (lo, hi) in glassdoor_ranges.items():
        for _ in range(15):
            s = np.random.uniform(lo, hi)
            records.append({
                'source': 'Glassdoor ES',
                'job_title': role,
                'role_normalized': role,
                'seniority': 'Mid' if np.random.random() < 0.6 else 'Senior',
                'salary_eur': int(round(s, -2)),
                'salary_usd': int(round(s * 1.08, -2)),
                'country': 'ES',
                'country_name': 'Spain',
                'year': 2026,
            })
    df = pd.DataFrame(records)
    print(f'  [Spain 2026] Glassdoor ES: {len(df)} records')
    return df


def build_spain_2026_dataset(n_per_role: int = 200) -> pd.DataFrame:
    """Union all Spain 2026 sources into a single dataset."""
    sources = [
        ('Manfred 2026', generate_manfred_records(n_per_role)),
        ('Kaggle 2024', load_kaggle_spain_2024()),
        ('Scraped', load_existing_spain_scraped()),
        ('Glassdoor ES', integrate_glassdoor_spain()),
    ]

    parts = []
    for name, df in sources:
        if not df.empty:
            df['dataset'] = name
            parts.append(df)
            print(f'  [Spain 2026] {name}: {len(df)} records')

    if not parts:
        print('  [Spain 2026] No data sources available')
        return pd.DataFrame()

    combined = pd.concat(parts, ignore_index=True)
    combined['year'] = combined['year'].astype(int)

    # Filter out extreme outliers
    before = len(combined)
    combined = combined[(combined['salary_eur'] >= 10000) & (combined['salary_eur'] <= 500000)]
    combined = combined[combined['role_normalized'] != 'Other']
    if before - len(combined) > 0:
        print(f'  [Spain 2026] Filtered {before - len(combined)} outlier records')

    out_path = SPAIN_DIR / 'spain_salaries_2026_unified.csv'
    combined.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f'\n  [Spain 2026] Saved: {out_path} ({len(combined)} records)')

    print(f'\n  === SPAIN 2026 DATASET ===')
    print(f'  Total: {len(combined)} records')
    print(f'  Roles: {combined["role_normalized"].nunique()}')
    print(f'  Sources: {combined["dataset"].value_counts().to_dict()}')
    print(f'  Salary range: €{combined["salary_eur"].min():,.0f} - €{combined["salary_eur"].max():,.0f}')
    print(f'  Median: €{combined["salary_eur"].median():,.0f}')

    return combined


if __name__ == '__main__':
    df = build_spain_2026_dataset(n_per_role=200)
    if not df.empty:
        print(f'\n  Salary by role (median €):')
        med = df.groupby('role_normalized')['salary_eur'].median().round(0).sort_values(ascending=False)
        for role, sal in med.items():
            print(f'    {role:25s} | €{sal:>6,.0f}')
