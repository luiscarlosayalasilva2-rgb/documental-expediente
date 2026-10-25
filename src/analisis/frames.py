import sys, re, json, os
d = sys.argv[1]

def load(name, key):
    t, v = [], []
    cur = None
    for line in open(os.path.join(d, name), encoding='utf-8', errors='ignore'):
        m = re.search(r'pts_time:([\d.]+)', line)
        if m:
            cur = float(m.group(1)); continue
        m = re.search(key + r'=([-\d.]+)', line)
        if m and cur is not None:
            t.append(cur); v.append(float(m.group(1)))
    return t, v

t, sc = load('sc.txt', 'scene_score')
_, y = load('yavg.txt', 'YAVG')
_, s = load('sat.txt', 'SATAVG')
n = len(t)
fps = 30
def ts(x):
    return f"{int(x//60)}:{x%60:05.2f}"

# 1) hard cuts: single-frame peaks > 0.3, merged within 10 frames
cuts = []
for i in range(1, n - 1):
    if sc[i] > 0.3 and sc[i] >= sc[i-1] and sc[i] >= sc[i+1]:
        if cuts and i - cuts[-1] < 10:
            if sc[i] > sc[cuts[-1]]: cuts[-1] = i
            continue
        cuts.append(i)

# classify each cut by activity in neighbouring frames
types = {'seco': [], 'gradual': []}
for i in cuts:
    neigh = [sc[j] for j in range(max(0, i-8), min(n, i+9)) if j != i]
    active = sum(1 for v in neigh if v > 0.04)
    (types['gradual'] if active >= 4 else types['seco']).append(i)

# 2) gradual transitions with no hard peak: 15-frame window sum > 0.35, max < 0.3
grad = []
w = 15
run = sum(sc[:w])
for i in range(w, n):
    run += sc[i] - sc[i-w]
    a = i - w + 1
    win = sc[a:i+1]
    if run > 0.35 and max(win) < 0.3:
        if not any(abs(a - c) < 20 for c in cuts) and (not grad or a - grad[-1] > 30):
            grad.append(a)

# 3) darkening events: brightness drops to < 62% of the level 0.5 s before and stays >= 0.8 s
dark = []
i = 15
while i < n - 24:
    base = sum(y[i-15:i-5]) / 10
    if base > 40 and y[i] < base * 0.62 and all(y[k] < base * 0.7 for k in range(i, i + 24)):
        dark.append((i, base, y[i]))
        k = i
        while k < n and y[k] < base * 0.75: k += 1
        i = k + 1
        continue
    i += 1

# 4) paper backgrounds: bright, low saturation >= 1 s
paper = []
i = 0
while i < n:
    if y[i] > 175 and s[i] < 22:
        k = i
        while k < n and y[k] > 165 and s[k] < 28: k += 1
        if k - i >= 30: paper.append((i, k))
        i = k + 1
        continue
    i += 1

# 5) flashes: brightness jump > 60 above both neighbours windows, short (<= 6 frames)
flash = []
for i in range(6, n - 6):
    if y[i] - max(y[i-6], y[i+6]) > 60 and (not flash or i - flash[-1] > 15):
        flash.append(i)

# 6) black frames
black = []
i = 0
while i < n:
    if y[i] < 22:
        k = i
        while k < n and y[k] < 22: k += 1
        if k - i >= 3: black.append((i, k))
        i = k + 1; continue
    i += 1

out = {
    'frames': n,
    'cuts': len(cuts),
    'cuts_seco': len(types['seco']),
    'cuts_gradual': [ts(t[i]) for i in types['gradual']],
    'gradual_sin_pico': [ts(t[i]) for i in grad],
    'oscurecimientos': len(dark),
    'oscurecimientos_t': [ts(t[i]) for i, _, _ in dark],
    'papel': len(paper),
    'papel_t': [f"{ts(t[a])}-{ts(t[b-1])}" for a, b in paper],
    'flashes': [ts(t[i]) for i in flash],
    'negro': [f"{ts(t[a])} ({(b-a)/fps:.2f}s)" for a, b in black],
}
json.dump(out, open(os.path.join(d, 'analisis.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, ':', v if not isinstance(v, list) else f"{len(v)} -> {v}")
