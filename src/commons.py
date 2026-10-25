"""Busca en Wikimedia Commons (material con licencia libre) y lista lo que hay por consulta.

Uso: python commons.py "consulta 1" "consulta 2" ...   -> imprime título, licencia, tamaño y URL de cada archivo
"""
import json, sys, urllib.parse, urllib.request

def api(params):
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({**params, 'format': 'json'})
    req = urllib.request.Request(url, headers={'User-Agent': 'colombia12-doc/1.0'})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())

for q in sys.argv[1:]:
    r = api({'action': 'query', 'generator': 'search', 'gsrsearch': q, 'gsrnamespace': 6, 'gsrlimit': 12,
             'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiurlwidth': 1920})
    pages = (r.get('query') or {}).get('pages', {})
    print(f'\n### {q}: {len(pages)}')
    for p in sorted(pages.values(), key=lambda p: p.get('index', 0)):
        ii = p['imageinfo'][0]; md = ii.get('extmetadata', {})
        lic = md.get('LicenseShortName', {}).get('value', '?')
        print(f"  {p['title'][5:80]} | {lic} | {ii['width']}x{ii['height']}")
