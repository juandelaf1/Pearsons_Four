import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from pipeline.config import UNIFIED_SCHEMA, ROLE_CATEGORIES, EXPERIENCE_MAP, REGIONS


def test_unified_schema_has_expected_fields():
    assert 'source' in UNIFIED_SCHEMA
    assert 'country' in UNIFIED_SCHEMA
    assert 'salary_usd' in UNIFIED_SCHEMA
    assert 'role_category' in UNIFIED_SCHEMA
    assert 'experience_level' in UNIFIED_SCHEMA


def test_role_categories_contains_data_roles():
    assert 'data scientist' in ROLE_CATEGORIES
    assert 'data engineer' in ROLE_CATEGORIES
    assert 'data analyst' in ROLE_CATEGORIES
    assert ROLE_CATEGORIES['data scientist'] == 'Data Scientist'


def test_experience_map_contains_key_levels():
    assert 'en' in EXPERIENCE_MAP
    assert 'senior' in EXPERIENCE_MAP
    assert EXPERIENCE_MAP['en'] == 'Entry'
    assert EXPERIENCE_MAP['senior'] == 'Senior'


def test_regions_contains_major_countries():
    assert REGIONS['US'] == 'North America'
    assert REGIONS['ES'] == 'Europe'
    assert REGIONS['IN'] == 'Asia'
    assert REGIONS['AU'] == 'Oceania'
    assert REGIONS['BR'] == 'LATAM'
    assert REGIONS['NG'] == 'Africa'
