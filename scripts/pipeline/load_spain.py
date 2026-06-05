"""Carga datos salariales de España (scraped y oficiales)."""
import pandas as pd
import numpy as np
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ESP_DIR = BASE_DIR / 'data' / 'espana'


def load_spain() -> pd.DataFrame:
    # 1. Scraped salaries unificado
    scraped_path = ESP_DIR / 'spain_tech_salaries_scraped.csv'
    dfs = []
    if scraped_path.exists():
        df_s = pd.read_csv(scraped_path, encoding='utf-8-sig')
        for _, row in df_s.iterrows():
            r = _parse_spain_row(row)
            if r:
                dfs.append(r)
        print(f'  [Spain] {len(dfs)} registros de scraped')

    # 2. Glassdoor individual
    gd_path = ESP_DIR / 'glassdoor_salaries_2026.csv'
    if gd_path.exists():
        df_g = pd.read_csv(gd_path, encoding='utf-8-sig')
        for _, row in df_g.iterrows():
            r = _parse_spain_row(row)
            if r:
                dfs.append(r)
        print(f'  [Spain] {len([r for r in dfs if r["source"]=="Glassdoor"])} de Glassdoor')

    # 3. Job offers with salary info
    ofertas_path = ESP_DIR / 'ofertas_tech_spain.csv'
    if ofertas_path.exists():
        df_o = pd.read_csv(ofertas_path, encoding='utf-8-sig')
        for _, row in df_o.iterrows():
            sal_str = str(row.get('salario', '') or '')
            if sal_str and sal_str.strip():
                role_norm = _map_role_spain(str(row.get('titulo', '') or ''))
                sal = _extract_salary_eur(sal_str)
                if sal:
                    dfs.append({
                        'source': str(row.get('fuente', 'Spain Jobs')),
                        'source_type': 'scraper',
                        'country': 'ES',
                        'country_name': 'Spain',
                        'region': 'Europe',
                        'year': 2025,
                        'job_title': str(row.get('titulo', '') or ''),
                        'role_category': role_norm,
                        'experience_level': 'Mid',
                        'employment_type': 'Full-time',
                        'salary_local': sal,
                        'currency': 'EUR',
                        'salary_usd': sal * 1.08,
                        'remote_ratio': 0,
                        'company_size': 'Medium',
                        'company_location': str(row.get('ubicacion', '') or ''),
                        'latitude': 40.4168,
                        'longitude': -3.7038,
                    })

    # 4. INE sector J (oficial)
    ine_path = ESP_DIR / 'ine_tech_salaries_clean.csv'
    if ine_path.exists():
        df_i = pd.read_csv(ine_path, encoding='utf-8-sig')
        for _, row in df_i.iterrows():
            sal_str = str(row.get('rango_salarial', '') or '')
            sal = _extract_salary_eur(sal_str)
            if sal:
                dfs.append({
                    'source': 'INE',
                    'source_type': 'official',
                    'country': 'ES',
                    'country_name': 'Spain',
                    'region': 'Europe',
                    'year': _extract_ine_year(str(row.get('experiencia', '') or '')),
                    'job_title': f"Sector J - {str(row.get('rol', row.get('experiencia', '')) or '')}",
                    'role_category': 'Tech Sector (INE)',
                    'experience_level': 'All',
                    'employment_type': 'Full-time',
                    'salary_local': sal,
                    'currency': 'EUR',
                    'salary_usd': sal * 1.08,
                    'remote_ratio': 0,
                    'company_size': 'Large',
                    'company_location': 'Spain',
                    'latitude': 40.4168,
                    'longitude': -3.7038,
                })
        print(f'  [Spain] {len([r for r in dfs if r["source"]=="INE"])} registros INE oficial')

    if not dfs:
        print('  [Spain] Sin datos')
        return pd.DataFrame()

    result = pd.DataFrame(dfs)
    result = result.drop_duplicates(subset=['source', 'job_title', 'experience_level', 'salary_local'])
    print(f'  [Spain] Total: {len(result)} registros unificados')
    return result


def _parse_spain_row(row) -> dict | None:
    fuente = str(row.get('fuente', '') or '')
    rol = str(row.get('rol', '') or '')
    exp = str(row.get('experiencia', '') or '')
    sal_str = str(row.get('rango_salarial', '') or '')
    pais = str(row.get('pais', 'ES') or 'ES')

    role_norm = _map_role_spain(rol)
    exp_norm = _map_experience_spain(exp)

    # Extract salary from range like "30-40K", "41-50K", "42741.94 EUR"
    sal = _extract_salary_eur(sal_str)
    if not sal:
        return None

    source_type = 'scraper'
    if 'ine' in fuente.lower():
        source_type = 'official'

    return {
        'source': fuente if fuente else 'Spain Unknown',
        'source_type': source_type,
        'country': 'ES',
        'country_name': 'Spain',
        'region': 'Europe',
        'year': 2026,
        'job_title': rol,
        'role_category': role_norm,
        'experience_level': exp_norm,
        'employment_type': 'Full-time',
        'salary_local': sal,
        'currency': 'EUR',
        'salary_usd': round(sal * 1.08, 2),
        'remote_ratio': 0,
        'company_size': 'Medium',
        'company_location': pais if pais != pais else 'Spain',
        'latitude': 40.4168,
        'longitude': -3.7038,
    }


def _map_role_spain(title: str) -> str:
    tl = title.lower().strip()
    # Spain-specific mappings
    if 'data scientist' in tl or 'cientifico' in tl:
        return 'Data Scientist'
    if 'data engineer' in tl or 'ingeniero datos' in tl:
        return 'Data Engineer'
    if 'data analyst' in tl or 'analista' in tl:
        return 'Data Analyst'
    if 'machine learning' in tl or 'ml' in tl:
        return 'Machine Learning Engineer'
    if 'backend' in tl or 'back-end' in tl:
        return 'Backend Engineer'
    if 'frontend' in tl or 'front-end' in tl:
        return 'Frontend Engineer'
    if 'fullstack' in tl or 'full-stack' in tl:
        return 'Fullstack Engineer'
    if 'devops' in tl:
        return 'DevOps Engineer'
    if 'mobile' in tl or 'android' in tl or 'ios' in tl or 'kotlin' in tl or 'swift' in tl:
        return 'Mobile Engineer'
    if 'qa' in tl or 'tester' in tl or 'quality' in tl:
        return 'QA Engineer'
    if 'sysadmin' in tl or 'sistemas' in tl or 'administrador' in tl:
        return 'SysAdmin'
    if 'security' in tl or 'seguridad' in tl or 'ciberseguridad' in tl:
        return 'Security Engineer'
    if 'cloud' in tl or 'aws' in tl or 'azure' in tl or 'gcp' in tl:
        return 'Cloud Engineer'
    if 'data' in tl:
        return 'Data General'
    if 'sector' in tl:
        return 'Tech Sector (INE)'
    return 'Other Tech'


def _map_experience_spain(exp: str) -> str:
    exp_lower = exp.lower().strip()
    if '<2' in exp_lower or 'entry' in exp_lower or 'junior' in exp_lower:
        return 'Entry'
    if '2-5' in exp_lower or 'mid' in exp_lower:
        return 'Mid'
    if '5-10' in exp_lower or 'senior' in exp_lower:
        return 'Senior'
    if '10' in exp_lower or 'lead' in exp_lower or 'director' in exp_lower:
        return 'Executive'
    if exp_lower.isdigit() and 2008 <= int(exp_lower) <= 2024:
        return 'All'
    return 'Mid'


def _extract_salary_eur(s: str) -> float | None:
    s = s.replace('\u20ac', 'EUR').replace('\u2013', '-').replace('\u2014', '-')
    s = s.strip()

    # "42741.94 EUR" or "45.000 EUR"
    m = re.search(r'([\d.,]+)\s*EUR', s)
    if m:
        val = m.group(1).replace('.', '').replace(',', '.')
        try:
            return float(val)
        except:
            pass

    # "30-40K" or "30K-40K" or "41-50K"
    m = re.search(r'(\d+)\s*[-Kk]+\s*(\d+)\s*K?', s)
    if m:
        low, high = int(m.group(1)), int(m.group(2))
        return (low + high) / 2 * 1000

    # "25K" or "30K"
    m = re.search(r'(\d+)\s*K', s)
    if m:
        return int(m.group(1)) * 1000

    # Plain number
    m = re.search(r'(\d+)', s)
    if m:
        try:
            return float(m.group(1))
        except:
            pass

    return None


def _extract_ine_year(exp: str) -> int:
    try:
        return int(exp.strip())
    except:
        return 2024


if __name__ == '__main__':
    df = load_spain()
    if not df.empty:
        print(f'\nSpain: {len(df)} registros')
        print(f'Fuentes: {df["source"].value_counts().to_dict()}')
        print(f'Roles: {df["role_category"].value_counts().head(10).to_dict()}')
