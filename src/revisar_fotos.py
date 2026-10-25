"""Revisión obligatoria de autenticidad de las fotos de un EDL (docs/AUTENTICIDAD_FOTOS.md).

Uso: python src/revisar_fotos.py final/edl.json [--fuentes media/google/fuentes.tsv ...]
Crea en final/revision/:
  - parada_XX.jpg  hoja de contacto por sección: cada foto con número, segundo y la frase que se oye
  - REVISION.md    planilla: una fila por foto con [ ] OK / [ ] CAMBIAR; se marca con una x tras mirarla
Avisa solo: fotos repetidas (iguales o casi iguales aunque tengan otro nombre), baja resolución y
fuentes sospechosas de otro país (según fuentes.tsv que guarda receptor.py: página y título de origen).
Si REVISION.md ya existe, conserva las marcas hechas.
"""
import argparse, glob, json, os, re
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OTRO_PAIS = re.compile(r'\b(m[eé]xico|mexicano|mexicana|mazatl[aá]n|sinaloa|culiac[aá]n|guadalajara|monterrey|ecuador|ecuatoriano|guayaquil|quito|'
                       r'per[uú]|peruano|uruguay|montevideo|argentina|buenos aires|venezuela|caracas|espa[nñ]a|madrid|casa ley|oxxo|soriana)\b'
                       r'|\.(mx|ec|pe|uy|ar|cl|ve|es)\b|s\.a\. de c\.v\.', re.I)

def dhash(path, n=8):
    g = Image.open(path).convert('L').resize((n + 1, n), Image.LANCZOS); p = list(g.getdata())
    return sum(1 << i for i in range(n * n) if p[(i // n) * (n + 1) + i % n] > p[(i // n) * (n + 1) + i % n + 1])

def duplicados(rutas, umbral=6, umbral_fino=20):
    """Grupos de fotos iguales o casi iguales, también en blanco y negro, coloreadas o reescaladas.
    Doble firma (dHash 8x8 y 16x16) para no confundir fotos distintas con fondo blanco liso."""
    hs = {}
    for r in rutas:
        try: hs[r] = (dhash(r), dhash(r, 16))
        except Exception: pass
    grupos, vistos = [], set()
    for a in hs:
        if a in vistos: continue
        g = [b for b in hs if b != a and b not in vistos and bin(hs[a][0] ^ hs[b][0]).count('1') <= umbral
             and bin(hs[a][1] ^ hs[b][1]).count('1') <= umbral_fino]
        if g:
            grupos.append([a] + g); vistos.update([a] + g)
    return grupos

def fotos_del_edl(edl, con_carrusel=False):
    out = []  # (t0, ruta, tipo)
    for p in edl['planos']:
        if p['tipo'] == 'imagen': out.append((p['t0'], p['src'], 'foto' + (' B/N' if p.get('bw') else '')))
        elif p['tipo'] == 'papel' and (con_carrusel or p['papel']['modo'] != 'carrusel'):
            out += [(p['t0'], f['src'], 'papel ' + p['papel']['modo']) for f in p['papel']['fotos']]
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('edl'); ap.add_argument('--fuentes', nargs='*')
    a = ap.parse_args()
    edl = json.load(open(a.edl, encoding='utf-8'))
    frases = []
    for cand in ('audio/frases.json', 'datos/frases.json'):
        if os.path.exists(os.path.join(RAIZ, cand)):
            frases = json.load(open(os.path.join(RAIZ, cand), encoding='utf-8')); break
    fuentes = {}
    for f in (a.fuentes or glob.glob(os.path.join(RAIZ, 'media', '*', 'fuentes.tsv'))):
        for linea in open(f, encoding='utf-8', errors='ignore'):
            c = linea.rstrip('\n').split('\t')
            if len(c) >= 3: fuentes[c[0]] = c[2]
    secs = sorted(c['t'] for c in edl['capas'] if c['tipo'] == 'file')
    nombres = {round(c['t'], 1): c['texto'] for c in edl['capas'] if c['tipo'] == 'file'}
    def seccion(t):
        k = sum(1 for s in secs if s - 2.4 <= t)
        return k
    def frase(t):
        f = next((f for f in frases if f['s'] - 0.3 <= t < f['e'] + 0.3), None)
        return f['texto'] if f else ''

    fotos = fotos_del_edl(edl)
    dest = os.path.join(os.path.dirname(os.path.abspath(a.edl)), 'revision'); os.makedirs(dest, exist_ok=True)
    avisos = {}
    for g in duplicados([r for _, r, _ in fotos if os.path.exists(r)]):
        for r in g: avisos.setdefault(r, []).append('REPETIDA con ' + ', '.join(os.path.basename(x) for x in g if x != r))
    for _, r, _ in fotos:
        if not os.path.exists(r): avisos.setdefault(r, []).append('NO EXISTE'); continue
        w, h = Image.open(r).size
        if w < 900: avisos.setdefault(r, []).append(f'baja resolución {w}x{h}')
        info = fuentes.get(os.path.basename(r), '')
        if info and OTRO_PAIS.search(info): avisos.setdefault(r, []).append('¿OTRO PAÍS? fuente: ' + info[:80])

    # planilla (conserva marcas previas)
    plan_path = os.path.join(dest, 'REVISION.md'); previas = {}
    if os.path.exists(plan_path):
        for l in open(plan_path, encoding='utf-8'):
            m = re.match(r'\|\s*(\d+)\s*\|.*\|\s*\[(.)\] OK\s*\[(.)\] CAMBIAR', l)
            if m: previas[int(m[1])] = (m[2], m[3])
    filas = ['# Revisión de autenticidad de las fotos', '',
             'Mira la hoja de cada parada y marca con **x** una sola casilla por foto, revisando los 6 filtros de docs/AUTENTICIDAD_FOTOS.md:',
             '**país** correcto · **marca** correcta (no un homónimo) · **sin dibujos** ni juguetes ni IA · **sin comerciales**, afiches ni marcas de agua · **muestra lo que dice la voz** · **sin repetir**.',
             'No se renderiza hasta que todas digan OK. Las marcadas CAMBIAR se reemplazan en el EDL y se vuelve a correr este script.', '',
             '| # | seg | parada | tipo | archivo | lo que se oye | avisos automáticos | revisión |', '|---|---|---|---|---|---|---|---|']
    por_sec = {}
    for k, (t, r, tipo) in enumerate(fotos, 1):
        s = seccion(t); por_sec.setdefault(s, []).append((k, t, r, tipo))
        ok, camb = previas.get(k, (' ', ' '))
        if avisos.get(r) and ok == ' ' and camb == ' ': pass
        filas.append(f"| {k} | {t:.1f} | {s} | {tipo} | {os.path.basename(r)} | {frase(t)[:70].replace('|', '/')} | "
                     f"{'; '.join(avisos.get(r, []))[:120].replace('|', '/')} | [{ok}] OK [{camb}] CAMBIAR |")
    open(plan_path, 'w', encoding='utf-8').write('\n'.join(filas) + '\n')

    # hojas de contacto por parada
    try: fnt = ImageFont.truetype(os.path.join(RAIZ, 'fuentes', 'SpecialElite-Regular.ttf'), 15)
    except Exception: fnt = ImageFont.load_default()
    for s, items in por_sec.items():
        cols, tw, th = 4, 400, 225
        filas_n = (len(items) + cols - 1) // cols
        hoja = Image.new('RGB', (cols * tw, filas_n * (th + 58)), (24, 24, 24)); d = ImageDraw.Draw(hoja)
        for j, (k, t, r, tipo) in enumerate(items):
            x, y = (j % cols) * tw, (j // cols) * (th + 58)
            try:
                im = Image.open(r).convert('RGB'); im.thumbnail((tw - 8, th)); hoja.paste(im, (x + (tw - im.width) // 2, y))
            except Exception:
                d.rectangle([x, y, x + tw - 8, y + th], fill=(90, 0, 0))
            color = (255, 90, 80) if avisos.get(r) else (255, 214, 0)
            d.text((x + 4, y + th + 2), f'#{k}  {t:.1f}s  {tipo}', font=fnt, fill=color)
            d.text((x + 4, y + th + 20), frase(t)[:46], font=fnt, fill=(230, 230, 230))
            if avisos.get(r): d.text((x + 4, y + th + 38), avisos[r][0][:46], font=fnt, fill=(255, 90, 80))
        hoja.save(os.path.join(dest, f'parada_{s:02d}.jpg'), quality=82)
    n_av = sum(1 for _, r, _ in fotos if avisos.get(r))
    print(f'{len(fotos)} fotos revisables | {n_av} con avisos automáticos | hojas y planilla en {dest}')
    for r, av in list(avisos.items())[:40]: print('  AVISO', os.path.basename(r), '->', '; '.join(av)[:140])

if __name__ == '__main__':
    main()
