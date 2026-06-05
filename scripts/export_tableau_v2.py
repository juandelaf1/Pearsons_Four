"""
export_tableau_v2.py — Exporta datasets optimizados para Tableau Public
Con salarios de España parseados a numérico + dataset consolidado limpio.
"""
import pandas as pd
import numpy as np
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / 'data' / 'tableau'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_salary_eur(s):
    """Parsea rango salarial español a valor numérico (midpoint en EUR)."""
    if pd.isna(s):
        return None
    s = str(s).replace('\u20ac', 'EUR').replace('\u2013', '-').replace('\u2014', '-').strip()

    m = re.search(r'([\d.,]+)\s*EUR', s)
    if m:
        try:
            return float(m.group(1).replace('.', '').replace(',', '.'))
        except:
            pass

    m = re.search(r'€?(\d+)\s*[–\-–]\s*€?(\d+)\s*K?', s)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        return (lo + hi) / 2 * 1000

    m = re.search(r'€?(\d+)\s*K', s)
    if m:
        return int(m.group(1)) * 1000

    m = re.search(r'(\d+)', s)
    if m:
        try:
            return float(m.group(1))
        except:
            pass
    return None


def export_linkedin_v2():
    path = BASE_DIR / 'data' / 'linkedin_data_roles_procesed.csv'
    if not path.exists():
        print("LinkedIn data not found")
        return None

    df = pd.read_csv(path)

    exp_map = {
        0: 'Internship', 1: 'Entry Level', 2: 'Associate',
        3: 'Mid-Senior', 4: 'Director', 5: 'Executive',
    }
    df['Experience_Level'] = df['experience_level_num'].map(exp_map).fillna('Unknown')
    df['Remote_Status'] = df['remote_allowed'].map({0: 'On-site', 1: 'Remote'}).fillna('Unknown')
    df['Work_Type'] = df['formatted_work_type'].fillna('Unknown')
    df['Country'] = 'United States'
    df['Currency'] = 'USD'
    df['Dataset'] = 'LinkedIn'
    df['Source'] = 'Kaggle (arshkon)'
    df['Salary_EUR'] = df['normalized_salary'] * 0.92

    out = pd.DataFrame({
        'Dataset': 'LinkedIn',
        'Source': 'Kaggle (arshkon)',
        'Role': df['title'].str.title(),
        'Experience_Level': df['Experience_Level'],
        'Salary_USD': df['normalized_salary'],
        'Salary_EUR': df['Salary_EUR'],
        'Views': df['views'],
        'Applies': df['applies'],
        'Remote': df['Remote_Status'],
        'Work_Type': df['Work_Type'],
        'Location': df['location'].str.title(),
        'Company': df['company_name'].str.title(),
        'Country': 'United States',
    })

    out_path = OUTPUT_DIR / 'linkedin_tableau.csv'
    out.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"LinkedIn: {len(out)} records -> {out_path}")
    return out


def export_spain_v2():
    path = BASE_DIR / 'data' / 'espana' / 'spain_tech_salaries_scraped.csv'
    if not path.exists():
        print("Spain scraped data not found")
        return None

    df = pd.read_csv(path, encoding='utf-8-sig')
    df['Salary_EUR'] = df['rango_salarial'].apply(parse_salary_eur)

    out = pd.DataFrame({
        'Dataset': 'Spain',
        'Source': df['fuente'],
        'Role': df['rol'],
        'Experience_Level': df['experiencia'],
        'Salary_USD': df['Salary_EUR'] * 1.08,
        'Salary_EUR': df['Salary_EUR'],
        'Views': None,
        'Applies': None,
        'Remote': 'Unknown',
        'Work_Type': 'Full-time',
        'Location': 'Spain',
        'Company': '',
        'Country': 'Spain',
    })

    out_path = OUTPUT_DIR / 'spain_scraped_tableau.csv'
    out.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"Spain scraped: {len(out)} records -> {out_path}")

    real_path = BASE_DIR / 'data' / 'espana' / 'spain_tech_salaries_real.csv'
    if real_path.exists():
        df_r = pd.read_csv(real_path, encoding='utf-8-sig')
        sal_col = 'salario_medio_anual' if 'salario_medio_anual' in df_r.columns else 'salario_bruto_anual_est'
        df_r['Salary_EUR'] = pd.to_numeric(df_r[sal_col], errors='coerce')

        out2 = pd.DataFrame({
            'Dataset': 'Spain_Real',
            'Source': 'INE + Manfred + Tecnoempleo',
            'Role': df_r.get('role_category', df_r.get('title', '')),
            'Experience_Level': df_r.get('experience_level', df_r.get('experiencia', '')),
            'Salary_USD': df_r['Salary_EUR'] * 1.08,
            'Salary_EUR': df_r['Salary_EUR'],
            'Views': None,
            'Applies': None,
            'Remote': 'Unknown',
            'Work_Type': 'Full-time',
            'Location': df_r.get('location_normalized', 'Spain'),
            'Company': '',
            'Country': 'Spain',
        })
        out2_path = OUTPUT_DIR / 'spain_real_tableau.csv'
        out2.to_csv(out2_path, index=False, encoding='utf-8-sig')
        print(f"Spain real: {len(out2)} records -> {out2_path}")
        return pd.concat([out, out2], ignore_index=True)

    return out


def export_consolidated_v2():
    li = export_linkedin_v2()
    es = export_spain_v2()

    parts = [p for p in [li, es] if p is not None and len(p) > 0]
    if not parts:
        print("No data to consolidate")
        return

    out = pd.concat(parts, ignore_index=True)

    out_path = OUTPUT_DIR / 'pearsons_four_consolidated.csv'
    out.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"\nConsolidated: {len(out)} records total -> {out_path}")

    print(f"\n  LinkedIn:    {len(li) if li is not None else 0} records")
    print(f"  Spain:       {len(es) if es is not None else 0} records")
    print(f"  With salary: {out['Salary_EUR'].notna().sum()} records")
    return out


def main():
    print("=" * 60)
    print("EXPORT TABLEAU V2 - PEARSON'S FOUR")
    print("=" * 60)
    export_consolidated_v2()

    print(f"\n{'='*60}")
    print("Archivos en data/tableau/:")
    for f in sorted(OUTPUT_DIR.glob('*.csv')):
        print(f"  {f.name} ({f.stat().st_size / 1e3:.0f} KB)")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
