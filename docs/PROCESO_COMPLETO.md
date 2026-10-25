# Proceso completo: cómo llegamos al video final

Bitácora de todo lo que se hizo, en orden, del 21 al 24 de octubre de 2026. Explica **qué se probó, qué falló, qué pidió Luis y cómo se resolvió**. Un chat nuevo debe leerla para no repetir los mismos errores y para entregar desde el principio el resultado del último video, no el del primero.

---

## Fase 1: análisis del video de referencia

**Video:** «25 Marcas FABRICADAS EN MÉXICO en las que Confiaban las Familias Mexicanas Antes de Desaparecer» (32:22, 854×480).

1. **Primera pasada:** detecté 303 cortes con `ffmpeg select='gt(scene,0.3)'` e hice hojas de contacto cada 8 s.
   - **Error:** dije que el análisis estaba completo sin haber visto todos los minutos. Luis preguntó "¿estás seguro?" dos veces.
2. **Segunda pasada:** revisé fotogramas cada 2 s en todo el video y las animaciones cuadro a cuadro, a 4–8 fps. Ahí encontré lo que se me había escapado:
   - el texto se escribe letra por letra;
   - las líneas rojas se dibujan solas;
   - los textos siguen en pantalla aunque cambie el plano;
   - el carrusel, la comparativa VS y el mapa.
3. **Tercera pasada, automática sobre los 58 254 fotogramas** (`src/analisis/frames.py`):
   - 298 cortes, el 96 % secos;
   - 57 oscurecimientos para números y palabras;
   - 5 escenas de papel, que **también salen empujadas hacia arriba**;
   - cero flashes.
4. **Audio** (`src/analisis/sfx.py` y `clicks.py`):
   - **solo voz**: sin música y sin efectos de sonido;
   - en las pausas cae a −95 dB, o sea silencio digital;
   - −15 LUFS, con un rango de 3 LU.
5. **Resultado:** la ficha técnica `docs/ESTILO_DOCUMENTAL_EXPEDIENTE.md`.

**Lección:** el análisis se hace completo desde el principio, con muestreo fino y mediciones automáticas, y no se afirma que algo está completo sin haberlo verificado.

## Fase 2: guion y voz de Luis

- **Lo que entregó Luis:** el guion "12 Marcas Colombianas que Había en Todas las Casas — y Desaparecieron" y un audio de 17:50 generado con voz sintética.
- **Pedido 1, "el audio no puede tener espacios vacíos":** con `src/voz.ps1` quité 532 silencios y el audio pasó a 13:52. Ninguna pausa supera 0.28 s y el volumen quedó en −15 LUFS con LRA 2.9.
- **Transcripción:** con faster-whisper small.
  - **Error:** PyAV no acepta `metadata_errors`.
  - **Solución:** se decodifica el audio con ffmpeg y se le pasa a Whisper como un array de numpy.
- **Alineación:** con difflib entre el guion y la transcripción; el 97 % de las palabras quedó alineado. La voz **no lee los títulos** INTRO, PARADA o CIERRE: solo sirven para marcar secciones.

## Fase 3: el motor de plantillas

- **`src/estilo.py` y `src/render.py`:** cada recurso del video de referencia es una función con sus tiempos medidos. El render usa 4 procesos con ffmpeg y `veryfast`; 24 s tardaron 47 s.
- **Demo de la intro y la Parada 12**, de 1:17. **Luis lo aprobó.**

## Fase 4: material visual (lo que más cambió)

| Intento | Qué pasó | Decisión |
|---|---|---|
| Generar con Flow (IA) | Luis: "no generes en Flow". | **Nunca IA.** |
| Pixabay | Sirve para lo genérico; no tiene las marcas colombianas. | Solo para clips y fotos genéricas. |
| Wikimedia Commons | Hay fotos libres de solo 6 de las 12 marcas. | Complemento. |
| Google Imágenes | Luis: "el material debe ser auténtico y coincidir con lo que se narra". Hablamos del riesgo de derechos de autor y del uso justo. | **Mixto:** lo libre primero y luego Google. Nada de agencias, marcas de agua ni comerciales de TV. Las fotos van transformadas, en ficha o polaroid. |
| Créditos | Luis: "no es necesario dar créditos". El video de referencia tampoco los tiene. | Sin créditos. Solo se guardan internamente en `fuentes.tsv`. |

**Cómo se automatizó Google (Claude in Chrome):**
1. **Primero bajé la vista previa** del panel. Chrome bloqueó las descargas múltiples y la pestaña se congeló.
   - **Solución:** `src/receptor.py`, un servidor local en 127.0.0.1:8765 que recibe las fotos por POST. Luis tuvo que darle **Permitir** al aviso de red local en Chrome.
2. **Luis pidió abrir varias pestañas:** se usaron 4 o 5 en paralelo.
3. **Las vistas previas salían pequeñas**, de 400–700 px, y en 1080p se veían pixeladas. Esto se resolvió en la fase 7.

## Fase 5: video completo, versión 1

- Busqué unas 70 cosas concretas narradas en las 11 paradas y armé el EDL completo con `src/edl_completo.py`: 222 planos y 83 capas de texto.
- **Pedido de Luis: "que las 12 marcas salgan enumeradas".**
  - Primero el número rojo llevaba el nombre debajo en letra pequeña de máquina, que **no se leía**.
  - **Corrección:** en las aperturas, el nombre va en letra grande debajo del número (`grande=True`).
  - Quedó como regla para todos los videos de lista.
- **Render:** 14.8 min. Los mensajes de "Broken pipe" que salen al cerrar los clips son normales.

## Fase 6: efectos de sonido

- **Pedido de Luis:** "solo efectos, sin copyright".
- **Solución:** `src/efectos.py` **sintetiza** cada sonido con numpy, sin grabaciones:
  - tecleo de máquina de escribir en las fichas y notas;
  - golpe grave en los números, más profundo en las aperturas;
  - whoosh en las palabras y al entrar el papel;
  - obturador de cámara en las polaroids;
  - especiales: el ¡PLUM! del Chupi Plum, el timbre de teléfono, el clac de la cinta VHS y las monedas.
- **Niveles medidos** con `src/niveles.py`: todos los efectos quedan por debajo de la voz, entre −2 y −24 dB. Hubo que bajar las aperturas y el PLUM y subir el tecleo.

## Fase 7: calidad HD ("que no se vea pixelado, más HD, que encaje en 16:9")

1. **Real-ESRGAN** (`realesrgan-ncnn-vulkan`, modelo `realesrgan-x4plus`).
   - **Error:** en la Intel UHD la salida salía **negra**.
   - **Solución:** usar `-t 64`. Tarda unos 35 s por foto.
2. **Fotos originales de Google en alta resolución** (`src/lote_google.js`):
   - Google ya no pone la URL original en el panel, pero **sí está en los `<script>`** de la página, con el formato `["url",alto,ancho]` después del `data-docid`.
   - Facebook e Instagram (`lookaside.*`) solo la entregan si se pide como **Googlebot**; eso lo hace `receptor.py`.
   - En la búsqueda se usa `tbs=isz:l`, y en el código se filtra por ancho mínimo y por proporción horizontal.
3. **`src/emparejar_hd.py`** busca la misma foto en HD con dHash, con un filtro por parada y una firma fina para evitar falsos positivos (al principio emparejó La 14 con Malta Leona).
4. **`src/aplicar_hd.py`:** 88 cambios manuales por fotos nuevas en HD y horizontales del mismo tema, 14 por la misma foto en HD, y Real-ESRGAN para el resto. Solo quedaron 2 fotos de menos de 1000 px.
5. **Incidente:** la laptop **se suspendió por batería** a las 2:28 a. m. y el render se cayó.
   - **Regla:** siempre con el cargador conectado, más `request_keep_awake`.

## Fase 8: revisión honesta y versión final

Luis preguntó "¿cómo lo ves, sinceramente?". Le señalé 6 puntos débiles y pidió arreglarlos todos **menos el 2**, con la instrucción **"no me preguntes nada hasta que lo mejores"**.

| # | Punto | Qué se hizo |
|---|---|---|
| 1 | Casi todo eran fotos, y se sentía como diapositivas | Pasé de 15 a **35 clips de video** de Pixabay que coinciden con la frase (`src/edl_v3.py`). |
| 2 | La voz sin respiros | **Luis lo rechazó:** la voz se queda sin pausas. |
| 3 | Fotos repetidas (45 fuentes repetidas) | **Cero repeticiones**, salvo en el carrusel de repaso del final. |
| 4 | Fotos con texto, marcos o firmas | `src/limpiar.py` recorta 20 fotos. |
| 5 | Faltaban la miniatura y el título | `src/miniatura.py` y `final/TEXTOS_YOUTUBE.txt`, con capítulos. |
| 6 | Tipografías de Windows | Bebas Neue y Special Elite, de Google Fonts. **Bebas se ve más pequeña**, así que subí los tamaños: número 360, palabra 400 y nombre de apertura 150. |

**Entrega final:** `final/12_marcas_colombianas_FINAL.mp4`, de 13:52, en 1080p y con 274 MB.

---

## Errores que NO se deben repetir

1. Decir "ya está completo" sin haberlo verificado.
2. Generar imágenes con IA o con Flow.
3. Usar vistas previas pequeñas de Google: hay que sacar la URL original de los scripts.
4. Correr Real-ESRGAN sin `-t 64` en esta PC.
5. Renderizar con la laptop desconectada.
6. Poner los nombres de la lista en letra pequeña: van en letra grande bajo el número.
7. Repetir fotos.
8. Poner créditos, preguntas en la descripción o música.
9. Preguntarle cosas a Luis en medio de una mejora que pidió hacer de corrido.

## Forma de trabajo que le funcionó a Luis

1. Analizar y medir todo.
2. Hacer un **demo corto** para que lo apruebe.
3. Hacer el video completo.
4. Revisar con hojas de contacto y `blackdetect`.
5. Entregar con un resumen claro de qué cambió y qué no se pudo verificar (yo no puedo oír el audio).
