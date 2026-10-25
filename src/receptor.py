"""Receptor local: guarda en media/google/ las imágenes que la pestaña de Chrome le envía por POST.

Escucha solo en 127.0.0.1:8765. POST /guardar?nombre=archivo.jpg&info=texto con el cuerpo = bytes de la imagen.
Cada guardado se anota en media/google/fuentes.tsv (nombre, tamaño, info) para los créditos.
"""
import os, re, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DEST = os.path.join(os.path.dirname(__file__), '..', 'media', os.environ.get('RECEPTOR_DIR', 'google'))
os.makedirs(DEST, exist_ok=True)

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        nombre = re.sub(r'[^A-Za-z0-9_.-]', '_', q.get('nombre', ['sin_nombre.jpg'])[0])
        datos = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        if q.get('u'):
            # foto original: la baja Python desde su página (sin CORS); si falla, se queda la vista previa enviada
            # las páginas de Facebook/Instagram solo entregan la imagen a buscadores; se prueba con varios agentes
            for ua in ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'):
                try:
                    req = urllib.request.Request(q['u'][0], headers={'User-Agent': ua, 'Referer': q.get('ref', [''])[0]})
                    orig = urllib.request.urlopen(req, timeout=20).read()
                    if len(orig) > max(len(datos), 20000) and orig[:3] in (b'\xff\xd8\xff', b'\x89PN', b'RIF'):
                        datos = orig; break
                except Exception:
                    pass
        if not datos:
            self.send_response(204); self._cors(); self.end_headers(); return
        with open(os.path.join(DEST, nombre), 'wb') as f:
            f.write(datos)
        with open(os.path.join(DEST, 'fuentes.tsv'), 'a', encoding='utf-8') as f:
            f.write(f"{nombre}\t{len(datos)}\t{q.get('info', [''])[0]}\n")
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b'ok')

    def log_message(self, *a):
        pass

ThreadingHTTPServer(('127.0.0.1', 8765), H).serve_forever()
