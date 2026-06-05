"""Carga el dataset Kaggle ruchi798/data-science-job-salaries."""
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'


def load_kaggle_ds() -> pd.DataFrame:
    try:
        import kagglehub
    except ImportError:
        print('  [Kaggle DS] kagglehub no instalado')
        return pd.DataFrame()

    try:
        path = kagglehub.dataset_download('ruchi798/data-science-job-salaries')
        df = pd.read_csv(path + '/ds_salaries.csv')
    except Exception as e:
        print(f'  [Kaggle DS] Error: {e}')
        return pd.DataFrame()

    print(f'  [Kaggle DS] Cargados {len(df)} registros raw')

    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    exp_map = {'EN': 'Entry', 'MI': 'Mid', 'SE': 'Senior', 'EX': 'Executive'}
    emp_map = {'FT': 'Full-time', 'PT': 'Part-time', 'CT': 'Contract', 'FL': 'Freelance'}
    size_map = {'S': 'Small', 'M': 'Medium', 'L': 'Large'}

    rows = []
    for _, row in df.iterrows():
        exp = exp_map.get(str(row.get('experience_level', '')), 'Unknown')
        role_norm = _map_role(str(row.get('job_title', '') or ''))
        country = str(row.get('company_location', '') or '')
        currency = str(row.get('salary_currency', '') or 'USD')
        salary_usd = row.get('salary_in_usd', 0)
        salary_local = row.get('salary', salary_usd)

        if pd.isna(salary_usd) or salary_usd <= 0:
            continue

        rows.append({
            'source': 'Kaggle DS Salaries',
            'source_type': 'kaggle',
            'country': country,
            'country_name': _country_name(country),
            'region': _region(country),
            'year': int(row.get('work_year', 2022)),
            'job_title': str(row.get('job_title', '') or ''),
            'role_category': role_norm,
            'experience_level': exp,
            'employment_type': emp_map.get(str(row.get('employment_type', '') or ''), 'Full-time'),
            'salary_local': float(salary_local),
            'currency': currency,
            'salary_usd': float(salary_usd),
            'remote_ratio': int(row.get('remote_ratio', 0)),
            'company_size': size_map.get(str(row.get('company_size', '') or ''), 'Medium'),
            'company_location': country,
            'latitude': None,
            'longitude': None,
        })

    result = pd.DataFrame(rows)
    print(f'  [Kaggle DS] {len(result)} registros unificados, '
          f'{result["country"].nunique()} paises, '
          f'{result["year"].nunique()} anos')
    return result


def _map_role(title: str) -> str:
    from .config import ROLE_CATEGORIES
    tl = title.lower().strip()
    for kw, cat in ROLE_CATEGORIES.items():
        if kw in tl:
            return cat
    return 'Other Data'


def _country_name(code: str) -> str:
    import pycountry
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        pass
    names = {
        'US': 'United States', 'ES': 'Spain', 'GB': 'United Kingdom',
        'DE': 'Germany', 'FR': 'France', 'CA': 'Canada', 'MX': 'Mexico',
        'IN': 'India', 'CN': 'China', 'JP': 'Japan', 'BR': 'Brazil',
        'AR': 'Argentina', 'CL': 'Chile', 'CO': 'Colombia', 'PT': 'Portugal',
        'IE': 'Ireland', 'NL': 'Netherlands', 'IT': 'Italy', 'CH': 'Switzerland',
        'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark', 'FI': 'Finland',
        'PL': 'Poland', 'AT': 'Austria', 'BE': 'Belgium', 'CZ': 'Czech Republic',
        'GR': 'Greece', 'HU': 'Hungary', 'RO': 'Romania', 'RU': 'Russia',
        'IL': 'Israel', 'SG': 'Singapore', 'HK': 'Hong Kong', 'AU': 'Australia',
        'NZ': 'New Zealand', 'AE': 'UAE', 'TR': 'Turkey', 'NG': 'Nigeria',
        'KE': 'Kenya', 'ZA': 'South Africa',
    }
    return names.get(code, code)


def _region(country: str) -> str:
    from .config import REGIONS
    return REGIONS.get(country, 'Other')


if __name__ == '__main__':
    df = load_kaggle_ds()
    if not df.empty:
        print(f'\nKaggle DS: {len(df)} registros')
        print(f'Paises: {df["country"].value_counts().head(15).to_dict()}')
        print(f'Roles: {df["role_category"].value_counts().to_dict()}')
