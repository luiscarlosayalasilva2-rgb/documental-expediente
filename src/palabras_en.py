"""Imprime las palabras de la voz con su segundo de inicio entre dos tiempos. Uso: python palabras_en.py desde hasta"""
import json, sys
a, b = float(sys.argv[1]), float(sys.argv[2])
w = json.load(open('audio/palabras.json', encoding='utf-8'))
print(' '.join(f"{x['w']}@{x['s']:.1f}" for x in w if a <= x['s'] < b))
