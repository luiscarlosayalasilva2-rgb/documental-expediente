"""Subtítulos .srt para subir a YouTube como pista aparte (en la imagen NO van subtítulos: es parte del estilo).

Usa el texto del guion (bien escrito) con los tiempos de la voz (audio/frases.json, que hace src/alinear.py).
Uso: python src/generar_srt.py audio/frases.json final/VIDEO.srt
Reglas: máximo 42 caracteres por línea, máximo 2 líneas y entre 1 y 7 s por subtítulo; frases largas se parten.
"""
import json, sys

frases = json.load(open(sys.argv[1], encoding='utf-8'))
MAXL, MAXS = 42, 7.0

def lineas(txt):
    out, cur = [], ''
    for w in txt.split():
        if len(cur) + len(w) + 1 > MAXL and cur:
            out.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    return out + ([cur] if cur else [])

def ts(t):
    h, r = divmod(max(0.0, t), 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}'

subs = []
for f in frases:
    ls = lineas(f['texto'].strip('[]'))
    bloques = [ls[i:i + 2] for i in range(0, len(ls), 2)]
    total = sum(len(' '.join(b)) for b in bloques) or 1
    t = f['s']
    for b in bloques:
        d = (f['e'] - f['s']) * len(' '.join(b)) / total
        subs.append((t, min(t + max(d, 1.0), t + MAXS), '\n'.join(b))); t += d

with open(sys.argv[2], 'w', encoding='utf-8') as fh:
    for k, (a, b, txt) in enumerate(subs, 1):
        fh.write(f'{k}\n{ts(a)} --> {ts(b)}\n{txt}\n\n')
print(sys.argv[2], len(subs), 'subtítulos')
