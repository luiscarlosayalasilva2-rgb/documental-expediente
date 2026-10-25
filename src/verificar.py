"""Verificador: mide un video terminado (y su EDL si existe) y lo compara con las metas del video de referencia
(final/12_marcas_colombianas_FINAL.mp4, el que Luis aprobó). Si algo falla, el video NO se entrega: se corrige y se vuelve a medir.

Uso: python src/verificar.py video.mp4 [edl.json]

Metas (medidas sobre el video aprobado; ver docs/REGLAS_DURAS.md):
- texto-en-papel en pantalla  <= 15 % del tiempo      (aprobado: ~8 %;   versión rechazada: 69 %)
- cortes por minuto            >= 12                    (aprobado: ~16;    rechazada: 8)
- sin corte visible por más de  30 s (medido en el video; el aprobado da ~28 s entre fotos parecidas, la rechazada 51 s)
- plano más largo en el EDL     <= 11 s (aprobado: 10.3 s, el carrusel del cierre)
- pantallas con número/palabra (fondo oscurecido) >= 3 por minuto
- negros de más de 0.3 s        = 0
- voz: integrado entre -16 y -13 LUFS y ninguna pausa > 0.35 s
- velocidad de la voz: 3.2 a 3.8 palabras por segundo (aprobado: 3.6). Prohibido acelerar el audio con atempo.
EL EDL ES OBLIGATORIO (sin él el video no se aprueba). Con EDL además: >= 25 clips de video, 0 fotos repetidas
(salvo carrusel), >= 1 número rojo por parada, >= 1 palabra gigante por minuto y medio, apertura numerada
(número grande + nombre) justo antes de CADA ficha, >= 1 imagen distinta cada 6 s en CADA parada,
y cierre con carrusel + palabra final.
"""
import json, os, re, subprocess, sys
from collections import Counter

video = sys.argv[1]
edl_path = sys.argv[2] if len(sys.argv) > 2 else None

def ff(args):
    return subprocess.run(['ffmpeg', '-hide_banner', *args], capture_output=True, text=True, errors='ignore').stderr

dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video],
                           capture_output=True, text=True).stdout)
mins = dur / 60

# cortes
log = ff(['-i', video, '-an', '-vf', "scale=320:-2,select='gt(scene,0.3)',showinfo", '-f', 'null', '-'])
cortes = [float(x) for x in re.findall(r'pts_time:([\d.]+)', log)]
bordes = [0.0] + cortes + [dur]
plano_max = max(b - a for a, b in zip(bordes, bordes[1:]))

# brillo y saturación a 2 fps: papel = claro y sin color; velo = oscuro tras un plano claro
log = ff(['-i', video, '-an', '-vf', 'fps=2,scale=160:90,signalstats,metadata=print:key=lavfi.signalstats.YAVG,'
          'metadata=print:key=lavfi.signalstats.SATAVG', '-f', 'null', '-'])
Y = [float(x) for x in re.findall(r'YAVG=([\d.]+)', log)]
S = [float(x) for x in re.findall(r'SATAVG=([\d.]+)', log)]
n = min(len(Y), len(S))
papel = sum(1 for i in range(n) if Y[i] > 185 and S[i] < 22) / max(1, n)
velos, i = 0, 4
while i < n:
    base = sum(Y[i - 4:i - 1]) / 3
    if base > 45 and Y[i] < base * 0.62 and Y[i] < 80:
        velos += 1; i += 4; continue
    i += 1

negros = len(re.findall(r'black_start', ff(['-i', video, '-an', '-vf', 'blackdetect=d=0.3:pix_th=0.08', '-f', 'null', '-'])))
lufs = re.findall(r'^\s+I:\s+([-\d.]+) LUFS', ff(['-i', video, '-vn', '-af', 'ebur128', '-f', 'null', '-']), re.M)
lufs = float(lufs[-1]) if lufs else 0.0
sil = [float(x) for x in re.findall(r'silence_duration: ([\d.]+)', ff(['-i', video, '-vn', '-af', 'silencedetect=n=-40dB:d=0.35', '-f', 'null', '-']))]

res = []
def chk(nombre, ok, valor, meta):
    res.append(ok); print(f"{'OK  ' if ok else 'FALLA'}  {nombre:42s} {valor:>12}   meta {meta}")

print(f'\n{os.path.basename(video)}  ({dur / 60:.1f} min)\n')
chk('texto en papel en pantalla', papel <= 0.15, f'{papel * 100:.0f} %', '<= 15 %')
chk('cortes por minuto', len(cortes) / mins >= 12, f'{len(cortes) / mins:.1f}', '>= 12')
chk('tramo sin corte visible', plano_max <= 30, f'{plano_max:.1f} s', '<= 30 s')
chk('números/palabras (fondo oscurecido) por min', velos / mins >= 3, f'{velos / mins:.1f}', '>= 3')
chk('negros > 0.3 s', negros == 0, str(negros), '0')
chk('volumen integrado de la voz', -16 <= lufs <= -13, f'{lufs:.1f} LUFS', '-16 a -13')
chk('pausas de la voz > 0.35 s', len(sil) <= 2, str(len(sil)), '<= 2')

# velocidad de la voz: palabras por segundo en 3 tramos de 40 s (detecta audio acelerado)
try:
    import numpy as np
    from faster_whisper import WhisperModel
    modelo = WhisperModel('small', device='cpu', compute_type='int8')
    pal, seg = 0, 0.0
    for f in (0.15, 0.5, 0.8):
        a = dur * f
        pcm = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-t', '40', '-i', video, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                             capture_output=True).stdout
        trozos, _ = modelo.transcribe(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768, language='es', vad_filter=False)
        pal += sum(len(t.text.split()) for t in trozos); seg += 40
    pps = pal / seg
    chk('velocidad de la voz (no acelerada)', 3.2 <= pps <= 3.8, f'{pps:.2f} pal/s', '3.2 a 3.8')
except ImportError:
    print('      (sin faster-whisper: no se midió la velocidad de la voz)')

if not edl_path:
    print()
    chk('EDL entregado junto al video', False, 'falta', 'obligatorio')

if edl_path:
    e = json.load(open(edl_path, encoding='utf-8'))
    P, C = e['planos'], e['capas']
    usos = Counter()
    for p in P:
        fs = [p['src']] if p.get('src') else ([] if p['papel']['modo'] == 'carrusel' else [f['src'] for f in p['papel']['fotos']])
        usos.update(os.path.basename(f) for f in fs)
    rep = sum(v - 1 for v in usos.values() if v > 1)
    tipos = Counter(c['tipo'] for c in C)
    aperturas = sum(1 for c in C if c['tipo'] == 'numero' and c.get('grande'))
    fichas = sum(1 for c in C if c['tipo'] == 'file')
    videos = sum(1 for p in P if p['tipo'] == 'video')
    papeles = sum(p['t1'] - p['t0'] for p in P if p['tipo'] == 'papel')
    print()
    chk('plano más largo (EDL)', max(p['t1'] - p['t0'] for p in P) <= 11, f"{max(p['t1'] - p['t0'] for p in P):.1f} s", '<= 11 s')
    chk('clips de video', videos >= 25 * dur / 832, str(videos), f'>= {round(25 * dur / 832)}')
    chk('fotos repetidas (sin contar carrusel)', rep == 0, str(rep), '0')
    chk('aperturas numeradas (número grande + nombre)', aperturas >= max(1, fichas), str(aperturas), f'= fichas ({fichas})')
    chk('números rojos de cifras (sin aperturas)', tipos['numero'] - aperturas >= fichas, str(tipos['numero'] - aperturas), f'>= {fichas}')
    chk('palabras gigantes', tipos['palabra'] >= mins / 1.5, str(tipos['palabra']), f'>= {mins / 1.5:.0f}')
    chk('notas a máquina (lemas)', tipos['nota'] >= fichas / 2, str(tipos['nota']), f'>= {fichas / 2:.0f}')
    chk('tiempo en escenas de papel', papeles / dur <= 0.15, f'{papeles / dur * 100:.0f} %', '<= 15 %')

    # apertura numerada justo antes de CADA ficha
    fts = sorted(c['t'] for c in C if c['tipo'] == 'file')
    ats = [c['t'] for c in C if c['tipo'] == 'numero' and c.get('grande')]
    sin_ap = [round(t) for t in fts if not any(0 <= t - a <= 4 for a in ats)]
    chk('cada ficha con su apertura numerada', not sin_ap, 'todas' if not sin_ap else f'faltan en {sin_ap}', 'todas')

    # imágenes distintas por parada (una por cada cosa narrada)
    def fuentes(p):
        if p['tipo'] == 'papel': return [f['src'] for f in p['papel']['fotos']]
        return [p['src']]
    peor = None
    for k, t0 in enumerate(fts):
        t1 = fts[k + 1] if k + 1 < len(fts) else dur
        dist = {os.path.basename(f) for p in P if p['t0'] < t1 and p['t1'] > t0 for f in fuentes(p)}
        ritmo = (t1 - t0) / max(1, len(dist))
        if peor is None or ritmo > peor[0]: peor = (ritmo, round(t0), len(dist), round(t1 - t0))
    if peor:
        chk('parada con menos imágenes', peor[0] <= 6, f'{peor[2]} en {peor[3]} s (t={peor[1]})', '>= 1 imagen distinta cada 6 s')

    # cierre: carrusel en el último minuto y palabra final hasta el final
    carr = any(p['tipo'] == 'papel' and p['papel']['modo'] == 'carrusel' and p['t0'] > dur - 60 for p in P)
    fin = any(c['tipo'] == 'palabra' and c['t'] + c['dur'] >= dur - 1.5 for c in C)
    chk('cierre (carrusel + palabra final)', carr and fin, ('carrusel ' if carr else '') + ('palabra' if fin else '') or 'falta', 'ambos')

print('\n' + ('APROBADO: cumple todas las metas.' if all(res) else f'NO APROBADO: {res.count(False)} metas fallan. Corregir antes de entregar.'))
sys.exit(0 if all(res) else 1)
