"""Compara el nivel de cada efecto con el de la voz en la misma ventana (dB). Uso: python niveles.py"""
import subprocess
import numpy as np

def leer(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '48000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float64) / 32768

voz, fx = leer('audio/voz_final.wav'), leer('audio/efectos.wav')
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
for nombre, t, d in [('tecleo ficha Betatonio', 79.5, 0.6), ('golpe apertura 11', 77.1, 0.4), ('golpe número 1975', 222.92, 0.3),
                     ('whoosh+golpe palabra HONOR', 188.44, 0.5), ('obturador polaroid', 101.75, 0.15), ('¡PLUM!', 517.05, 0.2),
                     ('timbre Telecom', 263.55, 0.8), ('monedas Conavi', 769.2, 1.5)]:
    a, b = int(t * 48000), int((t + d) * 48000)
    print(f'{nombre:28s} voz {db(voz[a:b]):6.1f} dB | efecto {db(fx[a:b]):6.1f} dB | efecto respecto a voz {db(fx[a:b]) - db(voz[a:b]):+5.1f} dB')
