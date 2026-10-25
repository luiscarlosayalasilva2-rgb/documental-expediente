"""Busca, para cada foto del EDL, la misma foto en mayor resolución dentro de media/google_hd (dHash).

Uso: python emparejar_hd.py edl.json mapa_hd.json
Salida: {foto_original: foto_hd} solo cuando es la misma imagen (distancia <= 10 de 64) y la HD es al menos 1.4x más ancha.
"""
import glob, json, os, sys
from PIL import Image

edl = json.load(open(sys.argv[1], encoding='utf-8'))
R = os.path.join(os.path.dirname(__file__), '..')

def dhash(im, n=8):
    g = im.convert('L').resize((n + 1, n), Image.LANCZOS)
    p = list(g.getdata())
    return sum(1 << i for i in range(n * n) if p[(i // n) * (n + 1) + i % n] > p[(i // n) * (n + 1) + i % n + 1])

def firmas(im):
    # la imagen completa y recortes centrales, porque la HD puede venir con otro encuadre
    w, h = im.size; out = [dhash(im)]
    for f in (0.9, 0.8):
        cw, ch = int(w * f), int(h * f)
        out.append(dhash(im.crop(((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2))))
    return out

usadas = set()
for p in edl['planos']:
    if p['tipo'] == 'imagen': usadas.add(p['src'])
    if p['tipo'] == 'papel': usadas.update(f['src'] for f in p['papel']['fotos'])
usadas = [u for u in usadas if os.sep + 'google' + os.sep in u or '/google/' in u]

hd = []
for f in glob.glob(os.path.join(R, 'media', 'google_hd', 'hd_*.jpg')):
    try:
        im = Image.open(f); im.load(); hd.append((f, im.size, firmas(im)))
    except Exception:
        pass
print('fotos usadas de Google:', len(usadas), '| candidatas HD:', len(hd))

parada = lambda ruta: os.path.basename(ruta).replace('hd_', '').split('_')[0]  # b05, p12, intro…
fino = {}
def dfino(f, im=None):
    if f not in fino: fino[f] = dhash(im or Image.open(f), 16)
    return fino[f]

mapa = {}
for u in sorted(usadas):
    im = Image.open(u); f0 = firmas(im)
    mejor = None
    for f, size, fh in hd:
        if parada(f) != parada(u) or size[0] < im.width * 1.4: continue
        d = min(bin(a ^ b).count('1') for a in f0 for b in fh)
        if d > 6: continue
        if bin(dfino(u, im) ^ dfino(f)).count('1') > 50: continue  # de 256: misma imagen, no solo parecida
        if mejor is None or (d, -size[0]) < (mejor[0], -mejor[2][0]):
            mejor = (d, f, size)
    if mejor:
        mapa[u] = mejor[1]
        print(f'  {os.path.basename(u):28s} {im.size} -> {os.path.basename(mejor[1])} {mejor[2]} (dist {mejor[0]})')
json.dump(mapa, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('reemplazos:', len(mapa))
