"""Miniatura 1280x720: franja blanca con título (negro + rojo) y collage de fotos reales de las marcas."""
import os, random
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
import estilo as E

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
G = lambda n: os.path.join(R, 'media', 'google_hd', n)
U = lambda n: os.path.join(R, 'media', 'hd_esrgan', n)
W, H = 1280, 720

fondo = ImageOps.fit(Image.open(U('intro_tienda_03.jpg')).convert('RGB'), (W, H), Image.LANCZOS)
fondo = ImageEnhance.Brightness(ImageOps.grayscale(fondo).convert('RGB')).enhance(0.35).filter(ImageFilter.GaussianBlur(3))
img = fondo.copy()

fotos = [  # (archivo, centro x, centro y, ancho, alto/ancho, giro, encuadre)
    (G('hd_b11_betatonio_00.jpg'), 165, 345, 310, 0.72, -5, (0.5, 0.5)),
    (G('hd_b03_cierre_02.jpg'), 175, 575, 310, 0.72, 4, (0.5, 0.3)),
    (G('hd_b05_la14_05.jpg'), 1115, 345, 310, 0.72, 5, (0.7, 0.4)),
    (G('hd_b04_chupiplum_00.jpg'), 1110, 575, 300, 0.72, -4, (0.5, 0.5)),
    (G('hd_p12_baloncito_01.jpg'), 640, 395, 440, 0.66, 0, (0.5, 0.5)),
    (U('b01_conavi_01.jpg'), 470, 610, 250, 0.72, -4, (0.5, 0.2)),
    (U('b10_konga_publi_01.jpg'), 810, 605, 190, 1.05, 4, (0.5, 0.45)),
]
for src, x, y, w, rel, ang, cen in fotos:
    im = Image.open(src).convert('RGB')
    h = int(w * rel)
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=cen)
    im = ImageEnhance.Color(im).enhance(1.25)
    marco = Image.new('RGB', (w + 16, h + 16), (250, 248, 240)); marco.paste(im, (8, 8))
    capa = Image.new('RGBA', (marco.width + 40, marco.height + 40), (0, 0, 0, 0))
    sh = Image.new('L', capa.size, 0); ImageDraw.Draw(sh).rectangle([20, 26, 20 + marco.width, 26 + marco.height], fill=170)
    capa.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(10)))
    capa.paste(marco, (20, 20))
    capa = capa.rotate(ang, Image.BICUBIC, expand=True)
    img.paste(capa, (x - capa.width // 2, y - capa.height // 2), capa)

# franja de título
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 205], fill=(250, 248, 242))
d.rectangle([0, 205, W, 213], fill=E.ROJO)
f1 = E.fuente(E.F_GRANDE, 112); f2 = E.fuente(E.F_GRANDE, 112)
t1, t2 = '12 MARCAS COLOMBIANAS', 'QUE DESAPARECIERON'
d.text(((W - d.textlength(t1, font=f1)) / 2, 2), t1, font=f1, fill=(20, 18, 16))
d.text(((W - d.textlength(t2, font=f2)) / 2, 98), t2, font=f2, fill=E.ROJO)
# sello rojo
fs = E.fuente(E.F_GRANDE, 54); txt = 'ANTES DE DESAPARECER'
sw = int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=fs)) + 40
sello = Image.new('RGBA', (sw, 74), (0, 0, 0, 0)); ds = ImageDraw.Draw(sello)
ds.rounded_rectangle([0, 0, sw - 1, 73], 8, fill=(20, 18, 16, 255))
ds.text((20, 6), txt, font=fs, fill=E.AMARILLO + (255,))
sello = sello.rotate(-3, Image.BICUBIC, expand=True)
# el sello repetía el título y tapaba la Konga: se deja fuera
out = os.path.join(R, 'final', 'miniatura.jpg')
img.save(out, quality=94); print(out)
