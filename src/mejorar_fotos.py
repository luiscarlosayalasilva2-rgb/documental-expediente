"""Agranda x4 con Real-ESRGAN (realesrgan-x4plus) las fotos del EDL con menos de 1000 px de ancho.

Uso: python mejorar_fotos.py edl.json carpeta_salida
Salida: <carpeta>/<nombre>.jpg reducido a 2400 px de ancho máx. Se salta lo ya hecho.
-t 64 evita la salida negra de la Intel UHD.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image

# instalar.ps1 lo deja en ../herramientas/realesrgan, al lado de la carpeta del repo
EXE = os.environ.get('REALESRGAN_EXE') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'herramientas', 'realesrgan', 'realesrgan-ncnn-vulkan.exe'))
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
    # temporal propio por foto y borrado antes: si Real-ESRGAN falla, nunca se guarda la imagen de la foto anterior
    tmp = os.path.join(tempfile.gettempdir(), f'esrgan_{os.getpid()}_{k}.png')
    if os.path.exists(tmp): os.remove(tmp)
    subprocess.run([EXE, '-i', f, '-o', tmp, '-n', 'realesrgan-x4plus', '-s', '4', '-t', '64'], capture_output=True)
    try:
        im = Image.open(tmp).convert('RGB')
        orig = Image.open(f).convert('L').resize((16, 16)); nueva = im.convert('L').resize((16, 16))
        if sum(abs(a - b) for a, b in zip(orig.getdata(), nueva.getdata())) / 256 > 40:
            raise ValueError('la salida no se parece a la foto original')
    except Exception as e:
        print(k, 'ERROR', f, e, flush=True); continue
    finally:
        if os.path.exists(tmp): os.remove(tmp)
    if im.width > 2400:
        im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
    im.save(os.path.join(dest, os.path.splitext(os.path.basename(f))[0] + '.jpg'), quality=92)
    print(k, os.path.basename(f), im.size, flush=True)
