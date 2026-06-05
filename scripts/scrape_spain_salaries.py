import csv, json, sys, os, re, time
from scrapling.fetchers import Fetcher

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'espana')
os.makedirs(OUTPUT_DIR, exist_ok=True)

MANFRED_ROLES = {
    0: 'Backend Engineer', 1: 'Frontend Engineer', 2: 'Full-Stack Engineer',
    3: 'AI Engineer', 4: 'Mobile Engineer', 5: 'QA & Testing',
    6: 'SysAdmin', 7: 'SRE/DevOps Engineer', 8: 'Data Engineer',
    9: 'Data Scientist', 10: 'Data Analyst', 11: 'MLOps Engineer',
    12: 'Data Architect', 13: 'Software Architect', 14: 'Tech Lead',
    15: 'Staff Engineer', 16: 'Engineering Manager', 17: 'VP Engineering',
    18: 'CTO / Head of Engineering', 19: 'Product Manager',
    20: 'Product Designer', 21: 'Security/Cybersecurity Engineer',
}

def fetch_manfred():
    print("[Manfred] Extrayendo guia salarial...")
    page = Fetcher.get(
        'https://www.getmanfred.com/en/blog/guia-salarial-2026-salarios-en-tecnologia-espana-manfred',
        impersonate='chrome', timeout=30000
    )
    if page.status != 200:
        print(f"  Error HTTP {page.status}")
        return []

    tables = page.css('table')
    records = []
    for idx, role in MANFRED_ROLES.items():
        if idx >= len(tables):
            continue
        for row in tables[idx].css('tr'):
            cells = [c.strip() for c in row.css('td::text, th::text').getall() if c.strip()]
            if len(cells) >= 2 and not cells[0].lower().startswith('experiencia'):
                records.append({
                    'fuente': 'Manfred 2026',
                    'rol': role,
                    'experiencia': cells[0],
                    'rango_salarial': cells[1],
                    'pais': 'Espana'
                })
    print(f"  {len(records)} registros")
    return records

def fetch_ine():
    print("[INE] Extrayendo datos oficiales...")
    ine_path = os.path.join(OUTPUT_DIR, 'ine_salaries_by_sector.csv')
    if not os.path.exists(ine_path):
        print("  No encontrado")
        return []
    records = []
    with open(ine_path, 'r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if 'informaci' in r.get('sector', '').lower():
                records.append({
                    'fuente': 'INE',
                    'rol': f"INE Sector J - {r.get('sexo', '')}",
                    'experiencia': str(r.get('year', '')),
                    'rango_salarial': f"{float(r.get('salario_bruto_anual', 0)):.2f} EUR",
                    'pais': 'Espana'
                })
    print(f"  {len(records)} registros")
    return records

def fetch_glassdoor(role_url, role_label):
    print(f"[Glassdoor] {role_label}...")
    url = f'https://www.glassdoor.es/Sueldos/{role_url}-sueldo-SRCH_KO0,14.htm'
    try:
        page = Fetcher.get(url, impersonate='chrome', timeout=30000)
        html = page.body.decode('utf-8', errors='replace')
        records = []

        # Salary ranges in "mil" format: "30 mil € - 50 mil €"
        for low, high in re.findall(r'(\d{2,3})\s*mil\s*[€]\s*(?:[–\-–]|al?)\s*(\d{2,3})\s*mil\s*[€]', html):
            records.append({
                'fuente': 'Glassdoor',
                'rol': role_label,
                'experiencia': 'rango',
                'rango_salarial': f"{low}.000-{high}.000 EUR",
                'pais': 'Espana'
            })

        # Specific salary figures
        seen = set()
        for a, b in re.findall(r'(\d{2,3})[.,](\d{3})\s*(?:€|EUR)', html):
            val = f"{a}.{b}"
            if val not in seen:
                seen.add(val)
                records.append({
                    'fuente': 'Glassdoor',
                    'rol': role_label,
                    'experiencia': 'estimacion',
                    'rango_salarial': f"{val} EUR",
                    'pais': 'Espana'
                })

        print(f"  {len(records)} registros")
        return records
    except Exception as e:
        print(f"  ERROR: {e}")
        return []

def fetch_tecnoempleo():
    print("[Tecnoempleo] Ofertas...")
    records = []
    for term in ['data', 'data+scientist', 'data+engineer']:
        try:
            page = Fetcher.get(
                f'https://www.tecnoempleo.com/ofertas-trabajo/?te={term}',
                impersonate='chrome', timeout=20000
            )
            for el in page.css('h3'):
                text = ' '.join(t.strip() for t in el.css('::text').getall() if t.strip())
                if text and len(text) > 5:
                    records.append({'fuente': 'Tecnoempleo', 'titulo': text})
            time.sleep(1)
        except:
            continue
    seen = set()
    unique = [r for r in records if not (r['titulo'] in seen or seen.add(r['titulo']))]
    print(f"  {len(unique)} ofertas")
    return unique

def fetch_ticjob():
    print("[Ticjob] Ofertas...")
    records = []
    for term in ['data', 'data+scientist', 'data+engineer', 'data+analyst']:
        try:
            page = Fetcher.get(
                f'https://ticjob.es/esp/busqueda?q={term}',
                impersonate='chrome', timeout=20000
            )
            for h in page.css('h2::text').getall():
                h = h.strip()
                if h and len(h) > 10 and 'filtros' not in h.lower():
                    records.append({'fuente': 'Ticjob', 'titulo': h})
            time.sleep(1.5)
        except:
            continue
    seen = set()
    unique = [r for r in records if not (r['titulo'] in seen or seen.add(r['titulo']))]
    print(f"  {len(unique)} ofertas")
    return unique

def save_csv(records, filename, fieldnames):
    if not records:
        print(f"  (vacio) {filename}")
        return
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(records)
    print(f"  -> {filename} ({len(records)} reg)")

if __name__ == '__main__':
    print("=" * 60)
    print("SCRAPER COMPLETO - SALARIOS TECH ESPANA")
    print("=" * 60)

    print("\n--- FASE 1: DATOS SALARIALES ---")
    m = fetch_manfred()
    ine = fetch_ine()
    gd = fetch_glassdoor('DATA-SCIENTIST', 'Data Scientist') + \
         fetch_glassdoor('DATA-ENGINEER', 'Data Engineer') + \
         fetch_glassdoor('DATA-ANALYST', 'Data Analyst')

    sh = ['fuente', 'rol', 'experiencia', 'rango_salarial', 'pais']
    save_csv(m, 'manfred_salaries_2026.csv', sh)
    save_csv(ine, 'ine_tech_salaries_clean.csv', sh)
    save_csv(gd, 'glassdoor_salaries_2026.csv', sh)
    save_csv(m + ine + gd, 'spain_tech_salaries_scraped.csv', sh)

    print("\n--- FASE 2: OFERTAS DE EMPLEO ---")
    tecno = fetch_tecnoempleo()
    tic = fetch_ticjob()
    save_csv(tecno, 'tecnoempleo_ofertas.csv', ['fuente', 'titulo'])
    save_csv(tic, 'ticjob_ofertas.csv', ['fuente', 'titulo'])

    print("\n" + "=" * 60)
    print(f"RESUMEN FINAL:")
    print(f"  Manfred:     {len(m)}")
    print(f"  INE:         {len(ine)}")
    print(f"  Glassdoor:   {len(gd)}")
    print(f"  Tecnoempleo: {len(tecno)}")
    print(f"  Ticjob:      {len(tic)}")
    print(f"  TOTAL:       {len(m + ine + gd)} registros salariales")
    print("=" * 60)
