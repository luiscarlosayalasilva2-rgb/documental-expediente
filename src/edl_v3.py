"""Versión final: parte de final/edl_hd.json y aplica
1) más video real (clips de Pixabay que coinciden con la frase),
2) sin fotos repetidas (salvo el carrusel de repaso del cierre),
3) fotos limpias (limpiar.py recorta logos, firmas y marcos).
CAMBIOS = {índice de plano: fuente}. 'v:' = clip de media/pixabay_v2, 'v1:' = media/pixabay_v, '#bw' = blanco y negro.
"""
import json, os
import limpiar

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
G = lambda n: os.path.join(R, 'media', 'google_hd', n)

CAMBIOS = {
    # intro
    7: 'v:colombia_old_town_street_3.mp4',
    221: 'hd_intro_tienda_04.jpg',
    # 12 Baloncito
    10: 'hd_p12_colegio_01.jpg',
    22: 'v:popsicle_eating_1.mp4',
    # 11 Betatonio
    24: 'v:bogota_colombia_street_3.mp4',
    28: 'hd_b11_videoclub_04.jpg',
    35: 'hd_b11_betatonio_03.jpg',
    40: 'hd_b11_betatonio_00.jpg#bw',
    43: 'v:video_rental_store_2.mp4',
    44: 'hd_b11_videoclub_03.jpg',
    # 10 Konga
    46: 'hd_b10_konga_02.jpg',
    51: 'fusionar',
    52: 'v:children_playing_soccer_street_1.mp4',
    58: 'v:family_lunch_table_3.mp4',
    # 9 Granahorrar
    64: 'v:horses_running_herd_2.mp4',
    66: 'b09_caballos_02.jpg',
    71: 'v:house_keys_door_1.mp4',
    74: 'hd_b09_casa_00.jpg#bw',
    76: 'hd_b09_granahorrar_01.jpg#bw',
    # 8 Telecom
    93: 'hd_b08_telecom_00.jpg',
    96: 'hd_b08_edificio_02.jpg',
    99: 'hd_b08_publico_05.jpg',
    # 7 Caravana
    109: 'hd_b07_caravana_03.jpg#bw',
    112: 'v:escalator_shopping_mall_2.mp4',
    114: 'v:department_store_2.mp4',
    # 6 Leona
    116: 'old_television_football_1.jpg',
    117: 'hd_b06_malta_02.jpg',
    119: 'hd_b06_malta_00.jpg',
    123: 'hd_b06_rana_00.jpg',
    124: 'v:watching_football_tv_family_2.mp4',
    125: 'hd_b06_malta_04.jpg',
    126: 'hd_b06_malta_01.jpg',
    127: 'hd_b06_leona_00.jpg',
    128: 'hd_b06_leona_01.jpg#bw',
    129: 'v1:rain_window_2.mp4',
    130: 'v:bogota_colombia_street_2.mp4',
    # 5 La 14
    131: 'v:cali_colombia_2.mp4',
    138: 'v:cilantro_herbs_market_3.mp4',
    142: 'v:empty_shopping_mall_closed_3.mp4',
    144: 'hd_b05_la14_04.jpg',
    145: 'hd_b05_la14_05.jpg',
    # 4 Chupi Plum
    150: 'hd_b04_tatuaje_00.jpg',
    157: 'v:empty_shopping_mall_closed_1.mp4',
    160: 'hd_b04_recreo_04.jpg',
    # 3 Tía
    162: 'v1:coffee_grinder_2.mp4',
    167: 'hd_b03_cierre_05.jpg',
    169: 'hd_b03_tia_05.jpg#bw',
    171: 'hd_b03_bogota_00.jpg',
    176: 'hd_b03_cierre_03.jpg',
    179: 'hd_b03_cierre_01.jpg',
    180: 'hd_b03_tia_00.jpg#bw',
    # 2 Ley
    192: 'v:department_store_3.mp4',
    193: 'hd_b02_ley_02.jpg',
    194: 'v:escalator_shopping_mall_1.mp4',
    199: 'v:empty_shopping_mall_closed_2.mp4',
    # 1 Conavi y cierre
    201: 'v:medellin_colombia_city_1.mp4',
    209: 'hd_b01_mil_02.jpg',
    210: 'v:children_playing_soccer_street_3.mp4',
    211: 'hd_b01_tarjeta_02.jpg',
    212: 'hd_b01_conavi_04.jpg#bw',
    214: 'hd_b01_tarjeta_00.jpg',
    218: 'hd_b09_abuela_00.jpg',
}

edl = json.load(open(os.path.join(R, 'final', 'edl_hd.json'), encoding='utf-8'))
P = edl['planos']
for i, f in CAMBIOS.items():
    p = P[i]
    if f == 'fusionar':
        continue
    bw = f.endswith('#bw'); f = f.replace('#bw', '')
    base = {'t0': p['t0'], 't1': p['t1']}
    if f.startswith(('v:', 'v1:')):
        carpeta = 'pixabay_v2' if f.startswith('v:') else 'pixabay_v'
        P[i] = {**base, 'tipo': 'video', 'src': os.path.join(R, 'media', carpeta, f.split(':', 1)[1]), 'ss': 1.0, 'bw': bw}
    else:
        src = next((c for c in (G(f), os.path.join(R, 'media', 'google', f), os.path.join(R, 'media', 'pixabay', f)) if os.path.exists(c)), G(f))
        up = os.path.join(R, 'media', 'hd_esrgan', os.path.splitext(f)[0] + '.jpg')
        if os.path.exists(up): src = up
        P[i] = {**base, 'tipo': 'imagen', 'src': src, 'bw': bw, 'mov': p.get('mov') or {'z0': 1.0, 'z1': 1.07}}
ESR = lambda n: os.path.join(R, 'media', 'hd_esrgan', n)
P[8]['papel']['fotos'][0]['src'] = G('hd_intro_tienda_02.jpg')
P[103]['papel']['fotos'][1]['src'] = ESR('b02_ley_01.jpg')
P[103]['papel']['fotos'][2]['src'] = ESR('b03_tia_05.jpg')
P[217]['papel']['fotos'][0]['src'] = G('hd_b01_conavi_00.jpg')
P[128] = {'t0': P[128]['t0'], 't1': P[128]['t1'], 'tipo': 'video', 'src': os.path.join(R, 'media', 'pixabay_v2', 'beer_bottles_cold_2.mp4'), 'ss': 1.0, 'bw': True}
# fusionar: el plano anterior se alarga
for i in sorted((i for i, f in CAMBIOS.items() if f == 'fusionar'), reverse=True):
    P[i - 1]['t1'] = P[i]['t1']; del P[i]

for p in P:
    if p['tipo'] == 'imagen': p['src'] = limpiar.limpiar(p['src'])
    if p['tipo'] == 'papel':
        for f in p['papel']['fotos']: f['src'] = limpiar.limpiar(f['src'])

# comprobaciones: todo existe, sin huecos, sin repetidos fuera del carrusel
import subprocess
from collections import Counter
for a, b in zip(P, P[1:]):
    assert abs(a['t1'] - b['t0']) < 0.05, (a['t1'], b['t0'])
usos = Counter()
for p in P:
    fs = [p['src']] if p.get('src') else ([] if p['papel']['modo'] == 'carrusel' else [f['src'] for f in p['papel']['fotos']])
    for f in fs:
        assert os.path.exists(f), f
        usos[os.path.basename(f)] += 1
for p in P:
    if p['tipo'] == 'video':
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p['src']], capture_output=True, text=True).stdout)
        if d < p['t1'] - p['t0'] + p.get('ss', 0) + 0.2:
            p['ss'] = 0.0
        assert d >= p['t1'] - p['t0'] + 0.2, ('clip corto', p['src'], d)
rep = {k: v for k, v in usos.items() if v > 1}
json.dump(edl, open(os.path.join(R, 'final', 'edl_v3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('planos', len(P), '| video', sum(p['tipo'] == 'video' for p in P), '| repetidos', rep)
