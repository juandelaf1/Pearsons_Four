import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from normalize_titles import (
    normalize_title,
    extract_seniority,
    extract_role,
    build_role_threshold_map,
    apply_normalization,
    SENIORITY_ORDER,
)


class TestExtractSeniority:
    def test_senior_detected(self):
        assert extract_seniority('Senior Data Scientist') == 'Senior'

    def test_junior_detected(self):
        assert extract_seniority('Junior Data Analyst') == 'Junior'

    def test_manager_detected(self):
        assert extract_seniority('Data Science Manager') == 'Manager'

    def test_intern_detected(self):
        assert extract_seniority('Data Analyst Intern') == 'Intern'

    def test_vp_detected(self):
        assert extract_seniority('VP of Data') == 'VP'

    def test_empty_for_no_seniority(self):
        assert extract_seniority('Data Scientist') == ''

    def test_sr_abbreviation(self):
        assert extract_seniority('Sr. Data Engineer') == 'Senior'

    def test_sr_space(self):
        assert extract_seniority('Sr Data Engineer') == 'Senior'

    def test_jr_abbreviation(self):
        assert extract_seniority('Jr. Analyst') == 'Junior'

    def test_principal_detected(self):
        assert extract_seniority('Principal Data Scientist') == 'Principal'

    def test_director_detected(self):
        assert extract_seniority('Director of Analytics') == 'Director'

    def test_lead_detected(self):
        assert extract_seniority('Lead Data Engineer') == 'Lead'

    def test_staff_detected(self):
        assert extract_seniority('Staff Data Scientist') == 'Staff'

    def test_head_of_detected(self):
        assert extract_seniority('Head of Data') == 'Director'

    def test_mid_detected(self):
        assert extract_seniority('Mid Level Data Analyst') == 'Mid'

    def test_entry_level(self):
        assert extract_seniority('Entry Level Analyst') == 'Junior'

    def test_trainee(self):
        assert extract_seniority('Trainee Data Analyst') == 'Junior'

    def test_svp(self):
        assert extract_seniority('SVP Data') == 'VP'

    def test_managing_detected(self):
        assert extract_seniority('Managing Director Data') == 'Director'

    def test_intermediate(self):
        assert extract_seniority('Intermediate Data Analyst') == 'Mid'

    def test_ii_roman(self):
        assert extract_seniority('Data Analyst II') == 'Mid'

    def test_iii_roman(self):
        assert extract_seniority('Data Analyst III') == 'Senior'


class TestExtractRole:
    def test_data_scientist(self):
        assert extract_role('Data Scientist') == 'Data Scientist'

    def test_data_engineer(self):
        assert extract_role('Data Engineer') == 'Data Engineer'

    def test_data_analyst(self):
        assert extract_role('Data Analyst') == 'Data Analyst'

    def test_ml_engineer(self):
        assert extract_role('Machine Learning Engineer') == 'ML Engineer'

    def test_ml_engineer_short(self):
        assert extract_role('ML Engineer') == 'ML Engineer'

    def test_ai_engineer(self):
        assert extract_role('AI Engineer') == 'AI Engineer'

    def test_bi_analyst(self):
        assert extract_role('BI Analyst') == 'BI Analyst'

    def test_data_architect(self):
        assert extract_role('Data Architect') == 'Data Architect'

    def test_research_scientist(self):
        assert extract_role('Research Scientist') == 'Research Scientist'

    def test_cv_engineer(self):
        assert extract_role('Computer Vision Engineer') == 'Computer Vision Engineer'

    def test_nlp_engineer(self):
        assert extract_role('NLP Engineer') == 'NLP Engineer'

    def test_analytics_engineer(self):
        assert extract_role('Analytics Engineer') == 'Data Analyst'

    def test_fullstack_engineer(self):
        assert extract_role('Fullstack Engineer') == 'Fullstack Engineer'

    def test_devops_engineer(self):
        assert extract_role('DevOps Engineer') == 'DevOps Engineer'

    def test_cloud_engineer(self):
        assert extract_role('Cloud Engineer') == 'Cloud Engineer'

    def test_security_engineer(self):
        assert extract_role('Security Engineer') == 'Security Engineer'

    def test_mobile_engineer(self):
        assert extract_role('Mobile Engineer') == 'Mobile Engineer'

    def test_qa_engineer(self):
        assert extract_role('QA Engineer') == 'QA Engineer'

    def test_product_manager(self):
        assert extract_role('Product Manager') == 'Product Manager'

    def test_crm_analyst(self):
        assert extract_role('CRM Analyst') == 'CRM Analyst'

    def test_marketing_analyst(self):
        assert extract_role('Marketing Analyst') == 'Marketing Analyst'

    def test_financial_analyst(self):
        assert extract_role('Financial Analyst') == 'Financial Analyst'

    def test_generic_data_role(self):
        assert extract_role('Data Generalist') == 'Data General'

    def test_generic_tech_role(self):
        assert extract_role('Software Engineer') == 'Tech General'

    def test_unknown_role(self):
        assert extract_role('Barista') == 'Other'


class TestNormalizeTitle:
    def test_simple_case(self):
        result = normalize_title('Data Scientist')
        assert result['role'] == 'Data Scientist'
        assert result['seniority'] == ''

    def test_with_seniority(self):
        result = normalize_title('Senior Data Scientist')
        assert result['role'] == 'Data Scientist'
        assert result['seniority'] == 'Senior'

    def test_compound_mapping_manager(self):
        result = normalize_title('Data Science Manager')
        assert result['role'] == 'Data Scientist'
        assert result['seniority'] == 'Manager'

    def test_compound_mapping_director(self):
        result = normalize_title('Director of Data Science')
        assert result['role'] == 'Data Scientist'
        assert result['seniority'] == 'Director'
        assert result['seniority'] == 'Director'

    def test_compound_mapping_vp(self):
        result = normalize_title('VP Data')
        assert result['role'] == 'Data Manager'
        assert result['seniority'] == 'VP'

    def test_compound_mapping_head_of(self):
        result = normalize_title('Head of Data')
        assert result['role'] == 'Data Manager'
        assert result['seniority'] == 'Director'

    def test_compound_mapping_principal(self):
        result = normalize_title('Principal Data Scientist')
        assert result['role'] == 'Data Scientist'
        assert result['seniority'] == 'Principal'

    def test_compound_mapping_staff(self):
        result = normalize_title('Staff Data Engineer')
        assert result['role'] == 'Data Engineer'
        assert result['seniority'] == 'Staff'

    def test_compound_mapping_lead(self):
        result = normalize_title('Lead Data Analyst')
        assert result['role'] == 'Data Analyst'
        assert result['seniority'] == 'Lead'

    def test_intern_title(self):
        result = normalize_title('Data Analyst Intern')
        assert result['role'] == 'Data Analyst'
        assert result['seniority'] == 'Intern'

    def test_fullstack_developer(self):
        result = normalize_title('Full Stack Developer')
        assert result['role'] == 'Fullstack Engineer'

    def test_returns_original(self):
        result = normalize_title('Custom Unusual Role')
        assert result['original'] == 'Custom Unusual Role'

    def test_case_insensitive(self):
        result = normalize_title('senior data scientist')
        assert result['role'] == 'Data Scientist'
        assert result['seniority'] == 'Senior'

    def test_machine_learning_scientist(self):
        result = normalize_title('Machine Learning Scientist')
        assert result['role'] == 'ML Engineer'


class TestBuildRoleThresholdMap:
    def test_basic_mapping(self):
        titles = pd.Series(['Data Scientist', 'Data Engineer', 'Data Analyst'])
        mapping = build_role_threshold_map(titles, min_count=1)
        assert mapping['Data Scientist'] == 'Data Scientist'
        assert mapping['Data Engineer'] == 'Data Engineer'
        assert mapping['Data Analyst'] == 'Data Analyst'

    def test_threshold_groups_rare_titles(self):
        titles = pd.Series([
            'Data Scientist', 'Data Scientist', 'Data Scientist',
            'Data Engineer', 'Data Engineer',
            'Unusual One',
        ])
        mapping = build_role_threshold_map(titles, min_count=3)
        assert mapping['Data Scientist'] == 'Data Scientist'
        assert mapping['Unusual One'] == 'Other Data'

    def test_other_data_for_below_threshold(self):
        titles = pd.Series(['Barista', 'Chef', 'Driver'])
        mapping = build_role_threshold_map(titles, min_count=5)
        for _, role in mapping.items():
            assert role == 'Other Data'


class TestApplyNormalization:
    def test_adds_columns(self):
        df = pd.DataFrame({'title': ['Data Scientist', 'Data Engineer', 'Data Analyst']})
        result = apply_normalization(df, min_count=1)
        assert 'role_normalized' in result.columns
        assert 'seniority' in result.columns
        assert len(result) == 3

    def test_does_not_mutate_original(self):
        df = pd.DataFrame({'title': ['Data Scientist']})
        original_len = len(df)
        result = apply_normalization(df)
        assert len(df) == original_len
        assert 'role_normalized' not in df.columns

    def test_seniority_extracted(self):
        df = pd.DataFrame({
            'title': ['Senior Data Scientist', 'Junior Data Analyst', 'Data Engineer']
        })
        result = apply_normalization(df, min_count=1)
        assert result['seniority'].iloc[0] == 'Senior'
        assert result['seniority'].iloc[1] == 'Junior'
        assert result['seniority'].iloc[2] == ''

    def test_role_mapped_correctly(self):
        df = pd.DataFrame({'title': ['Machine Learning Engineer', 'BI Analyst', 'Data Architect']})
        result = apply_normalization(df, min_count=1)
        assert result['role_normalized'].iloc[0] == 'ML Engineer'
        assert result['role_normalized'].iloc[1] == 'BI Analyst'
        assert result['role_normalized'].iloc[2] == 'Data Architect'

    def test_threshold_respected(self):
        df = pd.DataFrame({
            'title': ['Data Scientist', 'Data Scientist',
                      'Data Engineer', 'Rare Title']
        })
        result = apply_normalization(df, min_count=2)
        assert (result['role_normalized'] == 'Other Data').sum() >= 1
        assert (result['role_normalized'] == 'Data Scientist').sum() == 2

    def test_seniority_order_defined(self):
        assert SENIORITY_ORDER == ['Intern', 'Junior', 'Mid', 'Senior', 'Lead',
                                   'Manager', 'Staff', 'Principal', 'Director', 'VP']
