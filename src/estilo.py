"""Recursos visuales del estilo "Documental Expediente" (ver ESTILO_DOCUMENTAL_EXPEDIENTE.md).

Cada recurso es una función draw_*(frame, t_local, spec) que pinta sobre un Image RGB de 1920x1080.
Los tiempos de animación son los medidos en el video de referencia.
"""
import math, os, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1920, 1080
CREMA = (237, 230, 214)
CUADRICULA = (217, 208, 188)
ROJO = (200, 48, 42)
AMARILLO = (232, 199, 102)
TINTA = (34, 30, 26)
BLANCO_ROTO = (238, 232, 220)

FUENTES = os.path.join(os.path.dirname(__file__), '..', 'fuentes')
def _fuente(nombres):
    for n in nombres:
        for d in (FUENTES, r'C:\Windows\Fonts'):
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    raise FileNotFoundError(nombres)
F_GRANDE = _fuente(['BebasNeue-Regular.ttf', 'Oswald-Bold.ttf', 'impact.ttf'])
F_MAQUINA = _fuente(['SpecialElite-Regular.ttf', 'CourierPrime-Bold.ttf', 'courbd.ttf'])

@lru_cache(maxsize=64)
def fuente(path, size):
    return ImageFont.truetype(path, size)

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x
def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3
def ease_in_out(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x
def fade(t, dur, fin=0.25, fout=0.25):
    """Opacidad: entra en fin s y sale en fout s al final."""
    return clamp(min(t / fin if fin else 1, (dur - t) / fout if fout else 1))

# ---------- texto ----------
def texto_espaciado(draw, xy, txt, font, fill, tracking=0):
    x, y = xy
    for ch in txt:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x
def ancho_espaciado(txt, font, tracking=0):
    d = ImageDraw.Draw(Image.new('L', (1, 1)))
    return sum(d.textlength(ch, font=font) for ch in txt) + tracking * max(0, len(txt) - 1)
def escrito(txt, t, cps=22.0):
    """Efecto máquina de escribir: cuántos caracteres van en t segundos."""
    return txt[:max(0, int(t * cps))]
def partir(txt, font, max_w, tracking=0):
    palabras, lineas, cur = txt.split(), [], ''
    for p in palabras:
        prueba = (cur + ' ' + p).strip()
        if ancho_espaciado(prueba, font, tracking) <= max_w or not cur:
            cur = prueba
        else:
            lineas.append(cur); cur = p
    if cur: lineas.append(cur)
    return lineas

# ---------- papel ----------
@lru_cache(maxsize=4)
def papel(w=W, h=H, celda=54, seed=3):
    img = Image.new('RGB', (w, h), CREMA)
    d = ImageDraw.Draw(img)
    for x in range(0, w, celda): d.line([(x, 0), (x, h)], fill=CUADRICULA, width=1)
    for y in range(0, h, celda): d.line([(0, y), (w, y)], fill=CUADRICULA, width=1)
    rnd = random.Random(seed)
    ruido = Image.effect_noise((w // 4, h // 4), 18).resize((w, h), Image.BILINEAR)
    return Image.blend(img, Image.merge('RGB', [ruido] * 3).point(lambda v: v * 0 + v), 0.04)

def tarjeta(w, h, color=CREMA, radio=4, sombra=18):
    """Tarjeta de papel con sombra suave; devuelve RGBA con margen para la sombra."""
    m = sombra * 2
    base = Image.new('RGBA', (w + m * 2, h + m * 2), (0, 0, 0, 0))
    sh = Image.new('L', base.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 8, m + w, m + h + 8], radio, fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(sombra / 2))
    base.paste((0, 0, 0, 255), (0, 0), sh)
    card = Image.new('RGBA', (w, h), color + (255,))
    ruido = Image.effect_noise((w, h), 10).point(lambda v: 128 + (v - 128) // 3)
    card = Image.composite(card, Image.new('RGBA', (w, h), tuple(max(0, c - 10) for c in color) + (255,)), ruido)
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radio, fill=255)
    base.paste(card, (m, m), mask)
    return base, m

def pegar(frame, rgba, x, y, alpha=1.0, escala=1.0, angulo=0.0):
    if escala != 1.0:
        rgba = rgba.resize((max(1, int(rgba.width * escala)), max(1, int(rgba.height * escala))), Image.BICUBIC)
    if angulo:
        rgba = rgba.rotate(angulo, Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = rgba.getchannel('A').point(lambda v: int(v * alpha))
        rgba = rgba.copy(); rgba.putalpha(a)
    frame.paste(rgba, (int(x - rgba.width / 2), int(y - rgba.height / 2)), rgba)

def velo(frame, k, desat=0.55):
    """Oscurece y desatura la imagen de fondo (k=0..1)."""
    if k <= 0: return frame
    gris = ImageOps.grayscale(frame).convert('RGB')
    f = Image.blend(frame, gris, desat * k)
    return Image.blend(f, Image.new('RGB', f.size, (16, 15, 14)), 0.68 * k)

# ---------- A. ficha FILE ----------
def draw_file(frame, t, s):
    dur = s['dur']; nombre = s['texto'].upper()
    f = fuente(F_MAQUINA, 74); fl = fuente(F_MAQUINA, 22)
    lineas = partir(nombre, f, 1050, 2)
    cw = int(max(ancho_espaciado(l, f, 2) for l in lineas)) + 130
    cw = max(cw, 620); ch = 120 + 84 * len(lineas)
    card, m = tarjeta(cw, ch)
    d = ImageDraw.Draw(card)
    texto_espaciado(d, (m + 56, m + 30), s.get('etiqueta', 'FILE').upper(), fl, ROJO if s.get('etiqueta') else (110, 100, 90), 6)
    tt = t - 0.35
    resto = escrito(nombre, tt, 22)
    y = m + 62
    for l in lineas:
        parte = resto[:len(l)]; resto = resto[len(l) + 1:]
        texto_espaciado(d, (m + 56, y), parte, f, TINTA, 2)
        y += 84
    if not escrito(nombre, tt, 22) and int(t * 4) % 2 == 0:
        d.text((m + cw // 2, m + ch // 2), '-', font=f, fill=TINTA)
    k_linea = ease_out((tt - len(nombre) / 22 - 0.05) / 0.5)
    if k_linea > 0:
        d.rectangle([m + 56, m + ch - 34, m + 56 + int((cw - 112) * k_linea), m + ch - 30], fill=ROJO)
    # cinta adhesiva amarilla
    cinta = Image.new('RGBA', (170, 44), AMARILLO + (205,))
    card.alpha_composite(cinta.rotate(-3, expand=True), (m - 18, m - 22))
    k = ease_out(t / 0.12)
    escala = 1.10 - 0.10 * k; ang = 2.5 * (1 - k)
    alpha = fade(t, dur, 0.06, 0.3)
    pegar(frame, card, 150 + card.width / 2 - m, 230 + card.height / 2 - m, alpha, escala, ang)

# ---------- B. número rojo ----------
def draw_numero(frame, t, s):
    dur = s['dur']
    k = ease_out(t / 0.17) * fade(t, dur, 0.01, 0.3)
    frame = velo(frame, k)
    d = ImageDraw.Draw(frame, 'RGBA')
    a = int(255 * fade(t, dur, 0.08, 0.3))
    fn = fuente(F_GRANDE, 360)
    w = d.textlength(s['num'], font=fn)
    d.text(((W - w) / 2, 270), s['num'], font=fn, fill=ROJO + (a,))
    if s.get('grande') and t > 0.3:
        # apertura de parada: el nombre de la marca grande y legible bajo el número
        fn2 = fuente(F_GRANDE, 150)
        lab = s['label'].upper()
        lw = d.textlength(lab, font=fn2)
        while lw > W * 0.86:
            fn2 = fuente(F_GRANDE, fn2.size - 8); lw = d.textlength(lab, font=fn2)
        kk = ease_out((t - 0.3) / 0.2)
        al = int(255 * fade(t - 0.3, dur - 0.3, 0.15, 0.3))
        capa = Image.new('RGBA', (int(lw) + 20, fn2.size + 30), (0, 0, 0, 0))
        ImageDraw.Draw(capa).text((10, 0), lab, font=fn2, fill=BLANCO_ROTO + (al,))
        pegar(frame, capa, W / 2, 700 + capa.height / 2 - 20 * (1 - kk), 1.0, 1.08 - 0.08 * kk)
    elif t > 0.3:
        fl = fuente(F_MAQUINA, 30)
        lab = s['label'].upper()
        lw = ancho_espaciado(lab, fl, 9)
        al = int(255 * fade(t - 0.3, dur - 0.3, 0.2, 0.3))
        img = Image.new('RGBA', (int(lw) + 4, 44), (0, 0, 0, 0))
        texto_espaciado(ImageDraw.Draw(img), (0, 0), lab, fl, BLANCO_ROTO + (al,), 9)
        frame.paste(img, (int((W - lw) / 2), 640), img)
    return frame

# ---------- C. palabra gigante ----------
def draw_palabra(frame, t, s):
    dur = s['dur']
    k = ease_out(t / 0.25) * fade(t, dur, 0.01, 0.3)
    frame = velo(frame, k)
    d = ImageDraw.Draw(frame, 'RGBA')
    a = fade(t, dur, 0.05, 0.3)
    d.rectangle([W // 2 - 1, 0, W // 2 + 1, H], fill=ROJO + (int(200 * a),))
    palabra = s['palabra'].upper()
    size = 400
    while size > 140 and d.textlength(palabra, font=fuente(F_GRANDE, size)) > W * 0.84:
        size -= 10
    fp = fuente(F_GRANDE, size)
    kk = ease_out(t / 0.15)
    escala = 1.12 - 0.12 * kk; dy = -40 * (1 - kk)
    pw = int(d.textlength(palabra, font=fp)) + 20
    capa = Image.new('RGBA', (pw, size + 40), (0, 0, 0, 0))
    ImageDraw.Draw(capa).text((10, 0), palabra, font=fp, fill=BLANCO_ROTO + (255,))
    pegar(frame, capa, W / 2, 470 + dy, a, escala)
    if s.get('sub') and t > 0.25:
        fs = fuente(F_MAQUINA, 36)
        lineas = partir(s['sub'], fs, W * 0.66, 3)
        resto = escrito(s['sub'], t - 0.25, 55)
        y = 470 + size * 0.52
        for l in lineas:
            parte = resto[:len(l)]; resto = resto[len(l) + 1:]
            lw = ancho_espaciado(l, fs, 3)
            img = Image.new('RGBA', (int(lw) + 4, 50), (0, 0, 0, 0))
            texto_espaciado(ImageDraw.Draw(img), (0, 0), parte, fs, BLANCO_ROTO + (int(255 * a),), 3)
            frame.paste(img, (int((W - lw) / 2), int(y)), img)
            y += 52
    return frame

# ---------- D. tira a máquina ----------
def draw_nota(frame, t, s):
    dur = s['dur']; txt = s['texto'].upper(); hl = [h.upper() for h in s.get('resaltar', [])]
    f = fuente(F_MAQUINA, 40)
    lineas = partir(txt, f, 1100, 1)
    cw = int(max(ancho_espaciado(l, f, 1) for l in lineas)) + 90; ch = 50 + 54 * len(lineas)
    card, m = tarjeta(cw, ch)
    d = ImageDraw.Draw(card, 'RGBA')
    resto = escrito(txt, t - 0.15, 30)
    y = m + 26
    for l in lineas:
        parte = resto[:len(l)]; resto = resto[len(l) + 1:]
        x = m + 45
        for h in hl:
            i = l.find(h)
            if i >= 0 and len(parte) > i:
                x0 = x + ancho_espaciado(l[:i], f, 1); x1 = x + ancho_espaciado(l[:i + len(h)], f, 1)
                d.rectangle([x0 - 4, y + 6, x1 + 4, y + 46], fill=AMARILLO + (190,))
        texto_espaciado(d, (x, y), parte, f, TINTA, 1)
        y += 54
    k = ease_out(t / 0.15)
    pegar(frame, card, W / 2, H - 150 - card.height / 2 + m + 30 * (1 - k), fade(t, dur, 0.12, 0.3))

# ---------- E. notas EXHIBIT ----------
def draw_exhibit(frame, t, s):
    dur = s['dur']; items = s['items']
    letras = 'ABCDEF'
    pos = s.get('pos') or [(380, 300), (760, 560), (1300, 320), (1500, 640)][:len(items)]
    puntos = []
    for i, (txt, (x, y)) in enumerate(zip(items, pos)):
        ti = t - i * 1.2
        if ti < 0: break
        f = fuente(F_MAQUINA, 36); fl = fuente(F_MAQUINA, 20)
        lineas = partir(txt.upper(), f, 420, 1)
        cw = int(max(ancho_espaciado(l, f, 1) for l in lineas)) + 70; ch = 82 + 46 * len(lineas)
        card, m = tarjeta(cw, ch)
        d = ImageDraw.Draw(card)
        texto_espaciado(d, (m + 30, m + 20), f'EXHIBIT {letras[i]}', fl, (110, 100, 90), 4)
        resto = escrito(txt.upper(), ti - 0.15, 26); yy = m + 54
        for l in lineas:
            parte = resto[:len(l)]; resto = resto[len(l) + 1:]
            texto_espaciado(d, (m + 30, yy), parte, f, TINTA, 1); yy += 46
        k = ease_out(ti / 0.18)
        pegar(frame, card, x, y, fade(t, dur, 0.01, 0.35), 1.12 - 0.12 * k)
        puntos.append((x, y - card.height / 2 + m + 6))
    d = ImageDraw.Draw(frame, 'RGBA')
    for i in range(1, len(puntos)):
        k = ease_out((t - i * 1.2 - 0.3) / 0.6)
        (x0, y0), (x1, y1) = puntos[i - 1], puntos[i]
        pts = []
        for j in range(21):
            u = j / 20 * k
            pts.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + 60 * math.sin(math.pi * u)))
        if len(pts) > 1: d.line(pts, fill=ROJO + (230,), width=3)
    for (x, y) in puntos:
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=ROJO + (255,))
        d.ellipse([x - 4, y - 6, x + 1, y - 2], fill=(255, 160, 150, 255))

# ---------- F. escenas de papel ----------
@lru_cache(maxsize=32)
def foto(path, w, h, radio=10, bw=False):
    im = Image.open(path).convert('RGB')
    im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    if bw: im = ImageOps.grayscale(im).convert('RGB')
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radio, fill=255)
    out = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0))
    sh = Image.new('L', out.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([40, 50, 40 + w, 50 + h], radio, fill=140)
    out.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
    out.paste(im, (40, 40), mask)
    return out

def pie(frame, x, y, txt, t, alpha=1.0):
    f = fuente(F_MAQUINA, 24)
    parte = escrito(txt.upper(), t, 26)
    d = ImageDraw.Draw(frame, 'RGBA')
    texto_espaciado(d, (x, y), parte, f, TINTA + (int(255 * alpha),), 3)
    d.line([(x - 6, y + 36), (x + ancho_espaciado(txt.upper(), f, 3) + 6, y + 36)], fill=(120, 110, 100, int(160 * alpha)), width=1)
    d.rectangle([x + 300, y + 34, x + 340, y + 37], fill=ROJO + (int(255 * alpha),))

def escena_papel(t, s):
    """Fondo de papel con fotos. modos: unica, carrusel, polaroid, vs."""
    frame = papel().copy()
    modo = s['modo']; fotos = s['fotos']
    if modo == 'unica':
        fo = fotos[0]
        z = 1.0 + 0.06 * (t / s['dur'])
        im = foto(fo['src'], 1300, 730, 10, fo.get('bw', False))
        pegar(frame, im, W / 2, H / 2 - 30, 1.0, z)
        pie(frame, 330, 940, fo.get('pie', ''), t - 0.4)
    elif modo == 'carrusel':
        paso = s['dur'] / len(fotos)
        i = min(len(fotos) - 1, int(t / paso)); tl = t - i * paso
        for j, fo in enumerate(fotos):
            rel = j - i
            k = ease_in_out(tl / 0.6) if j == i and i > 0 else 1.0
            off = rel + (1 - k) if j == i else (rel + (1 - ease_in_out(tl / 0.6)) if j == i - 1 else rel)
            if abs(off) > 1.6: continue
            im = foto(fo['src'], 1060, 600, 10, fo.get('bw', False))
            a = 1.0 if abs(off) < 0.05 else 0.35
            pegar(frame, im, W / 2 + off * 1160, H / 2 - 40, a)
        pie(frame, 430, 880, fotos[i].get('pie', ''), tl - 0.5)
    elif modo == 'polaroid':
        n = len(fotos); gap = s['dur'] / (n + 0.5)
        xs = [W / 2] if n == 1 else [W / 2 - 400 + 800 * j / (n - 1) for j in range(n)] if n == 2 else [W / 2 + (j - (n - 1) / 2) * 560 for j in range(n)]
        for j, fo in enumerate(fotos):
            tj = t - 0.25 - j * gap
            if tj < 0: continue
            pw, ph = (600, 520) if n <= 2 else (480, 420)
            card = Image.new('RGBA', (pw + 60, ph + 140), (0, 0, 0, 0))
            sh = Image.new('L', card.size, 0)
            ImageDraw.Draw(sh).rectangle([30, 38, 30 + pw, 38 + ph + 100], fill=140)
            card.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(12)))
            ImageDraw.Draw(card).rectangle([30, 30, 30 + pw, 30 + ph + 100], fill=(250, 248, 242, 255))
            im = ImageOps.fit(Image.open(fo['src']).convert('RGB'), (pw - 40, ph - 40), Image.LANCZOS)
            card.paste(im, (50, 50))
            d = ImageDraw.Draw(card)
            kb = ease_out((tj - 0.3) / 0.3)
            if kb > 0:
                d.rectangle([60, ph + 50, 60 + int((pw - 60) * kb), ph + 92], fill=ROJO + (255,))
                fl = fuente(F_MAQUINA, 22)
                texto_espaciado(d, (74, ph + 58), escrito(fo.get('pie', '').upper(), tj - 0.55, 26), fl, (250, 245, 235), 2)
            k = ease_out(tj / 0.25)
            ang = fo.get('ang', [-3, 2.5, -1.5, 3][j % 4])
            pegar(frame, card, xs[j], H / 2 - 20 - 60 * (1 - k), k, 1.15 - 0.15 * k, ang)
            if j > 0:
                kl = ease_out((tj - 0.2) / 0.5)
                xm = (xs[j - 1] + xs[j]) / 2
                ImageDraw.Draw(frame).line([(xm, 200), (xm, 200 + 640 * kl)], fill=ROJO, width=3)
    elif modo == 'vs':
        f = fuente(F_MAQUINA, 46); fs = fuente(F_MAQUINA, 26)
        d = ImageDraw.Draw(frame)
        texto_espaciado(d, (260, 150), escrito(s['titulo'].upper(), t, 26), f, ROJO, 3)
        texto_espaciado(d, (262, 220), escrito(s.get('sub', ''), t - 0.8, 30), fs, TINTA, 2)
        for j, fo in enumerate(fotos[:2]):
            tj = t - 0.6 - j * 0.5
            if tj < 0: continue
            im = foto(fo['src'], 640, 420, 8)
            x = W / 2 - 380 + 760 * j
            pegar(frame, im, x, 560, ease_out(tj / 0.25))
            pie(frame, x - 150, 820, fo.get('pie', ''), tj - 0.3)
        if t > 1.2:
            ImageDraw.Draw(frame).line([(W / 2, 330), (W / 2, 330 + 520 * ease_out((t - 1.2) / 0.5))], fill=ROJO, width=3)
    return frame

DIBUJOS = {'file': draw_file, 'numero': draw_numero, 'palabra': draw_palabra, 'nota': draw_nota, 'exhibit': draw_exhibit}
