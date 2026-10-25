# Documental Expediente — "12 Marcas Colombianas que Desaparecieron"

Pipeline completo para hacer videos largos horizontales (16:9, ~14 min) con el estilo de edición copiado del video de referencia «25 Marcas FABRICADAS EN MÉXICO… Antes de Desaparecer»: fichas FILE a máquina, números rojos, palabras gigantes, notas con resaltado, polaroids, carrusel y papel cuadriculado.

**Si eres un chat nuevo de Claude: lee este archivo completo y luego `docs/ESTILO_DOCUMENTAL_EXPEDIENTE.md` antes de tocar nada.**

## Estado (2026-10-24)

El video "12 Marcas Colombianas" está **terminado y entregado**. Los archivos finales están en la PC de Luis, no en este repo, porque pesan demasiado o tienen fotos de terceros:

- `final/12_marcas_colombianas_FINAL.mp4`: la versión para subir.
- `final/miniatura.jpg` y `final/TEXTOS_YOUTUBE.txt`: estos sí están en el repo.

Lo que sigue es el próximo video, anunciado en el guion: **la tienda del colegio y los dulces que comprábamos con monedas**.

## Reglas de Luis (no negociables)

- **Material:** fotos **auténticas** que correspondan a lo que se narra. Se buscan en Google Imágenes, redes sociales y foros. **Nada de imágenes generadas con IA (no Flow).**
- **Créditos:** no se ponen en pantalla ni en la descripción. Solo se guardan internamente en `fuentes.tsv`.
- **Voz:** sin espacios vacíos. Pausas de 0.28 s como máximo. Luis rechazó devolverle respiros.
- **Audio:** solo efectos de sonido sintetizados con código, sin derechos de autor. **Sin música.**
- **Listas:** cada ítem sale **numerado**, con el número rojo grande y el nombre debajo.
- **Descripciones:** sin preguntas, sin mencionar IA, con 3 emojis y la palabra clave primero.
- **Calidad:** fotos HD y horizontales. Si una es pequeña, se mejora con Real-ESRGAN.
- **Forma de trabajar:** en mejoras grandes Luis dijo "no me preguntes nada hasta que lo mejores". Se trabaja de corrido y se entrega terminado.

## Herramientas en la PC de Luis

Windows 11, Intel i3 sin GPU dedicada, 7.7 GB de RAM.

- **Python 3.13** con faster-whisper, PIL y numpy.
- **ffmpeg** en el PATH.
- **Real-ESRGAN:** `C:\Users\luisa\calude\herramientas\realesrgan\realesrgan-ncnn-vulkan.exe`. Siempre con `-t 64`, porque si no la Intel UHD da imagen negra. Tarda unos 35 s por foto.
- **Pixabay:** la clave está en la variable de usuario `PIXABAY_API_KEY`. Se guarda con `src/guardar_clave_pixabay.ps1`.
- **Claude in Chrome** (la extensión) para bajar fotos de Google Imágenes.
- **Batería:** la laptop se suspende con batería baja y eso mata el render. Siempre con el cargador conectado.

## Pipeline paso a paso

| # | Paso | Script / comando |
|---|---|---|
| 1 | Quitar silencios de la voz y normalizar a −14 LUFS | `ffmpeg … silenceremove=…stop_duration=0.15…stop_silence=0.12` + `acompressor` + `loudnorm` de dos pasadas (ver `docs/memoria/colombia12-pipeline.md`) |
| 2 | Transcribir con tiempos por palabra | `python src/transcribir.py audio/voz_final.wav audio/palabras.json` |
| 3 | Alinear el guion con la voz (los títulos INTRO, PARADA N y CIERRE marcan secciones) | `python src/alinear.py guion.txt audio/palabras.json audio/frases.json` |
| 4 | Bajar material: Pixabay (fotos y video) y Wikimedia Commons | `python src/pixabay.py <carpeta> foto\|video <n> "consulta"…` · `python src/commons.py "consulta"` |
| 5 | Bajar fotos de Google Imágenes en tamaño original | `src/receptor.py` (servidor en 127.0.0.1:8765) + la función `loteHD` en Chrome (ver abajo) |
| 6 | Hojas de contacto para elegir | `python src/hoja.py <carpeta> <salida.jpg> "patrón"` |
| 7 | EDL: planos por frase + capas de texto | `src/edl_demo.py` (intro + parada 12) → `src/edl_completo.py` → `src/aplicar_hd.py` → `src/edl_v3.py` |
| 8 | Mejorar las fotos de menos de 1000 px | `python src/mejorar_fotos.py final/edl_hd.json media/hd_esrgan` |
| 9 | Encontrar la misma foto en HD (dHash) | `python src/emparejar_hd.py final/edl_completo.json final/mapa_hd.json` |
| 10 | Recortar logos, firmas y marcos | `src/limpiar.py` (diccionario `RECORTES`) |
| 11 | Render 1920×1080 a 30 fps (4 procesos, unos 15 min para 14 min de video) | `python src/render.py final/edl_v3.json salida.mp4 --workers 4` |
| 12 | Efectos de sonido sintetizados | `python src/efectos.py final/edl_v3.json audio/efectos_v3.wav`, y se mezclan con `amix` + `alimiter` |
| 13 | Miniatura | `python src/miniatura.py` |

### Motor visual

- **`src/estilo.py`:** cada recurso es una función que dibuja sobre el fotograma: `draw_file`, `draw_numero` (con `grande=True` en las aperturas), `draw_palabra`, `draw_nota`, `draw_exhibit` y `escena_papel` (con los modos `unica`, `carrusel`, `polaroid` y `vs`). Los tiempos de animación son los medidos en el video de referencia. Las tipografías Bebas Neue y Special Elite están en `fuentes/`, con licencia OFL/Apache.
- **`src/render.py`:**
  - Tipos de plano: `imagen` (zoom lento con temblor de cámara en mano; las fotos pequeñas o verticales van enmarcadas sobre fondo desenfocado), `video` y `papel`.
  - El papel entra y sale empujando la imagen hacia arriba.
  - Las capas de texto siguen en pantalla aunque cambie el plano de abajo.

### Formato del EDL (json)

```json
{"dur": 832.24, "audio": "audio/voz_final.wav",
 "planos": [{"t0":0,"t1":2.8,"tipo":"imagen","src":"…","mov":{"z0":1,"z1":1.07},"bw":false},
            {"t0":…,"tipo":"video","src":"….mp4","ss":1.0},
            {"t0":…,"tipo":"papel","papel":{"modo":"polaroid","fotos":[{"src":"…","pie":"…"}]}}],
 "capas":  [{"tipo":"numero","t":25.0,"dur":2.3,"num":"12","label":"Helados Baloncito","grande":true},
            {"tipo":"file","t":27.35,"dur":4,"texto":"Helados Baloncito","etiqueta":"Parada 12"},
            {"tipo":"palabra","t":…,"dur":2.9,"palabra":"Heredaba","sub":"frase completa"},
            {"tipo":"nota","t":…,"dur":3,"texto":"…","resaltar":["…"]}]}
```

### Fotos de Google en tamaño original (Claude in Chrome)

1. Arranca el receptor:
   ```powershell
   $env:RECEPTOR_DIR='google_hd'; python src/receptor.py
   ```
2. En Chrome, busca en Google Imágenes con `&udm=2&tbs=isz:l` (tamaño grande).
3. Ejecuta `eval(localStorage.loteHD); loteHD('prefijo', n, anchoMin, proporciónMin)`. La función está guardada en el `localStorage` de google.com; si se perdió, el código está en el historial de la sesión anterior y la idea se explica abajo.

Cómo funciona `loteHD`:
- La URL original y el tamaño de cada foto están en los `<script>` de la página, con el formato `["url",alto,ancho]` justo después del `data-docid` del resultado.
- Facebook e Instagram (`lookaside.*`) solo entregan la imagen si se pide como **Googlebot**, y eso lo hace `receptor.py` del lado de Python.
- Si Chrome pide permiso de "red local" o de "descargas múltiples", Luis debe darle **Permitir**.
- Se pueden usar 4 o 5 pestañas en paralelo. Con más, Google se pone lento.

## Archivos de documentación

- `docs/ESTILO_DOCUMENTAL_EXPEDIENTE.md`: ficha técnica completa del estilo (tiempos, colores, tipografías, estructura de cada parada).
- `docs/memoria/`: notas de trabajo de Claude (pipeline, reglas de feedback y velocidad de la PC).
- `guion.txt`: guion del video de las 12 marcas. Es la plantilla del formato.
- `final/TEXTOS_YOUTUBE.txt`: ejemplo de título, descripción, capítulos y etiquetas.
