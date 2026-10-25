"""EDL del demo: INTRO + PARADA 12 (0 - 77.4 s). Tiempos tomados de audio/palabras.json."""
import json, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
g = lambda n: os.path.join(R, 'media', 'google', n)
px = lambda n: os.path.join(R, 'media', 'pixabay', n)

def img(t0, t1, src, z0=1.0, z1=1.07, c0=(0.5, 0.5), c1=(0.5, 0.5), **kw):
    return {'t0': t0, 't1': t1, 'tipo': 'imagen', 'src': src, 'mov': {'z0': z0, 'z1': z1, 'c0': list(c0), 'c1': list(c1)}, **kw}

def papel(t0, t1, modo, fotos, **kw):
    return {'t0': t0, 't1': t1, 'tipo': 'papel', 'papel': {'modo': modo, 'fotos': fotos, **kw}}

planos = [
    # INTRO
    img(0.0, 2.8, g('intro_tienda_01.jpg'), 1.0, 1.06),
    img(2.8, 4.7, g('intro_tienda_00.jpg'), 1.06, 1.0),
    img(4.7, 5.8, g('intro_nevera_00.jpg'), 1.0, 1.05),
    img(5.8, 7.1, px('bedside_table_lamp_vintage_2.jpg'), 1.05, 1.0, (0.45, 0.5), (0.55, 0.5)),
    img(7.1, 8.4, px('old_wallet_leather_2.jpg'), 1.0, 1.06),
    img(8.4, 9.7, g('intro_tienda_02.jpg'), 1.05, 1.0),
    img(9.7, 12.8, g('intro_tienda_07.jpg'), 1.0, 1.07, bw=True),
    img(12.8, 19.3, g('intro_tienda_03.jpg'), 1.0, 1.08, (0.45, 0.5), (0.55, 0.5)),
    papel(19.3, 25.0, 'polaroid', [{'src': g('intro_tienda_00.jpg'), 'pie': 'La tienda de la esquina'},
                                   {'src': g('p12_colegio_07.jpg'), 'pie': 'El colegio, años 90'}]),
    # PARADA 12 — Baloncito
    img(25.0, 28.3, g('p12_colegio_06.jpg'), 1.0, 1.06),
    img(28.3, 32.0, g('p12_colegio_00.jpg'), 1.06, 1.0, (0.4, 0.5), (0.6, 0.5)),
    img(32.0, 35.0, g('p12_monedas_05.jpg'), 1.0, 1.08),
    img(35.0, 38.8, g('p12_carrito_05.jpg'), 1.0, 1.06),
    img(38.8, 42.1, g('p12_baloncito_05.jpg'), 1.06, 1.0),
    img(42.1, 45.6, g('p12_baloncito_campina_1.jpg'), 1.0, 1.07),
    img(45.6, 48.8, g('p12_baloncito_00.jpg'), 1.0, 1.06),
    papel(48.8, 54.9, 'unica', [{'src': g('p12_baloncito_01.jpg'), 'pie': 'El balón que se quedó en la casa'}]),
    img(54.9, 59.3, g('p12_baloncito_02.jpg'), 1.0, 1.06),
    img(59.3, 62.9, g('p12_mundial_03.jpg'), 1.0, 1.07),
    img(62.9, 65.1, g('p12_mundial_05.jpg'), 1.06, 1.0),
    img(65.1, 68.1, g('p12_carrito_04.jpg'), 1.0, 1.06),
    papel(68.1, 74.45, 'polaroid', [{'src': g('p12_coladetigre_04.jpg'), 'pie': 'Paleta Cola de Tigre'},
                                    {'src': g('p12_coladetigre_05.jpg'), 'pie': 'Las franjas de colores'}]),
    img(74.45, 77.4, px('boy_eating_ice_cream_1.jpg'), 1.0, 1.06),
]

capas = [
    {'tipo': 'palabra', 't': 1.75, 'dur': 2.9, 'palabra': 'Heredaba', 'sub': 'Hay marcas que uno no escogía: las heredaba.'},
    {'tipo': 'numero', 't': 14.25, 'dur': 3.0, 'num': '12', 'label': 'paradas, doce marcas'},
    {'tipo': 'file', 't': 25.75, 'dur': 4.4, 'texto': 'Helados Baloncito'},
    {'tipo': 'nota', 't': 42.1, 'dur': 3.4, 'texto': 'El helado duraba cinco minutos. El balón, toda la vida.', 'resaltar': ['toda la vida']},
    {'tipo': 'numero', 't': 55.85, 'dur': 2.8, 'num': '30', 'label': 'años después'},
    {'tipo': 'numero', 't': 61.25, 'dur': 2.6, 'num': '4', 'label': 'años entre mundiales'},
    {'tipo': 'palabra', 't': 74.45, 'dur': 2.95, 'palabra': 'Premio', 'sub': 'Sabía a premio. Sabía a «ya salí».'},
]

edl = {'dur': 77.4, 'audio': os.path.join(R, 'audio', 'voz_final.wav'), 'planos': planos, 'capas': capas}
json.dump(edl, open(os.path.join(R, 'demo', 'edl_demo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('planos', len(planos), 'capas', len(capas))
