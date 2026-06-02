"""
Spain Tech Salary Analysis - Real Data Pipeline
=================================================
Sources:
  - INE Table 28185: National salary by sector (tech avg = 42,742 EUR for 2024)
  - INE Table 28191: Salary by autonomous community (regional multipliers)
  - Manfred 2026 Salary Guide: Salary ranges by role & experience
  - Ametic/Expansion 2025: Tech avg = 48,900 EUR
  - INE Estadistica Continua de Poblacion: Real population by CCAA (2026)
"""

import pandas as pd
import numpy as np
import re, os

# =====================================================================
# 1. REAL INE DATA: National salary by sector (Table 28185, sector J)
# =====================================================================
# For 2024, tech sector (J - Information and communication) avg: 42,741.94 EUR
INE_TECH_AVG_2024 = 42741.94
INE_NATIONAL_AVG_2024 = 29540.26
INE_TECH_PREMIUM = INE_TECH_AVG_2024 / INE_NATIONAL_AVG_2024  # 1.447

# INE tech salaries by year (ambos sexos) for trend analysis
INE_TECH_TREND = {
    2008: 30628.48, 2009: 31551.65, 2010: 32425.68, 2011: 32491.04,
    2012: 32522.11, 2013: 33137.17, 2014: 32754.21, 2015: 33046.23,
    2016: 32448.31, 2017: 33664.26, 2018: 33117.64, 2019: 34641.28,
    2020: 35663.80, 2021: 36630.48, 2022: 37438.55, 2023: 39674.43,
    2024: 42741.94
}

# =====================================================================
# 2. REAL INE DATA: Regional multipliers (Table 28191, all sectors, 2024)
# =====================================================================
# These are the actual mean salaries by CCAA from INE, divided by national mean
# National mean 2024 (all sectors): 29,540.26
# Regional means from INE Table 28191 (both sexes, 2024)
REGIONAL_MEANS = {
    'Total Nacional': 29540.26,
    'Andalucia': 26089.70,
    'Aragon': 28061.94,
    'Asturias': 28562.31,
    'Balears': 26012.71,
    'Canarias': 25051.51,
    'Cantabria': 27916.60,
    'Castilla y Leon': 26745.93,
    'Castilla - La Mancha': 25046.60,
    'Cataluna': 31730.05,
    'Comunitat Valenciana': 26822.32,
    'Extremadura': 23194.02,
    'Galicia': 24527.96,
    'Madrid': 35170.28,
    'Murcia': 26547.27,
    'Navarra': 32605.28,
    'Pais Vasco': 31063.68,
    'Rioja, La': 26780.49
}

# Compute regional multipliers
NATIONAL_MEAN = REGIONAL_MEANS['Total Nacional']
REGIONAL_MULTIPLIERS = {
    k: round(v / NATIONAL_MEAN, 4) for k, v in REGIONAL_MEANS.items()
}

# Map job offer locations to INE CCAA names
LOCATION_TO_CCAA = {
    'barcelona': 'Cataluna', 'cataluna': 'Cataluna', 'catalonia': 'Cataluna',
    'madrid': 'Madrid', 'valencia': 'Comunitat Valenciana', 'alicante': 'Comunitat Valenciana',
    'sevilla': 'Andalucia', 'andalucia': 'Andalucia', 'malaga': 'Andalucia',
    'bilbao': 'Pais Vasco', 'pais vasco': 'Pais Vasco', 'guipuzcoa': 'Pais Vasco',
    'zaragoza': 'Aragon', 'aragon': 'Aragon',
    'asturias': 'Asturias', 'gijon': 'Asturias',
    'palma': 'Balears', 'baleares': 'Balears',
    'tenerife': 'Canarias', 'las palmas': 'Canarias', 'canarias': 'Canarias',
    'murcia': 'Murcia', 'navarra': 'Navarra', 'pamplona': 'Navarra',
    'galicia': 'Galicia', 'coruna': 'Galicia', 'vigo': 'Galicia',
    'castilla y leon': 'Castilla y Leon', 'valladolid': 'Castilla y Leon',
    'rioja': 'Rioja, La', 'logrono': 'Rioja, La',
    'extremadura': 'Extremadura', 'badajoz': 'Extremadura',
    'cantabria': 'Cantabria', 'santander': 'Cantabria',
    'castilla-la mancha': 'Castilla - La Mancha', 'toledo': 'Castilla - La Mancha',
}

# =====================================================================
# 3. REAL MANFRED 2026 SALARY RANGES (by role and experience)
# =====================================================================
MANFRED_RANGES = {
    'backend': {'Junior': (20000, 30000), 'Mid': (31000, 40000), 'Senior': (41000, 55000)},
    'frontend': {'Junior': (20000, 30000), 'Mid': (31000, 35000), 'Senior': (35000, 50000)},
    'fullstack': {'Junior': (22000, 32000), 'Mid': (33000, 42000), 'Senior': (43000, 55000)},
    'data_scientist': {'Junior': (25000, 35000), 'Mid': (36000, 48000), 'Senior': (50000, 75000)},
    'data_engineer': {'Junior': (26000, 36000), 'Mid': (37000, 50000), 'Senior': (52000, 78000)},
    'data_analyst': {'Junior': (22000, 30000), 'Mid': (31000, 42000), 'Senior': (43000, 55000)},
    'devops': {'Junior': (26000, 35000), 'Mid': (36000, 48000), 'Senior': (50000, 70000)},
    'mobile': {'Junior': (22000, 32000), 'Mid': (33000, 45000), 'Senior': (46000, 60000)},
    'qa': {'Junior': (18000, 26000), 'Mid': (27000, 36000), 'Senior': (37000, 48000)},
    'sysadmin': {'Junior': (18000, 25000), 'Mid': (26000, 35000), 'Senior': (36000, 45000)},
    'security': {'Junior': (26000, 36000), 'Mid': (37000, 50000), 'Senior': (52000, 75000)},
    'ai_engineer': {'Junior': (28000, 38000), 'Mid': (40000, 55000), 'Senior': (58000, 85000)},
}

def classify_role_and_experience(title):
    """Classify job title into role category and experience level."""
    t = str(title).lower()

    # Experience level detection
    if any(kw in t for kw in ['senior', 'sr ', 'lead', 'head of', 'manager', 'director', 'architect', 'principal', 'staff']):
        exp = 'Senior'
    elif any(kw in t for kw in ['junior', 'jr ', 'trainee', 'graduate', 'entry', 'practicas']):
        exp = 'Junior'
    elif any(kw in t for kw in ['mid', 'semi']):
        exp = 'Mid'
    else:
        # Default based on role maturity - most offers are mid-level
        exp = 'Mid'

    # Role classification
    if any(kw in t for kw in ['data scientist', 'data science', 'científico', 'cientifico']):
        role = 'data_scientist'
    elif any(kw in t for kw in ['data engineer', 'data engineering', 'ingeniero de datos']):
        role = 'data_engineer'
    elif any(kw in t for kw in ['data analyst', 'analista de datos', 'business intelligence', 'bi ', 'data analytics']):
        role = 'data_analyst'
    elif any(kw in t for kw in ['machine learning', 'ml ', 'deep learning', 'ai engineer', 'ia ', 'inteligencia artificial']):
        role = 'ai_engineer'
    elif any(kw in t for kw in ['backend', 'back-end', 'back end']):
        role = 'backend'
    elif any(kw in t for kw in ['frontend', 'front-end', 'front end']):
        role = 'frontend'
    elif any(kw in t for kw in ['full stack', 'fullstack', 'full-stack']):
        role = 'fullstack'
    elif any(kw in t for kw in ['devops', 'dev ops']):
        role = 'devops'
    elif any(kw in t for kw in ['mobile', 'ios', 'android', 'swift']):
        role = 'mobile'
    elif any(kw in t for kw in ['qa ', 'quality assurance', 'tester', 'testing']):
        role = 'qa'
    elif any(kw in t for kw in ['security', 'ciberseguridad', 'cyber']):
        role = 'security'
    elif any(kw in t for kw in ['sysadmin', 'system admin', 'administrador de sistemas']):
        role = 'sysadmin'
    else:
        # Default to data analyst for data-related, backend for IT
        if any(kw in t for kw in ['data', 'analytics', 'big data', 'sql']):
            role = 'data_analyst'
        elif any(kw in t for kw in ['software', 'developer', 'programmer', 'engineer', 'java', 'python', 'javascript', 'web']):
            role = 'backend'
        else:
            role = 'backend'  # most generic tech role

    return role, exp


def estimate_salary(role, exp_level, region_ccaa):
    """Estimate salary based on Manfred ranges + INE regional multiplier."""
    if role not in MANFRED_RANGES:
        role = 'backend'
    if exp_level not in MANFRED_RANGES[role]:
        exp_level = 'Mid'

    lo, hi = MANFRED_RANGES[role][exp_level]
    base = (lo + hi) / 2  # midpoint

    # Apply regional multiplier
    mult = REGIONAL_MULTIPLIERS.get(region_ccaa, 1.0)
    adjusted = base * mult

    return round(adjusted, 2)


# =====================================================================
# 4. REAL POPULATION DATA (INE Estadistica Continua, Jan 2026)
# =====================================================================
POPULATION_2026 = {
    'Total Nacional': 49570725,
    'Andalucia': 8733535,
    'Aragon': 1381842,
    'Asturias': 1021733,
    'Balears': 1259545,
    'Canarias': 2272734,
    'Cantabria': 597281,
    'Castilla y Leon': 2418425,
    'Castilla - La Mancha': 2154244,
    'Cataluna': 8208894,
    'Comunitat Valenciana': 5521600,
    'Extremadura': 1055197,
    'Galicia': 2728315,
    'Madrid': 7170906,
    'Murcia': 1604043,
    'Navarra': 689018,
    'Pais Vasco': 2252730,
    'Rioja, La': 329490
}

# =====================================================================
# 5. MAIN PIPELINE
# =====================================================================
def main():
    base_dir = r'C:\Users\JUAN\portfolio_notebooks'

    # Load existing cleaned master dataset
    master_path = os.path.join(base_dir, 'spain_tech_salary_master.csv')
    df = pd.read_csv(master_path, encoding='utf-8-sig')

    print(f"Master dataset loaded: {len(df)} job offers")
    print(f"Columns: {list(df.columns)}")

    title_col = 'title'
    location_col = 'location_normalized'

    # Classify each offer
    roles, exps = zip(*df[title_col].apply(classify_role_and_experience))
    df['role_category'] = roles
    df['experience_level'] = exps

    # Map locations to CCAA
    def map_location(loc):
        loc_str = str(loc).lower().strip()
        # Check direct match
        for key, val in LOCATION_TO_CCAA.items():
            if key in loc_str:
                return val
        # Try province-level: Barcelona, Madrid, etc. as keywords
        provinces_ccaa = {
            'barcelona': 'Cataluna', 'madrid': 'Madrid', 'valencia': 'Comunitat Valenciana',
            'alicante': 'Comunitat Valenciana', 'sevilla': 'Andalucia', 'malaga': 'Andalucia',
            'bilbao': 'Pais Vasco', 'zaragoza': 'Aragon', 'murcia': 'Murcia',
            'palma': 'Balears', 'tenerife': 'Canarias', 'asturias': 'Asturias',
            'navarra': 'Navarra', 'valladolid': 'Castilla y Leon', 'toledo': 'Castilla - La Mancha',
            'vigo': 'Galicia', 'coruna': 'Galicia', 'granada': 'Andalucia',
        }
        for prov, ccaa in provinces_ccaa.items():
            if prov in loc_str:
                return ccaa
        # Remote / unspecified
        if any(kw in loc_str for kw in ['remote', 'teletrabajo', 'remoto', 'home', 'online']):
            return 'Total Nacional'
        return 'Total Nacional'

    df['comunidad_autonoma'] = df[location_col].apply(map_location)

    # Estimate salaries
    df['salario_bruto_anual_est'] = df.apply(
        lambda r: estimate_salary(r['role_category'], r['experience_level'], r['comunidad_autonoma']),
        axis=1
    )

    # Add INE tech sector average as reference
    df['ine_tech_avg_2024'] = INE_TECH_AVG_2024

    # Add regional multiplier used
    df['regional_multiplier'] = df['comunidad_autonoma'].map(REGIONAL_MULTIPLIERS)

    # Add population data
    df['poblacion_ccaa_2026'] = df['comunidad_autonoma'].map(POPULATION_2026)

    # =================================================================
    # Summary Statistics
    # =================================================================
    print(f"\n{'='*60}")
    print(f"CLASSIFICATION SUMMARY")
    print(f"{'='*60}")
    print(f"\nRoles distribution:")
    print(df['role_category'].value_counts().to_string())
    print(f"\nExperience distribution:")
    print(df['experience_level'].value_counts().to_string())
    print(f"\nLocation distribution (top 10):")
    print(df['comunidad_autonoma'].value_counts().head(10).to_string())

    print(f"\n{'='*60}")
    print(f"SALARY ESTIMATES (REAL DATA)")
    print(f"{'='*60}")
    print(f"Sector J (INE 2024) reference: {INE_TECH_AVG_2024:,.2f} EUR")
    print(f"Ametic/Expansion 2025 avg: 48,900.00 EUR")
    print(f"Manfred Backend median: ~45,000.00 EUR")
    print(f"\nEstimated salary stats:")
    print(df['salario_bruto_anual_est'].describe().to_string())

    print(f"\nBy role average:")
    print(df.groupby('role_category')['salario_bruto_anual_est'].agg(['mean', 'min', 'max', 'count']).round(0).to_string())

    print(f"\nBy experience:")
    print(df.groupby('experience_level')['salario_bruto_anual_est'].agg(['mean', 'min', 'max', 'count']).round(0).to_string())

    print(f"\nBy region average:")
    print(df.groupby('comunidad_autonoma')['salario_bruto_anual_est'].agg(['mean', 'count']).round(0).sort_values('mean', ascending=False).to_string())

    # =================================================================
    # Save outputs
    # =================================================================
    output_path = os.path.join(base_dir, 'spain_tech_salaries_real.csv')
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nSaved enriched dataset ({len(df)} records) to {output_path}")

    # Also save the clean summary
    summary = df[[
        title_col, location_col, 'role_category', 'experience_level',
        'comunidad_autonoma', 'salario_bruto_anual_est', 'regional_multiplier'
    ]].copy()
    summary_path = os.path.join(base_dir, 'spain_tech_salaries_real_summary.csv')
    summary.to_csv(summary_path, index=False, encoding='utf-8-sig')
    print(f"Saved summary to {summary_path}")

    return df


if __name__ == '__main__':
    df = main()
