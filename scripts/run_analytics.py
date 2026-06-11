"""
run_analytics.py — Run SQL analytics via DuckDB on unified salary data.

Reads queries/01-05 *.sql, executes them with DuckDB,
writes result tables to data/analytics/ for dashboard consumption.

Usage:
    uv run python scripts/run_analytics.py
    uv run python scripts/run_analytics.py --rebuild    # rebuild global dataset first
"""
import duckdb
import pandas as pd
import argparse, sys, time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / 'data'
ANALYTICS_DIR = DATA_DIR / 'analytics'
QUERIES_DIR = BASE / 'queries'
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

SALARIES_SRC = DATA_DIR / 'global' / 'global_salaries_unified.csv'
FALLBACK_SRC = DATA_DIR / 'linkedin_data_normalized.csv'


def ensure_salaries_view(con: duckdb.DuckDBPyConnection, rebuild: bool = False):
    """Register the unified salaries table. Rebuild global dataset if requested."""
    if rebuild or not SALARIES_SRC.exists():
        print('Rebuilding global salaries...')
        sys.path.insert(0, str(BASE / 'scripts'))
        from load_global_salaries import build_global_dataset
        build_global_dataset()

    if SALARIES_SRC.exists():
        con.execute(f"CREATE TABLE salaries AS SELECT * FROM read_csv('{SALARIES_SRC}', auto_detect=true)")
        count = con.execute("SELECT COUNT(*) FROM salaries").fetchone()[0]
        print(f'  Table salaries: {count} rows from global dataset')
        return

    if FALLBACK_SRC.exists():
        con.execute(f"CREATE TABLE salaries AS SELECT *, NULL AS salary_ppp_usd, NULL AS country_name FROM read_csv('{FALLBACK_SRC}', auto_detect=true)")
        count = con.execute("SELECT COUNT(*) FROM salaries").fetchone()[0]
        print(f'  Table salaries: {count} rows from LinkedIn fallback')
        return

    print('  ERROR: no salary data found')
    raise FileNotFoundError('No salary CSV found')


def list_queries() -> list[dict]:
    """Return ordered list of query file paths and names."""
    files = sorted(QUERIES_DIR.glob('*.sql'))
    queries = []
    for f in files:
        name = f.stem  # e.g. "01_median_salary_by_role"
        label = name[3:].replace('_', ' ').title()
        queries.append({'path': f, 'name': name, 'label': label})
    return queries


def run_query(con: duckdb.DuckDBPyConnection, sql: str, label: str) -> pd.DataFrame:
    """Execute a SQL string and return results as DataFrame."""
    print(f'\n--- {label} ---')
    start = time.time()
    try:
        df = con.execute(sql).fetchdf()
        elapsed = time.time() - start
        print(f'  {len(df)} rows in {elapsed:.2f}s')
        return df
    except Exception as e:
        print(f'  ERROR: {e}')
        return pd.DataFrame()


def save_results(df: pd.DataFrame, name: str):
    """Save results as CSV and Markdown table."""
    csv_path = ANALYTICS_DIR / f'{name}.csv'
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  Saved: {csv_path}')

    md_path = ANALYTICS_DIR / f'{name}.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f'# {name[3:].replace("_", " ").title()}\n\n')
        if df.empty:
            f.write('*(No results)*\n')
        else:
            f.write(df.to_markdown(index=False, floatfmt=',.0f') + '\n')
    print(f'  Saved: {md_path}')


def main():
    parser = argparse.ArgumentParser(description='Run DuckDB analytics on salary data')
    parser.add_argument('--rebuild', action='store_true', help='Rebuild global dataset before running')
    args = parser.parse_args()

    con = duckdb.connect()

    print('=' * 60)
    print('PEARSONS FOUR ANALYTICS ENGINE')
    print('=' * 60)

    ensure_salaries_view(con, rebuild=args.rebuild)

    queries = list_queries()
    print(f'\nFound {len(queries)} queries in {QUERIES_DIR}')

    for q in queries:
        sql = q['path'].read_text(encoding='utf-8')
        df = run_query(con, sql, q['label'])
        if not df.empty:
            save_results(df, q['name'])
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 160)
            print(df.head(10).to_string(index=False))

    con.close()
    print(f'\n{"="*60}')
    print(f'All results saved to {ANALYTICS_DIR}')
    print(f'{"="*60}')


if __name__ == '__main__':
    main()
