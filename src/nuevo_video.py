"""Plantilla automática para un video NUEVO con la misma edición.

Lee el guion alineado y arma el ESQUELETO del EDL con toda la estructura del video aprobado.
La IA (o Luis) solo rellena los huecos: las fotos y videos marcados PENDIENTE y los textos marcados REVISAR.

  1) python src/nuevo_video.py plan audio/frases.json audio/palabras.json final/edl_NUEVO.json [--etiqueta Parada] [--voz audio/voz_final.wav]
     -> final/edl_NUEVO.json         (esqueleto: planos, aperturas, fichas, números, palabras, notas, papel, video, cierre)
     -> final/edl_NUEVO.huecos.md    (lista de cada hueco con su segundo y la frase que se oye: qué foto buscar)
  2) Rellenar: cada "src": "PENDIENTE…" por la ruta de la foto o el clip; cada "REVISAR" por el texto final.
  3) python src/nuevo_video.py validar final/edl_NUEVO.json   -> dice qué falta; no se renderiza hasta que salga LISTO.
  4) Render + verificación: src/mezclar.ps1 y src/verificar.py (ver README).

Reglas que aplica solas (las del video aprobado, docs/CATALOGO_DETALLES.md):
- Cada sección "PALABRA N — Nombre" abre con el número rojo grande + nombre (2.3 s) y la ficha "<etiqueta> N" 2.35 s después.
- Un plano por idea: las enumeraciones (3 o más partes con comas) se cortan en el segundo de cada parte; el resto,
  en tramos de unos 4.5 s cortando en palabras (mínimo 2.4 s). Nunca más de 6 s.
- Número rojo en el segundo de cada cifra escrita en dígitos (años, precios), sin pisarse con otros textos.
- Palabra gigante en la última frase de cada sección y una más en las secciones largas (frase con más carga, REVISAR).
- Nota a máquina en cada lema entre «comillas».
- Blanco y negro en las frases de pérdida (cerró, quebró, liquidó, desapareció, vacío, se apagó…).
- Escenas de papel alternadas: polaroid, foto única con pie, nada (cada 3 secciones), en una frase larga del medio.
- 1 de cada 6 planos es un hueco de VIDEO real.
- Cierre: número del total, carrusel con un hueco por ítem ("N · Nombre") y palabra final hasta el último segundo.
"""
import argparse, json, os, re, subprocess, sys, unicodedata

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PERDIDA = re.compile(r'\b(cerr[óo]|quebr[óo]|liquid|desapareci|se fue|se fueron|vac[ií]a|se apag|intervenid|muri[óo]|dejó de|ya no estaba|última vez|funeral|adi[oó]s)', re.I)
NUMEROS = {'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5, 'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10, 'once': 11,
           'doce': 12, 'trece': 13, 'catorce': 14, 'quince': 15, 'dieciséis': 16, 'diecisiete': 17, 'dieciocho': 18,
           'diecinueve': 19, 'veinte': 20, 'veinticinco': 25, 'treinta': 30}
SEC = re.compile(r'^(?P<tipo>[A-ZÁÉÍÓÚÑ]+)\s+(?P<num>\d+)\s*[—–-]\s*(?P<nombre>.+)$')

def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    return re.sub(r'[^a-z0-9$]', '', ''.join(c for c in w if unicodedata.category(c) != 'Mn'))

def plan(a):
    frases = json.load(open(a.frases, encoding='utf-8'))
    pal = json.load(open(a.palabras, encoding='utf-8'))
    if a.voz and os.path.exists(a.voz):
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.voz], capture_output=True, text=True).stdout)
    else:
        dur = frases[-1]['e'] + 0.6
    # secciones en orden de aparición
    secs = []
    for f in frases:
        if not secs or secs[-1]['nombre'] != f['seccion']:
            secs.append({'nombre': f['seccion'], 'frases': []})
        secs[-1]['frases'].append(f)
    for k, s in enumerate(secs):
        s['t0'] = s['frases'][0]['s'] if k else 0.0
        s['t1'] = secs[k + 1]['frases'][0]['s'] if k + 1 < len(secs) else dur
        m = SEC.match(s['nombre'])
        s['item'] = {'num': m['num'], 'nombre': re.sub(r'\s*\(.*?\)', '', m['nombre']).strip(), 'tipo': m['tipo']} if m else None
    items = [s for s in secs if s['item']]
    n_items = len(items)

    # ---- planos: cortes por idea ----
    cortes, enum = [], set()
    for s in secs:
        for f in s['frases']:
            ws = [w for w in pal if f['s'] - 0.05 <= w['s'] < f['e'] + 0.05]
            partes = [p for p in re.split(r',\s*', f['texto']) if p.strip()]
            if len(partes) >= 3 and ws:  # enumeración: un corte por parte
                idx, acum = 0, 0
                for p in partes:
                    n = len(p.split())
                    if idx < len(ws):
                        cortes.append(ws[min(idx, len(ws) - 1)]['s']); enum.add(round(ws[min(idx, len(ws) - 1)]['s'], 2))
                    idx += n
            else:
                t, fin = f['s'], f['e']
                cortes.append(t)
                while fin - t > 6.0:
                    obj = t + 4.5
                    sig = min((w['s'] for w in ws if w['s'] >= obj), default=obj)
                    if fin - sig < 1.5: break
                    cortes.append(sig); t = sig
    for s in secs: cortes.append(s['t0'])
    cortes = sorted({round(c, 2) for c in cortes if 0 <= c < dur - 0.5})
    limpios = []
    inicios = {round(s['t0'], 2) for s in secs}
    for c in cortes:  # planos de 2.4 s como mínimo, salvo las enumeraciones (1.0 s) y el inicio de cada sección
        if not limpios or c - limpios[-1] >= (1.0 if c in enum else 2.4) or c in inicios:
            if limpios and c in inicios and c - limpios[-1] < 1.0: limpios[-1] = c
            else: limpios.append(c)
    limpios[0] = 0.0
    bordes = limpios + [round(dur, 2)]

    def frase_en(t):
        return next((f for f in frases if f['s'] - 0.3 <= t < f['e'] + 0.3), None)

    planos = []
    for k, (t0, t1) in enumerate(zip(bordes, bordes[1:])):
        f = frase_en(t0 + 0.1)
        sec = next(s for s in secs if s['t0'] <= t0 < s['t1'])
        hueco = f"PENDIENTE: {(sec['item'] or {}).get('nombre', sec['nombre'])} | {f['texto'][:90] if f else ''}"
        z = [(1.0, 1.07), (1.07, 1.0)][k % 2]
        # B/N solo en el primer plano de una frase de pérdida, y nunca en la intro
        bw = bool(f and sec['item'] and PERDIDA.search(f['texto']) and not any(q.get('_f') == f['i'] for q in planos[-3:]))
        p = {'t0': t0, 't1': t1, 'tipo': 'imagen', 'src': hueco, 'mov': {'z0': z[0], 'z1': z[1]}, 'bw': bw, '_f': f['i'] if f else None}
        if k % 7 == 3:
            p = {'t0': t0, 't1': t1, 'tipo': 'video', 'src': 'PENDIENTE_VIDEO: ' + hueco[11:], 'ss': 1.0, 'bw': p['bw']}
        planos.append(p)

    # ---- escenas de papel: polaroid / única / nada, en una frase larga del medio de la sección ----
    papeles = []
    for k, s in enumerate(items):
        modo = ['polaroid', 'unica', None][k % 3]
        if not modo: continue
        medio = [f for f in s['frases'][2:-1] if f['e'] - f['s'] >= 4.5] or [f for f in s['frases'][1:-1]]
        if not medio: continue
        f = max(medio, key=lambda f: f['e'] - f['s'])
        t0 = max(f['s'], s['t0'] + 5.0); t1 = min(t0 + (6.5 if modo == 'polaroid' else 5.5), s['t1'] - 1.0)
        if t1 - t0 < 4: continue
        n = 2 if modo == 'polaroid' else 1
        papeles.append({'t0': round(t0, 2), 't1': round(t1, 2), 'tipo': 'papel', 'papel': {'modo': modo, 'fotos': [
            {'src': f"PENDIENTE: {s['item']['nombre']} | {f['texto'][:80]}", 'pie': 'REVISAR'} for _ in range(n)]}})
    # cierre: carrusel con un hueco por ítem
    cierre = next((s for s in secs if s['nombre'].upper().startswith('CIERRE')), None)
    if cierre and items:
        t0 = cierre['t0'] + 2.4; t1 = min(t0 + min(10.5, max(8.0, 0.9 * n_items)), cierre['t1'] - 2.5)
        papeles.append({'t0': round(t0, 2), 't1': round(t1, 2), 'tipo': 'papel', 'papel': {'modo': 'carrusel', 'fotos': [
            {'src': f"PENDIENTE: foto de {it['item']['nombre']} (la mejor de su sección)", 'pie': f"{it['item']['num']} · {it['item']['nombre']}"} for it in items]}})
    # el papel reemplaza los planos que pisa
    for pp in papeles:
        nuevos = []
        for p in planos:
            if p['t1'] <= pp['t0'] or p['t0'] >= pp['t1']: nuevos.append(p); continue
            if p['t0'] < pp['t0']: nuevos.append({**p, 't1': pp['t0']})
            if p['t1'] > pp['t1']: nuevos.append({**p, 't0': pp['t1']})
        planos = sorted(nuevos + [pp], key=lambda p: p['t0'])
    planos = [p for p in planos if p['t1'] - p['t0'] >= 0.4]
    for a_, b_ in zip(planos, planos[1:]): a_['t1'] = b_['t0']
    # ningún plano de foto o video de más de 6 s: se parte en partes iguales (cada parte, su propio hueco)
    partidos = []
    for p in planos:
        d = p['t1'] - p['t0']
        if p['tipo'] != 'papel' and d > 6.0:
            n = int(d // 4.0) + 1
            for j in range(n):
                q = dict(p); q['t0'] = round(p['t0'] + d * j / n, 2); q['t1'] = round(p['t0'] + d * (j + 1) / n, 2)
                if j: q['bw'] = False; q['src'] = q['src'].replace('PENDIENTE', f'PENDIENTE (parte {j + 1})', 1)
                partidos.append(q)
        else:
            partidos.append(p)
    planos = partidos
    for p in planos: p.pop('_f', None)

    # ---- capas ----
    capas = []
    def libre(t, d):
        return all(t + d <= c['t'] - 0.1 or t >= c['t'] + c['dur'] + 0.1 for c in capas if c['tipo'] in ('numero', 'palabra'))
    for s in items:
        it = s['item']
        capas.append({'tipo': 'numero', 't': round(s['t0'], 2), 'dur': 2.3, 'num': it['num'], 'label': it['nombre'], 'grande': True})
        capas.append({'tipo': 'file', 't': round(s['t0'] + 2.35, 2), 'dur': 4.0, 'texto': it['nombre'], 'etiqueta': f"{a.etiqueta} {it['num']}"})
    for s in secs:
        fs = s['frases']
        # cifras en dígitos
        for w in pal:
            if s['t0'] + 4.8 <= w['s'] < s['t1'] - 1.0 and re.match(r'^\$?\d', w['w']):
                num = re.sub(r'[^\d$.,]', '', w['w']).rstrip('.,')
                if num and libre(w['s'], 2.3):
                    capas.append({'tipo': 'numero', 't': round(w['s'], 2), 'dur': 2.3, 'num': num, 'label': 'REVISAR'})
        # lemas entre comillas
        for f in fs:
            for q in re.findall(r'«([^»]{3,80})»', f['texto']):
                w0 = next((w for w in pal if w['s'] >= f['s'] - 0.1 and norm(w['w']) == norm(q.split()[0])), None)
                t = w0['s'] if w0 else f['s']
                capas.append({'tipo': 'nota', 't': round(max(t - 0.3, s['t0'] + 6.5), 2), 'dur': min(3.4, max(2.4, len(q) / 14)),
                              'texto': f'«{q}».', 'resaltar': [' '.join(q.split()[-2:])]})
        # palabra gigante en la última frase y otra en la frase más larga si la sección dura más de 50 s
        objetivos = [fs[-1]] + ([max(fs[1:-1], key=lambda f: f['e'] - f['s'])] if s['t1'] - s['t0'] > 50 and len(fs) > 3 else [])
        for f in objetivos:
            d = round(min(3.4, max(1.7, f['e'] - f['s'] + 0.3)), 2)
            d = min(d, s['t1'] - f['s'] - 0.05) if f is fs[-1] else d
            if libre(f['s'], d):
                capas.append({'tipo': 'palabra', 't': round(f['s'], 2), 'dur': d, 'palabra': 'REVISAR', 'sub': f['texto']})
    # número del total en la intro y en el cierre (la frase que dice cuántos ítems son)
    for s in secs:
        if s['item']: continue
        for w in pal:
            if s['t0'] <= w['s'] < s['t1'] and (NUMEROS.get(norm(w['w'])) == n_items or norm(w['w']) == str(n_items)):
                if libre(w['s'], 2.3):
                    capas.append({'tipo': 'numero', 't': round(w['s'], 2), 'dur': 2.3, 'num': str(n_items), 'label': 'REVISAR'})
                break
    if cierre:  # palabra final hasta el último segundo
        fl = cierre['frases'][-1]
        capas = [c for c in capas if not (c['tipo'] == 'palabra' and c['t'] >= fl['s'] - 0.2)]
        capas.append({'tipo': 'palabra', 't': round(fl['s'], 2), 'dur': round(dur - fl['s'], 2), 'palabra': 'REVISAR', 'sub': fl['texto']})
    capas.sort(key=lambda c: c['t'])

    edl = {'dur': round(dur, 2), 'audio': os.path.relpath(a.voz, RAIZ) if a.voz else 'audio/voz_final.wav', 'planos': planos, 'capas': capas}
    json.dump(edl, open(a.salida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # lista de huecos para buscar fotos
    md = [f'# Huecos de {os.path.basename(a.salida)}\n',
          'Cada línea es una foto o clip que hay que conseguir. Busca **lo que se oye en ese segundo** (docs/IMAGENES_Y_SINCRONIA.md).\n',
          '| # | Segundo | Tipo | Sección y frase que se oye |', '|---|---|---|---|']
    k = 0
    for p in planos:
        srcs = [p['src']] if p['tipo'] != 'papel' else [f['src'] for f in p['papel']['fotos']]
        for sname in srcs:
            k += 1
            tipo = {'video': 'VIDEO real', 'papel': 'foto para ' + p.get('papel', {}).get('modo', '')}.get(p['tipo'], 'foto') + (' (B/N)' if p.get('bw') else '')
            md.append(f"| {k} | {p['t0']:.1f} | {tipo} | {sname.split(': ', 1)[-1]} |")
    open(os.path.splitext(a.salida)[0] + '.huecos.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    resumen(edl, n_items)

def resumen(edl, n_items=None):
    from collections import Counter
    P, C = edl['planos'], edl['capas']
    print(f"duración {edl['dur'] / 60:.1f} min | planos {len(P)} (plano medio {edl['dur'] / len(P):.1f} s, máx {max(p['t1'] - p['t0'] for p in P):.1f} s)")
    print('tipos de plano', dict(Counter(p['tipo'] for p in P)), '| papel', dict(Counter(p['papel']['modo'] for p in P if p['tipo'] == 'papel')),
          '| B/N', sum(1 for p in P if p.get('bw')))
    print('capas', dict(Counter(c['tipo'] for c in C)), '| aperturas', sum(1 for c in C if c.get('grande')), f'de {n_items}' if n_items else '')

def validar(a):
    edl = json.load(open(a.edl, encoding='utf-8'))
    faltan = []
    for p in edl['planos']:
        fs = [p['src']] if p['tipo'] != 'papel' else [f['src'] for f in p['papel']['fotos']] + [f.get('pie', '') for f in p['papel']['fotos']]
        for x in fs:
            if 'PENDIENTE' in x or x == 'REVISAR': faltan.append(f"{p['t0']:7.1f}s  {p['tipo']:7s} {x[:100]}")
            elif p['tipo'] != 'papel' or x == p.get('src') or x in [f['src'] for f in p['papel']['fotos']]:
                if not os.path.isabs(x) and not os.path.exists(os.path.join(RAIZ, x)) and not os.path.exists(x) and x and ('/' in x or '\\' in x):
                    faltan.append(f"{p['t0']:7.1f}s  {p['tipo']:7s} NO EXISTE: {x[:100]}")
    for c in edl['capas']:
        for campo in ('label', 'palabra', 'texto', 'num'):
            if c.get(campo) == 'REVISAR': faltan.append(f"{c['t']:7.1f}s  capa {c['tipo']} -> escribir '{campo}'" + (f" (frase: {c.get('sub', '')[:70]})" if c.get('sub') else ''))
    resumen(edl)
    if faltan:
        print(f'\nFALTAN {len(faltan)} cosas por rellenar:'); print('\n'.join(faltan[:400]))
        sys.exit(1)
    print('\nLISTO: no quedan huecos. Siguiente: render (src/mezclar.ps1) y src/verificar.py.')

ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
p1 = sp.add_parser('plan'); p1.add_argument('frases'); p1.add_argument('palabras'); p1.add_argument('salida')
p1.add_argument('--etiqueta', default='Parada'); p1.add_argument('--voz', default=os.path.join(RAIZ, 'audio', 'voz_final.wav'))
p2 = sp.add_parser('validar'); p2.add_argument('edl')
a = ap.parse_args()
plan(a) if a.cmd == 'plan' else validar(a)
