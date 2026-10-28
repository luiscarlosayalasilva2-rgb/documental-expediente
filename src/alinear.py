"""Alinea el guion (guion.txt) con la transcripción (palabras.json): cada frase del guion recibe su tiempo.

Salida: frases.json = [{'seccion', 'i', 'texto', 's', 'e'}]. Los títulos (INTRO, PARADA N — …, CIERRE) marcan secciones y no se leen.
"""
import difflib, json, re, sys, unicodedata

guion, palabras, out = sys.argv[1:4]

def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9ñ]', '', w)

NUM = {'doce': '12', 'once': '11', 'diez': '10', 'nueve': '9', 'ocho': '8', 'siete': '7', 'seis': '6', 'cinco': '5',
       'cuatro': '4', 'tres': '3', 'dos': '2', 'uno': '1'}

frases, seccion = [], 'TITULO'
for linea in open(guion, encoding='utf-8'):
    linea = linea.strip()
    if not linea:
        continue
    if re.match(r'^(INTRO|CIERRE|LLAMADO|PARADA \d+)', linea):
        seccion = linea; continue
    if seccion == 'TITULO':
        continue
    for f in re.split(r'(?<=[.!?…»])\s+(?=[«¿¡A-ZÁÉÍÓÚÑ\[])', linea.strip('[]')):
        if f.strip():
            frases.append({'seccion': seccion, 'texto': f.strip()})

g_tok, g_frase = [], []
for i, f in enumerate(frases):
    for w in f['texto'].split():
        n = norm(w)
        if n:
            g_tok.append(NUM.get(n, n)); g_frase.append(i)

T = json.load(open(palabras, encoding='utf-8'))
t_tok = [NUM.get(norm(x['w']), norm(x['w'])) for x in T]

sm = difflib.SequenceMatcher(None, g_tok, t_tok, autojunk=False)
mapa = {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        mapa[a + k] = b + k

for i, f in enumerate(frases):
    idx = [mapa[j] for j, fi in enumerate(g_frase) if fi == i and j in mapa]
    f['i'] = i
    f['s'] = T[min(idx)]['s'] if idx else None
    f['e'] = T[max(idx)]['e'] if idx else None
    f['cobertura'] = round(len(idx) / max(1, sum(1 for fi in g_frase if fi == i)), 2)

# frases sin coincidencia: interpolar entre vecinas
for i, f in enumerate(frases):
    if f['s'] is None:
        prev = next((frases[j]['e'] for j in range(i - 1, -1, -1) if frases[j]['e'] is not None), 0)
        nxt = next((frases[j]['s'] for j in range(i + 1, len(frases)) if frases[j]['s'] is not None), prev)
        f['s'], f['e'] = prev, nxt

json.dump(frases, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
baja = [f for f in frases if f['cobertura'] < 0.6]
print('frases:', len(frases), '| palabras alineadas:', len(mapa), 'de', len(g_tok), '| frases con cobertura baja:', len(baja))
for f in baja[:15]:
    print('  ', f['cobertura'], f['s'], f['texto'][:70])
secs = {}
for f in frases:
    secs.setdefault(f['seccion'], [f['s'], f['e']]); secs[f['seccion']][1] = f['e']
for k, (s, e) in secs.items():
    print(f'{s:7.1f} - {e:7.1f}  {k}')
