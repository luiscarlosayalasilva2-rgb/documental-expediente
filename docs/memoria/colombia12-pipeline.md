---
name: colombia12-pipeline
description: "Video \"12 Marcas Colombianas\" (estilo expediente) ENTREGADO 2026-10-22; pipeline reutilizable para próximas \"rutas\""
metadata:
  node_type: memory
  type: project
  originSessionId: e7fc08e7-3fb2-4af1-ad97-9370faba3811
  modified: 2026-10-22T12:25:58.459Z
---

Video entregado: `C:\Users\luisa\calude\colombia12\final\12_marcas_colombianas_desaparecidas.mp4` (13:52, 1080p). Próxima ruta anunciada en el guion: dulces de la tienda del colegio.

Pipeline en `colombia12\src\`: quitar silencios (silenceremove + loudnorm −14), transcribir.py (faster-whisper small, audio vía ffmpeg porque PyAV falla), alinear.py (guion↔palabras), estilo.py + render.py (motor de plantillas, 4 workers ≈ 15 min para 14 min), edl_*.py (EDL por frase), pixabay.py (clave en env PIXABAY_API_KEY), receptor.py (127.0.0.1:8765) + función `lote` guardada en localStorage de google.com para bajar fotos de Google Imágenes desde Claude in Chrome en 4 pestañas.

Efectos: Luis los pidió "solo efectos, sin copyright" → `src\efectos.py` los sintetiza con numpy (tecleo, golpe en números, whoosh en palabras/papel, obturador en polaroids, especiales) según el EDL; mezcla sin música, todo por debajo de la voz (−2 a −24 dB). Entrega final: `final\12_marcas_colombianas_con_efectos.mp4`.

Versión HD (2026-10-22, entrega vigente): `final\12_marcas_colombianas_HD.mp4`. Fotos de Google en tamaño original: la URL original está en los scripts de la página (`["url",alto,ancho]` tras el docid) y Facebook/Instagram solo la entregan con UA de Googlebot (receptor.py lo hace); `loteHD` en localStorage filtra por ancho/proporción. `emparejar_hd.py` (dHash) + `aplicar_hd.py` (elecciones manuales) + Real-ESRGAN (`C:\Users\luisa\calude\herramientas\realesrgan`, usar `-t 64` o sale negro en la Intel UHD, ~35 s/foto) para las de <1000 px. Ojo: la laptop se suspende por batería y mata el render — pedir cargador conectado.

Entrega vigente (2026-10-22): `final\12_marcas_colombianas_FINAL.mp4` + `final\miniatura.jpg` + `final\TEXTOS_YOUTUBE.txt`. v3 = `src\edl_v3.py` (35 clips de video, sin fotos repetidas, `limpiar.py` recorta logos/firmas) y fuentes Bebas Neue/Special Elite en `colombia12\fuentes` (con Bebas subir tamaños: número 360, palabra 400). Luis rechazó devolver pausas a la voz (quiere voz sin silencios) y pidió "no me preguntes nada hasta que lo mejores": en mejoras grandes, trabajar de corrido y entregar terminado.

**Why:** Luis quiere más videos con este método. **How to apply:** reutilizar estos scripts; fotos auténticas de Google (no Flow, no IA), sin créditos en pantalla ni descripción, números de lista grandes con el nombre ([[feedback-listas-numeradas]]). Estilo en [[estilo-documental-expediente]].
