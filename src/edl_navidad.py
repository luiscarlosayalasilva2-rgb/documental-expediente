"""12 costumbres navideñas: video completo.
Un plano por idea, fotos limpias (sin títulos), cortes en los tiempos de audio/frases.json y audio/palabras.json."""
import json, os, re, subprocess, sys, unicodedata
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))
import limpiar

limpiar.RECORTES.update({
    'p11_bolas_02.jpg': (0.0, 0.0, 1.0, 0.90),          # crédito de la foto abajo
    'p11_sala_02.jpg': (0.0, 0.0, 1.0, 0.88),           # todocoleccion
    'p09_abuela_00.jpg': (0.0, 0.0, 1.0, 0.82),         # logo abajo a la izquierda
    'p09_finca_03.jpg': (0.0, 0.0, 1.0, 0.74),          # logo NJ
    'p09_gallo_06.jpg': (0.0, 0.0, 1.0, 0.90),          # marca de agua abajo
    'p08_maracas_06.jpg': (0.0, 0.12, 1.0, 0.86),       # textos arriba y abajo
    'p08_panderetas_07.jpg': (0.0, 0.0, 1.0, 0.74),     # logo abajo
    'p05_menear_01.jpg': (0.03, 0.12, 0.97, 0.95),      # marco y título de la página
    'p04_volcanes_03.jpg': (0.15, 0.0, 0.78, 0.80),     # logos
    'r2_novena_01.jpg': (0.0, 0.0, 0.48, 1.0),          # solo la pandereta
    'r2_diciembre_00.jpg': (0.0, 0.45, 1.0, 1.0),       # texto de la página en el cielo
    'p09_abuela_05.jpg': (0.0, 0.0, 1.0, 0.90),         # sello de fecha
    'r2_pandereta_00.jpg': (0.0, 0.0, 0.48, 1.0),       # solo las manos con la pandereta
})

def G(n):
    for d in ('hd_esrgan', 'google_hd'):
        p = os.path.join(R, 'media', d, n + '.jpg')
        if os.path.exists(p): return limpiar.limpiar(p) if d == 'google_hd' else p
    raise FileNotFoundError(n)
V = lambda n: os.path.join(R, 'media', 'pixabay_v', n + '.mp4')
_k = [0]

PAL = json.load(open(os.path.join(R, 'audio', 'palabras.json'), encoding='utf-8'))
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))
def w(pal, desde, defecto=None):
    """Segundo en que empieza la palabra (primera aparición desde 'desde')."""
    for x in PAL:
        if x['s'] >= desde - 0.3 and norm(x['w']).startswith(norm(pal)):
            if x['s'] - desde < 15: return round(x['s'], 2)
            break
    if defecto is None: raise ValueError((pal, desde))
    return defecto

def plano(t0, t1, src, bw=False):
    if src.endswith('.mp4'):
        return {'t0': t0, 't1': t1, 'tipo': 'video', 'src': src, 'ss': 1.0, 'bw': bw}
    z = [(1.0, 1.07), (1.07, 1.0)][_k[0] % 2]; _k[0] += 1
    return {'t0': t0, 't1': t1, 'tipo': 'imagen', 'src': src, 'bw': bw, 'mov': {'z0': z[0], 'z1': z[1]}}

def papel(t0, t1, modo, fotos, **kw):
    return {'t0': t0, 't1': t1, 'tipo': 'papel', 'papel': {'modo': modo, 'fotos': [{'src': s, 'pie': p} for s, p in fotos], **kw}}

PAPELES = {
    'PAPEL_ESTREN': ('polaroid', [(G('p12_closet_05'), 'Guardado hasta el 24'), (G('p12_zapatos_02'), 'Los zapatos nuevos')], {}),
    'PAPEL_ARBOL': ('polaroid', [(G('p11_bombillos_02'), 'La instalación'), (G('p11_bolas_03'), 'Las bolas de vidrio')], {}),
    'PAPEL_CINTA': ('unica', [(G('p10_cinta_01'), 'Tarjeta por tarjeta, en la cinta de la sala')], {}),
    'PAPEL_ABUELOS': ('polaroid', [(G('p09_casa_03'), 'La casa llena'), (G('p09_finca_04'), 'Donde los abuelos')], {}),
    'PAPEL_VS': ('vs', [(G('p08_natilla_06'), 'La natilla'), (G('p08_bunuelos_06'), 'Los buñuelos')],
                 {'titulo': 'Natilla vs. buñuelos', 'sub': 'Ninguna casa quería quedar mal con la de ayer'}),
    'PAPEL_PESEBRE': ('polaroid', [(G('p06_figuras_00'), 'Una ovejita'), (G('p06_figuras_01'), 'Un pastorcito')], {}),
    'PAPEL_TIA': ('unica', [(G('p09_abuela_00'), 'La que sabía cuándo estaba lista')], {}),
    'PAPEL_CIERRE': ('carrusel', [(G('p12_san_victorino_02'), '12 · El estrén'), (G('r2_chamizo3_00'), '11 · El árbol de chamizo'),
                                  (G('p10_adpostal_04'), '10 · Las tarjetas por Adpostal'), (G('p09_casa_00'), '9 · La casa de los abuelos'),
                                  (G('p08_novena_01'), '8 · La novena de la cuadra'), (G('p07_anoviejo3_04'), '7 · El Año Viejo gigante'),
                                  (G('r2_pesebre_01'), '6 · El pesebre con musgo'), (G('r2_paila2_00'), '5 · La natilla en paila'),
                                  (G('p04_polvora_06'), '4 · La pólvora y los globos'), (G('p03_nino_dios_00'), '3 · El Niño Dios'),
                                  (G('p02_cadenetas_04'), '2 · La cuadra cerrada'), (G('p01_aguinaldos_06'), '1 · Los aguinaldos')], {}),
    'PAPEL_PAQUETE': ('unica', [(G('p03_juguete_00'), 'El paquete, al pie de la cama')], {}),
}

CIERRE = 735.9  # fin de la voz recibida; después va el cierre visual
L = [  # (inicio, fuente[, bw])
    # INTRO
    (0.0, G('in_natilla_00')),
    (w('pólvora', 2.5), G('in_polvora_06')),
    (w('musgo', 4.0), G('in_musgo_00')),
    (6.1, G('r2_alumbrado_07')),
    (w('armaba', 7.8), G('in_musgo_06')),
    (w('cuadra', 10.0), G('p02_cadenetas_00')),
    (w('casa', 11.2), G('ci_familia_05')),
    (12.9, G('r2_diciembre_00'), True),
    (15.1, G('p04_tienda_04')),
    (18.0, V('christmas_lights_3')),
    # 12 — el estrén
    (19.6, G('p12_almacen_00')),
    (24.0, G('p12_ninos_01'), True),
    (26.2, G('p12_zapatos_01')),
    (27.4, G('p12_zapatos_04')),
    (29.4, G('p12_carrera_01')),
    (31.4, G('p12_san_victorino_00')),
    (32.4, G('p12_vendedores_00')),
    (33.9, V('crowd_shopping_street_1')),
    (38.1, G('p12_centro_02')),
    (41.0, G('p12_san_victorino_01')),
    (45.3, G('p12_probador_03')),
    (48.3, G('p12_probador_00')),
    (50.4, G('p12_probador_07')),
    (52.7, G('p12_ninos_00'), True),
    (55.2, G('p12_bolsa_03')),
    (57.5, G('p12_closet_04')),
    (61.0, 'PAPEL_ESTREN'),
    (67.5, G('p12_closet_02')),
    (70.9, G('p12_ninos_02'), True),
    (74.0, G('p12_carrera_04'), True),
    (77.6, V('village_colombia_1')),
    (80.3, G('p12_san_victorino_07')),
    (83.5, G('p12_zapatos_05')),
    (87.1, V('crowd_shopping_street_2'), True),
    (89.6, G('p12_carrera_05'), True),
    # 11 — el árbol de chamizo
    (92.8, G('r2_chamizo3_00')),
    (95.5, G('r2_chamizo2_02')),
    (96.7, G('p11_rama_03')),
    (99.0, G('p11_rama_00')),
    (101.4, G('p11_rama_07')),
    (102.8, G('p11_rama_02')),
    (105.5, G('r2_chamizo3_02')),
    (108.0, G('p11_chamizo2_01')),
    (111.2, G('p11_arbol_00')),
    (114.0, G('p11_algodon_05')),
    (118.4, V('christmas_ornaments_3')),
    (122.2, G('r2_chamizo2_00')),
    (125.8, G('p11_arbol_02')),
    (129.8, G('p11_bolas_00')),
    (132.2, G('p11_bolas_06')),
    (134.2, G('p11_bolas_07')),
    (136.3, G('p11_bombillos_04')),
    (138.6, G('p11_bombillos_00'), True),
    (140.5, V('light_bulbs_garland_1')),
    (143.0, G('p11_sala_02')),
    (145.7, 'PAPEL_ARBOL'),
    (149.8, V('christmas_tree_lights_1')),
    (152.5, G('p11_sala_01')),
    (154.7, G('p11_bolas_05')),
    (157.6, G('p11_sala_03')),
    # 10 — tarjetas por Adpostal
    (159.4, G('p10_tarjetas_01')),
    (162.0, G('r2_escribir_01')),
    (165.9, G('p10_escribir_03')),
    (168.6, G('p10_sobre_03')),
    (170.5, G('p10_sobre_02')),
    (171.8, G('p10_escribir_07')),
    (174.0, G('p10_tarjetas_04')),
    (176.8, V('christmas_eve_family_2')),
    (180.6, G('p10_estampilla_00')),
    (183.1, G('p10_adpostal_04')),
    (184.8, G('p10_adpostal2_01')),
    (186.1, G('p10_adpostal_07')),
    (187.5, G('r2_cartero_04')),
    (189.7, V('mailbox_letter_2')),
    (193.8, G('p10_cinta_00')),
    (197.3, 'PAPEL_CINTA'),
    (201.5, G('p10_estampilla_02')),
    (204.5, G('p10_adpostal_06')),
    (207.7, G('p10_celular_04')),
    (209.5, G('p10_celular_03'), True),
    (211.1, G('p10_sobre_01')),
    (213.5, G('p10_estampilla_05')),
    # 9 — la casa de los abuelos
    (216.6, G('p09_casa_00')),
    (219.4, G('p09_finca_01')),
    (223.8, G('p09_familia_00'), True),
    (225.9, G('p08_novena2_00')),
    (227.4, G('p09_familia_02')),
    (229.2, G('p09_cocina_00')),
    (231.0, G('p09_abuela_05')),
    (233.0, G('p09_abuelo_06')),
    (236.0, G('p09_abuelo_02'), True),
    (239.0, G('p09_abuelo_04')),
    (242.8, V('candles_night_2')),
    (245.9, G('p09_colchones_00')),
    (247.3, G('p01_risa_02')),
    (251.2, G('p09_chocolate_03')),
    (254.7, G('p09_casa_01')),
    (255.5, G('p09_gallo_03')),
    (256.6, G('p09_casa_06')),
    (260.5, 'PAPEL_ABUELOS'),
    (266.5, G('p09_cocina_03')),
    (270.4, G('p09_casa_02'), True),
    (274.1, G('p09_abuela_06'), True),
    (276.5, G('p09_finca_03')),
    # 8 — la novena de la cuadra
    (279.5, G('p08_novena_01')),
    (283.2, G('p08_novena2_04')),
    (286.9, G('p08_novena2_03')),
    (288.9, G('p08_novena2_05')),
    (291.5, G('p08_novena_06')),
    (293.9, G('p08_villancicos_00')),
    (296.7, G('p08_panderetas_06')),
    (299.3, G('p08_panderetas_03')),
    (301.4, G('r2_pandereta_00')),
    (302.3, G('p08_maracas_06')),
    (304.4, G('r2_novena_05')),
    (306.0, G('p08_villancicos_02')),
    (308.2, G('p08_novena2_06')),
    (313.9, G('p08_natilla_02')),
    (318.5, G('p08_natilla_03')),
    (319.9, G('p08_bunuelos_00')),
    (320.9, G('r2_bunuelos_00')),
    (323.7, 'PAPEL_VS'),
    (327.5, G('p08_calle_03')),
    (329.1, G('p08_calle_05')),
    (331.3, V('christmas_market_2')),
    (334.9, G('p08_novena2_02')),
    (336.5, G('p08_bunuelos_01')),
    # 7 — el Año Viejo gigante
    (339.1, G('p07_anoviejo3_04')),
    (342.0, G('p07_quema2_06')),
    (344.9, G('r2_quema_06')),
    (346.4, G('p07_anoviejo2_04')),
    (348.2, G('r2_ropa_00')),
    (350.5, G('p07_anoviejo3_03')),
    (351.8, G('p07_aserrin_02')),
    (353.1, G('p07_periodico_07')),
    (354.3, G('r2_quema_05')),
    (356.3, G('r2_quema_04')),
    (358.9, G('p07_quema2_03')),
    (361.4, G('p07_anoviejo2_05')),
    (363.0, G('p07_anoviejo2_01')),
    (366.5, G('p07_quema_07')),
    (370.6, G('p07_quema_05')),
    (372.6, G('p07_quema_03')),
    (375.3, V('bonfire_night_1')),
    (377.6, G('p07_quema_06')),
    (378.3, V('fire_burning_1')),
    (381.0, G('p07_quema_01')),
    (382.5, V('bonfire_night_3')),
    (386.9, G('p07_quema2_01'), True),
    (390.2, G('r2_testamento_07'), True),
    (393.4, G('r2_alumbrado_00'), True),
    # LLAMADO
    (395.6, V('medellin_1')),
    (399.0, G('r2_alumbrado_02'), True),
    (401.9, G('in_cuadra_05')),
    # 6 — el pesebre con musgo
    (405.0, G('r2_pesebre_01')),
    (407.3, G('p06_pesebre_06')),
    (410.3, V('moss_forest_1')),
    (411.3, G('p06_plaza_04')),
    (413.8, G('p06_musgo_03')),
    (416.0, G('p06_musgo_02')),
    (417.2, G('in_musgo_01')),
    (420.3, G('in_musgo_03')),
    (423.2, G('r2_pesebre_04')),
    (424.7, G('p06_espejo_03')),
    (426.6, G('p06_pesebre_02')),
    (429.1, G('p06_figuras_06')),
    (430.5, G('p06_figuras_04')),
    (431.6, G('p06_reyes_04')),
    (434.8, G('p06_nino_02')),
    (437.3, G('p06_pesebre2_04')),
    (441.0, 'PAPEL_PESEBRE'),
    (444.7, V('nativity_scene_1')),
    (447.9, G('p06_musgo_06'), True),
    (450.5, G('p06_musgo_05')),
    (453.1, G('r2_pesebre_00')),
    # 5 — la natilla en paila
    (457.8, G('r2_paila2_00')),
    (460.2, G('p05_menear_01')),
    (462.2, G('p05_maiz_05')),
    (465.9, G('p05_molino_02')),
    (467.3, G('p05_molino_03')),
    (469.4, V('corn_1')),
    (470.8, G('p05_paila_05')),
    (472.5, G('p05_paila2_02')),
    (474.3, G('p05_fogon_00')),
    (475.4, V('grandmother_cooking_3')),
    (478.4, G('p05_menear_02')),
    (481.5, G('p05_panela_02')),
    (483.3, V('cinnamon_3')),
    (484.6, G('p05_fogon_06')),
    (489.2, 'PAPEL_TIA'),
    (495.6, G('p05_paila2_03')),
    (498.0, G('r2_paila_04')),
    (501.4, G('p08_natilla_07')),
    (504.0, G('r2_paila_05')),
    (507.4, G('p05_caja_02')),
    (508.7, G('p05_caja_05')),
    (510.4, G('p05_canela_02'), True),
    (514.2, G('r2_abuela_07')),
    # 4 — la pólvora y los globos
    (517.6, G('p04_polvora_06')),
    (519.6, G('in_polvora_07')),
    (522.0, G('p04_totes_03')),
    (524.1, G('p04_chispitas_02')),
    (525.3, G('p04_chispitas_06')),
    (526.8, G('p04_volcanes_04')),
    (527.6, V('firecracker_2')),
    (528.8, G('p04_tienda_03')),
    (529.8, G('r2_globos_03')),
    (531.9, G('p04_globos2_04')),
    (533.7, G('r2_globos2_03'), True),
    (535.1, V('fireworks_night_1')),
    (537.9, G('p04_globos_01')),
    (539.7, G('r2_globos2_06')),
    (541.5, G('p02_bicicleta_01')),
    (544.2, G('r2_globos_02')),
    (546.4, G('p02_calle_05')),
    (548.6, G('in_polvora_01'), True),
    (552.1, G('p04_quemados_07')),
    (555.2, G('p04_quemados_01')),
    (557.7, G('in_polvora_03')),
    (559.3, G('p04_quemados_05'), True),
    (561.8, V('sparkler_1')),
    (564.5, G('p04_polvora_02')),
    # 3 — el Niño Dios
    (567.5, G('p03_nino_dios_00')),
    (570.9, G('p06_nino_05')),
    (572.0, G('p03_nino_dios_06')),
    (575.4, G('p03_cama_06')),
    (578.5, G('p03_cama_07')),
    (581.2, G('p03_carta_06')),
    (583.8, V('writing_letter_1')),
    (587.5, G('p03_juguete_05')),
    (590.0, G('r2_carta2_02')),
    (591.7, G('p06_pesebre_05')),
    (593.0, V('christmas_eve_family_3')),
    (597.7, G('p03_nino_dios_01')),
    (599.6, G('p03_juguete_04')),
    (604.5, 'PAPEL_PAQUETE'),
    (610.0, V('family_dinner_christmas_1')),
    (611.8, G('p03_juguete_01')),
    (615.0, G('p03_juguete_06'), True),
    (618.0, G('p03_papanoel_05'), True),
    (621.3, G('p06_nino_04')),
    (623.2, G('r2_pesebre_03')),
    # 2 — la cuadra cerrada
    (625.5, G('p02_cadenetas_04')),
    (628.9, G('p02_cadenetas_01')),
    (632.2, G('p02_calle_03')),
    (633.8, G('p02_calle_02')),
    (635.4, G('p02_caseta_01')),
    (637.0, G('p02_caseta_00')),
    (638.4, G('p02_cadenetas_05')),
    (641.3, G('in_natilla_06')),
    (642.2, G('p08_bunuelos_07')),
    (643.4, G('p02_calle_01')),
    (644.6, G('p02_patines_02')),
    (645.9, G('p02_bicicleta_00')),
    (647.6, G('p02_bailando_00')),
    (649.8, V('dancing_street_party_1')),
    (651.4, G('p02_cadenetas_06')),
    (653.5, G('p02_radio_06')),
    (656.5, G('p02_radio_00')),
    (658.1, G('p02_calle_06')),
    (660.9, G('p02_seleccion_05')),
    (662.4, G('p02_rejas_00'), True),
    (664.5, G('p02_rejas_05'), True),
    (666.5, G('p02_rejas_02'), True),
    (668.4, V('bogota_1')),
    # 1 — los aguinaldos
    (673.5, G('p01_aguinaldos_06')),
    (675.9, G('r2_aguinaldos_03')),
    (680.1, G('p01_risa_03')),
    (683.7, G('p01_familia_06')),
    (686.4, G('p01_abuela_07')),
    (687.3, G('p01_colegio_05')),
    (688.1, G('p01_colegio_00')),
    (688.7, G('p08_calle_00')),
    (690.3, G('p01_aguinaldos_00')),
    (691.9, G('p01_aguinaldos_04')),
    (696.7, G('p01_aguinaldos_01')),
    (702.0, G('p01_abuela_01')),
    (707.5, G('p01_tres_pies_07')),
    (709.4, G('p01_tres_pies_03')),
    (712.0, G('p01_risa_01')),
    (714.8, G('p01_familia_02')),
    (717.8, G('ci_familia_07')),
    (719.0, V('children_playing_street_2')),
    (721.1, G('p01_pajita_06')),
    (724.7, V('children_laughing_1')),
    (726.5, G('p01_risa_05')),
    (729.6, G('p01_abuela_00')),
    (730.6, G('p01_risa_07')),
    (732.0, G('p01_abuela_05')),
    (733.6, G('p01_familia_00')),
    (CIERRE, 'PAPEL_CIERRE'),
    (CIERRE + 7.1, G('r2_alumbrado_06'), True),
]
DUR = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                            os.path.join(R, 'audio', 'voz_final.wav')], capture_output=True, text=True).stdout)
planos = []
for i, x in enumerate(L):
    t0, src = x[0], x[1]; bw = x[2] if len(x) > 2 else False
    t1 = L[i + 1][0] if i + 1 < len(L) else DUR
    if src in PAPELES:
        modo, fotos, kw = PAPELES[src]
        planos.append(papel(t0, t1, modo, fotos, **kw))
    else:
        planos.append(plano(t0, t1, src, bw))

def P(t, palabra, sub, dur=1.8): return {'tipo': 'palabra', 't': t, 'dur': dur, 'palabra': palabra, 'sub': sub}
def N(t, num, label, dur=1.9, grande=False):
    c = {'tipo': 'numero', 't': t, 'dur': dur, 'num': num, 'label': label}
    if grande: c['grande'] = True
    return c
def ABRE(t, n, nombre, dur_file=4.0):  # número grande + ficha 2.35 s después
    return [N(t, str(n), nombre, 2.3, True), {'tipo': 'file', 't': t + 2.35, 'dur': dur_file, 'texto': nombre, 'etiqueta': f'Costumbre {n}'}]
def NOTA(t, texto, resaltar, dur=2.6): return {'tipo': 'nota', 't': t, 'dur': dur, 'texto': texto, 'resaltar': resaltar}

capas = [
    # INTRO
    {'tipo': 'file', 't': 0.6, 'dur': 4.6, 'texto': 'Así era la Navidad en Colombia', 'etiqueta': 'Expediente diciembre', 'titulo': True},
    P(6.2, 'Hecha', 'La Navidad no se compraba hecha: se armaba entre todos.', 1.8),
    N(12.9, '12', 'costumbres de diciembre', 2.0),
    N(w('uno', 15.3), '1', 'no se compraba en ninguna tienda', 1.9),
    # 12 — el estrén
    *ABRE(19.6, 12, 'El estrén'),
    N(w('tres', 41.0), '3', 'veces preguntaba el precio', 1.8),
    N(w('24', 57.5), '24', 'de diciembre, ni un día antes', 2.0),
    N(w('24', 70.6), '24', 'bañado y peinado con agua', 1.8),
    P(74.4, 'Otra persona', 'Uno se lo ponía y se sentía otra persona.', 2.0),
    P(89.6, 'Como esa', 'Por eso ya ninguna se siente como esa.', 2.4),
    # 11 — el árbol de chamizo
    *ABRE(92.8, 11, 'El árbol de chamizo'),
    P(125.8, 'Nieve', 'Nieve en tierra caliente. Así de grande era la ilusión.', 3.2),
    N(w('uno', 138.8), '1', 'se fundía y se apagaban todos', 1.6),
    P(152.6, 'Callados', 'Toda la familia se quedaba callada mirándolo.', 2.0),
    P(157.6, 'El nuestro', 'No era el árbol más bonito del mundo. Era el nuestro.', 1.8),
    # 10 — tarjetas por Adpostal
    *ABRE(159.4, 10, 'Las tarjetas por Adpostal'),
    P(187.5, 'La espera', 'Esperar al cartero era parte de la Navidad.', 2.0),
    P(201.6, 'El cariño', 'Entre más tarjetas colgadas, más gente se había acordado de uno.', 2.2),
    P(213.5, 'Todo diciembre', 'Y se quedaba colgada en la sala todo diciembre.', 2.4),
    # 9 — la casa de los abuelos
    *ABRE(216.6, 9, 'La casa de los abuelos'),
    NOTA(w('vamos', 219.4), '«Vamos donde los abuelos»', ['los abuelos'], 3.0),
    P(239.1, 'Su momento', 'Porque era su historia, y ese era su momento.', 2.0),
    P(256.7, 'Quieto', 'En esa casa, el tiempo se quedaba quieto.', 2.0),
    P(276.5, 'Esa casa', 'Hay olores que todavía vienen de esa casa.', 2.4),
    # 8 — la novena de la cuadra
    *ABRE(279.5, 8, 'La novena de la cuadra'),
    N(w('16', 283.0), '16', 'al 24, una casa distinta cada noche', 2.2),
    P(306.0, 'Con alegría', 'Sonaba como sonaba, pero sonaba con alegría.', 2.0),
    NOTA(w('tutaina', 308.5, 309.6), '«Tutaina tuturumá»', ['tuturumá'], 3.0),
    P(336.6, 'Comiendo junta', 'Y después, comiendo junta.', 2.4),
    # 7 — el Año Viejo gigante
    *ABRE(339.1, 7, 'El Año Viejo gigante'),
    NOTA(w('limosnita', 368.0), '«Una limosnita para el Año Viejo»', ['limosnita'], 2.8),
    N(w('31', 373.5), '31', 'de diciembre, a las doce', 2.0),
    P(382.5, 'Limpio', 'Uno lo veía arder y sentía que el año nuevo empezaba limpio.', 2.2),
    P(393.4, 'Un año entero', 'Esa noche no se despedía un muñeco. Se despedía un año entero.', 2.2),
    # LLAMADO
    P(401.9, 'Lo mejor viene ahora', 'Y quédate, que lo mejor viene ahora.', 2.0),
    # 6 — el pesebre con musgo
    *ABRE(405.0, 6, 'El pesebre con musgo'),
    N(w('24', 435.8), '24', 'el Niño Dios no se ponía antes', 1.6),
    NOTA(w('no', 438.4), '«No me toquen el pesebre»', ['no me toquen'], 2.5),
    P(455.0, 'La memoria', 'Ese olor a monte mojado no se va de la memoria.', 2.3),
    # 5 — la natilla en paila
    *ABRE(457.8, 5, 'La natilla en paila'),
    P(460.8, 'Todo el día', 'Era una faena de todo el día.', 1.8),
    P(w('meni', 476.0), 'Menear', 'Y menear, y menear, durante horas.', 1.9),
    P(501.5, 'La raspa', 'Lo mejor quedaba al final: la raspa del fondo de la paila.', 2.2),
    P(514.2, 'Distinto', 'Por eso sabe distinto.', 1.6),
    # 4 — la pólvora y los globos
    *ABRE(517.6, 4, 'La pólvora y los globos'),
    P(537.9, 'Una lucecita', 'Subir y subir hasta volverse una lucecita en el cielo.', 1.8),
    P(557.8, 'Manos y ojos', 'Esas normas salvaron manos y ojos.', 1.5),
    P(564.6, 'Sin querer', 'Cuando huele pólvora, se devuelve en el tiempo sin querer.', 2.4),
    # 3 — el Niño Dios
    *ABRE(567.5, 3, 'El Niño Dios'),
    N(w('24', 593.0), '24', 'con el corazón a mil', 1.8),
    NOTA(597.7, '¿Será que sí viene?', ['sí viene'], 1.9),
    N(w('25', 599.4), '25', 'de diciembre, todavía oscuro', 2.0),
    P(606.3, 'El paquete', 'Y ahí estaba. El paquete.', 1.6),
    P(623.2, 'La ilusión', 'Traía la ilusión más grande que tuvimos.', 2.3),
    # 2 — la cuadra cerrada
    *ABRE(625.5, 2, 'La cuadra cerrada'),
    P(651.4, 'Una sola familia', 'En diciembre la cuadra era una sola familia.', 2.0),
    P(660.9, '¡Gol!', 'Como si hubiera ganado la Selección.', 1.5),
    P(671.0, 'En la calle', 'La Navidad no estaba en la sala. Estaba en la calle.', 2.4),
    # 1 — los aguinaldos
    *ABRE(673.5, 1, 'Los aguinaldos'),
    P(680.1, 'La malicia', 'Se jugaba con la voz, con la mirada y con la malicia.', 1.8),
    N(w('16', 684.0), '16', 'al 24, todo el mundo jugaba', 1.6),
    NOTA(w('dar', 691.5), '«Dar y no recibir»', ['no recibir'], 2.4),
    NOTA(w('pajita', 696.5), '«Pajita en boca»', ['pajita'], 2.4),
    NOTA(w('al', 701.8), '«Al sí y al no»', ['sí', 'no'], 2.4),
    N(w('mil', 706.2), '1000', 'veces te preguntaban', 1.0),
    NOTA(w('tres', 707.3), '«Tres pies»', ['tres pies'], 2.2),
    P(w('mis', 713.5), '¡Mis aguinaldos!', 'Y cuando uno pillaba al otro, gritaba.', 1.6),
    P(732.0, 'La risa', 'Esa risa no la compra nadie.', 1.6),
    # CIERRE (sin voz: el audio de Luis llegó cortado)
    P(CIERRE + 7.2, 'Nos vemos en el pasado', 'Doce costumbres que hacíamos con las manos, con la cuadra y con la familia.', DUR - CIERRE - 7.2),
]
for c in capas:
    if c['tipo'] == 'palabra' and c['dur'] < 1.4: c['dur'] = 1.4
capas.sort(key=lambda c: c['t'])
pis = [(a['t'], a['dur'], a.get('palabra') or a.get('num') or a.get('texto'), b['t']) for a, b in zip(capas, capas[1:])
       if not (a['t'] + a['dur'] <= b['t'] + 0.05 or a['tipo'] == 'file' or b['tipo'] == 'file')]
for x in pis: print('se pisan', x)
assert not pis
for p in planos:
    for f in ([p['src']] if p.get('src') else [x['src'] for x in p['papel']['fotos']]):
        assert os.path.exists(f), f
    assert 0 < p['t1'] - p['t0'] <= 11, (p['t0'], p['t1'])
especiales = []
edl = {'dur': DUR, 'audio': os.path.join(R, 'audio', 'voz_final.wav'), 'planos': planos, 'capas': capas, 'especiales': especiales}
json.dump(edl, open(os.path.join(R, 'final', 'edl_navidad_final.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('planos', len(planos), '| capas', len(capas), '| videos', sum(p['tipo'] == 'video' for p in planos),
      '| oscuras/min', round(sum(c['tipo'] in ('numero', 'palabra') for c in capas) / (DUR / 60), 2))
