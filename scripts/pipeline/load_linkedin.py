"""Carga datos de LinkedIn desde CSV local."""
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'


def load_linkedin() -> pd.DataFrame:
    path = DATA_DIR / 'linkedin_data_roles_procesed.csv'
    if not path.exists():
        print('  [LinkedIn] CSV no encontrado, intentando kagglehub...')
        return _load_from_kaggle()
    df = pd.read_csv(path)
    print(f'  [LinkedIn] Cargados {len(df)} registros locales')

    rows = []
    for _, row in df.iterrows():
        exp = str(row.get('formatted_experience_level', '') or '').lower().strip()
        exp_norm = _map_experience(exp)
        role_norm = _map_role(str(row.get('title', '') or ''))
        location = str(row.get('location', '') or '')
        country = _extract_country(location)
        remote = row.get('remote_allowed', 0)
        if pd.isna(remote):
            remote = 0
        remote = int(remote)

        salary = row.get('normalized_salary')
        if pd.isna(salary) or salary is None or salary <= 0:
            continue

        rows.append({
            'source': 'LinkedIn',
            'source_type': 'kaggle',
            'country': country,
            'country_name': _country_name(country),
            'region': _region(country),
            'year': _extract_year(row),
            'job_title': str(row.get('title', '') or ''),
            'role_category': role_norm,
            'experience_level': exp_norm,
            'employment_type': 'Full-time',
            'salary_local': float(salary),
            'currency': 'USD',
            'salary_usd': float(salary),
            'remote_ratio': 100 if remote == 1 else 0,
            'company_size': 'M',
            'company_location': location,
            'latitude': None,
            'longitude': None,
        })

    result = pd.DataFrame(rows)
    print(f'  [LinkedIn] {len(result)} registros unificados')
    return result


def _load_from_kaggle() -> pd.DataFrame:
    try:
        import kagglehub
        path = kagglehub.dataset_download('arshkon/linkedin-job-postings')
        df = pd.read_csv(os.path.join(path, 'postings.csv'))
    except Exception as e:
        print(f'  [LinkedIn] Error: {e}')
        return pd.DataFrame()

    data_kw = 'data scientist|data engineer|data analyst|machine learning|ml engineer|ai engineer|business intelligence|data architect|analytics|data manager'
    df_data = df[df['title'].str.contains(data_kw, case=False, na=False)].copy()
    df_data['title'] = df_data['title'].str.lower().str.strip()
    df_data['location'] = df_data['location'].str.lower().str.strip()

    rows = []
    for _, row in df_data.iterrows():
        exp = str(row.get('formatted_experience_level', '') or '').lower().strip()
        exp_norm = _map_experience(exp)
        role_norm = _map_role(str(row.get('title', '') or ''))
        location = str(row.get('location', '') or '')
        country = _extract_country(location)

        salary = row.get('normalized_salary')
        if pd.isna(salary) or salary is None or salary <= 0:
            continue

        rows.append({
            'source': 'LinkedIn',
            'source_type': 'kaggle',
            'country': country,
            'country_name': _country_name(country),
            'region': _region(country),
            'year': _extract_year(row),
            'job_title': str(row.get('title', '') or ''),
            'role_category': role_norm,
            'experience_level': exp_norm,
            'employment_type': 'Full-time',
            'salary_local': float(salary),
            'currency': 'USD',
            'salary_usd': float(salary),
            'remote_ratio': 100 if row.get('remote_allowed', 0) == 1 else 0,
            'company_size': 'M',
            'company_location': location,
            'latitude': None,
            'longitude': None,
        })

    df_out = pd.DataFrame(rows)
    df_out.to_csv(DATA_DIR / 'linkedin_data_roles_procesed.csv', index=False)
    print(f'  [LinkedIn] {len(df_out)} registros desde Kaggle (guardados localmente)')
    return df_out


def _map_experience(exp: str) -> str:
    from .config import EXPERIENCE_MAP
    if not exp:
        return 'Unknown'
    return EXPERIENCE_MAP.get(exp, 'Unknown')


def _map_role(title: str) -> str:
    from .config import ROLE_CATEGORIES
    title_lower = title.lower().strip()
    for kw, cat in ROLE_CATEGORIES.items():
        if kw in title_lower:
            return cat
    return 'Other Tech'


def _extract_country(location: str) -> str:
    if not location:
        return 'US'
    loc_lower = location.lower()
    if 'united states' in loc_lower or 'usa' in loc_lower or 'us' == loc_lower.strip():
        return 'US'
    if 'spain' in loc_lower or 'espana' in loc_lower or 'españa' in loc_lower:
        return 'ES'
    if 'united kingdom' in loc_lower or 'uk' in loc_lower or 'england' in loc_lower:
        return 'GB'
    if 'germany' in loc_lower or 'deutschland' in loc_lower:
        return 'DE'
    if 'france' in loc_lower:
        return 'FR'
    if 'canada' in loc_lower:
        return 'CA'
    if 'mexico' in loc_lower:
        return 'MX'
    if 'india' in loc_lower:
        return 'IN'
    if 'china' in loc_lower:
        return 'CN'
    if 'japan' in loc_lower or 'japan' in loc_lower:
        return 'JP'
    return 'US'


def _country_name(code: str) -> str:
    names = {'US': 'United States', 'ES': 'Spain', 'GB': 'United Kingdom',
             'DE': 'Germany', 'FR': 'France', 'CA': 'Canada', 'MX': 'Mexico',
             'IN': 'India', 'CN': 'China', 'JP': 'Japan'}
    return names.get(code, code)


def _region(country: str) -> str:
    from .config import REGIONS
    return REGIONS.get(country, 'Other')


def _extract_year(row):
    try:
        ts = row.get('original_listed_time') or row.get('listed_time')
        if pd.notna(ts):
            return int(pd.to_datetime(ts, unit='s').year)
    except:
        pass
    return 2023


if __name__ == '__main__':
    df = load_linkedin()
    print(f'LinkedIn: {len(df)} registros, {df["country"].nunique()} paises')
    print(df['country'].value_counts().head(10))
