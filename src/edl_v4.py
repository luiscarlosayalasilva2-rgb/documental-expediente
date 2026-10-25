"""v4 del video aprobado: igual que edl_v3.json pero sin las 9 fotos repetidas que detectó revisar_fotos.py
(8 reemplazos + el Chupi Plum que Real-ESRGAN había guardado con la imagen equivocada, ya regenerado).
Los índices son los de final/edl_v3.json.
"""
import json, os
import limpiar

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def foto(n):
    # recortada y luego agrandada con Real-ESRGAN (media/hd_esrgan_limpias) si el recorte quedó pequeño
    up = os.path.join(R, 'media', 'hd_esrgan_limpias', n)
    if os.path.exists(up): return up
    for d in ('hd_esrgan', 'google_hd', 'google'):
        p = os.path.join(R, 'media', d, n)
        if os.path.exists(p): return limpiar.limpiar(p)
    raise FileNotFoundError(n)

e = json.load(open(os.path.join(R, 'final', 'edl_v3.json'), encoding='utf-8'))
P = e['planos']
P[16]['papel']['fotos'][0]['src'] = foto('p12_matera_00.jpg')          # balón que se quedó en la casa
P[30]['src'] = foto('hd_b11_videoclub_02.jpg')                          # la pelea por la última copia
P[75]['src'] = foto('b09_granahorrar_07.jpg')                           # intervenido en 1998 (B/N)
P[84]['src'] = foto('b08_fila_03.jpg')                                  # fila frente a las cabinas
P[102]['papel']['fotos'][0]['src'] = foto('b07_caravana_06.jpg')       # polaroid de Caravana
P[105] = {'t0': P[105]['t0'], 't1': P[105]['t1'], 'tipo': 'video', 'ss': 1.0, 'bw': False,
          'src': os.path.join(R, 'media', 'pixabay_v2', 'escalator_shopping_mall_3.mp4')}  # montar en las escaleras
P[155]['src'] = foto('b04_chupiplum_05.jpg')                           # el Chupi Plum original (era la misma foto de la caja)
P[179]['src'] = foto('b03_tia_03.jpg')                                 # el Tía no desapareció del mundo (B/N)
P[216]['papel']['fotos'][0].update(src=foto('b01_alcancia_03.jpg'), pie='La abejita que nos enseñó a ahorrar')

json.dump(e, open(os.path.join(R, 'final', 'edl_v4.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('final/edl_v4.json')
