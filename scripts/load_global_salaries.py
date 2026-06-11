"""
load_global_salaries.py — Load & unify global salary datasets.

Integrates multiple public sources into a single unified schema:
  1. Kaggle DS Salaries (global, 2020-2024)
  2. LinkedIn (Kaggle arshkon, US-centric, 2023)
  3. Spain scraped data (Manfred, INE, Glassdoor ES)

Output: unified global dataframe with PPP-adjusted salary column.
"""
import pandas as pd
import numpy as np
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = DATA_DIR / 'global'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE_DIR / 'scripts'))
sys.path.insert(0, str(BASE_DIR / 'scripts' / 'pipeline'))
from pipeline.config import ROLE_CATEGORIES, REGIONS
from normalize_titles import normalize_title


def extract_country(location: str) -> str:
    """Extract country code from LinkedIn location string."""
    if pd.isna(location):
        return 'US'
    loc = location.lower()
    # Known country names
    for country, code in [('united states', 'US'), ('spain', 'ES'), ('france', 'FR'),
                          ('germany', 'DE'), ('united kingdom', 'GB'), ('canada', 'CA'),
                          ('australia', 'AU'), ('india', 'IN'), ('brazil', 'BR'),
                          ('mexico', 'MX'), ('netherlands', 'NL'), ('sweden', 'SE'),
                          ('denmark', 'DK'), ('norway', 'NO'), ('switzerland', 'CH')]:
        if country in loc:
            return code
    # US state abbreviations (2-letter codes preceded by comma)
    us_states = {'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga',
                 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md',
                 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj',
                 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
                 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy'}
    parts = [p.strip() for p in loc.replace(',', ' ').split()]
    if any(p in us_states for p in parts):
        return 'US'
    return 'US'  # default for LinkedIn Kaggle dataset (US-centric)


def load_linkedin_unified() -> pd.DataFrame:
    """Load already-normalized LinkedIn data."""
    path = DATA_DIR / 'linkedin_data_normalized.csv'
    if not path.exists():
        print('  [Global] LinkedIn normalized not found, running normalization...')
        from normalize_titles import apply_normalization
        raw = pd.read_csv(DATA_DIR / 'linkedin_data_roles_procesed.csv')
        df = apply_normalization(raw)
        df.to_csv(path, index=False, encoding='utf-8-sig')
    else:
        df = pd.read_csv(path)

    df['country'] = df['location'].apply(extract_country)
    df['country_name'] = df['country'].map({'US': 'United States', 'ES': 'Spain',
        'FR': 'France', 'DE': 'Germany', 'GB': 'United Kingdom', 'CA': 'Canada',
        'AU': 'Australia', 'IN': 'India', 'BR': 'Brazil', 'MX': 'Mexico',
        'NL': 'Netherlands', 'SE': 'Sweden', 'DK': 'Denmark', 'NO': 'Norway',
        'CH': 'Switzerland'}).fillna('United States')
    
    # Standardize columns for unified schema
    df['job_title'] = df['title']
    df['year'] = pd.to_datetime(df['listed_time'], unit='ms').dt.year
    # Use best available salary, preferring normalized_salary > med_salary > (min+max)/2
    df['salary_usd'] = df['normalized_salary'].fillna(
        df['med_salary'].fillna(
            (df['min_salary'].fillna(0) + df['max_salary'].fillna(0)) / 2
        )
    )
    df['salary_usd'] = df['salary_usd'].replace(0, np.nan)

    print(f'  [Global] LinkedIn: {len(df)} records ({df["country"].nunique()} countries, '
          f'{df["salary_usd"].notna().sum()} with salary)')
    return df


def load_kaggle_ds_unified() -> pd.DataFrame:
    """Load Kaggle DS Salaries dataset via kagglehub or local cache."""
    cache = DATA_DIR / 'global' / 'kaggle_ds_salaries.csv'
    if cache.exists():
        df = pd.read_csv(cache)
        print(f'  [Global] Kaggle DS: {len(df)} records (cached)')
        return df

    try:
        import kagglehub
        path = kagglehub.dataset_download('ruchi798/data-science-job-salaries')
        raw = pd.read_csv(f'{path}/ds_salaries.csv')
    except Exception as e:
        print(f'  [Global] Kaggle DS error: {e}')
        return pd.DataFrame()

    df = raw.copy()
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    exp_map = {'EN': 'Entry', 'MI': 'Mid', 'SE': 'Senior', 'EX': 'Executive'}
    df['experience_level'] = df['experience_level'].map(exp_map).fillna('Unknown')
    df['role_normalized'] = df['job_title'].apply(lambda t: normalize_title(t)['role'])
    df['seniority'] = df['experience_level']
    df['source'] = 'Kaggle DS Salaries'

    cols = {
        'job_title': 'job_title',
        'salary_in_usd': 'salary_usd',
        'company_location': 'country',
        'salary_currency': 'currency',
        'remote_ratio': 'remote_ratio',
        'company_size': 'company_size',
        'work_year': 'year',
    }
    df = df.rename(columns={k: v for k, v in cols.items()})

    country_names = {
        'US': 'United States', 'ES': 'Spain', 'GB': 'United Kingdom',
        'DE': 'Germany', 'FR': 'France', 'CA': 'Canada', 'IN': 'India',
        'PT': 'Portugal', 'NL': 'Netherlands', 'IE': 'Ireland', 'IT': 'Italy',
        'CH': 'Switzerland', 'SE': 'Sweden', 'DK': 'Denmark', 'NO': 'Norway',
        'FI': 'Finland', 'PL': 'Poland', 'CZ': 'Czechia', 'HU': 'Hungary',
        'RO': 'Romania', 'BG': 'Bulgaria', 'HR': 'Croatia', 'SI': 'Slovenia',
        'SK': 'Slovakia', 'LT': 'Lithuania', 'LV': 'Latvia', 'EE': 'Estonia',
        'CY': 'Cyprus', 'MT': 'Malta', 'LU': 'Luxembourg', 'GR': 'Greece',
        'AT': 'Austria', 'BE': 'Belgium', 'JP': 'Japan', 'AU': 'Australia',
        'BR': 'Brazil', 'MX': 'Mexico', 'NG': 'Nigeria', 'KE': 'Kenya',
        'SG': 'Singapore', 'HK': 'Hong Kong', 'IL': 'Israel', 'TR': 'Turkey',
        'ZA': 'South Africa', 'AE': 'UAE', 'CN': 'China', 'TW': 'Taiwan',
        'CO': 'Colombia', 'CL': 'Chile', 'AR': 'Argentina', 'PE': 'Peru',
        'RU': 'Russia', 'UA': 'Ukraine', 'PK': 'Pakistan', 'BD': 'Bangladesh',
        'VN': 'Vietnam', 'TH': 'Thailand', 'PH': 'Philippines', 'ID': 'Indonesia',
        'MY': 'Malaysia', 'NZ': 'New Zealand',
    }
    df['country_name'] = df['country'].map(country_names).fillna(df['country'])

    df.to_csv(cache, index=False, encoding='utf-8-sig')
    print(f'  [Global] Kaggle DS: {len(df)} records')
    return df


def load_spain_unified() -> pd.DataFrame:
    """Load Spain scraped data in unified format."""
    path = DATA_DIR / 'espana' / 'spain_tech_salaries_scraped.csv'
    if not path.exists():
        print('  [Global] Spain data not found')
        return pd.DataFrame()

    raw = pd.read_csv(path, encoding='utf-8-sig')
    df = raw.copy()

    def parse_salary_range(r: str) -> float | None:
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

    df['job_title'] = df['rol']
    df['role_normalized'] = df['rol'].apply(lambda t: normalize_title(t)['role'])
    df['seniority'] = df['experiencia']
    df['country'] = 'ES'
    df['country_name'] = 'Spain'
    df['salary_usd'] = df['rango_salarial'].apply(parse_salary_range)
    df['year'] = 2026

    print(f'  [Global] Spain: {len(df)} records ({df["salary_usd"].notna().sum()} with salary)')
    return df[['job_title', 'role_normalized', 'seniority', 'salary_usd',
               'country', 'country_name', 'year']]


def load_eurostat_context() -> pd.DataFrame:
    """Load Eurostat PPP rates from local or download."""
    eurostat_dir = DATA_DIR / 'eurostat'
    ppp_path = eurostat_dir / 'ppp_rates.csv'

    if ppp_path.exists():
        df = pd.read_csv(ppp_path)
        print(f'  [Global] Eurostat: {len(df)} PPP rates loaded')
        return df

    print('  [Global] Eurostat PPP not found. Run scripts/load_eurostat.py first.')
    return pd.DataFrame()


def build_global_dataset() -> pd.DataFrame:
    """Union all sources into a single global dataset."""
    sources = []
    for src_name, src_fn in [
        ('LinkedIn', load_linkedin_unified),
        ('Kaggle DS', load_kaggle_ds_unified),
        ('Spain', load_spain_unified),
    ]:
        print(f'\n--- Loading {src_name} ---')
        df = src_fn()
        if not df.empty:
            df['dataset'] = src_name
            sources.append(df)

    if not sources:
        print('No data sources available')
        return pd.DataFrame()

    # Union with common columns
    common = ['source', 'dataset', 'job_title', 'role_normalized', 'seniority',
              'salary_usd', 'country', 'country_name', 'year']
    parts = []
    for s in sources:
        available = [c for c in common if c in s.columns]
        parts.append(s[available])

    global_df = pd.concat(parts, ignore_index=True)
    global_df['salary_usd'] = pd.to_numeric(global_df['salary_usd'], errors='coerce')

    print(f'\n=== GLOBAL DATASET ===')
    print(f'Total records: {len(global_df)}')
    print(f'Sources: {global_df["dataset"].value_counts().to_dict()}')
    print(f'Countries: {global_df["country"].nunique()}')
    print(f'Roles: {global_df["role_normalized"].nunique()}')

    # Merge Eurostat context
    eurostat = load_eurostat_context()
    if not eurostat.empty:
        global_df = merge_eurostat_context(global_df, eurostat)

    out_path = OUTPUT_DIR / 'global_salaries_unified.csv'
    global_df.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f'\nSaved: {out_path} ({len(global_df)} records)')
    return global_df


def merge_eurostat_context(df: pd.DataFrame, eurostat: pd.DataFrame) -> pd.DataFrame:
    """Merge PPP rates for salary adjustment."""
    # Map country codes
    country_map = {'US': 'US', 'ES': 'ES', 'GB': 'UK', 'DE': 'DE', 'FR': 'FR',
                   'CA': 'CA', 'IN': 'IN', 'PT': 'PT', 'NL': 'NL', 'IT': 'IT',
                   'IE': 'IE', 'CH': 'CH', 'SE': 'SE', 'DK': 'DK', 'NO': 'NO',
                   'FI': 'FI', 'PL': 'PL', 'AT': 'AT', 'BE': 'BE', 'CZ': 'CZ',
                   'HU': 'HU', 'RO': 'RO', 'GR': 'GR', 'HR': 'HR', 'SK': 'SK',
                   'BG': 'BG', 'LT': 'LT', 'LV': 'LV', 'EE': 'EE', 'SI': 'SI',
                   'LU': 'LU', 'MT': 'MT', 'CY': 'CY'}

    df['country_eurostat'] = df['country'].map(country_map).fillna('OTHER')
    df['year_int'] = df['year'].astype(int)

    eurostat_clean = eurostat[['country_code', 'year', 'gdp_per_capita_usd', 'ppp_rate']].copy()
    eurostat_clean['year_int'] = eurostat_clean['year'].astype(int)

    merged = df.merge(
        eurostat_clean,
        left_on=['country_eurostat', 'year_int'],
        right_on=['country_code', 'year_int'],
        how='left'
    )

    # Apply PPP adjustment
    merged['salary_ppp_usd'] = merged.apply(
        lambda r: r['salary_usd'] / r['ppp_rate'] if pd.notna(r['ppp_rate'])
        and r['ppp_rate'] > 0 and pd.notna(r['salary_usd']) else np.nan,
        axis=1
    )

    print(f'  [Global] PPP-adjusted salaries: {merged["salary_ppp_usd"].notna().sum()} records')
    return merged


if __name__ == '__main__':
    import sys
    df = build_global_dataset()
    if not df.empty:
        print(f'\nGlobal salaries by region:')
        region_sal = df.groupby('dataset')['salary_usd'].agg(['count', 'median', 'mean']).round(0)
        print(region_sal.to_string())
