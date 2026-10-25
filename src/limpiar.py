"""Recorta logos, firmas, marcas de agua, marcos y textos de publicaciones (media/limpias/<nombre>).

RECORTES = {nombre_archivo: (izq, arriba, der, abajo)} en fracciones de la imagen.
Se aplica al archivo que use el EDL, venga de google, google_hd o hd_esrgan (se busca por nombre).
"""
import glob, os
from PIL import Image

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RECORTES = {
    'intro_tienda_07.jpg': (0.22, 0.0, 1.0, 1.0),          # logo NOSTALGIAS
    'hd_p12_colegio_00.jpg': (0.0, 0.0, 1.0, 0.88),        # #MemoriaSeñoraEscolar
    'hd_p12_monedas_00.jpg': (0.0, 0.0, 1.0, 0.88),        # @MonedasColombia
    'p12_baloncito_campina_1.jpg': (0.08, 0.08, 0.92, 0.92),  # marco de Instagram
    'p12_baloncito_01.jpg': (0.08, 0.08, 0.92, 0.92),
    'p12_baloncito_00.jpg': (0.5, 0.0, 1.0, 0.5),          # collage "Los ochenteros": solo el balón amarillo
    'b11_betatonio_05.jpg': (0.0, 0.0, 0.5, 0.5),          # collage: solo la fachada
    'hd_b10_konga_00.jpg': (0.08, 0.10, 0.80, 0.86),       # marca de agua del comercial
    'hd_b08_caballo_00.jpg': (0.05, 0.18, 0.85, 0.88),     # "Fotos Suba D.E" y firma
    'hd_b08_publico_04.jpg': (0.0, 0.0, 0.85, 0.90),       # logo del periódico
    'b07_caravana_01.jpg': (0.04, 0.08, 0.96, 0.91),       # texto y marco del grupo
    'b07_caravana_04.jpg': (0.04, 0.08, 0.96, 0.91),
    'hd_b07_centro_02.jpg': (0.0, 0.0, 1.0, 0.86),         # "La Playa x Junín / Memoria Visual"
    'hd_b02_ley2_00.jpg': (0.03, 0.03, 0.97, 0.87),        # pie de foto y marco
    'hd_b02_ley2_01.jpg': (0.04, 0.04, 0.96, 0.88),
    'b08_fila_00.jpg': (0.0, 0.0, 1.0, 0.93),              # "Archivo de Bogotá"
    'b08_fila_04.jpg': (0.0, 0.0, 1.0, 0.93),
    'hd_b01_mil_01.jpg': (0.0, 0.0, 1.0, 0.86),            # @MonedasColombia
    'b04_tatuaje_03.jpg': (0.07, 0.05, 0.93, 0.95),        # marco amarillo
    'hd_b03_bogota_01.jpg': (0.0, 0.08, 0.90, 1.0),        # marca de agua HFBC
}

def limpiar(ruta):
    """Devuelve la ruta de la versión recortada (creándola si hace falta) o la misma ruta."""
    n = os.path.basename(ruta)
    if n not in RECORTES: return ruta
    dest = os.path.join(R, 'media', 'limpias', n)
    if not os.path.exists(dest) or os.path.getmtime(dest) < os.path.getmtime(ruta):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im = Image.open(ruta).convert('RGB'); w, h = im.size
        l, t, r, b = RECORTES[n]
        im.crop((int(l * w), int(t * h), int(r * w), int(b * h))).save(dest, quality=93)
    return dest
