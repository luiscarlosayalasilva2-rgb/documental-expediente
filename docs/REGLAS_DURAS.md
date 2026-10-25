# Reglas duras (OBLIGATORIAS para cualquier IA: Claude, Muse u otra)

Luis quiere **exactamente la edición del video aprobado**, `final/12_marcas_colombianas_FINAL.mp4`. Las reglas son medibles, y `src/verificar.py` las comprueba. **Si el verificador dice NO APROBADO, el video no se entrega**: se corrige y se vuelve a medir.

```
python src/verificar.py final/MI_VIDEO.mp4 final/mi_edl.json
```

## Lo que NO se hace (pasó con una versión rechazada, el v4 hecho con otro agente)

![no hacer](referencia/NO_HACER_texto_de_la_narracion_en_tarjeta.jpg)

- **PROHIBIDO escribir un editor propio o rediseñar las plantillas.** Se usa `src/render.py` + `src/estilo.py` tal cual; solo cambia el EDL. La versión rechazada hizo su propio editor, con otro diseño y sin la mitad de los recursos.
- **PROHIBIDO poner la narración escrita en tarjetas de papel** como relleno. La voz ya la dice. En la versión rechazada eso ocupó el **69 %** del video.
- **PROHIBIDO dejar una imagen o tarjeta quieta** durante muchos segundos. La versión rechazada tuvo un tramo de 51 s sin cambiar.
- **PROHIBIDO usar frames de comerciales de TV** (las hormiguitas de "Aló, Mamá", la abejita del comercial de Conavi). Content ID los detecta.
- **PROHIBIDO imágenes generadas con IA.**
- **Si no hay foto de algo:** se busca más (Google, redes, foros), se usa una foto de la época o un **clip de video real** del ambiente. **Nunca** se resuelve con texto en pantalla.

## Metas medidas (video aprobado y versión rechazada)

| Medida | Meta | Aprobado | Rechazado (v4) |
|---|---|---|---|
| Texto en papel en pantalla | **≤ 15 %** | 6 % | 69 % |
| Cortes por minuto | **≥ 12** | 13.7 | 8.2 |
| Plano más largo (EDL) | **≤ 11 s** | 10.3 s | — |
| Tramo sin corte visible | **≤ 30 s** | 28.5 s* | 50.8 s |
| Números o palabras gigantes (fondo oscurecido) | **≥ 3 por minuto** | 3.5 | 0.4 |
| Clips de video real | **≥ 25 por cada 14 min** | 35 | casi 0 |
| Fotos repetidas (sin contar el carrusel del cierre) | **0** | 0 | — |
| Aperturas numeradas (número grande + nombre) | **1 por ítem** | 12 de 12 | parcial |
| Números rojos de cifras (años, precios) | **≥ 1 por ítem** | 24 | casi 0 |
| Palabras gigantes | **≥ 1 cada 1.5 min** | 24 | 0 |
| Notas a máquina (lemas entre comillas) | **≥ 1 cada 2 ítems** | 11 | 0 |
| Voz: volumen y pausas | −16 a −13 LUFS, pausas ≤ 0.35 s | −15.4 / 0 | −14.7 / 0 ✔ |

\*Son fotos en blanco y negro muy parecidas, en las que el detector no ve el corte. La duración real de cada plano la da el EDL.

## Así debe verse cada recurso (fotogramas del video aprobado)

![referencia](referencia/_todos.jpg)

| Recurso | Cuándo se usa | Ejemplo |
|---|---|---|
| Apertura numerada | primer segundo de cada ítem: número rojo grande + nombre en mayúsculas (2.3 s) | `referencia/01_apertura_numerada.jpg` |
| Ficha "PARADA N" | 2.35 s después de la apertura, arriba a la izquierda, sobre la foto | `02_ficha_parada.jpg` |
| Foto con zoom lento | la base del video: **la foto real de lo que se narra**, de 2 a 6 s | `03_foto_con_zoom.jpg` |
| Video real | ambientes y acciones, cerca de 1 de cada 6 planos | `04_video_real.jpg` |
| Número rojo | en el segundo exacto en que la voz dice un año o una cifra | `05_numero_rojo.jpg` |
| Palabra gigante | en la frase emocional más fuerte y al final de cada ítem | `06_palabra_gigante.jpg` |
| Nota a máquina | **solo** para lemas o frases célebres entre comillas, abajo y corta, **sobre una foto** | `07_nota_a_maquina.jpg` |
| Polaroid / VS / carrusel | 1 o 2 por ítem, de 6 a 8 s, con fotos reales | `08`, `09`, `10` |

**La pantalla casi siempre es una FOTO o un VIDEO real** que muestra lo que se narra. Los textos son acentos cortos encima de la imagen, nunca el contenido principal.

## Orden de trabajo obligatorio

1. Leer `README.md`, `docs/IMAGENES_Y_SINCRONIA.md` y este archivo.
2. Bajar las fotos **reales** de cada cosa narrada (una búsqueda por cosa, unas 10 por ítem).
3. Armar el EDL con `src/edl_completo.py` como plantilla.
4. Renderizar **un demo de 1 minuto** y pasarle `src/verificar.py`. Luis lo aprueba.
5. Renderizar el video completo, pasarle `src/verificar.py` y entregarlo **solo si sale APROBADO**.
