"""Genera final/edl_hd.json: reemplaza cada foto por su mejor versión disponible.

Orden: 1) elección manual (foto HD nueva, horizontal, del mismo tema), 2) la misma foto en HD (mapa_hd.json),
3) versión agrandada con Real-ESRGAN (media/hd_esrgan), 4) la original.
Las claves "archivo@segundo" cambian solo ese plano; "archivo" cambia todos sus usos.
"""
import json, os
from PIL import Image

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HD = lambda n: os.path.join(R, 'media', 'google_hd', n)

MANUAL = {
    # intro + parada 12
    'intro_tienda_01.jpg': 'hd_intro_tienda_01.jpg',
    'p12_colegio_06.jpg': 'hd_p12_colegio_00.jpg',
    'p12_monedas_05.jpg': 'hd_p12_monedas_00.jpg',
    'p12_carrito_05.jpg': 'hd_p12_carrito_04.jpg',
    'p12_baloncito_05.jpg': 'hd_p12_baloncito_01.jpg',
    'p12_baloncito_02.jpg': 'hd_p12_baloncito_00.jpg',
    'p12_mundial_03.jpg': 'hd_p12_mundial_02.jpg',
    'p12_mundial_05.jpg': 'hd_p12_mundial_01.jpg',
    'p12_carrito_04.jpg': 'hd_p12_carrito_00.jpg',
    'p12_coladetigre_05.jpg': 'hd_p12_coladetigre_03.jpg',
    # 11 Betatonio
    'b11_betatonio_03.jpg': 'hd_b11_betatonio_00.jpg',
    'b11_videoclub_01.jpg': 'hd_b11_videoclub_00.jpg',
    'b11_videoclub_04.jpg': 'hd_b11_betatonio_02.jpg',
    'b11_nintendo_05.jpg': 'hd_b11_nintendo_05.jpg',
    'b11_nintendo_00.jpg': 'hd_b11_nintendo_02.jpg',
    'b11_nintendo_02.jpg': 'hd_b11_nintendo_01.jpg',
    'b11_rebobinar_01.jpg': 'hd_b11_betatonio_04.jpg',
    'b11_nintendo_04.jpg': 'hd_b11_videoclub_00.jpg',
    # 10 Konga
    'b10_konga_publi_01.jpg@152': 'hd_b10_konga_03.jpg',
    'b10_konga_publi_01.jpg@150': 'hd_b10_konga_03.jpg',
    'soda_bottles_glass_2.jpg': 'hd_b10_konga_00.jpg',
    # 9 Granahorrar
    'b09_casa_02.jpg@190': 'hd_b09_casa_01.jpg',
    'b09_granahorrar_03.jpg': 'hd_b09_granahorrar_00.jpg',
    'b09_granahorrar_04.jpg': 'hd_b09_granahorrar_05.jpg',
    'b09_caballos_01.jpg': 'hd_b09_granahorrar_04.jpg',
    'b09_libreta_00.jpg': 'hd_b09_libreta_00.jpg',
    'b09_granahorrar_07.jpg': 'hd_b09_granahorrar_02.jpg',
    # 8 Telecom
    'b08_caballo_02.jpg': 'hd_b08_caballo_00.jpg',
    'b08_caballo_04.jpg': 'hd_b08_caballo_01.jpg',
    'b08_telecom_02.jpg': 'hd_b08_fila_03.jpg',
    'b08_publico_03.jpg': 'hd_b08_publico_03.jpg',
    'b08_telecom_05.jpg': 'hd_b08_publico_04.jpg',
    'b08_publico_02.jpg': 'hd_b08_fila_00.jpg',
    'b08_publico_01.jpg': 'hd_b08_telecom_04.jpg',
    # 7 Caravana
    'b07_escaleras_00.jpg': 'hd_b07_escaleras_00.jpg',
    'b07_carabobo_04.jpg': 'hd_b07_centro_00.jpg',
    'b07_centro_02.jpg': 'hd_b07_centro_02.jpg',
    'b07_centro_04.jpg': 'hd_b07_centro_04.jpg',
    'escalator_vintage_3.jpg': 'hd_b07_escaleras_03.jpg',
    # 6 Leona
    'b06_leona_02.jpg': 'hd_b06_leona_01.jpg',
    # 5 La 14
    'children_playground_school_3.jpg@465': 'hd_b05_calima_01.jpg',
    'children_playground_school_2.jpg@469': 'hd_b05_calima_00.jpg',
    'colombian_empanadas_1.jpg@473': 'hd_b03_cafeteria_00.jpg',
    'b05_cierre_02.jpg@475': 'hd_b05_cierre_02.jpg',
    'b05_cilantro_03.jpg': 'hd_b05_cilantro_01.jpg',
    'b05_cilantro_04.jpg': 'hd_b05_cilantro_03.jpg',
    'b05_cierre_03.jpg': 'hd_b05_la14_03.jpg',
    'b05_cierre_01.jpg': 'hd_b05_la14_02.jpg',
    # 4 Chupi Plum
    'b04_chupiplum_02.jpg': 'hd_b04_chupiplum_00.jpg',
    'b04_tatuaje_01.jpg': 'hd_b04_tatuaje_02.jpg',
    # 3 Tía
    'b03_bogota_04.jpg': 'hd_b03_bogota_01.jpg',
    'b03_tia_05.jpg': 'hd_b03_tia_01.jpg',
    'b03_tia_03.jpg': 'hd_b03_tia_04.jpg',
    'b03_cierre_03.jpg': 'hd_b03_tia_02.jpg',
    'b03_cierre_05.jpg': 'hd_b03_cierre_02.jpg',
    'b03_cierre_02.jpg': 'hd_b03_cierre_04.jpg',
    'b03_cierre_01.jpg': 'hd_b03_cierre_00.jpg',
    'colombian_empanadas_1.jpg@612': 'hd_b03_cafeteria_01.jpg',
    'colombian_empanadas_1.jpg@570': 'hd_b03_cafeteria_03.jpg',
    # 2 Ley
    'b02_ley_01.jpg': 'hd_b02_ley2_00.jpg',
    'b02_ley_04.jpg': 'hd_b02_ley_04.jpg',
    'b02_ley_06.jpg': 'hd_b02_ley_05.jpg',
    'b02_pueblo_03.jpg': 'hd_b02_pueblo_00.jpg',
    'b02_pueblo_01.jpg': 'hd_b02_pueblo_03.jpg',
    'b02_ley_02.jpg@679': 'hd_b02_ley2_01.jpg',
    'b02_donjulio_03.jpg': 'hd_b02_donjulio_01.jpg',
    'colombian_empanadas_1.jpg@683': 'hd_b03_cafeteria_02.jpg',
    # 1 Conavi y cierre
    'b01_alcancia_04.jpg@734': 'hd_b01_conavi_02.jpg',
    'b01_mil_01.jpg': 'hd_b01_mil_01.jpg',
    'b01_natilla_00.jpg': 'hd_b01_natilla_00.jpg',
    'b01_conavi_04.jpg@796': 'hd_b01_tarjeta_01.jpg',
    'b01_tarjeta_02.jpg': 'hd_b01_conavi_01.jpg',
    'grandmother_hands_3.jpg': 'hd_b01_tarjeta_03.jpg',
    'b00_familia_02.jpg': 'hd_b00_familia_01.jpg',
}

edl = json.load(open(os.path.join(R, 'final', 'edl_completo.json'), encoding='utf-8'))
auto = json.load(open(os.path.join(R, 'final', 'mapa_hd.json'), encoding='utf-8'))
cuenta = {'manual': 0, 'misma_hd': 0, 'esrgan': 0, 'original': 0}

def agrandada(src):
    up = os.path.join(R, 'media', 'hd_esrgan', os.path.splitext(os.path.basename(src))[0] + '.jpg')
    return up if os.path.exists(up) and Image.open(src).width < 1000 else None

def mejor(src, t0):
    b = os.path.basename(src)
    elegido, tipo = src, 'original'
    for k in (f'{b}@{int(t0)}', b):
        if k in MANUAL and os.path.exists(HD(MANUAL[k])):
            elegido, tipo = HD(MANUAL[k]), 'manual'; break
    else:
        if src in auto:
            elegido, tipo = auto[src], 'misma_hd'
    up = agrandada(elegido)
    if up:
        elegido, tipo = up, ('esrgan' if tipo == 'original' else tipo + '+esrgan')
    cuenta[tipo] = cuenta.get(tipo, 0) + 1
    return elegido

for p in edl['planos']:
    if p['tipo'] == 'imagen':
        p['src'] = mejor(p['src'], p['t0'])
    elif p['tipo'] == 'papel':
        for f in p['papel']['fotos']:
            f['src'] = mejor(f['src'], p['t0'])

faltan = [k for k, v in MANUAL.items() if not os.path.exists(HD(v))]
assert not faltan, faltan
json.dump(edl, open(os.path.join(R, 'final', 'edl_hd.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(cuenta)
