import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from pipeline.enrich_countries import enrich_countries, COUNTRY_METADATA


def test_country_metadata_contains_key_countries():
    assert 'US' in COUNTRY_METADATA
    assert 'ES' in COUNTRY_METADATA
    assert 'IN' in COUNTRY_METADATA


def test_enrich_countries_adds_coordinates():
    df = pd.DataFrame({
        'country': ['US', 'ES', 'XX'],
        'salary_usd': [100000, 50000, 75000],
    })
    result = enrich_countries(df)
    assert 'latitude' in result.columns
    assert 'longitude' in result.columns
    assert 'gdp_per_capita' in result.columns
    assert 'ppp_factor' in result.columns
    assert 'salary_ppp' in result.columns

    us_row = result[result['country'] == 'US'].iloc[0]
    assert us_row['latitude'] == 37.0902
    assert us_row['gdp_per_capita'] == 76399
    assert us_row['ppp_factor'] == 1.0
    assert us_row['salary_ppp'] == 100000.0

    es_row = result[result['country'] == 'ES'].iloc[0]
    assert es_row['gdp_per_capita'] == 34820
    assert es_row['ppp_factor'] == 0.72
