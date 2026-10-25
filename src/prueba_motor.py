"""EDL de prueba (24 s) con todos los recursos, usando fotogramas de relleno del scratchpad."""
import json, sys
S = sys.argv[1]  # carpeta con imágenes de relleno
img = lambda n: f'{S}/{n}'
edl = {
    'dur': 24.0, 'audio': sys.argv[2],
    'planos': [
        {'t0': 0, 't1': 5, 'tipo': 'imagen', 'src': img('k_55.5.jpg'), 'mov': {'z0': 1.0, 'z1': 1.1}},
        {'t0': 5, 't1': 9, 'tipo': 'imagen', 'src': img('k_22.5.jpg'), 'mov': {'z0': 1.1, 'z1': 1.0, 'c0': [0.4, 0.5], 'c1': [0.6, 0.5]}},
        {'t0': 9, 't1': 13, 'tipo': 'imagen', 'src': img('k_46.5.jpg')},
        {'t0': 13, 't1': 19, 'tipo': 'papel', 'papel': {'modo': 'polaroid', 'fotos': [
            {'src': img('k_385.jpg'), 'pie': 'Betatonio, Bogotá'}, {'src': img('k_104.jpg'), 'pie': 'Cierre en 2007'}]}},
        {'t0': 19, 't1': 24, 'tipo': 'imagen', 'src': img('k_385.jpg'), 'mov': {'z0': 1.0, 'z1': 1.06}},
    ],
    'capas': [
        {'tipo': 'file', 't': 0.6, 'dur': 4.0, 'texto': 'Helados Baloncito'},
        {'tipo': 'numero', 't': 5.4, 'dur': 2.6, 'num': '27', 'label': 'años abierto'},
        {'tipo': 'palabra', 't': 9.3, 'dur': 3.2, 'palabra': 'Rebobinada', 'sub': 'La cinta se devolvía rebobinada… o se pagaba la multa.'},
        {'tipo': 'exhibit', 't': 19.2, 'dur': 4.6, 'items': ['Escoger la película', 'Rebobinar la cinta', 'Pagar la multa']},
        {'tipo': 'nota', 't': 2.0, 'dur': 2.8, 'texto': 'El helado duraba cinco minutos. El balón, toda la vida.', 'resaltar': ['toda la vida']},
    ],
}
json.dump(edl, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
