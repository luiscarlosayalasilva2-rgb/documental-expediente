# Prompts de investigación para Gemini (Deep Research)

Sirven para preparar un video nuevo **antes** del guion y de la edición. Se usan en orden, en **Gemini con Deep Research activado**, y cada resultado se guarda como documento. Cambia lo que está entre [corchetes].

El resultado de los prompts 1 a 4 alimenta el **guion** (prompt 5). El guion sale con el formato que necesita `src/nuevo_video.py` (`INTRO`, `PARADA N — Nombre`, `CIERRE`). El prompt 4 da las búsquedas de fotos auténticas que pide `docs/AUTENTICIDAD_FOTOS.md`.

---

## Prompt 1 · Elegir los ítems del video

```
Actúa como investigador de cultura popular de [PAÍS]. Quiero hacer un video documental de nostalgia de unos 14 minutos sobre: [TEMA, ej. "marcas colombianas que había en todas las casas y desaparecieron"].

Investiga y dame una lista de 20 candidatos. Para cada uno:
1. Nombre exacto y tipo de negocio o producto.
2. Años en que existió (fundación y desaparición o cambio) y en qué ciudades o regiones fue fuerte.
3. Por qué la gente lo recuerda con cariño: qué momento de la vida o de la familia evoca.
4. Qué tan conocido fue a nivel nacional (alto, medio o regional).
5. Si hay fotos reales disponibles en internet: fachadas, empaques, publicidad impresa de la época o fotos de archivo (sí, pocas o no).
6. Si existe otra marca con el mismo nombre en otro país que pueda confundir (por ejemplo, Almacenes Ley de Colombia y Casa Ley de México).

Después recomiéndame los [N, ej. 12] mejores para el video, ordenados de menor a mayor carga emocional: el último debe ser el más emotivo. Explica en una línea por qué cada uno.
Cita las fuentes de cada dato.
```

## Prompt 2 · Ficha completa de cada ítem (datos verificables)

```
Para cada uno de estos ítems: [LISTA DE LOS N ELEGIDOS], en [PAÍS], haz una ficha con datos VERIFICABLES y cita la fuente de cada dato:

- Nombre oficial completo y nombre popular. Si es sigla, qué significa.
- Fundación: año, ciudad y fundador.
- Época de oro: años y qué la hacía especial.
- Cifras concretas, en números: años que duró, cantidad de tiendas, precios recordados, ventas, sabores, etc.
- Lemas o eslóganes publicitarios exactos, entre comillas.
- Personajes, mascotas o campañas famosas (solo descríbelos, no necesito imágenes).
- Cómo y cuándo desapareció o cambió: quiebra, venta, fusión o liquidación, con fecha exacta y el nombre de quién la compró.
- Datos que la gente suele recordar mal o que conviene corregir (por ejemplo, "Telecom no quebró, la liquidaron").
- Si hoy existe otra marca con el mismo nombre en otro país: cuál es, y cómo distinguir sus fotos de las de la marca de [PAÍS].

Marca con [DUDOSO] cualquier dato que no confirmen al menos dos fuentes.
```

## Prompt 3 · Anécdotas reales de la gente

```
Busca recuerdos y anécdotas REALES de personas de [PAÍS] sobre: [LISTA DE ÍTEMS]. Búscalos en grupos de nostalgia de Facebook, comentarios de YouTube, foros, Reddit, X/Twitter, notas de prensa con testimonios y crónicas de El Tiempo, El Colombiano, El Espectador, Semana o el medio local que corresponda.

Para cada ítem dame de 4 a 6 anécdotas concretas, de este tipo:
- escenas de familia (quién iba, qué se compraba, qué día de la semana);
- detalles sensoriales (olores, sonidos, frases que se decían);
- historias de vida (alguien que trabajó ahí, que se enamoró ahí, que construyó su casa gracias a esa marca);
- rituales o reglas no escritas;
- cómo vivieron el cierre (qué hizo la gente, qué sintieron).

Para cada anécdota: un resumen en 2 o 3 líneas, de dónde salió (enlace o nombre del grupo o medio) y si es un testimonio de una persona o algo que repite mucha gente. NO inventes anécdotas: si no encuentras suficientes, dilo.
```

## Prompt 4 · Dónde están las fotos auténticas

```
Para el video necesito fotos REALES y de [PAÍS] de cada ítem: [LISTA DE ÍTEMS]. Para cada uno dime:

1. Qué fotos reales suelen existir: fachadas en distintas épocas, empaques, productos, publicidad impresa, fotos de archivo en blanco y negro, fotos del cierre.
2. En qué páginas o grupos se encuentran: grupos de Facebook de nostalgia de cada ciudad, archivos de periódicos, Wikimedia Commons, bibliotecas o archivos públicos, Mercado Libre (empaques viejos), foros.
3. Las 5 mejores búsquedas para Google Imágenes, con marca + tipo de negocio + ciudad + época (por ejemplo, "Almacenes Tía Bogotá carrera décima años 70").
4. Los HOMÓNIMOS que hay que evitar: marcas con el mismo nombre en otros países y cómo reconocer sus fotos (logo, colores, país, época).
5. Qué NO usar para ese ítem: comerciales de TV, afiches o personajes con derechos muy cuidados.

Responde como una tabla por ítem.
```

## Prompt 5 · El guion (con el formato del método)

```
Con la investigación anterior (fichas, anécdotas y datos verificados), escribe el guion de un video documental de nostalgia de unos 14 minutos (2.800 a 3.000 palabras) sobre [TEMA].

FORMATO OBLIGATORIO (lo lee un programa, no lo cambies):
- Título en la primera línea.
- Secciones con estos encabezados exactos, cada uno en su propia línea:
  INTRO
  PARADA [N] — [Nombre del ítem]   (de la [N] a la 1; la 1 es la más emotiva)
  CIERRE
- Los encabezados NO se leen en voz alta: el texto de cada sección empieza en la línea siguiente.

ESTILO:
- Narrador cercano, como un amigo que cuenta historias. Trata de "usted" y usa expresiones naturales de [PAÍS], sin caricaturizar.
- La INTRO dura unos 25 s: tres o cuatro objetos cotidianos ("en la nevera, en la mesa de noche…"), el número de paradas y un gancho hacia la última.
- Cada PARADA dura de 50 a 80 s (unas 180 a 280 palabras) y sigue esta estructura: una escena que pone al espectador en el momento ("Es viernes…"), qué era la marca, 1 o 2 anécdotas reales, el dato del final (cómo y cuándo se fue) y una frase final corta y emotiva.
- Escribe los años, precios y cantidades CON NÚMEROS (1975, 27 años, 365 pesos): el programa los convierte en números rojos en pantalla.
- Pon los lemas y frases célebres entre comillas angulares: «Siempre te da más».
- Cuando algo se cierre, quiebre o desaparezca, dilo con palabras claras ("cerró", "se liquidó", "desapareció"): esas frases salen en blanco y negro.
- Frases cortas, fáciles de decir en voz alta, con puntos y comas donde haya pausa natural. Enumeraciones de 3 o 4 cosas separadas por comas.
- Corrige con respeto los mitos ("Antes de que me lo corrijan: …").
- Hacia la mitad, una línea entre corchetes para la invitación a suscribirse: [Si este viaje le está gustando…].
- El CIERRE repite el número total, invita a comentar qué marca vivió en su casa y anuncia la próxima ruta. Termina con una frase de despedida fija, por ejemplo "Nos vemos en el pasado."

PROHIBIDO: inventar datos o anécdotas, usar datos marcados [DUDOSO] sin decir "cuentan que…", hacer preguntas retóricas en exceso y nombrar a personas privadas con nombre y apellido.

Al final, aparte del guion, dame una lista con cada cifra y cada fecha que usaste y su fuente, para verificarlas.
```

## Prompt 6 · Verificar el guion terminado

```
Verifica este guion línea por línea contra fuentes confiables. [PEGA EL GUION]

Para cada afirmación con dato (fecha, año, cifra, nombre, lema, quién compró a quién):
- ✔ si está confirmada, con la fuente;
- ✘ si está equivocada, con el dato correcto y la fuente;
- ? si no se puede confirmar, y cómo reformularla ("cuentan que…").
Revisa también que ninguna marca se confunda con un homónimo de otro país.
Al final dame el guion corregido con el MISMO formato (INTRO / PARADA N — Nombre / CIERRE).
```

---

## Después de Gemini

1. El guion corregido se guarda como `guion.txt` y se graba la voz.
2. Sigue la receta del `README.md`: `voz.ps1` → `transcribir.py` → `alinear.py` → `nuevo_video.py plan` → fotos (con la tabla de homónimos del prompt 4) → `revisar_fotos.py` → render → `verificar.py`.
