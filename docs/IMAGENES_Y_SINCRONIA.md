# Imágenes que correspondan al tema y que encajen con el audio

Es la regla más importante del método. Luis la pidió así: **"el material debe ser auténtico y coincidir con lo que se narra"**. Cada imagen tiene que mostrar **lo que la voz dice en ese segundo**, y entrar y salir exactamente cuando la voz empieza y termina esa idea.

## 1. Qué imagen va en cada frase

Por cada frase de `audio/frases.json`:

1. **Subraya los sustantivos concretos:** objetos, lugares, personas, marcas, años. Por ejemplo, en "Es viernes. Y si usted creció en **Bogotá**, el viernes tenía un plan sagrado: ir al **videoclub**" los sustantivos son *Bogotá* y *videoclub*.
2. **Elige la búsqueda según la prioridad**, de la más auténtica a la más genérica:
   1. **La marca exacta con el objeto o el lugar:** "Betatonio videoclub Bogotá", "gaseosa Konga Bavaria botella", "Almacenes Tía cierre Bogotá 2017".
   2. **La misma época y el mismo país:** "tienda de barrio Bogotá años 80 foto antigua", "colegio Bogotá años 90 uniforme".
   3. **La acción o el ambiente**, en fotos o video de Pixabay: "ice cream vendor", "horses running", "escalator", "empty shopping mall".
3. **Haz una búsqueda por cada cosa concreta**, no una por parada. En este video fueron unas 120 búsquedas para 12 paradas.

### Ejemplos reales de este video

| Lo que dice la voz | Qué se puso |
|---|---|
| "en la nevera, en la mesa de noche, en la billetera del papá, en la tienda de la esquina" | 4 cortes de 1.1–1.3 s: nevera vieja, lámpara de mesa de noche, billetera, tienda de barrio |
| "trae las monedas contadas tres veces" | moneda colombiana de 20 pesos de 1982 |
| "el helado que viene dentro de un balón de plástico" | los balones reales de La Campiña |
| "cuando llegaba el Mundial" | álbum Panini de Italia 90 y la Selección Colombia de 1990 |
| "un comercial con una manada de caballos corriendo" | clip de video de caballos corriendo |
| "en Cali queda una escultura de caballos" | foto de la escultura de caballos |
| "Esta casa es nuestra" | manos con llaves de casa |
| "se hacía fila frente a las cabinas" | foto de archivo de cabinas de Telecom con gente |
| "las primeras escaleras eléctricas de Medellín" | foto de archivo de las escaleras de Caravana en blanco y negro |
| "Y ahora sí, déjeme llevarlo a mi tierra. A Cali." | video aéreo de Cali |
| "vendiéndole cilantro a La 14" | plaza de mercado de Cali |
| "vieron los pasillos vacíos, con las luces titilando" | video de un pasillo de centro comercial vacío |
| "Niñas de catorce años… las sabatinas" | foto sepia de niñas en el Tía comprando útiles |
| "llegaba Don Julio con las ofertas" | Don Julio de sombrero de copa frente a un almacén Ley |
| "se fue volviendo Éxito" | fachada de un almacén Éxito |
| "Bancolombia revivió a la abejita en una tarjeta" | la tarjeta nueva de Bancolombia con la abejita |

## 2. Qué foto se rechaza (revisando con los ojos)

En las hojas de contacto (`src/hoja.py`) **se mira cada foto** y se descarta si:

- es de **otro país** o de **otra marca**, aunque el nombre se parezca (en la búsqueda de Konga salió Twist; en la de Tía salió Tía de Ecuador o Perú);
- es una **miniatura de YouTube o TikTok**, con texto tipo "QUÉ PASÓ CON…", flechas, caras de youtuber o un botón de play;
- trae **marca de agua** de un banco de imágenes (Shutterstock, Alamy, Dreamstime, Getty), el **logo de un periódico** o un **pie de nota** ("Emotiva carta de…");
- es **moderna** cuando la frase habla del pasado, o al revés;
- está hecha con **IA** o es un dibujo, cuando lo que se narra es real;
- mide **menos de 900–1000 px** de ancho y no hay una versión mejor. En ese caso se busca la misma foto en HD o se mejora con Real-ESRGAN.

Si una foto buena trae una firma o un marco pequeño, se **recorta** con `src/limpiar.py` en vez de descartarla.

## 3. Sincronía con el audio

- Los tiempos salen de **`audio/palabras.json`**, que tiene el segundo en que empieza cada palabra, y de **`audio/frases.json`**, que tiene el inicio y el fin de cada frase.
  - Para ver las palabras de un tramo: `python src/palabras_en.py <desde> <hasta>`.
  - Dentro del EDL se usa `w('palabra', desde, defecto)`, que da el segundo exacto en que se dice una palabra.
- **Cada plano empieza cuando la voz empieza la idea** y termina cuando empieza la siguiente. En `edl_completo.py` esto lo hace `tramos([(inicio, [fuentes])…])`.
- **Las enumeraciones van en cortes rápidos**, uno por cosa nombrada, cortando en el segundo de cada palabra.
- **Los números rojos entran en el segundo en que se dice la cifra**: `numero(w('1975', …), '1975', 'compraron la casa')`.
- **La palabra gigante entra con la frase emocional** y dura lo que dura esa frase.
- **Los lemas entre comillas** («Siempre te da más») van como nota a máquina mientras se dicen.
- **Lo triste o perdido va en blanco y negro** justo cuando la voz lo dice: "cerró", "quebró", "quedó vacía", "se apagó".
- **Cada parada empieza exactamente en su primera palabra**, con el número grande, el nombre y luego la ficha "PARADA N".

## 4. Comprobación antes de entregar

1. **Demo corto:** se renderiza la intro y la primera sección y Luis lo aprueba antes del video completo.
2. **Hoja de contacto del video final**, un fotograma cada 8 s: se revisa que cada imagen corresponda a su parada y que no haya fotos repetidas. `edl_v3.py` las cuenta solo.
3. **Revisión de frases sueltas:** se eligen algunas al azar, se mira el fotograma en su segundo y se comprueba que muestre lo que dice esa frase.
4. Si algo **no se pudo conseguir**, se le dice a Luis en la entrega. Por ejemplo: "no encontré foto del juego de rana con la leona; usé el juego de rana genérico".
