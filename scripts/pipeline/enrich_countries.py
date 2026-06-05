"""Enriquece datos con metadatos de paises: coordenadas, region, GDP, PPP."""
import pandas as pd
import numpy as np

COUNTRY_METADATA = {
    'US': {'lat': 37.0902, 'lon': -95.7129, 'gdp_per_capita': 76399, 'ppp': 1.0, 'currency': 'USD'},
    'ES': {'lat': 40.4637, 'lon': -3.7492, 'gdp_per_capita': 34820, 'ppp': 0.72, 'currency': 'EUR'},
    'GB': {'lat': 55.3781, 'lon': -3.4360, 'gdp_per_capita': 45649, 'ppp': 0.78, 'currency': 'GBP'},
    'DE': {'lat': 51.1657, 'lon': 10.4515, 'gdp_per_capita': 49692, 'ppp': 0.76, 'currency': 'EUR'},
    'FR': {'lat': 46.6034, 'lon': 1.8883, 'gdp_per_capita': 42930, 'ppp': 0.74, 'currency': 'EUR'},
    'IT': {'lat': 41.8719, 'lon': 12.5674, 'gdp_per_capita': 36556, 'ppp': 0.71, 'currency': 'EUR'},
    'NL': {'lat': 52.1326, 'lon': 5.2913, 'gdp_per_capita': 56237, 'ppp': 0.79, 'currency': 'EUR'},
    'PT': {'lat': 39.3999, 'lon': -8.2245, 'gdp_per_capita': 26118, 'ppp': 0.65, 'currency': 'EUR'},
    'IE': {'lat': 53.1424, 'lon': -7.6921, 'gdp_per_capita': 102394, 'ppp': 0.85, 'currency': 'EUR'},
    'BE': {'lat': 50.5039, 'lon': 4.4699, 'gdp_per_capita': 47647, 'ppp': 0.77, 'currency': 'EUR'},
    'AT': {'lat': 47.5162, 'lon': 14.5501, 'gdp_per_capita': 50907, 'ppp': 0.78, 'currency': 'EUR'},
    'CH': {'lat': 46.8182, 'lon': 8.2275, 'gdp_per_capita': 87727, 'ppp': 1.02, 'currency': 'CHF'},
    'SE': {'lat': 60.1282, 'lon': 18.6435, 'gdp_per_capita': 52575, 'ppp': 0.82, 'currency': 'SEK'},
    'NO': {'lat': 60.4720, 'lon': 8.4689, 'gdp_per_capita': 74169, 'ppp': 0.88, 'currency': 'NOK'},
    'DK': {'lat': 56.2639, 'lon': 9.5018, 'gdp_per_capita': 57980, 'ppp': 0.83, 'currency': 'DKK'},
    'FI': {'lat': 61.9241, 'lon': 25.7482, 'gdp_per_capita': 49922, 'ppp': 0.80, 'currency': 'EUR'},
    'PL': {'lat': 51.9194, 'lon': 19.1451, 'gdp_per_capita': 18734, 'ppp': 0.56, 'currency': 'PLN'},
    'CZ': {'lat': 49.8175, 'lon': 15.4730, 'gdp_per_capita': 25320, 'ppp': 0.62, 'currency': 'CZK'},
    'GR': {'lat': 39.0742, 'lon': 21.8243, 'gdp_per_capita': 19971, 'ppp': 0.58, 'currency': 'EUR'},
    'HU': {'lat': 47.1625, 'lon': 19.5033, 'gdp_per_capita': 17382, 'ppp': 0.55, 'currency': 'HUF'},
    'RO': {'lat': 45.9432, 'lon': 24.9668, 'gdp_per_capita': 14862, 'ppp': 0.50, 'currency': 'RON'},
    'BG': {'lat': 42.7339, 'lon': 25.4858, 'gdp_per_capita': 12920, 'ppp': 0.47, 'currency': 'BGN'},
    'HR': {'lat': 45.1000, 'lon': 15.2000, 'gdp_per_capita': 17421, 'ppp': 0.57, 'currency': 'EUR'},
    'EE': {'lat': 58.5953, 'lon': 25.0136, 'gdp_per_capita': 23784, 'ppp': 0.61, 'currency': 'EUR'},
    'LU': {'lat': 49.8153, 'lon': 6.1296, 'gdp_per_capita': 126964, 'ppp': 0.90, 'currency': 'EUR'},
    'MT': {'lat': 35.9375, 'lon': 14.3754, 'gdp_per_capita': 31002, 'ppp': 0.68, 'currency': 'EUR'},
    'SI': {'lat': 46.1512, 'lon': 14.9955, 'gdp_per_capita': 26802, 'ppp': 0.64, 'currency': 'EUR'},
    'SK': {'lat': 48.6690, 'lon': 19.6990, 'gdp_per_capita': 19869, 'ppp': 0.57, 'currency': 'EUR'},
    'LT': {'lat': 55.1694, 'lon': 23.8813, 'gdp_per_capita': 20233, 'ppp': 0.58, 'currency': 'EUR'},
    'LV': {'lat': 56.8796, 'lon': 24.6032, 'gdp_per_capita': 17012, 'ppp': 0.53, 'currency': 'EUR'},
    'CA': {'lat': 56.1304, 'lon': -106.3468, 'gdp_per_capita': 52495, 'ppp': 0.92, 'currency': 'CAD'},
    'MX': {'lat': 23.6345, 'lon': -102.5528, 'gdp_per_capita': 9910, 'ppp': 0.39, 'currency': 'MXN'},
    'BR': {'lat': -14.2350, 'lon': -51.9253, 'gdp_per_capita': 8104, 'ppp': 0.33, 'currency': 'BRL'},
    'AR': {'lat': -38.4161, 'lon': -63.6167, 'gdp_per_capita': 12421, 'ppp': 0.35, 'currency': 'ARS'},
    'CL': {'lat': -35.6751, 'lon': -71.5430, 'gdp_per_capita': 15503, 'ppp': 0.48, 'currency': 'CLP'},
    'CO': {'lat': 4.5709, 'lon': -74.2973, 'gdp_per_capita': 6861, 'ppp': 0.31, 'currency': 'COP'},
    'PE': {'lat': -9.1900, 'lon': -75.0152, 'gdp_per_capita': 6953, 'ppp': 0.33, 'currency': 'PEN'},
    'UY': {'lat': -32.5228, 'lon': -55.7658, 'gdp_per_capita': 19865, 'ppp': 0.55, 'currency': 'UYU'},
    'EC': {'lat': -1.8312, 'lon': -78.1834, 'gdp_per_capita': 6389, 'ppp': 0.30, 'currency': 'USD'},
    'CR': {'lat': 9.7489, 'lon': -83.7534, 'gdp_per_capita': 12767, 'ppp': 0.43, 'currency': 'CRC'},
    'IN': {'lat': 20.5937, 'lon': 78.9629, 'gdp_per_capita': 2729, 'ppp': 0.21, 'currency': 'INR'},
    'CN': {'lat': 35.8617, 'lon': 104.1954, 'gdp_per_capita': 12178, 'ppp': 0.45, 'currency': 'CNY'},
    'JP': {'lat': 36.2048, 'lon': 138.2529, 'gdp_per_capita': 38633, 'ppp': 0.80, 'currency': 'JPY'},
    'SG': {'lat': 1.3521, 'lon': 103.8198, 'gdp_per_capita': 64740, 'ppp': 0.88, 'currency': 'SGD'},
    'HK': {'lat': 22.3193, 'lon': 114.1694, 'gdp_per_capita': 47500, 'ppp': 0.82, 'currency': 'HKD'},
    'KR': {'lat': 35.9078, 'lon': 127.7669, 'gdp_per_capita': 33723, 'ppp': 0.76, 'currency': 'KRW'},
    'AU': {'lat': -25.2744, 'lon': 133.7751, 'gdp_per_capita': 53715, 'ppp': 0.90, 'currency': 'AUD'},
    'NZ': {'lat': -40.9006, 'lon': 174.8860, 'gdp_per_capita': 43340, 'ppp': 0.82, 'currency': 'NZD'},
    'IL': {'lat': 31.0461, 'lon': 34.8516, 'gdp_per_capita': 51200, 'ppp': 0.85, 'currency': 'ILS'},
    'AE': {'lat': 23.4241, 'lon': 53.8478, 'gdp_per_capita': 41350, 'ppp': 0.78, 'currency': 'AED'},
    'NG': {'lat': 9.0820, 'lon': 8.6753, 'gdp_per_capita': 2486, 'ppp': 0.18, 'currency': 'NGN'},
    'KE': {'lat': -0.0236, 'lon': 37.9062, 'gdp_per_capita': 2126, 'ppp': 0.17, 'currency': 'KES'},
    'ZA': {'lat': -30.5595, 'lon': 22.9375, 'gdp_per_capita': 6134, 'ppp': 0.32, 'currency': 'ZAR'},
    'TR': {'lat': 38.9637, 'lon': 35.2433, 'gdp_per_capita': 13333, 'ppp': 0.38, 'currency': 'TRY'},
    'RU': {'lat': 61.5240, 'lon': 105.3188, 'gdp_per_capita': 11399, 'ppp': 0.40, 'currency': 'RUB'},
    'PK': {'lat': 30.3753, 'lon': 69.3451, 'gdp_per_capita': 1560, 'ppp': 0.15, 'currency': 'PKR'},
    'PH': {'lat': 12.8797, 'lon': 121.7740, 'gdp_per_capita': 2785, 'ppp': 0.19, 'currency': 'PHP'},
    'VN': {'lat': 14.0583, 'lon': 108.2772, 'gdp_per_capita': 1876, 'ppp': 0.17, 'currency': 'VND'},
    'MY': {'lat': 4.2105, 'lon': 101.9758, 'gdp_per_capita': 11234, 'ppp': 0.42, 'currency': 'MYR'},
}


def enrich_countries(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ['latitude', 'longitude', 'gdp_per_capita', 'ppp_factor', 'salary_ppp']:
        if col not in df.columns:
            df[col] = None

    for code, meta in COUNTRY_METADATA.items():
        mask = df['country'] == code
        if mask.any():
            df.loc[mask, 'latitude'] = df.loc[mask, 'latitude'].fillna(meta['lat'])
            df.loc[mask, 'longitude'] = df.loc[mask, 'longitude'].fillna(meta['lon'])
            df.loc[mask, 'gdp_per_capita'] = meta['gdp_per_capita']
            df.loc[mask, 'ppp_factor'] = meta['ppp']
            df.loc[mask, 'salary_ppp'] = (
                df.loc[mask, 'salary_usd'] / meta['ppp']
                if meta['ppp'] > 0 else df.loc[mask, 'salary_usd']
            )

    missing = df['latitude'].isna()
    if missing.any():
        print(f'  [Enrich] {missing.sum()} registros sin coordenadas')
        df.loc[missing, 'latitude'] = 20.0
        df.loc[missing, 'longitude'] = 0.0
        df.loc[missing, 'gdp_per_capita'] = 20000
        df.loc[missing, 'ppp_factor'] = 0.5
        df.loc[missing, 'salary_ppp'] = df.loc[missing, 'salary_usd'] / 0.5

    df['salary_ppp'] = df['salary_ppp'].round(2)
    df['gdp_per_capita'] = df['gdp_per_capita'].fillna(20000)
    df['ppp_factor'] = df['ppp_factor'].fillna(0.5)

    print(f'  [Enrich] Coordenadas: {df["latitude"].notna().sum()} registros')
    print(f'  [Enrich] PPP ajustados: {df["salary_ppp"].notna().sum()} registros')
    return df
