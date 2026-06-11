"""
normalize_titles.py — Job title normalization and role categorization.

Normalizes 1,000+ unique job titles into ~15 standard role categories
with seniority levels. Roles below threshold grouped as 'Other Data'.
"""
import re
import pandas as pd
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent

SENIORITY_KEYWORDS = {
    'vp': 'VP',
    'vice president': 'VP',
    'svp': 'VP',
    'director': 'Director',
    'head of': 'Director',
    'principal': 'Principal',
    'staff': 'Staff',
    'lead': 'Lead',
    'senior': 'Senior',
    'sr.': 'Senior',
    'sr ': 'Senior',
    'manager': 'Manager',
    'managing': 'Manager',
    'mid': 'Mid',
    'intermediate': 'Mid',
    'ii': 'Mid',
    'iii': 'Senior',
    'junior': 'Junior',
    'jr.': 'Junior',
    'jr ': 'Junior',
    'entry': 'Junior',
    'trainee': 'Junior',
    'intern': 'Intern',
    'internship': 'Intern',
}

SENIORITY_ORDER = ['Intern', 'Junior', 'Mid', 'Senior', 'Lead', 'Manager',
                   'Staff', 'Principal', 'Director', 'VP']

ROLE_KEYWORDS = [
    (['data scientist', 'data science', 'decision science'], 'Data Scientist'),
    (['data engineer', 'data engineering', 'big data engineer', 'bi data engineer'], 'Data Engineer'),
    (['data analyst', 'data analytics', 'analytics engineer', 'data analyst intern'], 'Data Analyst'),
    (['machine learning', 'ml engineer', 'ml ops', 'mlops', 'deep learning'], 'ML Engineer'),
    (['ai engineer', 'ai scientist', 'ai research', 'generative ai', 'gen ai', 'llm'], 'AI Engineer'),
    (['business intelligence', 'bi developer', 'bi engineer', 'bi analyst'], 'BI Analyst'),
    (['data architect', 'data architecture', 'data modeler'], 'Data Architect'),
    (['research scientist', 'applied scientist', 'research engineer'], 'Research Scientist'),
    (['computer vision', 'cv engineer'], 'Computer Vision Engineer'),
    (['nlp', 'natural language'], 'NLP Engineer'),
    (['data manager', 'data science manager', 'data engineering manager', 'head of data'], 'Data Manager'),
    (['analytics manager', 'analytics director'], 'Analytics Manager'),
    (['backend', 'back-end', 'back end'], 'Backend Engineer'),
    (['frontend', 'front-end', 'front end', 'ui engineer'], 'Frontend Engineer'),
    (['fullstack', 'full-stack', 'full stack'], 'Fullstack Engineer'),
    (['devops', 'dev ops', 'sre', 'site reliability'], 'DevOps Engineer'),
    (['cloud', 'aws', 'azure', 'gcp', 'cloud engineer'], 'Cloud Engineer'),
    (['security', 'cyber', 'infosec'], 'Security Engineer'),
    (['mobile', 'ios', 'android', 'kotlin', 'swift'], 'Mobile Engineer'),
    (['qa', 'quality assurance', 'tester', 'test engineer'], 'QA Engineer'),
    (['product manager', 'product data', 'technical product manager'], 'Product Manager'),
    (['salesforce', 'crm analyst', 'crm data'], 'CRM Analyst'),
    (['marketing', 'marketing analytics'], 'Marketing Analyst'),
    (['financial', 'finance data', 'risk analyst', 'risk data'], 'Financial Analyst'),
    (['supply chain', 'logistics', 'operations'], 'Supply Chain Analyst'),
    (['healthcare', 'clinical', 'health data', 'bioinformatics'], 'Healthcare Data Specialist'),
]

SENIORITY_ROLE_OVERLAP = {
    'data science manager': ('Data Scientist', 'Manager'),
    'data engineering manager': ('Data Engineer', 'Manager'),
    'analytics manager': ('Data Analyst', 'Manager'),
    'head of data': ('Data Manager', 'Director'),
    'head of data science': ('Data Scientist', 'Director'),
    'vp data': ('Data Manager', 'VP'),
    'director of analytics': ('Data Analyst', 'Director'),
    'director of data': ('Data Manager', 'Director'),
    'director of data science': ('Data Scientist', 'Director'),
    'director of data engineering': ('Data Engineer', 'Director'),
    'manager data engineering': ('Data Engineer', 'Manager'),
    'manager data science': ('Data Scientist', 'Manager'),
    'principal data scientist': ('Data Scientist', 'Principal'),
    'principal data engineer': ('Data Engineer', 'Principal'),
    'principal data analyst': ('Data Analyst', 'Principal'),
    'staff data scientist': ('Data Scientist', 'Staff'),
    'staff data engineer': ('Data Engineer', 'Staff'),
    'lead data scientist': ('Data Scientist', 'Lead'),
    'lead data engineer': ('Data Engineer', 'Lead'),
    'lead data analyst': ('Data Analyst', 'Lead'),
    'senior data scientist': ('Data Scientist', 'Senior'),
    'senior data engineer': ('Data Engineer', 'Senior'),
    'senior data analyst': ('Data Analyst', 'Senior'),
}


def extract_seniority(title: str) -> str:
    """Extract seniority level from title. Returns standardized level or empty string."""
    t = title.lower().strip()
    for pattern, level in sorted(SENIORITY_KEYWORDS.items(), key=lambda x: -len(x[0])):
        if pattern in t:
            return level
    return ''


def extract_role(title: str) -> str:
    """Extract standardized role category from title."""
    t = title.lower().strip()

    # Check compound (role+seniority) mappings first
    exact_variants = [
        'data science manager', 'data engineering manager', 'analytics manager',
        'head of data', 'head of data science', 'vp data', 'vp of data',
        'director of analytics', 'director of data science', 'director of data engineering',
        'principal data scientist', 'principal data engineer', 'principal data analyst',
        'staff data scientist', 'staff data engineer',
        'lead data scientist', 'lead data engineer', 'lead data analyst',
        'senior data scientist', 'senior data engineer', 'senior data analyst',
        'junior data scientist', 'junior data engineer', 'junior data analyst',
        'machine learning engineer', 'ml engineer', 'data engineer ii',
        'business intelligence', 'data architect', 'analytics engineer',
        'research scientist', 'computer vision', 'nlp engineer',
    ]
    keywords = '|'.join(exact_variants)
    # Remove seniority prefixes to get core role
    for prefix in ['senior ', 'sr. ', 'sr ', 'lead ', 'principal ', 'staff ',
                   'junior ', 'jr. ', 'jr ', 'vp ', 'vice president ',
                   'director of ', 'director ', 'manager of ', 'manager ',
                   'head of ', 'intern ', 'internship ']:
        if t.startswith(prefix):
            t = t[len(prefix):]

    # Check role keywords
    for patterns, category in ROLE_KEYWORDS:
        for p in patterns:
            if p in t:
                return category

    # Check generic data-related terms
    data_terms = ['data', 'analytics', 'analyst', 'analytical', 'insights', 'reporting']
    if any(term in t for term in data_terms):
        if 'data' in t or 'analytics' in t:
            return 'Data General'
        return 'Analytics General'

    # Tech fallback
    tech_terms = ['engineer', 'developer', 'software', 'architect', 'platform',
                  'infrastructure', 'technical', 'solutions', 'consultant']
    if any(term in t for term in tech_terms):
        return 'Tech General'

    return 'Other'


def normalize_title(title: str) -> dict:
    """
    Normalize a raw job title into standardized role + seniority.
    
    Returns:
        dict with 'role', 'seniority', 'original'
    """
    t = str(title).lower().strip()
    
    # Check compound mappings first (longest key first to avoid substring collisions)
    for key, (role, seniority) in sorted(
        SENIORITY_ROLE_OVERLAP.items(), key=lambda x: -len(x[0])
    ):
        if key in t:
            return {'role': role, 'seniority': seniority, 'original': title}
    
    role = extract_role(title)
    seniority = extract_seniority(title)
    
    return {'role': role, 'seniority': seniority, 'original': title}


def build_role_threshold_map(titles: pd.Series, min_count: int = 5) -> dict:
    """
    Build a mapping of original titles -> normalized role.
    Roles with fewer than min_count occurrences are grouped as 'Other'.
    
    Returns dict: {original_title: normalized_role}
    """
    normalized = titles.apply(lambda t: normalize_title(t)['role'])
    counts = normalized.value_counts()
    
    threshold_roles = set(counts[counts >= min_count].index)
    
    def map_title(t):
        role = normalize_title(t)['role']
        return role if role in threshold_roles else 'Other Data'
    
    return {t: map_title(t) for t in titles.unique()}


def apply_normalization(df: pd.DataFrame, title_col: str = 'title',
                        min_count: int = 5) -> pd.DataFrame:
    """Apply title normalization to a dataframe. Adds role_normalized and seniority columns."""
    df = df.copy()
    mapping = build_role_threshold_map(df[title_col].str.lower().str.strip(), min_count)
    
    t_lower = df[title_col].str.lower().str.strip()
    df['role_normalized'] = t_lower.map(mapping)
    
    seniority_map = {t: normalize_title(t)['seniority'] for t in t_lower.unique()}
    df['seniority'] = t_lower.map(seniority_map)
    
    return df


def main():
    path = BASE_DIR / 'data' / 'linkedin_data_roles_procesed.csv'
    if not path.exists():
        print("File not found")
        return
    
    df = pd.read_csv(path)
    print(f"Loaded: {len(df)} records, {df['title'].nunique()} unique titles")
    
    # Apply normalization with min_count=5
    df_norm = apply_normalization(df, min_count=5)
    
    print(f"\n=== ROLE DISTRIBUTION (threshold >= 5) ===")
    role_counts = df_norm['role_normalized'].value_counts()
    for role, count in role_counts.items():
        pct = count / len(df_norm) * 100
        print(f"  {role:25s} | {count:4d} ({pct:4.1f}%)")
    
    print(f"\nCaptured: {role_counts[role_counts.index != 'Other Data'].sum()} / {len(df_norm)} "
          f"({(role_counts[role_counts.index != 'Other Data'].sum()/len(df_norm))*100:.0f}%)")
    
    # Save normalized dataset
    out_path = BASE_DIR / 'data' / 'linkedin_data_normalized.csv'
    df_norm.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"\nSaved normalized dataset: {out_path}")
    
    # Print sample of "Other Data" for quality check
    other = df_norm[df_norm['role_normalized'] == 'Other Data']
    print(f"\n=== SAMPLE OF 'Other Data' ({len(other)} records) ===")
    for t in other['title'].value_counts().head(20).index:
        print(f"  {t}")


if __name__ == '__main__':
    main()
