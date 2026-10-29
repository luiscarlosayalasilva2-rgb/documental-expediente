# Novedades del método (leer SIEMPRE antes de trabajar)

Este repo se actualiza cada vez que revisamos un video. **Antes de empezar o de corregir un video:**

```
git pull
```

Después lee esta página de arriba hacia abajo **hasta la última versión que ya aplicaste**. Cada entrada dice **qué cambió** y **qué hay que corregir** en un video que esté en curso. Por último, vuelve a correr `src/revisar_fotos.py` y `src/verificar.py`: las reglas nuevas también se aplican a los videos que ya estaban hechos.

---

## 2026-10-28 · Video de comerciales sin frames de comerciales

**Qué cambió**
- **Ejemplo nuevo de tema:** `src/edl_comerciales.py`, `src/miniatura_comerciales.py`, `docs/ejemplos/guion_comerciales10.txt` y `docs/ejemplos/comerciales10/clips.json` (10 comerciales colombianos, 11:20).
- **Aunque el tema sean comerciales, NO se usan frames de comerciales.** El guion traía marcas `[CLIP: comercial de…]` y Luis eligió "Sin comerciales" por Content ID: se muestran los empaques, productos y personas reales (la tarjeta y la libreta de Conavi, el Renault 4, René Higuita) y clips de ambiente. En Google salen frames de Frutiño con Higuita y del granito de Águila Roja: no sirven.
- **`edl_comerciales.py` rellena el esqueleto de `nuevo_video.py` con listas:** fotos por sección en orden de narración, clips por sección (`datos/clips.json`), papeles y carrusel. Si a una sección le faltan fotos, alarga el plano anterior, pero **nunca una escena de papel** (eso dejó un papel de 23 s en la primera pasada) y avisa.
- **`nuevo_video.py` solo pone notas a máquina en lemas entre «comillas angulares».** Si el guion usa comillas rectas, las 5 notas se agregan a mano (ver el script).
- **Revisar el audio contra el guion:** la voz se saltó una frase del Renault 4; se quitó del `guion.txt` antes de alinear.
- Fuentes de Argentina, Perú o México en fotos "genéricas" de televisores o salas también se descartan (salen con letreros como "Archivo TV Cine Piura Perú").

**Qué corregir si tienes un video en curso**
- Nada obligatorio. Si tu tema es de publicidad, aplica la regla de no usar frames de comerciales.

## 2026-10-27 · Voz con pausas naturales, letrero inicial y video de Navidad

**Qué cambió**
- **Voz:** Luis pidió "no hagas tantos cortes en el audio donde hay espacios vacíos" y que el video no baje de la duración pedida por cortar silencios. `src/voz.ps1` ahora usa `src/pausas.py`: **solo los silencios de más de 0.8 s quedan en 0.5 s**; las pausas normales entre frases no se tocan (en el video de Navidad: 12:45 → 12:16). Antes se quitaba toda pausa de más de 0.15 s.
- **Verificador:** la meta de pausas pasa a "ninguna > 0.9 s" y la de velocidad a **2.9–3.8 palabras/s** (con pausas naturales sale ~3.1; el techo sigue detectando voz acelerada).
- **Letrero en los primeros 5 s:** Luis lo pidió para que el espectador sepa de qué va el video. Es una ficha a máquina en el segundo 0.6 que dura 4.6 s, con `"titulo": true` para que el verificador no la cuente como parada: `{"tipo":"file","t":0.6,"dur":4.6,"texto":"Así era la Navidad en Colombia","etiqueta":"Expediente diciembre","titulo":true}`.
- **Sección LLAMADO:** `src/alinear.py` acepta el título `LLAMADO` (el "suscríbete" a mitad del video) como sección propia, para que no se mezcle con la parada anterior.
- **Efectos especiales desde el EDL:** `src/efectos.py` lee `"especiales": [{"t": seg, "sonido": "plum|timbre|vhs|moneda"}]`; sin esa clave usa los del video de referencia.
- **Ejemplo nuevo de tema:** `src/edl_navidad.py`, `src/miniatura_navidad.py` y `docs/ejemplos/guion_navidad12.txt` (12 costumbres navideñas, 12:25, APROBADO).
- **Luis ya no quiere demos:** se entrega directamente el video completo, verificado.
- **Revisar que el audio esté completo** antes de armar el EDL: transcribir los últimos 20 s del original. En el video de Navidad el audio venía cortado y faltaba el cierre.

**Qué corregir si tienes un video en curso**
1. Vuelve a generar la voz con el `src/voz.ps1` nuevo, y después rehaz la transcripción, la alineación y el EDL (los tiempos cambian).
2. Agrega el letrero de los primeros 5 s.

## 2026-10-25 · Prompts de investigación para Gemini
- [PROMPTS_INVESTIGACION_GEMINI.md](PROMPTS_INVESTIGACION_GEMINI.md): 6 prompts en orden (elegir ítems, fichas con datos verificables, anécdotas reales, dónde están las fotos auténticas y homónimos, guion con el formato del método y verificación). El guion sale listo para `nuevo_video.py`.

## 2026-10-25 · Fotos repetidas por imagen, fallo de Real-ESRGAN y video aprobado v4

**Qué cambió**
- `src/revisar_fotos.py` y `src/verificar.py` detectan las **fotos repetidas comparando la imagen** (doble dHash), aunque tengan otro nombre, estén en blanco y negro o coloreadas. **El propio video aprobado tenía 9 pares repetidos**; se corrigieron en `final/edl_v4.json`, que es el nuevo EDL de referencia.
- **Fallo corregido en `src/mejorar_fotos.py`:** cuando Real-ESRGAN fallaba con una foto, se guardaba la imagen de la **foto anterior**. En el video aprobado, el "Chupi Plum original" mostraba en realidad una foto de un recreo. Ahora cada foto usa su propio archivo temporal y se comprueba que la salida se parezca a la original.
- `src/limpiar.py`: recortes nuevos para quitar créditos ("FOTO: …"), títulos de publicaciones y marcas de tiendas.

**Qué corregir si tienes un video en curso**
1. Compara cada foto de `media/hd_esrgan/` con su original. Si alguna no coincide, bórrala y vuelve a correr `mejorar_fotos.py`. Para encontrarlas: `python src/revisar_fotos.py edl.json` y mira las hojas.
2. Corre `python src/revisar_fotos.py final/edl.json` y cambia **todas** las repetidas que marque.
3. Llena la planilla `final/revision/REVISION.md` (todas en OK) y vuelve a correr `src/verificar.py`.

## 2026-10-25 · Autenticidad de las fotos (por el v7)
- Guía nueva: [AUTENTICIDAD_FOTOS.md](AUTENTICIDAD_FOTOS.md). Sus 6 filtros: país, marca correcta (sin homónimos como Casa Ley de México, Tía de Ecuador o CONAVI de México), nada de dibujos ni juguetes, nada de comerciales ni afiches, que corresponda a la voz y sin repetir.
- `src/revisar_fotos.py` es obligatorio: hojas por parada, avisos y planilla OK/CAMBIAR. El verificador no aprueba sin la planilla completa.
- **Qué corregir en el v7:** cambiar las fotos de Ley (México), Tía (Ecuador moderno), CONAVI (México), la abeja dibujada, el juguete de pato, los frames del comercial del Chupi Plum, la hormiguita de Telecom, el tenis y el supermercado Cañaveral de La 14 y la cerveza El León. Además, quitar las repetidas y **entregar el EDL**.

## 2026-10-24 · Plantilla automática `src/nuevo_video.py`
- El EDL de un tema nuevo se arma con `nuevo_video.py plan` y se comprueba con `nuevo_video.py validar`. Ya no se arma desde cero.

## 2026-10-24 · Catálogo de detalles y verificador ampliado (por el v6)
- [CATALOGO_DETALLES.md](CATALOGO_DETALLES.md): los 12 detalles de la edición con su animación y frecuencia.
- Además se volvió obligatorio:
  - una imagen distinta cada 6 s en cada parada;
  - la apertura numerada en todas las paradas;
  - el cierre con carrusel;
  - no acelerar la voz;
  - entregar el EDL;
  - entregar el `.srt` (con `src/generar_srt.py`).

## 2026-10-24 · Reglas duras y verificador (por el v4)
- [REGLAS_DURAS.md](REGLAS_DURAS.md) y `src/verificar.py`. Quedó prohibido poner la narración escrita en tarjetas y escribir un editor propio.
