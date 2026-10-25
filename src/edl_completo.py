"""EDL del video completo (0 - 832.24 s): intro + 12 paradas + cierre.

La intro y la Parada 12 vienen del demo aprobado (edl_demo.py). Cada parada abre con su número rojo
(feedback del usuario: las 12 marcas salen enumeradas) y la ficha FILE con etiqueta "PARADA N".
Los tiempos de cifras dentro de frases largas se buscan en audio/palabras.json con w().
"""
import json, os, re, unicodedata
import edl_demo as demo

R = demo.R
g, px = demo.g, demo.px
pv = lambda n: os.path.join(R, 'media', 'pixabay_v', n)
DUR = 832.24

PAL = json.load(open(os.path.join(R, 'audio', 'palabras.json'), encoding='utf-8'))
def _n(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))
def w(palabra, desde, defecto):
    """Segundo en que se dice `palabra` (primera vez después de `desde`); si no aparece, `defecto`."""
    p = _n(palabra)
    for x in PAL:
        if x['s'] >= desde and _n(x['w']).startswith(p):
            return round(x['s'], 2)
    return defecto

_zoom = [(1.0, 1.07), (1.07, 1.0), (1.0, 1.06), (1.06, 1.0)]
_k = [0]
def foto(t0, t1, src, **kw):
    z0, z1 = _zoom[_k[0] % 4]; _k[0] += 1
    return demo.img(t0, t1, src, z0, z1, **kw)
def video(t0, t1, src, ss=1.0, **kw):
    return {'t0': t0, 't1': t1, 'tipo': 'video', 'src': src, 'ss': ss, **kw}

def seg(t0, t1, fuentes):
    """Reparte el tramo [t0, t1) en partes iguales entre las fuentes (rutas o planos ya hechos)."""
    out, n = [], len(fuentes)
    for i, f in enumerate(fuentes):
        a, b = t0 + (t1 - t0) * i / n, t0 + (t1 - t0) * (i + 1) / n
        if isinstance(f, dict):
            out.append({**f, 't0': a, 't1': b})
        elif f.endswith('.mp4'):
            out.append(video(a, b, f))
        else:
            out.append(foto(a, b, f, bw=f.endswith('#bw')) if not f.endswith('#bw') else foto(a, b, f[:-3], bw=True))
    return out

def tramos(lista, fin):
    """lista = [(inicio, [fuentes]), ...]: cada tramo dura hasta el inicio del siguiente."""
    out = []
    for i, (t0, fu) in enumerate(lista):
        t1 = lista[i + 1][0] if i + 1 < len(lista) else fin
        out += seg(t0, t1, fu)
    return out

def P(modo, fotos, **kw):
    return {'tipo': 'papel', 'papel': {'modo': modo, 'fotos': fotos, **kw}}

capas = []
def numero(t, num, label, dur=2.4, grande=False): capas.append({'tipo': 'numero', 't': t, 'dur': dur, 'num': num, 'label': label, 'grande': grande})
def palabra(t, pal, sub, dur=2.9): capas.append({'tipo': 'palabra', 't': t, 'dur': dur, 'palabra': pal, 'sub': sub})
def nota(t, txt, res, dur=3.0): capas.append({'tipo': 'nota', 't': t, 'dur': dur, 'texto': txt, 'resaltar': res})
def ficha(t, n, txt, dur=4.0): capas.append({'tipo': 'file', 't': t, 'dur': dur, 'texto': txt, 'etiqueta': f'Parada {n}'})
def abre(t, n, marca):
    numero(t, str(n), marca, 2.3, grande=True)
    ficha(t + 2.35, n, marca)

# ---------------- INTRO + PARADA 12 (demo aprobado) ----------------
planos = [p for p in demo.planos]
capas += [c for c in demo.capas if c['tipo'] != 'file']
capas[-1] = {**capas[-1], 'dur': 2.6}  # PREMIO termina antes del número 11
abre(25.0, 12, 'Helados Baloncito')
planos[-1] = {**planos[-1], 't1': 77.1}

# ---------------- PARADA 11 — Betatonio ----------------
planos += tramos([
    (77.1, [pv('old_television_static_2.mp4')]),
    (78.0, [g('b11_betatonio_03.jpg'), g('b11_betatonio_01.jpg')]),
    (82.5, [g('b11_videoclub_01.jpg'), g('b11_videoclub_02.jpg')]),
    (87.1, [px('vhs_tapes_shelf_2.jpg'), g('b11_videoclub_04.jpg')]),
    (91.8, [g('b11_betatonio_06.jpg'), g('b11_nintendo_05.jpg')]),
    (98.9, [g('b11_rebobinar_03.jpg')]),
    (101.5, [P('polaroid', [{'src': g('b11_betatonio_00.jpg'), 'pie': 'Betatonio, Bogotá'},
                            {'src': g('b11_carnet_01.jpg'), 'pie': 'Promociones para socios'}])]),
    (109.1, [g('b11_betatonio_05.jpg')]),
    (113.2, [g('b11_betatonio_00.jpg')]),
    (117.3, [g('b11_nintendo_00.jpg'), g('b11_nintendo_02.jpg')]),
    (121.4, [pv('vhs_player_insert_tape_1.mp4'), g('b11_rebobinar_01.jpg')]),
    (127.6, [g('b11_betatonio_01.jpg') + '#bw']),
    (130.4, [g('b11_dvd_03.jpg'), g('b11_dvd_02.jpg')]),
    (133.7, [g('b11_nintendo_04.jpg'), pv('old_television_static_1.mp4')]),
], 144.2)
abre(77.1, 11, 'Betatonio')
palabra(w('socio', 109, 111.9), 'Socio', '«Era pupi estar afiliado a Betatonio».', 3.0)
nota(w('rebobinada', 121.4, 124.6) - 0.6, 'La cinta se devolvía rebobinada… o se pagaba la multa.', ['rebobinada'], 3.2)
numero(w('27', 127.6, 128.6), '27', 'años abierto', 1.5)
numero(w('2007', 129.0, 130.4), '2007', 'año de cierre', 2.2)
palabra(142.3, 'Pantalla', 'Eso no lo ha reemplazado ninguna pantalla.', 1.9)

# ---------------- PARADA 10 — Konga ----------------
planos += tramos([
    (144.2, [g('b10_konga_06.jpg')]),
    (150.2, [g('b10_konga_publi_01.jpg')]),
    (152.2, [P('vs', [{'src': g('b10_konga_publi_01.jpg'), 'pie': 'Konga · Bavaria'},
                      {'src': g('b10_postobon_04.jpg'), 'pie': 'Manzana · Postobón'}],
               titulo='Konga vs Postobón', sub='La guerra de las gaseosas de los noventa')]),
    (160.8, [g('b10_link_00.jpg'), g('b10_link_01.jpg')]),
    (163.9, [px('soda_bottles_glass_2.jpg'), g('b10_konga_06.jpg')]),
    (167.6, [g('b10_link_04.jpg'), g('b10_postobon_00.jpg')]),
    (173.4, [g('b10_postobon_01.jpg')]),
    (177.1, [g('b10_almuerzo_01.jpg')]),
    (181.6, [g('b10_konga_publi_01.jpg') + '#bw']),
    (183.4, [g('b10_almuerzo_03.jpg'), g('b10_almuerzo_00.jpg')]),
], 190.3)
abre(144.2, 10, 'Gaseosas Konga')
palabra(150.3, 'Rebelde', 'Era la gaseosa rebelde de los noventa.', 1.9)
nota(173.5, '«La de manzana era mejor que la de Postobón».', ['manzana'], 3.3)
palabra(w('honor', 186.0, 188.9) - 1.2, 'Honor', 'Hasta la gaseosa del almuerzo era una cuestión de honor.', 1.65)

# ---------------- PARADA 9 — Granahorrar ----------------
t1975, t15, t1990 = w('1975', 219.6, 223.0), w('quince', 219.6, 225.5), w('1990', 225, 228.5)
planos += tramos([
    (190.3, [g('b09_casa_02.jpg'), g('b09_casa_05.jpg')]),
    (195.1, [g('b09_casa_03.jpg')]),
    (196.9, [g('b09_granahorrar_00.jpg'), g('b09_granahorrar_03.jpg')]),
    (202.4, [g('b09_caballos_02.jpg'), g('b09_granahorrar_04.jpg'), g('b09_caballos_01.jpg')]),
    (215.5, [g('b09_abuela_00.jpg')]),
    (219.6, [g('b09_casa_01.jpg'), px('house_keys_hand_2.jpg'), g('b09_libreta_00.jpg')]),
    (232.8, [px('house_keys_hand_3.jpg')]),
    (236.6, [px('grandmother_hands_1.jpg'), g('b09_abuela_03.jpg')]),
    (243.5, [g('b09_casa_05.jpg') + '#bw']),
    (248.6, [g('b09_casa_02.jpg') + '#bw']),
    (254.0, [g('b09_granahorrar_00.jpg') + '#bw']),
    (258.9, [g('b09_granahorrar_07.jpg')]),
], 264.5)
abre(190.3, 9, 'Granahorrar')
numero(t1975, '1975', 'compraron la casa', 2.2)
numero(t15, '15', 'años pagando, cuota por cuota', 2.2)
numero(t1990, '$5.000', 'el último pago, en 1990', 2.4)
palabra(233.6, 'Nuestra', '«Esta casa es nuestra».', 2.4)
palabra(249.0, 'UPAC', 'Casas que terminaron costando mucho más de lo que valían.', 3.4)
numero(w('1998', 254.0, 255.0), '1998', 'año de la intervención', 2.4)
nota(260.2, 'No todo lo que se fue era dulce. Pero todo lo que se fue era nuestro.', ['era nuestro'], 3.7)

# ---------------- PARADA 8 — Telecom ----------------
t2000 = w('dos', 288.8, 289.6)
planos += tramos([
    (264.5, [g('b08_edificio_02.jpg')]),
    (266.6, [g('b08_telecom_04.jpg'), g('b08_publico_04.jpg')]),
    (271.6, [g('b08_edificio_04.jpg')]),
    (274.9, [px('rotary_phone_2.jpg'), pv('telephone_booth_2.mp4')]),
    (279.0, [g('b08_fila_00.jpg'), g('b08_fila_04.jpg')]),
    (283.3, [g('b08_caballo_02.jpg'), g('b08_caballo_04.jpg')]),
    (288.8, [g('b08_telecom_02.jpg'), g('b08_publico_03.jpg'), pv('rain_window_1.mp4')]),
    (299.5, [P('unica', [{'src': g('b08_mapa_03.jpg'), 'pie': 'Indicativos de larga distancia'}])]),
    (303.9, [px('rotary_phone_1.jpg'), g('b08_telecom_02.jpg')]),
    (312.6, [g('b08_publico_01.jpg')]),
    (317.1, [g('b08_edificio_00.jpg')]),
    (322.1, [g('b08_edificio_00.jpg') + '#bw']),
    (326.1, [g('b08_publico_02.jpg'), g('b08_telecom_05.jpg'), pv('telephone_booth_2.mp4')]),
], 336.6)
abre(264.5, 8, 'Telecom y sus cabinas')
numero(t2000, '$2.000', 'costaba el minuto', 2.4)
palabra(w('aló', 303.9, 306.5) - 0.3, 'Aló, mamá', 'Unas hormiguitas rosadas nos cantaban «Aló, Mamá».', 3.0)
nota(313.8, '«Listo Medellín, cabina 8».', ['cabina 8'], 2.8)
numero(w('2003', 322.1, 322.7), '2003', 'año de la liquidación', 2.4)
palabra(w('gritos', 330.0, 333.2) - 0.5, 'A gritos', 'Esa forma tan nuestra de extrañar a la familia a gritos.', 2.9)

# ---------------- PARADA 7 — Caravana ----------------
planos += tramos([
    (336.6, [g('b07_carabobo_04.jpg'), g('b07_centro_02.jpg')]),
    (341.4, [g('b07_caravana_01.jpg')]),
    (347.6, [P('polaroid', [{'src': g('b07_caravana_04.jpg'), 'pie': 'Caravana'},
                            {'src': g('b02_ley_01.jpg'), 'pie': 'Ley'},
                            {'src': g('b03_tia_05.jpg'), 'pie': 'Tía'}])]),
    (355.0, [g('b07_escaleras_00.jpg')]),
    (360.6, [pv('escalator_people_1.mp4')]),
    (364.0, [g('b07_caravana_03.jpg')]),
    (367.3, [pv('escalator_people_2.mp4'), px('escalator_vintage_3.jpg')]),
    (372.6, [g('b07_caravana_04.jpg') + '#bw']),
    (378.6, [g('b07_centro_04.jpg'), g('b07_carabobo_03.jpg')]),
    (382.2, [g('b07_escaleras_00.jpg'), g('b07_centro_03.jpg')]),
    (390.0, [g('b07_caravana_01.jpg')]),
], 394.3)
abre(336.6, 7, 'Almacenes Caravana')
nota(343.2, '«Caravana, el gigante de los precios enanos».', ['precios enanos'], 3.2)
numero(w('1955', 355.0, 356.6), '1955', 'las primeras escaleras eléctricas de Medellín', 2.6)
numero(w('1998', 372.6, 373.4), '1998', 'año de cierre', 2.3)
palabra(390.2, 'Diversiones', 'El parque de diversiones de los que no tenían para parque de diversiones.', 3.4)

# ---------------- PARADA 6 — Leona ----------------
planos += tramos([
    (394.3, [g('b06_abuelo_03.jpg')]),
    (396.7, [pv('old_television_static_1.mp4'), g('b06_leona_06.jpg'), g('b06_malta_05.jpg')]),
    (406.7, [g('b06_leona_01.jpg'), pv('beer_pouring_glass_1.mp4')]),
    (412.6, [g('b06_leona_02.jpg'), g('b06_leona_06.jpg'), px('beer_bottle_cold_1.jpg')]),
    (423.8, [px('old_television_football_1.jpg'), g('b06_malta_05.jpg')]),
    (433.5, [g('b06_malta_05.jpg'), g('b06_leona_01.jpg')]),
    (442.6, [g('b06_abuelo_03.jpg') + '#bw']),
    (445.5, [px('stickers_album_3.jpg'), g('b00_familia_01.jpg')]),
], 452.4)
abre(394.3, 6, 'Cervecería Leona')
palabra(w('milagro', 430.9, 432.4) - 1.0, 'Milagro', 'Más de uno se las tomó todas esperando el milagro.', 2.4)
palabra(443.8, 'Vacía', 'Y esa silla del abuelo quedó vacía.', 1.7)

# ---------------- PARADA 5 — La 14 ----------------
planos += tramos([
    (452.4, [g('b05_la14_04.jpg')]),
    (458.4, [g('b05_la14_05.jpg')]),
    (459.0, [g('b05_la14_02.jpg')]),
    (465.4, [px('children_playground_school_3.jpg'), px('children_playground_school_2.jpg')]),
    (473.2, [px('colombian_empanadas_1.jpg')]),
    (475.9, [g('b05_cierre_02.jpg')]),
    (480.1, [g('b05_cilantro_01.jpg'), g('b05_cilantro_03.jpg'), g('b05_cilantro_04.jpg')]),
    (492.5, [g('b05_cierre_03.jpg')]),
    (495.5, [px('empty_supermarket_aisle_2.jpg'), px('empty_supermarket_aisle_1.jpg')]),
    (505.8, [g('b05_cierre_01.jpg')]),
    (506.6, [g('b05_la14_05.jpg'), g('b05_cierre_02.jpg')]),
], 514.6)
abre(452.4, 5, 'Almacenes La 14')
numero(w('1964', 459.0, 459.8), '1964', 'año de fundación', 2.3)
nota(462.4, '«¡Siempre te da más!»', ['te da más'], 2.6)
palabra(488.0, 'Cilantro', 'Un almacén que le compraba el cilantro a la señora del barrio.', 3.0)
numero(w('2021', 493.8, 494.3), '2021', 'llegó la liquidación', 2.3)
palabra(511.5, 'Se lloran', 'Las casas, cuando se caen, no se olvidan: se lloran.', 2.9)

# ---------------- PARADA 4 — Chupi Plum ----------------
planos += tramos([
    (514.6, [g('b04_chupiplum_02.jpg')]),
    (517.8, [g('b04_recreo_01.jpg')]),
    (521.2, [g('b04_tatuaje_00.jpg'), g('b04_caja_02.jpg')]),
    (529.4, [g('b04_tatuaje_01.jpg'), g('b04_tatuaje_03.jpg')]),
    (535.5, [g('b04_recreo_02.jpg')]),
    (539.6, [px('stickers_album_3.jpg'), g('b04_album_02.jpg')]),
    (547.7, [g('b04_chupiplum_07.jpg')]),
    (552.4, [g('b04_chupiplum_02.jpg') + '#bw']),
    (553.5, [P('unica', [{'src': g('b04_caja_02.jpg'), 'pie': 'Lo que todavía se guarda'}])]),
    (560.9, [px('children_playground_school_1.jpg'), g('b04_recreo_01.jpg')]),
], 570.0)
numero(514.6, '4', 'Chupi Plum', 1.85, grande=True)
palabra(516.4, '¡Plum!', 'Escuche: ¡PLUM!', 1.4)
ficha(517.9, 4, 'Chupi Plum')
palabra(559.8, 'Recreo', 'No están guardando una caja. Están guardando el recreo.', 1.9)

# ---------------- PARADA 3 — Tía ----------------
t365 = w('365', 597.4, 604.0)
planos += tramos([
    (570.0, [g('b03_bogota_04.jpg'), px('coffee_grinding_beans_3.jpg'), px('colombian_empanadas_1.jpg')]),
    (575.2, [g('b03_tia_05.jpg')]),
    (577.5, [g('b03_tia_03.jpg')]),
    (583.8, [g('b03_cierre_03.jpg')]),
    (585.2, [g('b03_tia_07.jpg'), g('b03_cierre_05.jpg')]),
    (592.0, [g('b03_tia_05.jpg') + '#bw']),
    (597.4, [g('b03_cierre_02.jpg'), g('b03_tia_03.jpg')]),
    (608.6, [g('b03_cierre_01.jpg')]),
    (612.1, [px('colombian_empanadas_1.jpg'), px('coffee_grinding_beans_3.jpg')]),
    (621.3, [g('b03_tia_07.jpg')]),
    (626.8, [g('b03_cierre_02.jpg')]),
    (630.4, [pv('candles_burning_2.mp4'), px('candles_flowers_door_2.jpg')]),
    (637.2, [g('b03_cierre_05.jpg')]),
    (641.0, [g('b03_tia_05.jpg') + '#bw']),
], 643.9)
abre(570.0, 3, 'Almacenes Tía')
numero(w('1940', 577.5, 578.5), '1940', 'año de fundación', 2.2)
nota(w('tiendas', 580.0, 581.2), 'Tiendas Industriales Asociadas', ['T', 'I', 'A'], 2.6)
palabra(w('sabatinas', 594.0, 595.6) - 0.3, 'Sabatinas', 'Niñas de catorce años que trabajaban sábados y domingos.', 2.4)
numero(t365, '$365', 'el paguito del fin de semana', 2.4)
nota(622.8, '«Donde compra como pobre y come como rico».', ['come como rico'], 3.4)
numero(w('2017', 626.8, 628.5) - 0.8, '2017', '23 de noviembre', 2.4)
palabra(635.3, 'Funeral', 'Como en un funeral. Porque eso fue.', 1.8)

# ---------------- PARADA 2 — Ley ----------------
planos += tramos([
    (643.9, [g('b02_ley_02.jpg')]),
    (646.9, [g('b02_ley_01.jpg')]),
    (653.7, [g('b02_ley_04.jpg')]),
    (658.6, [g('b02_ley_06.jpg')]),
    (661.3, [g('b02_pueblo_03.jpg'), g('b02_pueblo_01.jpg'), pv('christmas_lights_town_2.mp4')]),
    (670.3, [g('b02_perros_01.jpg'), pv('supermarket_shopping_1.mp4')]),
    (679.2, [g('b02_ley_02.jpg')]),
    (683.2, [px('colombian_empanadas_1.jpg')]),
    (686.2, [g('b02_ley_04.jpg') + '#bw']),
    (688.6, [g('b02_ley_01.jpg'), g('b02_ley_06.jpg')]),
    (699.8, [g('b02_donjulio_02.jpg'), g('b02_donjulio_03.jpg')]),
    (707.1, [g('b02_exito_00.jpg'), g('b02_exito_02.jpg')]),
    (717.8, [g('b02_ley_02.jpg') + '#bw']),
], 722.3)
abre(643.9, 2, 'Almacenes Ley')
palabra(650.6, 'Ley', 'A secas. Nunca «El Ley».', 2.7)
numero(w('1922', 653.7, 656.8), '1922', 'lo fundó Luis Eduardo Yepes', 2.4)
numero(w('57', 688.6, 691.5), '$57', 'ganaba la supervisora', 2.2)
palabra(697.9, 'Enamorados', 'Se enamoraron entre esos pasillos.', 1.8)
numero(w('2012', 711.3, 715.8), '2012', 'el último Ley se volvió Éxito', 2.3)
palabra(719.8, 'Adioses', 'Hubo una década entera de adioses chiquitos.', 2.0)

# ---------------- PARADA 1 — Conavi ----------------
planos += tramos([
    (722.3, [g('b01_conavi_01.jpg')]),
    (729.0, [g('b01_conavi_01.jpg') + '#bw']),
    (734.9, [g('b01_alcancia_04.jpg')]),
    (738.9, [pv('coins_piggy_bank_2.mp4'), g('b01_natilla_00.jpg')]),
    (746.1, [g('b00_familia_01.jpg'), g('b00_familia_02.jpg')]),
    (757.2, [g('b01_alcancia_04.jpg')]),
    (759.6, [g('b01_mil_01.jpg'), pv('coins_piggy_bank_2.mp4')]),
    (772.2, [px('old_television_football_1.jpg'), g('b01_conavi_01.jpg')]),
    (781.9, [g('b01_conavi_01.jpg') + '#bw']),
    (785.7, [px('grandmother_hands_3.jpg'), px('old_wallet_leather_2.jpg')]),
    (796.2, [g('b01_conavi_04.jpg'), g('b01_tarjeta_02.jpg')]),
    (805.7, [P('polaroid', [{'src': g('b01_alcancia_04.jpg'), 'pie': 'La alcancía de la casa'},
                            {'src': g('b01_conavi_04.jpg'), 'pie': 'La abejita volvió'}])]),
], 809.4)
abre(722.3, 1, 'Conavi, la abejita')
numero(w('1974', 729.0, 730.0), '1974', 'nació en Medellín', 2.3)
nota(769.1, 'Así, moneda por moneda, aprendimos a ahorrar.', ['aprendimos a ahorrar'], 2.6)
nota(778.7, '«Conavi quiere a la gente».', ['quiere a la gente'], 2.6)
numero(w('2005', 781.9, 782.4), '2005', 'se unió con Bancolombia', 2.4)
palabra(803.7, 'Abejita', 'No por un banco. Por una abejita.', 1.9)

# ---------------- CIERRE ----------------
planos += tramos([
    (809.4, [g('b00_familia_01.jpg')]),
    (811.8, [P('carrusel', [{'src': g('p12_baloncito_05.jpg'), 'pie': '12 · Baloncito'},
                            {'src': g('b11_betatonio_03.jpg'), 'pie': '11 · Betatonio'},
                            {'src': g('b10_konga_06.jpg'), 'pie': '10 · Konga'},
                            {'src': g('b08_publico_04.jpg'), 'pie': '8 · Telecom'},
                            {'src': g('b05_la14_04.jpg'), 'pie': '5 · La 14'},
                            {'src': g('b03_tia_07.jpg'), 'pie': '3 · Tía'},
                            {'src': g('b01_conavi_01.jpg'), 'pie': '1 · Conavi'}])]),
    (822.1, [g('b00_dulces_01.jpg')]),
    (829.5, [g('intro_tienda_00.jpg') + '#bw']),
], DUR)
numero(809.4, '12', 'paradas, doce marcas', 2.3)
palabra(830.9, 'Pasado', 'Nos vemos en el pasado.', DUR - 830.9)

# ---------------- comprobaciones ----------------
planos.sort(key=lambda p: p['t0'])
for a, b in zip(planos, planos[1:]):
    assert abs(a['t1'] - b['t0']) < 0.05, ('hueco o solape', a['t1'], b['t0'], a.get('src'))
faltan = [p['src'] for p in planos if p.get('src') and not os.path.exists(p['src'])]
faltan += [f['src'] for p in planos if p['tipo'] == 'papel' for f in p['papel']['fotos'] if not os.path.exists(f['src'])]
assert not faltan, faltan
capas.sort(key=lambda c: c['t'])
os.makedirs(os.path.join(R, 'final'), exist_ok=True)
edl = {'dur': DUR, 'audio': os.path.join(R, 'audio', 'voz_final.wav'), 'planos': planos, 'capas': capas}
json.dump(edl, open(os.path.join(R, 'final', 'edl_completo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('planos', len(planos), '| capas', len(capas), '| duración media de plano', round(DUR / len(planos), 2), 's')
for a, b in zip(capas, capas[1:]):
    if b['t'] < a['t'] + a['dur'] - 0.05 and {a['tipo'], b['tipo']} & {'numero', 'palabra'} and a['tipo'] != 'file' and b['tipo'] != 'file':
        print('  capas encimadas:', a['tipo'], round(a['t'], 1), '->', b['tipo'], round(b['t'], 1))
