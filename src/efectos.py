"""Pista de efectos sintetizados (sin grabaciones ajenas, sin derechos de autor) colocada según el EDL.

Uso: python efectos.py edl.json salida.wav
- ficha FILE y notas: tecleo de máquina de escribir mientras se escribe el texto
- número rojo: golpe grave (más profundo en las aperturas de parada)
- palabra gigante y entrada de papel: whoosh suave
- polaroid: obturador de cámara; carrusel: whoosh por foto
- especiales de la narración: ¡PLUM!, timbre de teléfono, VHS, monedas
"""
import json, sys, wave
import numpy as np

SR = 48000
edl = json.load(open(sys.argv[1], encoding='utf-8'))
out = np.zeros(int(edl['dur'] * SR) + SR, dtype=np.float64)
rng = np.random.default_rng(7)

def poner(t, x, gan):
    i = int(t * SR)
    if i < 0 or i >= len(out): return
    n = min(len(x), len(out) - i)
    out[i:i + n] += x[:n] * gan

def env_exp(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))

def pasabanda(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))

def norm(x):
    m = np.max(np.abs(x)) or 1
    return x / m

def tecla():
    n = int(0.045 * SR)
    golpe = pasabanda(rng.standard_normal(n), 1800, 6500) * env_exp(n, 0.004)
    cuerpo = np.sin(2 * np.pi * rng.uniform(170, 230) * np.arange(n) / SR) * env_exp(n, 0.010) * 0.5
    return norm(golpe + cuerpo)

def golpe(grave=False):
    dur = 0.9 if grave else 0.45
    n = int(dur * SR); t = np.arange(n) / SR
    f0, f1 = (70, 34) if grave else (95, 48)
    fase = 2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t / 0.06)) / SR
    tono = np.sin(fase) * env_exp(n, 0.28 if grave else 0.12)
    ataque = pasabanda(rng.standard_normal(n), 200, 3000) * env_exp(n, 0.006) * 0.35
    return norm(tono + ataque)

def whoosh(dur=0.55, sube=True):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    ruido = rng.standard_normal(n)
    corte = (400 + 3600 * t) if sube else (4000 - 3600 * t)
    a = np.exp(-2 * np.pi * corte / SR); y = np.zeros(n); acc = 0.0
    for i in range(n):  # pasa-bajos de un polo con corte variable
        acc = (1 - a[i]) * ruido[i] + a[i] * acc; y[i] = acc
    y -= pasabanda(y, 0, 120)
    return norm(y * np.sin(np.pi * t) ** 1.5)

def obturador():
    x = np.zeros(int(0.16 * SR))
    for k, (t0, g) in enumerate([(0.0, 1.0), (0.075, 0.7)]):
        n = int(0.03 * SR); i = int(t0 * SR)
        x[i:i + n] += pasabanda(rng.standard_normal(n), 1200, 8000) * env_exp(n, 0.005) * g
    return norm(x)

def plum():
    n = int(0.25 * SR); t = np.arange(n) / SR
    fase = 2 * np.pi * np.cumsum(110 + 380 * np.exp(-t / 0.03)) / SR
    return norm(np.sin(fase) * env_exp(n, 0.06) + pasabanda(rng.standard_normal(n), 300, 5000) * env_exp(n, 0.008) * 0.6)

def timbre(dur=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    campana = np.sin(2 * np.pi * 850 * t) + 0.6 * np.sin(2 * np.pi * 1270 * t) + 0.3 * np.sin(2 * np.pi * 2050 * t)
    martillo = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 20 * t))
    return norm(campana * martillo * np.minimum(1, (dur - t) / 0.15))

def moneda():
    n = int(0.5 * SR); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * t) * env_exp(n, d) for f, a, d in [(2100, 1, 0.20), (3420, .7, .14), (5230, .5, .09), (7100, .3, .06)])
    return norm(y + pasabanda(rng.standard_normal(n), 3000, 9000) * env_exp(n, 0.003) * 0.8)

def vhs():
    n = int(0.5 * SR); x = np.zeros(n)
    for t0, g in [(0.0, 1.0), (0.18, 0.6), (0.32, 0.8)]:
        m = int(0.06 * SR); i = int(t0 * SR); tt = np.arange(m) / SR
        x[i:i + m] += (np.sin(2 * np.pi * 140 * tt) * 0.8 + pasabanda(rng.standard_normal(m), 500, 4000) * 0.5) * env_exp(m, 0.012) * g
    return norm(x)

def tecleo(t0, texto, cps, cada=1, gan=0.10):
    for k, ch in enumerate(texto):
        if ch.strip() and k % cada == 0:
            poner(t0 + k / cps + rng.uniform(-0.004, 0.004), tecla(), gan * rng.uniform(0.75, 1.0))

# ---- capas ----
for c in edl['capas']:
    t = c['t']
    if c['tipo'] == 'file':
        tecleo(t + 0.35, c['texto'].upper(), 22, 1, 0.16)
    elif c['tipo'] == 'nota':
        tecleo(t + 0.15, c['texto'].upper(), 30, 2, 0.12)
    elif c['tipo'] == 'numero':
        poner(t, golpe(c.get('grande')), 0.30 if c.get('grande') else 0.24)
    elif c['tipo'] == 'palabra':
        poner(t - 0.18, whoosh(0.5), 0.10)
        poner(t + 0.05, golpe(), 0.12)
    elif c['tipo'] == 'exhibit':
        for i in range(len(c['items'])):
            poner(t + i * 1.2, obturador(), 0.10)

# ---- escenas de papel ----
planos = edl['planos']
for i, p in enumerate(planos):
    if p['tipo'] != 'papel': continue
    s = p['papel']; dur = p['t1'] - p['t0']
    if i > 0 and planos[i - 1]['tipo'] != 'papel':
        poner(p['t0'] - 0.1, whoosh(0.5), 0.09)
    if s['modo'] == 'polaroid':
        gap = dur / (len(s['fotos']) + 0.5)
        for j in range(len(s['fotos'])):
            poner(p['t0'] + 0.25 + j * gap, obturador(), 0.13)
    elif s['modo'] == 'carrusel':
        paso = dur / len(s['fotos'])
        for j in range(1, len(s['fotos'])):
            poner(p['t0'] + j * paso - 0.1, whoosh(0.45), 0.07)

# ---- especiales de la narración ----
# En un tema nuevo se definen en el EDL: "especiales": [{"t": seg, "sonido": "plum|timbre|vhs|moneda", "gan": 0.12}]
ESPECIALES = {'plum': lambda: plum(), 'timbre': lambda: timbre(0.85), 'vhs': lambda: vhs(), 'moneda': lambda: moneda()}
if 'especiales' in edl:
    for e_ in edl['especiales']:
        if e_['sonido'] in ESPECIALES: poner(e_['t'], ESPECIALES[e_['sonido']](), e_.get('gan', 0.12))
else:  # EDL del video de referencia (12 marcas): tiempos de su audio/palabras.json
    poner(517.05, plum(), 0.30)              # "Escuche: ¡PLUM!"
    poner(263.55, timbre(0.85), 0.07)        # antes de «Voy al Telecom»
    poner(121.4, vhs(), 0.16)                # la cinta en la videocasetera
    for k in range(4):                       # "moneda por moneda, aprendimos a ahorrar"
        poner(769.2 + k * 0.42, moneda(), 0.10 * (1 - k * 0.12))

# ---- guardar ----
pk = np.max(np.abs(out)); print('pico efectos', round(20 * np.log10(pk), 1), 'dBFS')
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
with wave.open(sys.argv[2], 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
print(sys.argv[2])
