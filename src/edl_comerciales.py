"""10 comerciales colombianos: rellena el esqueleto de nuevo_video.py (final/edl_comerciales.json).
Fotos en orden de narración por sección; si una sección tiene menos fotos que huecos, el plano anterior se alarga
(nunca se repite una foto). Sin frames de comerciales (Luis 2026-10-28: "Sin comerciales")."""
import json, os, re, sys, unicodedata
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))
import limpiar

limpiar.RECORTES.update({
    'p7_r4_01.jpg': (0.0, 0.0, 1.0, 0.92),
    'p4_higuita_00.jpg': (0.0, 0.0, 1.0, 1.0),
    'p5_doloran_02.jpg': (0.0, 0.0, 0.66, 1.0),         # solo la tapa, sin el señor
    'p1_tarjeta_04.jpg': (0.0, 0.0, 1.0, 1.0),
    'in_tvsala_06.jpg': (0.0, 0.0, 1.0, 1.0),
    'p10_bavaria_cami_00.jpg': (0.0, 0.0, 1.0, 0.90),  # firma Gloria B.
    'p10_bavaria_cami_03.jpg': (0.0, 0.0, 1.0, 0.90),
    'p6_tostadora_02.jpg': (0.0, 0.0, 1.0, 0.88),      # texto de la página
    'p9_fila_01.jpg': (0.0, 0.0, 1.0, 0.92),           # controles del reproductor
    'in_tvvieja_01.jpg': (0.12, 0.0, 0.88, 0.90),      # logo y texto de captura
})

def G(n):
    for d in ('hd_esrgan', 'google_hd'):
        p = os.path.join(R, 'media', d, n + '.jpg')
        if os.path.exists(p): return limpiar.limpiar(p) if d == 'google_hd' else p
    raise FileNotFoundError(n)
def V(n):
    for d in ('pixabay_v', 'clips'):
        p = os.path.join(R, 'media', d, n + '.mp4')
        if os.path.exists(p): return p
    raise FileNotFoundError(n)

PAL = json.load(open(os.path.join(R, 'audio', 'palabras.json'), encoding='utf-8'))
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))
def w(pal, desde, defecto=None):
    for x in PAL:
        if x['s'] >= desde - 0.3 and norm(x['w']).startswith(norm(pal)):
            if x['s'] - desde < 25: return round(x['s'], 2)
            break
    if defecto is None: raise ValueError((pal, desde))
    return defecto

# fotos por sección, en el orden en que se narran
FOTOS = {
    'INTRO': ['in_tvvieja_00', 'in_tvsala_06', 'r2_tvninos_01', 
              'in_bus_01', 'in_bus_00', 'in_tvvieja_02', 'r2_tvcol_01', 'in_bus_03', 'in_bus_02', 'ci_control_05'],
    'Bavaria': ['p10_bavaria_01', 'p10_bavaria_cami_00', 'p10_bavaria_04', 'p10_bavaria_cami_04', 'p10_cervezas_00',
                'p10_colegio_00', 'p10_tienda_00', 'p10_bavaria_07', 'p10_bavaria_cami_06', 'p10_bavaria_03', 'p10_bavaria_cami_03'],
    'Noel': ['r2_noel2_00', 'p9_noel_05', 'p9_noelfab_02', 'p9_lonchera_01', 'p9_recreo_00', 'p9_noel_06', 'p9_lonchera_02',
             'p9_noel_07', 'p9_carro_07', 'p9_cocina_01', 'p9_fila_03', 'p9_noelfab_01', 'r2_noel_00', 'p9_lonchera_05'],
    'Gudiz': ['p8_gudiz2_02', 'r2_gudiz2_05', 'p8_gudiz2_04', 'p8_lonchera2_01', 'p9_lonchera_06', 'p8_profesora_00',
              'p8_profesora_02', 'p9_lonchera_03', 'p10_colegio_06', 'p9_lonchera_00', 'p8_profesora_01', 'p9_lonchera_07', 'p10_colegio_03', 'p9_recreo_05', 'p9_recreo_07'],
    'Renault': ['p7_r4_01', 'r2_lavar_02', 'p7_r4lavar_01', 'p7_r4lavar_07', 'p7_r4_05', 'p7_r4campo_00', 'p7_r4campo_02',
                'p7_r4mercado_00', 'p7_r4mercado_01', 'p7_r4empujar_04', 'p7_r4empujar_05',
                'p7_r4calle_00', 'p7_r4_06', 'p7_r4calle_02', 'p7_r4_00', 'p7_r4sofasa_07'],
    'La Fina': ['r2_lafina_01', 'p6_tostadora_02', 'p6_chocolate_00', 'p6_radio_00', 'p6_radio_06', 'p6_lafina_00', 'p6_arepa_00',
                'p6_arepa_05', 'p6_desayuno_03', 'p6_arepa_01', 'p6_chocolate_02', 'r2_lafina_03',
                'p6_chocolate_03', 'p6_tostadora_06', 'p6_arepa_07'],
    'Dolor': ['p5_doloran_03', 'p5_doloran_06', 'p5_futbolcuadra_00', 'p5_doloran_05', 'p5_partido_00',
              'p5_vuelta_00', 'p5_partido_02', 'p5_vuelta_03', 'p5_botiquin_00', 'p5_botiquin_02', 'p5_futbolcuadra_01',
              'p5_futbolcuadra_04', 'p5_doloran_02', 'p5_vuelta_06', 'p5_partido_01', 'p5_futbolcuadra_07'],
    'LLAMADO': ['ci_control_00', 'ci_control_02', 'in_bus_04', 'p5_vuelta_05'],
    'Higuita': ['p4_frutino_03', 'p4_higuita2_00', 'p4_higuita2_07', 'p4_higuita2_03', 'p4_higuita_00', 'p4_cancha_01',
                'p4_cancha_02', 'p4_higuita_05', 'p4_cancha_07', 'p4_higuita3_04', 'p4_higuita3_05', 'p4_higuita3_01',
                'p4_higuitanac_00', 'p4_higuita_06', 'p4_higuitanac_03', 'p4_higuitanac_01', 'r2_frutino_04'],
    'Davivienda': ['p3_davivienda2_01', 'p3_davivienda2_03', 'p3_daviviendalogo_02', 'p3_davivienda_03', 'p3_davivienda_04',
                   'p3_davivienda_05', 'p3_daviviendalogo_00', 'p3_daviviendalogo_06', 'p3_daviviendalogo_07', 'p10_tienda_04', 'p10_tienda_05', 'p9_fila_05', 'p9_fila_01', 'p10_tienda_06', 'p3_davivienda_06'],
    'guila': ['p2_aguila_00', 'p2_aguilaroja_00', 'p2_pesebre_00', 'p2_aguila_02', 'p2_cafegrano_00', 'p2_cafetal_04',
              'p2_aguilaroja_04', 'p2_cafegrano_03', 'p2_pesebre_01', 'p2_pesebre_03', 'p2_pesebre_06', 'p2_bunuelos_00',
              'p2_bunuelos_05', 'p2_cocina_00', 'p2_cocina_03', 'p2_cocina_04', 'p2_cafetal_07', 'p2_cafegrano_05',
              'p2_pesebre_04', 'p2_cafetal_01', 'p2_bunuelos_06', 'p2_aguila_01'],
    'Conavi': ['p1_tarjeta_05', 'p1_conavi_03', 'p1_upac_07', 'p1_libreta_02', 'p1_conavisuc_07', 'p1_monedas_03',
               'p1_monedas_07', 'p1_monedas_05', 'p1_monedas_06', 'p1_libreta_06', 'p1_conavi_07', 'p1_bancolombia_00',
               'p1_bancolombia_03', 'p1_conavi_00', 'p1_libreta_00', 'p1_libreta_05', 'p1_bancolombia_04'],
    'CIERRE': ['ci_cobija_07', 'ci_cobija_00', 'ci_celular_02', 'ci_celular_06', 'ci_celular_07', 'ci_chiva_00', 'ci_chiva_03',
               'ci_celular_01', 'ci_control_01', 'ci_chiva_04', 'ci_chiva_05', 'ci_chiva_06'],
}
# clips por sección (se rellenan con lo bajado de Pixabay)
CLIPS = json.load(open(os.path.join(R, 'datos', 'clips.json'), encoding='utf-8'))

PAPELES = {  # sección -> fotos del papel (polaroid/única)
    'Bavaria': [('p10_colegio_01', 'En el patio del colegio'), ('p10_tienda_03', 'En la tienda del barrio')],
    'Noel': [('p9_noelfab_07', 'Las galletas de la lonchera')],
    'Renault': [('p7_r4_07', 'El amigo fiel'), ('p7_r4calle_05', 'Cuadrado y sin lujos')],
    'La Fina': [('p6_chocolate_07', 'La mesa del desayuno')],
    'Higuita': [('p4_higuita2_05', 'El arquero'), ('p4_higuita3_07', 'René')],
    'Davivienda': [('r2_alcancia_06', 'La banca bajo un solo techo')],
    'Conavi': [('p1_tarjeta_06', 'La abejita'), ('p1_tarjeta_04', 'Conavi quiere a la gente')],
}
CARRUSEL = [('p10_bavaria_01', '10 · Bavaria, el Orejón'), ('p9_noel_05', '9 · Galletas Noel'), ('p8_gudiz2_02', '8 · Gudiz'),
            ('p7_r4_01', '7 · Renault 4'), ('r2_lafina_01', '6 · Margarina La Fina'), ('p5_doloran_03', '5 · Pomada Dolorán'),
            ('p4_higuita2_03', '4 · Frutiño y René Higuita'), ('p3_davivienda2_01', '3 · Davivienda'),
            ('p2_aguila_00', '2 · Café Águila Roja'), ('p1_tarjeta_05', '1 · Conavi')]

LABELS = {'10': 'comerciales', '15': 'minutos de recreo', '4': 'Renault 4', '1995': 'Wembley', '90': 'Los noventa',
          '1990': 'Primer granito de café', '2014': 'Pasó a 3D', '1974': 'Nace la abejita', '2000': 'Se apagó la abejita',
          '2025': 'Vuelve en una tarjeta'}
PALABRAS = [  # (segundo aprox. del esqueleto, palabra, sub)
    (82.14, 'PERSONAJE', 'El que se le metió en la casa'),
    (92.0, 'SE PEGABA', 'La canción de los castores'),
    (128.3, 'LA LONCHERA', 'Se acuerda de la lonchera y del recreo'),
    (161.18, 'EL RITUAL', 'Las de cierto color se dejaban para el final'),
    (184.26, 'INFANCIA', 'Donde mejor suena'),
    (255.78, 'LA MESA', 'Siempre estaba el que se untaba de más'),
    (283.14, 'EL DESAYUNO', 'Con todos sentados alrededor'),
    (327.18, 'EL OLOR', 'Se quedaba en las sábanas y en la ropa'),
    (341.02, '¡SÍ, SEÑOR!', 'Todavía contesta alguien en la casa'),
    (353.32, 'QUÉDATE', 'Los que faltan son los más grandes'),
    (399.1, 'PRIMERO', 'Lo vimos antes en un comercial'),
    (454.32, 'EQUIVOCADO', 'Usted está en el lugar equivocado'),
    (472.84, 'UNA NOVELA', 'Equivocación tras equivocación'),
    (520.42, 'DICIEMBRE', 'Cuando sonaba, ya era diciembre'),
    (577.56, 'UNA FIESTA', 'Cuando la alcancía se llenaba'),
    (621.1, 'EXTRAÑAR', 'Otros que nunca dejamos de extrañar'),
    (638.42, 'JUNTOS', 'En el mismo sofá, con la misma cobija'),
    (677.52, 'EN EL PASADO', 'Nos vemos en el pasado'),
]

def clave(seccion):
    for k in FOTOS:
        if k in seccion: return k
    raise KeyError(seccion)

def main():
    edl = json.load(open(os.path.join(R, 'final', 'edl_comerciales.json'), encoding='utf-8'))
    pend = lambda p: p['tipo'] != 'papel' and p['src'].startswith('PENDIENTE')
    fotos = {k: list(v) for k, v in FOTOS.items()}
    clips = {k: list(v) for k, v in CLIPS.items()}
    planos, prev_sec = [], None
    for p in edl['planos']:
        if p['tipo'] == 'papel':
            fs = p['papel']['fotos']
            if p['papel']['modo'] == 'carrusel':
                p['papel']['fotos'] = [{'src': G(n), 'pie': t} for n, t in CARRUSEL]
            else:
                k = clave(fs[0]['src'].split('|')[0].split(':', 1)[1])
                lista = PAPELES[k]
                p['papel']['modo'] = 'polaroid' if len(lista) > 1 else 'unica'
                p['papel']['fotos'] = [{'src': G(n), 'pie': t} for n, t in lista]
            planos.append(p); continue
        if not pend(p): planos.append(p); continue
        k = clave(p['src'].split('|')[0].split(':', 1)[1])
        primero = k != prev_sec; prev_sec = k
        if p['tipo'] == 'video' and clips.get(k) and not primero:
            p['src'] = V(clips[k].pop(0)); planos.append(p); continue
        if fotos[k]:
            z = p.get('mov') or {'z0': 1.0, 'z1': 1.07}
            planos.append({'t0': p['t0'], 't1': p['t1'], 'tipo': 'imagen', 'src': G(fotos[k].pop(0)), 'bw': p.get('bw', False), 'mov': z})
        elif clips.get(k):
            p['tipo'] = 'video'; p['src'] = V(clips[k].pop(0)); p.setdefault('ss', 1.0); p.pop('mov', None); planos.append(p)
        else:  # sin material nuevo: se alarga el plano anterior (nunca una escena de papel)
            if planos[-1]['tipo'] == 'papel': raise SystemExit(f'falta material después del papel en {k} ({p["t0"]:.1f} s)')
            planos[-1]['t1'] = p['t1']
    # blanco y negro en la pérdida
    for p in planos:
        if p['tipo'] == 'imagen' and any(x in p['src'] for x in ('p7_r4_00', 'p10_bavaria_03', 'p9_noelfab_02', 'p5_partido_00', 'r2_noel2_00')): p['bw'] = True
    # blanco y negro también en "ya no sale", "ya no", "quedó atrás", "se apagó"
    for t in (w('sale', 182.5), w('no', 340.0), w('atrás', 470.3), w('apagó', 602.5)):
        for p in planos:
            if p['tipo'] == 'imagen' and p['t0'] <= t < p['t1']: p['bw'] = True
    edl['planos'] = planos
    for f, quedan in fotos.items():
        if quedan: print('sin usar', f, quedan)

    # textos
    for c in edl['capas']:
        if c['tipo'] == 'numero' and c.get('label') == 'REVISAR': c['label'] = LABELS.get(c['num'], 'REVISAR')
        if c['tipo'] == 'palabra' and c.get('palabra') == 'REVISAR':
            pal = min(PALABRAS, key=lambda x: abs(x[0] - c['t']))
            c['palabra'], c['sub'] = pal[1], pal[2]
    # el '90' del granito es "a finales de los noventa"
    for c in edl['capas']:
        if c['tipo'] == 'numero' and c['num'] == '90' and c['t'] > 480: c['label'] = 'Se volvió animado'
    for c in edl['capas']:
        if c['tipo'] == 'numero' and c['num'] == '90' and c['t'] > 480: c['dur'] = 2.0
    edl['capas'] += [
        {'tipo': 'numero', 't': w('dos', 99.0), 'dur': 2.0, 'num': '2', 'label': 'minutos y todo el salón cantando'},
        {'tipo': 'numero', 't': w('tercer', 226.0), 'dur': 1.6, 'num': '3', 'label': 'intentos para arrancar'},
        {'tipo': 'numero', 't': w('1500', 489.4), 'dur': 1.8, 'num': '1.500', 'label': 'dibujos'},
        {'tipo': 'palabra', 't': w('tesoro', 139.0), 'dur': 2.2, 'palabra': 'UN TESORO', 'sub': 'Esas bolitas de colores'},
        {'tipo': 'palabra', 't': w('todos', 267.5), 'dur': 2.2, 'palabra': 'TODOS LOS DÍAS', 'sub': 'No era de lujo ni de ocasión especial'},
        {'tipo': 'palabra', 't': w('botiqu', 312.0), 'dur': 2.2, 'palabra': 'EL BOTIQUÍN', 'sub': 'La pomada que sacaba la mamá'},
        {'tipo': 'palabra', 't': w('pesebre', 494.0), 'dur': 2.2, 'palabra': 'EL PESEBRE', 'sub': 'Hasta llegar al Niño Dios'},
        {'tipo': 'palabra', 't': w('propia', 560.5), 'dur': 2.2, 'palabra': 'CASA PROPIA', 'sub': 'El sueño de las familias'},
        {'tipo': 'palabra', 't': 208.0, 'dur': 2.2, 'palabra': 'SIN LUJOS', 'sub': 'Cuadrado, humilde y aguantador'},
        {'tipo': 'palabra', 't': 303.0, 'dur': 2.2, 'palabra': 'LA RISA', 'sub': 'Todo el mundo se moría de la risa'},
        {'tipo': 'palabra', 't': 393.0, 'dur': 2.2, 'palabra': '¡GOL!', 'sub': 'Por andar haciéndose el Higuita'},
        {'tipo': 'palabra', 't': 539.5, 'dur': 2.2, 'palabra': 'LOS QUE YA NO ESTÁN', 'sub': 'La Navidad de cuando era niño'},
        {'tipo': 'palabra', 't': 607.2, 'dur': 2.2, 'palabra': 'DOLIÓ DISTINTO', 'sub': 'Las otras siguieron, ella no'},
        {'tipo': 'palabra', 't': w('escorpi', 363.5), 'dur': 2.4, 'palabra': 'EL ESCORPIÓN', 'sub': 'Algo que nadie había visto'},
    ]
    t_r4 = w('miembro', 228)
    edl['capas'].append({'tipo': 'palabra', 't': round(t_r4 - 1.2, 2), 'dur': 2.4, 'palabra': 'FAMILIA', 'sub': 'Era un miembro de la familia'})
    notas = [('viste', 58, '"¿Viste el del Orejón?"', ['Orejón']),
             ('vamos', 95, '"¡Vamos castores, vamos!"', ['castores']),
             ('sufre', 290, '"¿Sufre usted de calambres?"', ['calambres']),
             ('dinero', 436, '"Su dinero puede estar en el lugar equivocado"', ['lugar equivocado']),
             ('konavi', 556, '"Conavi quiere a la gente"', ['quiere a la gente'])]
    for pal, desde, texto, res in notas:
        t = w(pal, desde)
        edl['capas'].append({'tipo': 'nota', 't': round(t - 0.2, 2), 'dur': 3.2, 'texto': texto, 'resaltar': res})
    edl['capas'].insert(0, {'tipo': 'file', 't': 0.6, 'dur': 4.6, 'texto': 'Los comerciales que nos sabíamos', 'etiqueta': 'Expediente TV', 'titulo': True})
    edl['capas'].sort(key=lambda c: c['t'])
    out = os.path.join(R, 'final', 'edl_comerciales_final.json')
    json.dump(edl, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('->', out, len(planos), 'planos')

if __name__ == '__main__':
    main()
