"""
export_tableau.py — Exporta datasets consolidados para Tableau Public
Genera CSVs planos y unificados listos para conectar desde Tableau.
"""
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / 'data' / 'tableau'
EXPORT_DIR = BASE_DIR / 'data'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def export_linkedin_tableau():
    """Exporta LinkedIn data roles en formato Tableau-friendly."""
    path = EXPORT_DIR / 'linkedin_data_roles_procesed.csv'
    if not path.exists():
        print("LinkedIn data not found")
        return

    df = pd.read_csv(path)

    exp_map = {
        0: 'Internship', 1: 'Entry Level', 2: 'Associate',
        3: 'Mid-Senior', 4: 'Director', 5: 'Executive',
    }
    df['experience_level'] = df['experience_level_num'].map(exp_map).fillna('Unknown')

    remote_map = {0: 'On-site', 1: 'Remote', np.nan: 'Unknown'}
    df['remote_status'] = df['remote_allowed'].map(remote_map).fillna('Unknown')

    keep = [
        'title', 'experience_level', 'remote_status',
        'normalized_salary', 'views', 'applies',
        'location', 'company_name', 'formatted_work_type',
        'formatted_experience_level', 'industry_id',
        'max_salary', 'med_salary', 'min_salary',
        'pay_period', 'currency', 'company_size',
        'zip_code', 'fips', 'city', 'state', 'country',
        'timestamp', 'original_listed_time',
    ]
    keep = [c for c in keep if c in df.columns]

    out = df[keep].copy()
    out.columns = [c.replace('_', ' ').title() for c in out.columns]

    out_path = OUTPUT_DIR / 'linkedin_data_roles_tableau.csv'
    out.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"LinkedIn Tableau: {len(out)} records -> {out_path}")
    return out


def export_spain_tableau():
    """Exporta Spain salary data en formato Tableau-friendly."""
    scraped_path = EXPORT_DIR / 'espana' / 'spain_tech_salaries_scraped.csv'
    if not scraped_path.exists():
        print("Spain data not found")
        return

    df = pd.read_csv(scraped_path, encoding='utf-8-sig')
    out_path = OUTPUT_DIR / 'spain_salaries_tableau.csv'
    df.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"Spain Tableau: {len(df)} records -> {out_path}")

    real_path = EXPORT_DIR / 'espana' / 'spain_tech_salaries_real.csv'
    if real_path.exists():
        df_r = pd.read_csv(real_path, encoding='utf-8-sig')
        out_path2 = OUTPUT_DIR / 'spain_salaries_real_tableau.csv'
        df_r.to_csv(out_path2, index=False, encoding='utf-8-sig')
        print(f"Spain Real Tableau: {len(df_r)} records -> {out_path2}")

    return df


def export_consolidated():
    """Crea un dataset consolidado LinkedIn + España para dashboard Tableau."""
    li = EXPORT_DIR / 'linkedin_data_roles_procesed.csv'
    es = EXPORT_DIR / 'espana' / 'spain_tech_salaries_scraped.csv'

    records = []

    if li.exists():
        df = pd.read_csv(li)
        df['dataset'] = 'LinkedIn'
        df['country_standard'] = 'US'
        df['currency_standard'] = 'USD'
        df['salary_annual'] = df['normalized_salary']
        df['source_detail'] = 'Kaggle (arshkon)'
        for _, row in df.iterrows():
            records.append({
                'Dataset': 'LinkedIn',
                'Source': 'Kaggle (arshkon)',
                'Role': str(row.get('title', '')),
                'Experience': str(row.get('formatted_experience_level', '')),
                'Salary': row.get('normalized_salary'),
                'Views': row.get('views'),
                'Applies': row.get('applies'),
                'Location': str(row.get('location', '')),
                'Company': str(row.get('company_name', '')),
                'Work_Type': str(row.get('formatted_work_type', '')),
                'Remote_Allowed': row.get('remote_allowed'),
                'Country': 'United States',
                'Currency': 'USD',
            })

    if es.exists():
        df_es = pd.read_csv(es, encoding='utf-8-sig')
        for _, row in df_es.iterrows():
            records.append({
                'Dataset': 'Spain',
                'Source': str(row.get('fuente', '')),
                'Role': str(row.get('rol', '')),
                'Experience': str(row.get('experiencia', '')),
                'Salary': None,
                'Views': None,
                'Applies': None,
                'Location': 'Spain',
                'Company': '',
                'Work_Type': '',
                'Remote_Allowed': None,
                'Country': 'Spain',
                'Currency': 'EUR',
            })

    out = pd.DataFrame(records)
    out_path = OUTPUT_DIR / 'datascope_consolidated_tableau.csv'
    out.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"Consolidated: {len(out)} records -> {out_path}")
    return out


def main():
    print("=" * 60)
    print("EXPORT TABLEAU - DATASCOPE")
    print("=" * 60)

    print("\n--- LinkedIn Data Roles ---")
    export_linkedin_tableau()

    print("\n--- Spain Salary Data ---")
    export_spain_tableau()

    print("\n--- Consolidated Dataset ---")
    export_consolidated()

    print(f"\n{'='*60}")
    print(f"Archivos exportados a: {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob('*.csv')):
        print(f"  {f.name} ({f.stat().st_size / 1e3:.0f} KB)")
    print(f"{'='*60}")
    print("\n>> Abre Tableau Public -> Conectar -> Texto/CSV -> selecciona un archivo")
    print(">> Recomendado: datascope_consolidated_tableau.csv para dashboard completo")


if __name__ == '__main__':
    main()
