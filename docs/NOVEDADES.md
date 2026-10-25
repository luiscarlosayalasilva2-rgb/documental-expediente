# Novedades del método (leer SIEMPRE antes de trabajar)

Este repo se actualiza cada vez que revisamos un video. **Antes de empezar o de corregir un video:**

```
git pull
```

Después lee esta página de arriba hacia abajo **hasta la última versión que ya aplicaste**. Cada entrada dice **qué cambió** y **qué hay que corregir** en un video que esté en curso. Por último, vuelve a correr `src/revisar_fotos.py` y `src/verificar.py`: las reglas nuevas también se aplican a los videos que ya estaban hechos.

---

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
