"""Agranda x4 con Real-ESRGAN (realesrgan-x4plus) las fotos del EDL con menos de 1000 px de ancho.

Uso: python mejorar_fotos.py edl.json carpeta_salida
Salida: <carpeta>/<nombre>.jpg reducido a 2400 px de ancho máx. Se salta lo ya hecho.
-t 64 evita la salida negra de la Intel UHD.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image

EXE = r'C:\Users\luisa\calude\herramientas\realesrgan\realesrgan-ncnn-vulkan.exe'
edl, dest = json.load(open(sys.argv[1], encoding='utf-8')), sys.argv[2]
os.makedirs(dest, exist_ok=True)
fotos = set()
for p in edl['planos']:
    if p['tipo'] == 'imagen': fotos.add(p['src'])
    if p['tipo'] == 'papel': fotos.update(f['src'] for f in p['papel']['fotos'])
pend = [f for f in sorted(fotos) if Image.open(f).width < 1000
        and not os.path.exists(os.path.join(dest, os.path.splitext(os.path.basename(f))[0] + '.jpg'))]
print('por mejorar:', len(pend), flush=True)
for k, f in enumerate(pend, 1):
    tmp = os.path.join(tempfile.gettempdir(), 'esrgan_tmp.png')
    subprocess.run([EXE, '-i', f, '-o', tmp, '-n', 'realesrgan-x4plus', '-s', '4', '-t', '64'], capture_output=True)
    try:
        im = Image.open(tmp).convert('RGB')
    except Exception as e:
        print(k, 'ERROR', f, e, flush=True); continue
    if im.width > 2400:
        im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
    im.save(os.path.join(dest, os.path.splitext(os.path.basename(f))[0] + '.jpg'), quality=92)
    print(k, os.path.basename(f), im.size, flush=True)
