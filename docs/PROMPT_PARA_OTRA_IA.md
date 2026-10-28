# Prompt para pegar en otro chat (Claude, Muse u otra IA)

Copia esto tal cual al empezar un chat nuevo y cambia lo que está entre [corchetes]:

---

Vas a editar un video documental largo, horizontal 16:9, **exactamente con la misma edición** que el video aprobado de este repositorio: https://github.com/luiscarlosayalasilva2-rgb/documental-expediente

Antes de hacer nada: **`git pull`** (el repo se actualiza seguido) y lee **`docs/NOVEDADES.md`**, que dice qué cambió y qué hay que corregir en un video que ya tengas hecho. Después lee completos y en este orden:
1. `docs/REGLAS_DURAS.md`: reglas obligatorias, metas medibles y fotos de cómo debe verse cada recurso.
   - `docs/CATALOGO_DETALLES.md`: **todos los detalles de la edición** con su animación y cuántas veces van. Hay que ponerlos **todos**: papel que empuja con foto y pie, polaroids, VS, carrusel, blanco y negro y notas.
2. `README.md`: la receta paso a paso y las reglas de edición.
3. `docs/IMAGENES_Y_SINCRONIA.md`: cómo elegir cada imagen según lo que se narra y pegarla al segundo del audio.
4. `docs/PROCESO_COMPLETO.md`: los errores que ya se cometieron y cómo se resolvieron.

Reglas que no se negocian:
- Usa el motor del repo (`src/render.py` y `src/estilo.py`) sin modificar el diseño. No escribas tu propio editor: solo armas el EDL (json) y lo renderizas con `src/mezclar.ps1`.
- El EDL **se arma con `python src/nuevo_video.py plan …`**, que crea el esqueleto con toda la estructura. Tú solo rellenas los `PENDIENTE` (una foto o un clip real de lo que se oye en ese segundo, guiándote por el archivo `.huecos.md`) y los `REVISAR` (textos). Antes de renderizar corre `python src/nuevo_video.py validar …` hasta que diga LISTO.
- La pantalla casi siempre muestra una **foto o un video real de lo que la voz dice en ese segundo**, con zoom lento. **Nunca** se pone la narración escrita en tarjetas. Los textos (número rojo, palabra gigante, ficha, nota corta) son acentos encima de la imagen.
- Cortes cada 3 o 4 s en promedio, ningún plano de más de 11 s, unos 35 clips de video en 14 min, cero fotos repetidas.
- Cada ítem de la lista abre con su **número rojo grande y el nombre** debajo, y luego la ficha "PARADA N".
- Fotos auténticas (Google, redes, foros, Pixabay o Commons). Nada de imágenes de IA, frames de comerciales de TV ni marcas de agua.
- **Autenticidad:** lee `docs/AUTENTICIDAD_FOTOS.md`. Cada foto debe ser **del país del video** y de **la marca correcta**, no de un homónimo: nada de Casa Ley de México, Tía de Ecuador ni CONAVI de México. **Nada de dibujos genéricos, juguetes, afiches ni comerciales.** Antes de buscar, escribe la tabla de homónimos de las marcas del guion. Antes de renderizar, corre `python src/revisar_fotos.py final/edl.json`, mira cada hoja y marca cada foto OK o CAMBIAR en `final/revision/REVISION.md`; se renderiza solo cuando todas digan OK.
- Voz con pausas naturales (solo se acortan los silencios de más de 0.8 s), sin música, solo los efectos sintetizados de `src/efectos.py`. Sin créditos.
- Antes de entregar, corre `python src/verificar.py video.mp4 edl.json`. **Solo se entrega si dice APROBADO.**
- **Una imagen distinta cada 6 s como mínimo en cada parada** (una por cada cosa que se narra), nunca la misma foto durante toda una parada.
- **Apertura numerada (número grande + nombre) en las 12 paradas**, sobre una foto de esa marca, y el **cierre** con carrusel y palabra final.
- **No aceleres la voz.** Usa el audio tal como sale de `src/voz.ps1`.
- Entrega siempre: el video, el **EDL (json)**, el **.srt** (`src/generar_srt.py`), la miniatura, los textos y la salida del verificador.
- Primero haz un **demo de 1 minuto** para que lo apruebe.

El tema nuevo es: **[TEMA]**. Te paso el guion (con secciones INTRO, PARADA N — Nombre y CIERRE) y el audio de la voz.

---

## Nota para agentes con su propio PC (Muse u otros)

La versión v4 hecha con un agente que sí podía bajar fotos y videos salió rechazada por dos motivos, y por eso estas reglas son obligatorias:
1. **Escribió su propio editor** en vez de usar el del repo. El resultado tenía otro diseño de tarjetas y le faltaban los números, las palabras gigantes, las polaroids y el zoom. **Hay que usar `src/render.py` + `src/estilo.py` tal cual**, sin escribir ni rediseñar plantillas. Solo cambia el EDL (json).
2. **Rellenó con la narración escrita en tarjetas** cuando no encontró fotos. Está prohibido. Si falta una imagen: se busca más (otras palabras, redes, foros), se usa una foto de la época o un clip de video real del ambiente.

Antes de dar el video por terminado, el agente corre `python src/verificar.py` sobre su video y su EDL, y repite hasta que diga APROBADO.

**Si el agente trabaja en Linux o Mac**, los `.ps1` no corren, pero los `.py` sí. Instalación: `pip install -r requirements.txt` más ffmpeg. Los mismos pasos que hace `mezclar.ps1` son:

```bash
python src/render.py final/edl.json final/_sin_audio.mp4 --workers 4
python src/efectos.py final/edl.json audio/efectos.wav
ffmpeg -y -i final/_sin_audio.mp4 -i audio/voz_final.wav -i audio/efectos.wav -filter_complex "[1:a]aresample=48000[v];[2:a]aresample=48000[e];[v][e]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k final/VIDEO_FINAL.mp4
python src/verificar.py final/VIDEO_FINAL.mp4 final/edl.json
```

Las tipografías están en `fuentes/`, así que no dependen de Windows.
