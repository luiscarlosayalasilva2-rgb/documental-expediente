"""Compositor del estilo expediente: lee un EDL (json) y renderiza el video 1920x1080 30 fps.

Uso: python render.py edl.json salida.mp4 [--desde S --hasta S] [--workers N]
"""
import argparse, json, math, os, subprocess, sys, tempfile
from multiprocessing import Pool
from PIL import Image, ImageOps
import estilo as E

FPS = 30
W, H = E.W, E.H
TRANS = 0.5  # empuje del papel, s

def encuadrar(im):
    """Foto pequeña o vertical: nítida al centro con sombra, sobre ella misma desenfocada y oscurecida."""
    from PIL import ImageDraw, ImageFilter, ImageEnhance
    cw, ch = int(W * 1.25), int(H * 1.25)
    fondo = ImageOps.fit(im, (cw // 4, ch // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(6)).resize((cw, ch), Image.BILINEAR)
    fondo = ImageEnhance.Brightness(ImageEnhance.Color(fondo).enhance(0.6)).enhance(0.45)
    esc = min(ch * 0.78 / im.height, cw * 0.70 / im.width)
    fg = im.resize((int(im.width * esc), int(im.height * esc)), Image.LANCZOS)
    x, y = (cw - fg.width) // 2, (ch - fg.height) // 2
    sombra = Image.new('L', (cw, ch), 0)
    ImageDraw.Draw(sombra).rounded_rectangle([x + 6, y + 18, x + fg.width + 6, y + fg.height + 18], 12, fill=170)
    fondo.paste((0, 0, 0), (0, 0), sombra.filter(ImageFilter.GaussianBlur(22)))
    mask = Image.new('L', fg.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, fg.width - 1, fg.height - 1], 12, fill=255)
    fondo.paste(fg, (x, y), mask)
    return fondo

class Imagen:
    def __init__(self, p):
        im = Image.open(p['src']).convert('RGB')
        if p.get('bw'):
            im = ImageOps.grayscale(im).convert('RGB')
        if p.get('encuadre', im.width < 1100 or im.width / im.height < 1.3):
            im = encuadrar(im)
        self.im = ImageOps.fit(im, (int(W * 1.25), int(H * 1.25)), Image.LANCZOS)
        m = p.get('mov', {})
        self.z0, self.z1 = m.get('z0', 1.0), m.get('z1', 1.08)
        self.c0, self.c1 = m.get('c0', [0.5, 0.5]), m.get('c1', [0.5, 0.5])
        self.dur = p['t1'] - p['t0']
        self.mano = m.get('mano', True)

    def frame(self, tl):
        u = E.ease_in_out(tl / self.dur) * 0.85 + 0.15 * E.clamp(tl / self.dur)
        z = self.z0 + (self.z1 - self.z0) * u
        cx = self.c0[0] + (self.c1[0] - self.c0[0]) * u
        cy = self.c0[1] + (self.c1[1] - self.c0[1]) * u
        iw, ih = self.im.size
        bw, bh = iw / 1.25 / z, ih / 1.25 / z
        if self.mano:  # leve temblor de cámara en mano
            cx += 0.0016 * math.sin(tl * 1.7) + 0.0009 * math.sin(tl * 4.3)
            cy += 0.0014 * math.sin(tl * 1.3 + 1) + 0.0008 * math.sin(tl * 3.7)
        x0 = E.clamp(cx * iw - bw / 2, 0, iw - bw); y0 = E.clamp(cy * ih - bh / 2, 0, ih - bh)
        return self.im.transform((W, H), Image.EXTENT, (x0, y0, x0 + bw, y0 + bh), Image.BILINEAR)

class Video:
    def __init__(self, p):
        self.p = p; self.proc = None; self.idx = -1; self.last = None
        self.dur = p['t1'] - p['t0']

    def _abrir(self, desde):
        ss = self.p.get('ss', 0) + desde
        vf = f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}'
        if self.p.get('bw'): vf += ',hue=s=0'
        self.proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', self.p['src'], '-an', '-vf', vf,
                                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        self.idx = int(round(desde * FPS)) - 1

    def frame(self, tl):
        want = int(round(tl * FPS))
        if self.proc is None or want < self.idx:
            self._abrir(max(0, tl))
        while self.idx < want:
            buf = self.proc.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            self.last = Image.frombytes('RGB', (W, H), buf); self.idx += 1
        return self.last.copy() if self.last else Image.new('RGB', (W, H))

class Papel:
    def __init__(self, p):
        self.s = dict(p['papel']); self.s['dur'] = p['t1'] - p['t0']
    def frame(self, tl):
        return E.escena_papel(tl, self.s)

def fuente_de(p):
    return {'imagen': Imagen, 'video': Video, 'papel': Papel}[p['tipo']](p)

def render_tramo(args):
    edl, f0, f1, out = args
    planos = edl['planos']; capas = edl.get('capas', [])
    cache = {}
    def src(i):
        if i not in cache:
            for k in list(cache):
                if abs(k - i) > 1: del cache[k]
            cache[i] = fuente_de(planos[i])
        return cache[i]
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19',
                            '-pix_fmt', 'yuv420p', '-threads', '2', out], stdin=subprocess.PIPE)
    i = 0
    for fi in range(f0, f1):
        t = fi / FPS
        while i < len(planos) - 1 and t >= planos[i]['t1']: i += 1
        while i > 0 and t < planos[i]['t0']: i -= 1
        p = planos[i]; tl = t - p['t0']
        fr = src(i).frame(tl)
        # empuje vertical del papel al entrar y al salir
        if p['tipo'] == 'papel' and i > 0 and planos[i - 1]['tipo'] != 'papel' and tl < TRANS:
            k = E.ease_in_out(tl / TRANS)
            prev = src(i - 1).frame(t - planos[i - 1]['t0'])
            lienzo = Image.new('RGB', (W, H)); lienzo.paste(prev, (0, int(-H * k))); lienzo.paste(fr, (0, int(H * (1 - k)))); fr = lienzo
        if p['tipo'] == 'papel' and i < len(planos) - 1 and planos[i + 1]['tipo'] != 'papel' and p['t1'] - t < TRANS:
            k = E.ease_in_out(1 - (p['t1'] - t) / TRANS)
            nxt = src(i + 1).frame(0)
            lienzo = Image.new('RGB', (W, H)); lienzo.paste(fr, (0, int(-H * k))); lienzo.paste(nxt, (0, int(H * (1 - k)))); fr = lienzo
        for c in capas:
            if c['t'] <= t < c['t'] + c['dur']:
                r = E.DIBUJOS[c['tipo']](fr, t - c['t'], c)
                if r is not None: fr = r
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('edl'); ap.add_argument('out')
    ap.add_argument('--desde', type=float, default=0); ap.add_argument('--hasta', type=float)
    ap.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    edl = json.load(open(a.edl, encoding='utf-8'))
    hasta = a.hasta or edl['dur']
    f0, f1 = int(a.desde * FPS), int(hasta * FPS)
    tmp = tempfile.mkdtemp(prefix='render_', dir=os.path.dirname(os.path.abspath(a.out)))
    n = max(1, a.workers); paso = math.ceil((f1 - f0) / n)
    tramos = [(edl, f0 + k * paso, min(f1, f0 + (k + 1) * paso), os.path.join(tmp, f'tramo_{k:02d}.mp4')) for k in range(n) if f0 + k * paso < f1]
    with Pool(len(tramos)) as pool:
        partes = pool.map(render_tramo, tramos)
    lista = os.path.join(tmp, 'lista.txt')
    with open(lista, 'w') as fh:
        for pth in partes: fh.write(f"file '{pth}'\n")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lista, '-ss', str(a.desde), '-t', str(hasta - a.desde),
                    '-i', edl['audio'], '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', a.out], check=True)
    print(a.out)

if __name__ == '__main__':
    main()
