import sys, subprocess, struct, math
src = sys.argv[1]
# (label, onset seconds) of overlays measured frame by frame
events = [
    ('FILE escribe DANESA 33', 486.8), ('FILE HELADOS BING', 53.9), ('palabra CONFIABA', 45.1),
    ('numero 33', 74.9), ('numero 160', 21.5), ('EXHIBIT A', 384.0), ('polaroid PENAFIEL', 1410.3),
    ('desliz papel 0:57', 57.2), ('collage glitch', 273.9), ('palabra BANCARROTA', 633.6),
]
SR = 22050
def pcm(start, dur, hp):
    af = f'highpass=f={hp}' if hp else 'anull'
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(dur), '-i', src, '-vn', '-ac', '1',
           '-ar', str(SR), '-af', af, '-f', 's16le', '-']
    raw = subprocess.run(cmd, capture_output=True).stdout
    return struct.unpack('<%dh' % (len(raw) // 2), raw)

def env(x, win):
    out = []
    for i in range(0, len(x) - win, win):
        seg = x[i:i + win]
        r = math.sqrt(sum(v * v for v in seg) / win) or 1e-9
        out.append(20 * math.log10(r / 32768))
    return out

win = SR // 50  # 20 ms
for label, t in events:
    full = env(pcm(t - 1.0, 2.5, None), win)
    hf = env(pcm(t - 1.0, 2.5, 4000), win)
    pre_full = sorted(full[:40])[20]
    on_full = max(full[45:65])
    pre_hf = sorted(hf[:40])[20]
    on_hf = max(hf[45:65])
    quiet = sum(1 for v in full[45:75] if v < -45)
    print(f"{label:24s} total antes {pre_full:6.1f} / al entrar {on_full:6.1f} dB | agudos(>4kHz) antes {pre_hf:6.1f} / al entrar {on_hf:6.1f} dB | ventanas silenciosas tras la entrada: {quiet}")
