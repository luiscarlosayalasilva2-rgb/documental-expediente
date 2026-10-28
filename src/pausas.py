"""Acorta solo las pausas largas de la voz (Luis 2026-10-27: no cortar tanto, que quede de ~12 min).
Cada silencio de más de LARGA s (silencedetect -40 dB) queda en DEJAR s; los demás no se tocan.
Uso: python src/pausas.py audio/original.wav audio/sin_silencios.wav [LARGA] [DEJAR]"""
import re, subprocess, sys
import numpy as np, wave
ent, sal = sys.argv[1], sys.argv[2]
LARGA = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
DEJAR = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
log = subprocess.run(['ffmpeg', '-hide_banner', '-i', ent, '-af', f'silencedetect=n=-40dB:d={LARGA}', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
w = wave.open(ent); sr = w.getframerate(); assert w.getnchannels() == 1 and w.getsampwidth() == 2
x = np.frombuffer(w.readframes(w.getnframes()), np.int16); w.close()
partes, t = [], 0
for a, b in zip(ini, fin):
    m = (a + b) / 2
    partes.append(x[int(t * sr):int((m - DEJAR / 2) * sr)] if a > 0.05 else x[0:0])
    t = m + DEJAR / 2
partes.append(x[int(t * sr):])
y = np.concatenate(partes)
o = wave.open(sal, 'wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
print(f'{len(ini)} pausas acortadas: {len(x)/sr:.1f} s -> {len(y)/sr:.1f} s')
