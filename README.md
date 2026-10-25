# Documental Expediente — "12 Marcas Colombianas que Desaparecieron"

Pipeline completo para hacer videos largos horizontales (16:9, ~14 min) con el estilo de edición copiado del video de referencia «25 Marcas FABRICADAS EN MÉXICO… Antes de Desaparecer»: fichas FILE a máquina, números rojos, palabras gigantes, notas con resaltado, polaroids, carrusel y papel cuadriculado.

**Si eres un chat nuevo de Claude: lee este archivo completo, luego `docs/PROCESO_COMPLETO.md` (toda la historia, errores y correcciones hasta el video final) y `docs/ESTILO_DOCUMENTAL_EXPEDIENTE.md`, antes de tocar nada. El objetivo es replicar ESTA edición con el tema que Luis dé, entregando desde el inicio la calidad del último video.**

## ⚠️ Antes de todo: [docs/REGLAS_DURAS.md](docs/REGLAS_DURAS.md)

Ahí están las reglas obligatorias con metas medibles, las fotos de cómo debe verse cada recurso y lo que está **prohibido**: poner la narración escrita en tarjetas, que pasó en una versión rechazada. Ningún video se entrega sin que **`python src/verificar.py video.mp4 edl.json`** diga **APROBADO**. Las fotos deben pasar los filtros de **[docs/AUTENTICIDAD_FOTOS.md](docs/AUTENTICIDAD_FOTOS.md)** (país, marca correcta, sin dibujos ni comerciales, sin repetir) y la revisión de `python src/revisar_fotos.py final/edl.json`. Para empezar en otra IA hay un prompt listo en [docs/PROMPT_PARA_OTRA_IA.md](docs/PROMPT_PARA_OTRA_IA.md). **Todos los detalles de la edición** (papel que empuja, foto con pie, polaroids, VS, carrusel, blanco y negro…), con su animación cuadro a cuadro y cuántas veces van, están en **[docs/CATALOGO_DETALLES.md](docs/CATALOGO_DETALLES.md)**.

## Estado (2026-10-24)

El video "12 Marcas Colombianas" está **terminado y entregado**. Los archivos finales están en la PC de Luis, no en este repo, porque pesan demasiado o tienen fotos de terceros:

- `final/12_marcas_colombianas_FINAL.mp4`: la versión para subir.
- `final/miniatura.jpg` y `final/TEXTOS_YOUTUBE.txt`: estos sí están en el repo.

Lo que sigue es el próximo video, anunciado en el guion: **la tienda del colegio y los dulces que comprábamos con monedas**.

## Reglas de Luis (no negociables)

- **Material:** fotos **auténticas** que correspondan a lo que se narra, cada imagen pegada al segundo exacto en que la voz lo dice. Guía completa en **`docs/IMAGENES_Y_SINCRONIA.md`**. Se buscan en Google Imágenes, redes sociales y foros. **Nada de imágenes generadas con IA (no Flow).**
- **Créditos:** no se ponen en pantalla ni en la descripción. Solo se guardan internamente en `fuentes.tsv`.
- **Voz:** sin espacios vacíos. Pausas de 0.28 s como máximo. Luis rechazó devolverle respiros.
- **Audio:** solo efectos de sonido sintetizados con código, sin derechos de autor. **Sin música.**
- **Listas:** cada ítem sale **numerado**, con el número rojo grande y el nombre debajo.
- **Descripciones:** sin preguntas, sin mencionar IA, con 3 emojis y la palabra clave primero.
- **Calidad:** fotos HD y horizontales. Si una es pequeña, se mejora con Real-ESRGAN.
- **Forma de trabajar:** en mejoras grandes Luis dijo "no me preguntes nada hasta que lo mejores". Se trabaja de corrido y se entrega terminado.

## Instalación en una PC nueva (o para comprobar esta)

Desde la carpeta del repo:

```powershell
powershell -ExecutionPolicy Bypass -File instalar.ps1
```

El script instala desde sus fuentes oficiales todo lo que falte:
- **Python 3.13** y **ffmpeg**, con winget;
- **faster-whisper, numpy y pillow**, con las versiones de `requirements.txt`;
- **Real-ESRGAN**, el release oficial de xinntao/Real-ESRGAN, que deja en `..\herramientas\realesrgan`;
- el **modelo small de Whisper**.

Se puede volver a correr sin problema: salta lo que ya está instalado.

Hay dos cosas que quedan a mano:
- la **clave de Pixabay**, con `src\guardar_clave_pixabay.ps1`;
- la extensión **Claude in Chrome**.

Estos programas no se suben al repo porque son de terceros y tienen su propia licencia y distribución. El instalador los baja de su sitio original.

## Herramientas en la PC de Luis

Windows 11, Intel i3 sin GPU dedicada, 7.7 GB de RAM.

- **Python 3.13** con faster-whisper, PIL y numpy.
- **ffmpeg** en el PATH.
- **Real-ESRGAN:** `C:\Users\luisa\calude\herramientas\realesrgan\realesrgan-ncnn-vulkan.exe`. Siempre con `-t 64`, porque si no la Intel UHD da imagen negra. Tarda unos 35 s por foto.
- **Pixabay:** la clave está en la variable de usuario `PIXABAY_API_KEY`. Se guarda con `src/guardar_clave_pixabay.ps1`.
- **Claude in Chrome** (la extensión) para bajar fotos de Google Imágenes.
- **Batería:** la laptop se suspende con batería baja y eso mata el render. Siempre con el cargador conectado.

## Receta para un video NUEVO, editado igual que este

Luis entrega dos cosas: el **guion** con secciones `INTRO`, `PARADA N — Nombre` y `CIERRE`, y el **audio** de la voz.

1. **Voz:** `powershell -File src\voz.ps1 -Entrada "<audio.wav>"`.
2. **Guion:** se guarda como `guion.txt` y se corren `src/transcribir.py` y `src/alinear.py`. Así cada frase queda con su segundo exacto, en `audio/frases.json`; para una palabra concreta se usa `src/palabras_en.py`.
3. **Búsquedas:** se hace una lista de búsquedas, **una por cada cosa concreta que se narra**, con el nombre de la marca más el objeto, el lugar o la época. Se lanzan en 4 o 5 pestañas de Chrome con `src/lote_google.js` (filtro `tbs=isz:l`). Para lo genérico se usa Pixabay, en fotos y video.
4. **Hojas de contacto:** con `src/hoja.py` se revisan **todas las fotos con los ojos** y se eligen solo las que muestran lo que se narra.
5. **EDL, con la plantilla automática:**
   ```
   python src/nuevo_video.py plan audio/frases.json audio/palabras.json final/edl_NUEVO.json --etiqueta Parada
   ```
   Arma solo el **esqueleto** con toda la estructura del video aprobado: aperturas y fichas de cada ítem, cortes por idea, números rojos en cada cifra, palabras gigantes, notas en los lemas, blanco y negro en las pérdidas, escenas de papel, huecos de video y el cierre con carrusel.
   - Además deja `final/edl_NUEVO.huecos.md` con **cada foto que hay que buscar** y la frase que se oye en ese segundo.
   - Hay que **rellenar** cada `PENDIENTE` con la ruta de la foto o el clip, y cada `REVISAR` con el texto final (la palabra gigante, la etiqueta del número, los pies).
   - `python src/nuevo_video.py validar final/edl_NUEVO.json` dice qué falta. No se renderiza hasta que salga **LISTO**.
   - `--etiqueta` cambia el texto de la ficha ("Parada", "N°", "Capítulo"…). Los guiones con secciones `INTRO`, `ITEM N — Nombre` y `CIERRE` funcionan con cualquier palabra en lugar de PARADA.
   - Para ajustes finos se puede usar `src/edl_completo.py` como ejemplo de un EDL hecho a mano.
6. **HD:** `src/emparejar_hd.py`, luego `src/aplicar_hd.py`, luego `src/mejorar_fotos.py` (Real-ESRGAN) y `src/limpiar.py` para los recortes.
7. **Video corto de prueba:** antes del video completo se renderiza la intro y la primera parada (`--desde/--hasta`) y se le envía a Luis para que la apruebe.
8. **Final:** `powershell -File src\mezclar.ps1 -Edl final\edl_X.json -Salida final\X_FINAL.mp4`. Después se revisa la hoja de fotogramas cada 8 s y se buscan negros con `blackdetect`.
9. **Miniatura y textos:** `src/miniatura.py`, cambiando las fotos, y un `TEXTOS_YOUTUBE.txt` con los capítulos sacados de los tiempos de cada `abre()`.

### Reglas de edición

Así se construyeron los EDL de este video, que son la referencia exacta: `final/edl_v3.json`.

**Planos**
- **Un plano por idea narrada.** Duración media de 3.7 s, con un mínimo de 0.6 s y casi nunca más de 7 s.
- **Las enumeraciones van en cortes rápidos**, uno por cosa, cortando en el segundo de cada palabra. Ejemplo: "en la nevera, en la mesa de noche, en la billetera, en la tienda" son 4 cortes de 1.1 a 1.3 s.
- **La imagen muestra lo que se dice en ese momento.** Si se habla de una cifra o una fecha, se ve el lugar o el objeto de la marca.
- **El zoom lento alterna** entre acercarse y alejarse: 1.0 → 1.07 y 1.07 → 1.0.
- **Pasado y pérdida en blanco y negro (`#bw`):** cierres, quiebras, "ya no está", "la silla del abuelo quedó vacía".
- **Mezcla de material:** alrededor de **1 clip de video cada 6 planos**, con unos 35 clips en 14 min. Se usan para ambientes (ciudad aérea, mercado, escaleras, pasillos vacíos) y acciones (comer paleta, caballos corriendo, llaves).
- **Sin repetir fotos**, salvo en el carrusel de repaso del cierre.

**Estructura de cada parada**
1. `abre(t, N, 'Marca')`: el número rojo grande, de 2.3 s, con el nombre de la marca debajo en letras grandes. Luego la ficha **FILE** "PARADA N", 2.35 s después.
2. Fotos de la marca y del contexto, siguiendo la narración.
3. **Número rojo** (`numero`, de 2.0 a 2.4 s) en cada **año o cifra clave** de la narración: fundación, cierre, precios, cantidades. Entra en el segundo exacto en que se dice la cifra, buscado con `w('cifra', desde, defecto)`.
4. **Palabra gigante** (`palabra`, de 1.7 a 3.4 s) en la frase emocional más fuerte: más o menos **una cada 60 s**, y siempre en la frase final de la parada. La palabra va en mayúsculas, con la frase completa debajo.
5. **Nota a máquina** (`nota`) para los **lemas y frases célebres** entre comillas («Siempre te da más», «Listo Medellín, cabina 8»), resaltando de 1 a 3 palabras.
6. **Escena de papel** (polaroid, foto única o VS), de 6 a 8 s, una o dos por parada. Polaroid para comparaciones o para tres marcas juntas, VS para rivalidades (Konga contra Postobón).

**Intro y cierre**
- **Intro:** cortes rápidos con objetos cotidianos, la palabra clave del tema y un número con el total de ítems.
- **Cierre:** el número del total, un carrusel con una foto de cada marca y su número, y la palabra final.

**Textos que se pisan:** dos números o palabras no pueden encimarse; el script lo avisa. Si pasa, se acorta el `dur`.

**Audio:** voz sin pausas y los efectos sintetizados que genera `src/efectos.py` según las capas del EDL. Sin música.

## Pipeline paso a paso

| # | Paso | Script / comando |
|---|---|---|
| 1 | Quitar silencios de la voz y normalizar a −14 LUFS | `powershell -File src\voz.ps1 -Entrada <audio.wav>` |
| 2 | Transcribir con tiempos por palabra | `python src/transcribir.py audio/voz_final.wav audio/palabras.json` |
| 3 | Alinear el guion con la voz (los títulos INTRO, PARADA N y CIERRE marcan secciones) | `python src/alinear.py guion.txt audio/palabras.json audio/frases.json` |
| 4 | Bajar material: Pixabay (fotos y video) y Wikimedia Commons | `python src/pixabay.py <carpeta> foto\|video <n> "consulta"…` · `python src/commons.py "consulta"` |
| 5 | Bajar fotos de Google Imágenes en tamaño original | `src/receptor.py` (servidor en 127.0.0.1:8765) + `src/lote_google.js` en Chrome (ver abajo) |
| 6 | Hojas de contacto para elegir | `python src/hoja.py <carpeta> <salida.jpg> "patrón"` |
| 7 | EDL: planos por frase + capas de texto | `src/edl_demo.py` (intro + parada 12) → `src/edl_completo.py` → `src/aplicar_hd.py` → `src/edl_v3.py` |
| 8 | Mejorar las fotos de menos de 1000 px | `python src/mejorar_fotos.py final/edl_hd.json media/hd_esrgan` |
| 9 | Encontrar la misma foto en HD (dHash) | `python src/emparejar_hd.py final/edl_completo.json final/mapa_hd.json` |
| 10 | Recortar logos, firmas y marcos | `src/limpiar.py` (diccionario `RECORTES`) |
| 11 | Render 1920×1080 a 30 fps (4 procesos, unos 15 min para 14 min de video) | `python src/render.py final/edl_v3.json salida.mp4 --workers 4` |
| 12 | Render + efectos de sonido sintetizados + mezcla con la voz | `powershell -File src\mezclar.ps1 -Edl final\edl_v3.json -Salida final\X.mp4` |
| 13 | Miniatura | `python src/miniatura.py` |
| 14 | Subtítulos .srt para YouTube (no van en la imagen) | `python src/generar_srt.py audio/frases.json final/X.srt` |
| 15 | Verificación obligatoria (con EDL) | `python src/verificar.py final/X.mp4 final/edl.json` |

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
3. Pega el contenido de `src/lote_google.js` en la pestaña, con `javascript_tool` de Claude in Chrome, y llama a `loteHD('prefijo', n, anchoMin, proporciónMin)`. Si lo guardas en `localStorage.loteHD`, las demás pestañas de google.com lo reutilizan con `eval(localStorage.loteHD)`.

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
- `datos/palabras.json`, `datos/frases.json`: la transcripción con tiempos y la alineación del guion de este video.
- `src/analisis/`: los scripts con los que se analizó el video de referencia (cortes, brillo por fotograma y efectos de sonido).
- `CLAUDE.md`: hace que Claude lea este README al abrir la carpeta.

## Reproducir ESTE mismo video

**En la misma PC de Luis** funciona tal cual. Los EDL (`final/*.json`) apuntan a las fotos y clips que siguen en `C:\Users\luisa\calude\colombia12\media\` y a la voz en `audio\`. Basta con:

```powershell
powershell -File src\mezclar.ps1 -Edl final\edl_v3.json -Salida final\copia.mp4
```

**En otra PC** hay que copiar también las carpetas `media\` y `audio\`, que pesan unos 4.6 GB y no están en GitHub, y ajustar las rutas de los EDL.
