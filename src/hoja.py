"""Hoja de contacto con nombre de archivo, para elegir material. Uso: python hoja.py carpeta salida.jpg [patron]"""
import glob, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
carpeta, salida = sys.argv[1], sys.argv[2]
patron = sys.argv[3] if len(sys.argv) > 3 else '*'
archivos = sorted(glob.glob(os.path.join(carpeta, patron)))
archivos = [a for a in archivos if a.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.mp4'))]
tw, th, cols = 384, 216, 6
filas = (len(archivos) + cols - 1) // cols
hoja = Image.new('RGB', (tw * cols, (th + 22) * filas), (20, 20, 20))
f = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 15)
for i, a in enumerate(archivos):
    try:
        if a.endswith('.mp4'):
            png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '2', '-i', a, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
            import io; im = Image.open(io.BytesIO(png))
        else:
            im = Image.open(a)
        im = im.convert('RGB'); im.thumbnail((tw, th))
    except Exception:
        im = Image.new('RGB', (tw, th), (80, 0, 0))
    x, y = (i % cols) * tw, (i // cols) * (th + 22)
    hoja.paste(im, (x + (tw - im.width) // 2, y))
    ImageDraw.Draw(hoja).text((x + 4, y + th + 3), os.path.basename(a)[:44], font=f, fill=(255, 230, 0))
hoja.save(salida, quality=85)
print(salida, len(archivos))
