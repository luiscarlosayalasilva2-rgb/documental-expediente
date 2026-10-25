"""Busca y descarga material libre de Pixabay (fotos y videos).

Uso: python pixabay.py <carpeta_destino> <tipo foto|video> <n> "consulta 1" "consulta 2" ...
Guarda cada resultado como <slug>_<k>.<ext> y un indice.json con autor, página y etiquetas (para créditos).
"""
import json, os, re, sys, urllib.parse, urllib.request

KEY = os.environ.get('PIXABAY_API_KEY')
if not KEY:
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as k:
        KEY = winreg.QueryValueEx(k, 'PIXABAY_API_KEY')[0]

dest, tipo, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
os.makedirs(dest, exist_ok=True)
idx_path = os.path.join(dest, 'indice.json')
indice = json.load(open(idx_path, encoding='utf-8')) if os.path.exists(idx_path) else {}

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

for q in sys.argv[4:]:
    slug = re.sub(r'[^a-z0-9]+', '_', q.lower()).strip('_')
    base = 'https://pixabay.com/api/videos/' if tipo == 'video' else 'https://pixabay.com/api/'
    params = {'key': KEY, 'q': q, 'per_page': max(3, n), 'safesearch': 'true'}
    if tipo == 'foto':
        params.update({'image_type': 'photo', 'orientation': 'horizontal', 'min_width': 1600})
    hits = json.loads(get(base + '?' + urllib.parse.urlencode(params)))['hits'][:n]
    for k, h in enumerate(hits, 1):
        if tipo == 'video':
            v = h['videos'].get('large') or {}
            if not v.get('url') or v.get('width', 0) < 1280:
                v = h['videos']['medium']
            url, ext = v['url'], 'mp4'
            extra = {'dur': h.get('duration'), 'w': v.get('width'), 'h': v.get('height')}
        else:
            url, ext = h.get('largeImageURL') or h['webformatURL'], 'jpg'
            extra = {'w': h.get('imageWidth'), 'h': h.get('imageHeight')}
        nombre = f'{slug}_{k}.{ext}'
        ruta = os.path.join(dest, nombre)
        if not os.path.exists(ruta):
            open(ruta, 'wb').write(get(url))
        indice[nombre] = {'consulta': q, 'tipo': tipo, 'autor': h.get('user'), 'pagina': h.get('pageURL'), 'tags': h.get('tags'), **extra}
        print(nombre, '|', h.get('tags'), '|', extra)
    json.dump(indice, open(idx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
