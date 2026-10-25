# Prompt para pegar en otro chat (Claude, Muse u otra IA)

Copia esto tal cual al empezar un chat nuevo y cambia lo que está entre [corchetes]:

---

Vas a editar un video documental largo, horizontal 16:9, **exactamente con la misma edición** que el video aprobado de este repositorio: https://github.com/luiscarlosayalasilva2-rgb/documental-expediente

Antes de hacer nada, lee completos y en este orden:
1. `docs/REGLAS_DURAS.md`: reglas obligatorias, metas medibles y fotos de cómo debe verse cada recurso.
2. `README.md`: la receta paso a paso y las reglas de edición.
3. `docs/IMAGENES_Y_SINCRONIA.md`: cómo elegir cada imagen según lo que se narra y pegarla al segundo del audio.
4. `docs/PROCESO_COMPLETO.md`: los errores que ya se cometieron y cómo se resolvieron.

Reglas que no se negocian:
- Usa el motor del repo (`src/render.py` y `src/estilo.py`) sin modificar el diseño. No escribas tu propio editor: solo armas el EDL (json) y lo renderizas con `src/mezclar.ps1`.
- La pantalla casi siempre muestra una **foto o un video real de lo que la voz dice en ese segundo**, con zoom lento. **Nunca** se pone la narración escrita en tarjetas. Los textos (número rojo, palabra gigante, ficha, nota corta) son acentos encima de la imagen.
- Cortes cada 3 o 4 s en promedio, ningún plano de más de 11 s, unos 35 clips de video en 14 min, cero fotos repetidas.
- Cada ítem de la lista abre con su **número rojo grande y el nombre** debajo, y luego la ficha "PARADA N".
- Fotos auténticas (Google, redes, foros, Pixabay o Commons). Nada de imágenes de IA, frames de comerciales de TV ni marcas de agua.
- Voz sin silencios, sin música, solo los efectos sintetizados de `src/efectos.py`. Sin créditos.
- Antes de entregar, corre `python src/verificar.py video.mp4 edl.json`. **Solo se entrega si dice APROBADO.**
- Primero haz un **demo de 1 minuto** para que lo apruebe.

El tema nuevo es: **[TEMA]**. Te paso el guion (con secciones INTRO, PARADA N — Nombre y CIERRE) y el audio de la voz.

---

## Nota para agentes con su propio PC (Muse u otros)

La versión v4 hecha con un agente que sí podía bajar fotos y videos salió rechazada por dos motivos, y por eso estas reglas son obligatorias:
1. **Escribió su propio editor** en vez de usar el del repo. El resultado tenía otro diseño de tarjetas y le faltaban los números, las palabras gigantes, las polaroids y el zoom. **Hay que usar `src/render.py` + `src/estilo.py` tal cual**, sin escribir ni rediseñar plantillas. Solo cambia el EDL (json).
2. **Rellenó con la narración escrita en tarjetas** cuando no encontró fotos. Está prohibido. Si falta una imagen: se busca más (otras palabras, redes, foros), se usa una foto de la época o un clip de video real del ambiente.

Antes de dar el video por terminado, el agente corre `python src/verificar.py` sobre su video y su EDL, y repite hasta que diga APROBADO.
