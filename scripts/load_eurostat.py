"""
load_eurostat.py — Download and process Eurostat demographic & economic data.

Provides population (demo_pjan) and GDP (nama_10_gdp) for PPP-adjusted salary
comparisons across EU countries.

Sources:
  - demo_pjan: Population by age, sex, and NUTS region
  - nama_10_gdp: GDP and main components by NUTS region

Downloads via TSV bulk download (more reliable than JSON-stat).
"""
import pandas as pd
import numpy as np
import requests, io, gzip, os, sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data' / 'eurostat'
DATA_DIR.mkdir(parents=True, exist_ok=True)

TSV_BASE = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{}/?format=TSV&compressed=true'


def download_tsv(dataset_code: str) -> pd.DataFrame:
    """Download Eurostat dataset as compressed TSV, return DataFrame."""
    url = TSV_BASE.format(dataset_code)
    print(f'  [Eurostat] Downloading {dataset_code}...')

    try:
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        content = gzip.decompress(r.content).decode('utf-8', errors='replace')
    except Exception as e:
        print(f'  [Eurostat] ERROR: {e}')
        return pd.DataFrame()

    # Parse TSV: Eurostat format is dim1,dim2,...\t1960\t1961\t...
    lines = content.strip().split('\n')
    if len(lines) < 2:
        print('  [Eurostat] Empty response')
        return pd.DataFrame()

    header_parts = lines[0].split('\t')
    # First column is "dim1,dim2,...\TIME_PERIOD", rest are year columns
    years = [h.strip() for h in header_parts[1:]]

    records = []
    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        dim_key = parts[0].strip()
        values_raw = parts[1:]

        for idx, val in enumerate(values_raw):
            if idx >= len(years):
                break
            year = years[idx]
            val = val.strip()
            # Eurostat missing values are ": " or ":" or ": "
            if val in (':', ': ', '', ':', ':', 'Na', 'NA'):
                continue

            # Remove flags (e.g. "1234.5 b" means break in series)
            val_clean = val.split()[0].strip()
            try:
                num_val = float(val_clean)
            except ValueError:
                continue

            records.append({
                'dim_key': dim_key,
                'dataset': dataset_code,
                'year': year,
                'value': num_val,
            })

    df = pd.DataFrame(records)
    print(f'  [Eurostat] {dataset_code}: {len(df)} records parsed')
    return df


def parse_dim_key(dim_key: str, dataset: str, dim_names: list) -> dict:
    """Parse a dimension key like 'A,NR,TOTAL,F,ES' into individual dimensions."""
    parts = dim_key.split(',')
    result = {}
    for i, name in enumerate(dim_names):
        val = parts[i] if i < len(parts) else ''
        result[name] = val
    return result


def load_population() -> pd.DataFrame:
    """Load Eurostat population (demo_pjan). Total, national level, yearly."""
    path = DATA_DIR / 'population_national.csv'
    if path.exists():
        df = pd.read_csv(path)
        print(f'  [Eurostat] Population loaded from cache: {len(df)} rows')
        return df

    df = download_tsv('demo_pjan')
    if df.empty:
        return df

    # Parse dim_key: format is freq\unit\age\sex\geo
    dim_names = ['freq', 'unit', 'age', 'sex', 'geo']
    parsed = df['dim_key'].apply(lambda k: parse_dim_key(k, 'demo_pjan', dim_names))
    parsed_df = pd.json_normalize(parsed)
    df = pd.concat([df, parsed_df], axis=1)

    # Filter: total population (all ages, both sexes)
    for col in ['age', 'sex', 'unit']:
        if col not in df.columns:
            print(f'  [Eurostat] WARNING: column "{col}" not found in population data')
            return pd.DataFrame()
    df = df[df['age'] == 'TOTAL']
    df = df[df['sex'] == 'T']
    df = df[df['unit'] == 'NR']

    df = df.rename(columns={'geo': 'country_code', 'value': 'population', 'year': 'year'})
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['population'] = pd.to_numeric(df['population'], errors='coerce')
    df = df[df['population'] > 0]

    eurostat_map = {
        'ES': 'Spain', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy',
        'PT': 'Portugal', 'NL': 'Netherlands', 'BE': 'Belgium', 'AT': 'Austria',
        'IE': 'Ireland', 'GR': 'Greece', 'FI': 'Finland', 'SE': 'Sweden',
        'DK': 'Denmark', 'PL': 'Poland', 'CZ': 'Czechia', 'HU': 'Hungary',
        'RO': 'Romania', 'BG': 'Bulgaria', 'HR': 'Croatia', 'SI': 'Slovenia',
        'SK': 'Slovakia', 'LT': 'Lithuania', 'LV': 'Latvia', 'EE': 'Estonia',
        'CY': 'Cyprus', 'MT': 'Malta', 'LU': 'Luxembourg',
        'UK': 'United Kingdom', 'CH': 'Switzerland', 'NO': 'Norway',
        'US': 'United States', 'IS': 'Iceland', 'LI': 'Liechtenstein',
        'EU27_2020': 'EU27', 'EA20': 'Eurozone',
    }
    df['country_name'] = df['country_code'].map(eurostat_map).fillna(df['country_code'])

    cols = ['country_code', 'country_name', 'year', 'population']
    df = df[cols].dropna(subset=['year']).reset_index(drop=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f'  [Eurostat] Population saved: {len(df)} rows')
    return df


def load_gdp() -> pd.DataFrame:
    """Load Eurostat GDP (nama_10_gdp). GDP at market prices, CP_MEUR."""
    path = DATA_DIR / 'gdp_national.csv'
    if path.exists():
        df = pd.read_csv(path)
        print(f'  [Eurostat] GDP loaded from cache: {len(df)} rows')
        return df

    df = download_tsv('nama_10_gdp')
    if df.empty:
        return df

    dim_names = ['freq', 'unit', 'na_item', 'geo']
    parsed = df['dim_key'].apply(lambda k: parse_dim_key(k, 'nama_10_gdp', dim_names))
    parsed_df = pd.json_normalize(parsed)
    df = pd.concat([df, parsed_df], axis=1)

    # Filter: GDP at market prices, current prices MEUR
    df = df[df.get('na_item', '') == 'B1GQ']
    df = df[df.get('unit', '') == 'CP_MEUR']

    df = df.rename(columns={'geo': 'country_code', 'value': 'gdp_meur', 'year': 'year'})
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['gdp_meur'] = pd.to_numeric(df['gdp_meur'], errors='coerce')
    df = df[df['gdp_meur'] > 0]

    eurostat_map = {
        'ES': 'Spain', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy',
        'PT': 'Portugal', 'NL': 'Netherlands', 'BE': 'Belgium', 'AT': 'Austria',
        'IE': 'Ireland', 'GR': 'Greece', 'FI': 'Finland', 'SE': 'Sweden',
        'DK': 'Denmark', 'PL': 'Poland', 'CZ': 'Czechia', 'HU': 'Hungary',
        'RO': 'Romania', 'BG': 'Bulgaria', 'HR': 'Croatia', 'SI': 'Slovenia',
        'SK': 'Slovakia', 'LT': 'Lithuania', 'LV': 'Latvia', 'EE': 'Estonia',
        'CY': 'Cyprus', 'MT': 'Malta', 'LU': 'Luxembourg',
        'UK': 'United Kingdom', 'CH': 'Switzerland', 'NO': 'Norway',
        'EU27_2020': 'EU27', 'EA20': 'Eurozone',
    }
    df['country_name'] = df['country_code'].map(eurostat_map).fillna(df['country_code'])

    cols = ['country_code', 'country_name', 'year', 'gdp_meur']
    df = df[cols].dropna(subset=['year']).reset_index(drop=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f'  [Eurostat] GDP saved: {len(df)} rows')
    return df


def compute_ppp_rates(pop_df: pd.DataFrame, gdp_df: pd.DataFrame) -> pd.DataFrame:
    """Compute GDP per capita as PPP proxy for salary adjustments."""
    # Use the country_name from population (more comprehensive mapping)
    country_map = pop_df[['country_code', 'country_name']].drop_duplicates()

    merged = pd.merge(
        gdp_df[['country_code', 'year', 'gdp_meur']],
        pop_df[['country_code', 'year', 'population']],
        on=['country_code', 'year'], how='inner'
    )
    merged = merged.merge(country_map, on='country_code', how='left')
    merged['gdp_per_capita_eur'] = (merged['gdp_meur'] * 1e6) / merged['population']
    merged['gdp_per_capita_usd'] = merged['gdp_per_capita_eur'] * 1.08

    # Compute PPP rate relative to US (or EU average if US not in dataset)
    us = merged[merged['country_code'] == 'US'][['year', 'gdp_per_capita_usd']].rename(
        columns={'gdp_per_capita_usd': 'us_gdp_pc'})
    merged = merged.merge(us, on='year', how='left')

    if us.empty:
        print('  [Eurostat] US not in EU data — using EU-average-based PPP proxy')
        eu_avg = merged.groupby('year')['gdp_per_capita_usd'].transform('mean')
        merged['ppp_rate'] = (merged['gdp_per_capita_usd'] / eu_avg).round(4)
    else:
        merged['ppp_rate'] = (merged['gdp_per_capita_usd'] / merged['us_gdp_pc']).round(4)

    return merged


def main():
    print('=' * 60)
    print('EUROSTAT DATA LOADER - PEARSONS FOUR')
    print('=' * 60)

    print('\n--- Population ---')
    pop = load_population()
    if not pop.empty:
        print(f'  Years: {pop["year"].min()} - {pop["year"].max()}')
        print(f'  Countries: {pop["country_code"].nunique()}')

    print('\n--- GDP ---')
    gdp = load_gdp()
    if not gdp.empty:
        print(f'  Years: {gdp["year"].min()} - {gdp["year"].max()}')
        print(f'  Countries: {gdp["country_code"].nunique()}')

    if not pop.empty and not gdp.empty:
        print('\n--- PPP Rates ---')
        ppp = compute_ppp_rates(pop, gdp)
        ppp_path = DATA_DIR / 'ppp_rates.csv'
        ppp.to_csv(ppp_path, index=False, encoding='utf-8-sig')

        print(f'  PPP rates computed: {len(ppp)} rows')
        print(f'  Latest year: {ppp["year"].max()}')
        latest = ppp[ppp['year'] == ppp['year'].max()].sort_values('gdp_per_capita_eur', ascending=False)
        print(f'\n  Top 5 by GDP/capita ({int(ppp["year"].max())}):')
        for _, r in latest.head(5).iterrows():
            print(f'    {r["country_name"]:15s} | {r["gdp_per_capita_eur"]:>8,.0f} EUR | PPP: {r["ppp_rate"]:.3f}')

    print(f'\n{"="*60}')
    print(f'Data saved to: {DATA_DIR}')
    print(f'{"="*60}')


if __name__ == '__main__':
    main()
