# -*- coding: utf-8 -*-
"""
Klausur-Referenz-Orakel (unabhaengige Zweitimplementierung des Datenkerns).

Zweck: Differential Testing gegen das JS-Tool (klausur-rueckmeldung). Das Orakel
implementiert die KORREKTE Logik direkt aus der Spec (KMK-NP-Tabelle, FQ-Abzug,
LRS-Notenschutz, BE = Summe der Kriterien) — NICHT die JS-Heuristiken. Jede
Divergenz zwischen Orakel und Tool auf echten Dateien ist ein Bug (in einem von beiden).

Reine stdlib (zipfile + re). Schreibt oracle-result.json fuer den Browser-Differential-Lauf.
"""
import zipfile, re, sys, glob, os, json
sys.stdout.reconfigure(encoding='utf-8')

# ----- minimaler xlsx-Leser -----
def _shared_strings(z):
    sst = []
    if 'xl/sharedStrings.xml' in z.namelist():
        s = z.read('xl/sharedStrings.xml').decode('utf-8', 'ignore')
        for si in re.findall(r'<si>(.*?)</si>', s, re.S):
            txt = ''.join(re.findall(r'<t[^>]*>(.*?)</t>', si, re.S))
            for a, b in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")]:
                txt = txt.replace(a, b)
            sst.append(txt)
    return sst

def _sheet_target(z, name):
    wb = z.read('xl/workbook.xml').decode('utf-8', 'ignore')
    rels = z.read('xl/_rels/workbook.xml.rels').decode('utf-8', 'ignore')
    rid = None
    for m in re.finditer(r'<sheet[^>]*?name="([^"]+)"[^>]*?r:id="([^"]+)"', wb):
        if m.group(1) == name:
            rid = m.group(2); break
    tgt = None
    if rid:
        for m in re.finditer(r'<Relationship[^>]*?Id="([^"]+)"[^>]*?Target="([^"]+)"', rels):
            if m.group(1) == rid:
                tgt = m.group(2); break
    if not tgt:
        return None
    if not tgt.startswith('xl/'):
        tgt = 'xl/' + tgt.lstrip('/')
    return tgt

def read_sheet(path, name):
    """Gibt cells[(col,row)] = (value, formula_or_None) zurueck — Wert UND Formel,
    damit leere Formel-Caches (wie beim Tool) ueber die Formel rekonstruierbar sind."""
    z = zipfile.ZipFile(path)
    sst = _shared_strings(z)
    tgt = _sheet_target(z, name)
    if tgt is None:
        return None
    xml = z.read(tgt).decode('utf-8', 'ignore')
    cells = {}
    for cm in re.finditer(r'<c r="([A-Z]+)(\d+)"([^>]*)>(.*?)</c>', xml, re.S):
        col, row, attrs, inner = cm.group(1), int(cm.group(2)), cm.group(3), cm.group(4)
        t = re.search(r't="([^"]+)"', attrs); t = t.group(1) if t else None
        vm = re.search(r'<v>(.*?)</v>', inner, re.S)
        fm = re.search(r'<f[^>]*>(.*?)</f>', inner, re.S)
        val = vm.group(1) if vm else ''
        formula = fm.group(1) if fm else None
        if t == 's' and val != '':
            try: val = sst[int(val)]
            except: pass
        cells[(col, row)] = (val, formula)
    return cells

def cval(cells, c, r):
    x = cells.get((c, r)); return x[0] if x else ''
def cform(cells, c, r):
    x = cells.get((c, r)); return x[1] if x else None

def decode_fq(formula):
    """FQ-Formel ist Fehler*100/Woerter, in der Datei konstant-gefaltet als 'num/den'.
    fq = num/den (= der gesuchte Fehlerquotient). Rekonstruiert FQ trotz leerem Cache."""
    if not formula: return None
    f = str(formula).replace('=', '').strip()
    m = re.match(r'^\(?\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*\)?$', f)
    if not m: return None
    num, den = float(m.group(1)), float(m.group(2))
    return (num / den) if den else None

def num(v):
    try:
        if str(v).strip() == '': return None
        return float(v)
    except: return None

# ----- KORREKTE Spec -----
NP_TABLE = [(95,15),(90,14),(85,13),(80,12),(75,11),(70,10),(65,9),(60,8),
            (55,7),(50,6),(45,5),(40,4),(33,3),(27,2),(20,1),(0,0)]
def grade_for_percent(p):
    for thr, npv in NP_TABLE:
        if p >= thr: return npv
    return 0

def meta_maxbe(path):
    cells = read_sheet(path, '_Meta')
    if not cells: return None
    maxrow = max((r for (c, r) in cells), default=0)
    for r in range(1, maxrow + 1):
        if str(cval(cells, 'A', r)).strip() == 'max_gesamt':
            return num(cval(cells, 'B', r))
    return None

def oracle(path):
    cells = read_sheet(path, 'Bewertungen')
    if not cells:
        return {'error': 'kein Bewertungen-Blatt'}
    maxrow = max(r for (c, r) in cells)
    headers = {str(val).strip(): c for (c, r), (val, formula) in cells.items() if r == 1}
    name_col = headers.get('Nachname_voll')
    na_col   = headers.get('Nachteilsausgleich')
    fq_col   = headers.get('FQ')
    np_col   = headers.get('Notenpunkte')
    crit_cols = [c for h, c in headers.items() if re.match(r'^\d+\s+\S', h)]   # "1 Einleitung" etc.
    maxbe = meta_maxbe(path) or 100.0
    students = []
    for r in range(2, maxrow + 1):
        name = str(cval(cells, name_col, r)).strip() if name_col else ''
        if not name:
            continue   # Schuelerzeile = hat einen Namen. Korrekt, keine Heuristik.
        has_crit = any(num(cval(cells, c, r)) is not None for c in crit_cols)
        be = sum((num(cval(cells, c, r)) or 0) for c in crit_cols)
        lrs = bool(str(cval(cells, na_col, r)).strip()) if na_col else False
        fq  = num(cval(cells, fq_col, r)) if fq_col else None
        if fq is None and fq_col:                      # leerer Cache -> FQ aus der Formel rekonstruieren
            fq = decode_fq(cform(cells, fq_col, r))
        np_stored = num(cval(cells, np_col, r)) if np_col else None
        pct = (be / maxbe * 100.0) if maxbe else 0.0
        base = grade_for_percent(pct)
        ded = 0
        if not lrs and fq is not None:
            if fq >= 6: ded = 2
            elif fq >= 3: ded = 1
        np_comp = max(0, base - ded) if has_crit else None
        students.append({'name': name, 'be': round(be, 2), 'lrs': lrs,
                         'fq': (round(fq, 3) if fq is not None else None),
                         'np_stored': (int(np_stored) if np_stored is not None else None),
                         'np_computed': np_comp, 'pct': round(pct, 1)})
    return {'maxbe': maxbe, 'count': len(students), 'students': students}

# ----- Lauf: Pfade/Ordner als Argumente, sonst Default Downloads -----
if len(sys.argv) > 1:
    files = []
    for a in sys.argv[1:]:
        files += sorted(glob.glob(os.path.join(a, '*.xlsx'))) if os.path.isdir(a) else [a]
else:
    files = sorted(glob.glob(r'C:\Users\Jaro\Downloads\Klausur*.xlsx'))
out = {}
for f in files:
    base = os.path.basename(f)
    res = oracle(f)
    out[base] = res
    print("=" * 80); print("DATEI:", base, "| maxBE:", res.get('maxbe'), "| Schueler:", res.get('count'))
    for s in res.get('students', []):
        flag = ''
        if s['np_computed'] is not None and s['np_stored'] is not None and s['np_computed'] != s['np_stored']:
            flag = '  <-- computed != stored!'
        graded = s['be'] != 0 or s['np_stored'] is not None
        if graded:
            print(f"  {s['name']:<6} BE={s['be']:<7} {s['pct']:>5}% LRS={str(s['lrs']):<5} FQ={s['fq']} | NP stored={s['np_stored']} computed={s['np_computed']}{flag}")

with open('oracle-result.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False)
print("\noracle-result.json geschrieben (optional fuer Browser-Differential).")
