# Autenticidad de las fotos: OBLIGATORIO

La edición ya se puede copiar bien. Lo que tumbó la versión v7 (hecha con otro agente) fueron **las fotos**: varias eran de **otro país**, de **otra marca con el mismo nombre**, **dibujos genéricos** o **frames de comerciales**, y otras se **repetían**. El público de estos videos es colombiano y nota esos errores al instante. Cada foto tiene que pasar los 6 filtros de abajo, y `src/revisar_fotos.py` obliga a revisarlas una por una antes del render.

## Los 6 filtros (cada foto debe pasarlos todos)

### 1. País correcto
La foto es **del país del video** (aquí, Colombia) y **de la época** que narra la voz.

Errores reales del v7:

| La voz habla de… | Lo que se puso (MAL) | Lo correcto |
|---|---|---|
| Almacenes **Ley** (Colombia, 1922–2012) | supermercados **Casa Ley de México**: logo rojo moderno, folletos "Aniversario Ley" | fachadas viejas de Almacenes Ley en Colombia, el aviso "almacenes LEY", Don Julio |
| Almacenes **Tía** de Bogotá (cerró en 2017) | **Tía de Ecuador** moderno, con fachada roja y blanca | el Tía de la Décima en Bogotá, fotos en blanco y negro, la fachada azul con el letrero "Tía" |
| **Conavi** (banco colombiano, abejita) | logo naranja "CONAVI™" de la **Comisión Nacional de Vivienda de México** | el logo de Conavi con la abejita amarilla, la alcancía, la tarjeta |

Pistas para saber de qué país es una foto:
- **Pistas de que no es Colombia:** placas de carro, moneda ($ MXN, USD), palabras como "S.A. de C.V.", "Sucursal Mazatlán", "Guayaquil" o "Quito", cadenas que no existen en Colombia (Oxxo, Soriana, Casa Ley), banderas, uniformes de policía, el idioma del letrero.
- **Pistas de que sí es Colombia:** taxis amarillos, buses de Bogotá o Medellín, nombres de barrios, "Ltda." o "S.A.", Éxito, Carulla, Postobón, Bavaria, El Tiempo o El Colombiano.

### 2. Marca correcta (no un homónimo)
Muchas marcas comparten nombre con otras. **Siempre se busca con el país y el tipo de negocio**: "Almacenes Ley **Colombia**", "Conavi **banco** abejita", "cerveza Leona **Bavaria**".

| Marca del video | Homónimos que NO sirven |
|---|---|
| Almacenes Ley (Colombia) | Casa Ley / Supermercados Ley (México) |
| Almacenes Tía (Colombia) | Tía Ecuador, Tía Uruguay, Tía Argentina, Tía Perú (modernos) |
| Conavi (banco, Colombia) | CONAVI, la Comisión Nacional de Vivienda de México |
| Cerveza Leona (Bavaria) | Cerveza El León, León (México), otras cervezas con león |
| Telecom (Colombia) | Telecom Argentina, Telecom Italia, Telecom de otros países |
| Konga (gaseosa, Bavaria) | Konga (Nigeria), Kongas |
| Link (gaseosa, Bavaria) | otras "Link" modernas de otros países |

En un tema nuevo, **antes de buscar**, se escribe esta misma tabla de homónimos para las marcas del guion.

### 3. Nada de dibujos, clipart, juguetes ni IA
- **Prohibido:** dibujos genéricos (una abeja cualquiera en lugar de la abejita de Conavi), clipart, íconos, renders 3D, peluches o juguetes que no son de la marca, e imágenes generadas con IA.
- **Excepción:** un personaje o logo **oficial** de la marca, de la época, en una foto real (la alcancía real, el logo real de Conavi en una sucursal o en la tarjeta).

### 4. Nada de comerciales, afiches ni capturas con marca de agua
- **Prohibido:** frames de comerciales de TV (las hormiguitas de "Aló, Mamá", el comercial de la abejita, el señor del comercial del Chupi Plum), afiches publicitarios (la hormiguita de Telecom), capturas con logo de canal o de página ("ARCHIVOS", "Los ochenteros", @usuario), miniaturas de YouTube o TikTok y marcas de agua de bancos de imágenes.
- **Por qué:** YouTube los detecta como contenido con dueño, y además se ven sucios.
- Si una foto buena trae **una firma pequeña en una esquina**, se recorta con `src/limpiar.py`. Si la marca está en el centro, se descarta.

### 5. Que muestre lo que dice la voz en ese segundo
- Si la voz dice "el Chupi Plum", se ve **el Chupi Plum**, no un niño en un recreo cualquiera.
- Si dice "las escaleras eléctricas de Caravana", se ven esas escaleras.
- **Prohibido el relleno sin relación**, como una mano con un tenis en la parada de La 14 o un supermercado de otra marca.
- Cuando de verdad no exista una foto de algo, se usa **una foto de la época y del lugar** o **un clip de video real del ambiente**, y se le avisa a Luis en la entrega.

### 6. Sin repetir
- **La misma foto no aparece dos veces**, aunque sea con otro nombre de archivo, otro recorte o en blanco y negro.
- Solo se permite repetir en el **carrusel del cierre**, que es un repaso.
- `src/verificar.py` detecta las repetidas **comparando las imágenes** (dHash), no los nombres de archivo.

## Cómo se busca para que salgan fotos auténticas

- **Fórmula:** `marca + tipo de negocio + país o ciudad + época`. Por ejemplo: "Almacenes Ley Medellín foto antigua", "Tía Bogotá carrera décima años 70", "Conavi banco abejita alcancía".
- **Fuentes que suelen servir:** grupos de nostalgia de Facebook ("Bogotá tiempo atrás", "Medellín, historias y fotografías del pasado"), El Tiempo, El Colombiano, Wikimedia Commons, foros y Mercado Libre Colombia (para empaques y productos viejos).
- Si en los resultados **dominan las fotos de otro país**, se cambia la búsqueda: se agrega la ciudad, "antiguo", la década o el nombre completo.

## Revisión obligatoria antes del render: `src/revisar_fotos.py`

```
python src/revisar_fotos.py final/edl_NUEVO.json
```

El script hace tres cosas:
1. **Hojas de contacto por parada** en `final/revision/`. Cada foto sale con su número, su segundo y la frase que se oye en ese momento.
2. **Avisos automáticos:**
   - **fotos repetidas** (iguales o casi iguales);
   - **fotos de baja resolución**;
   - **fuentes sospechosas de otro país**, según el título o la página de origen guardados en `fuentes.tsv` (México, Ecuador, Perú, Mazatlán, Guayaquil, .mx, .ec, .pe…).
3. **Una planilla** `final/revision/REVISION.md`. Por cada foto se marca **OK** o **CAMBIAR** y se revisan los 6 filtros.

**No se renderiza hasta que todas las fotos digan OK.** El verificador falla si la planilla tiene fotos sin revisar o marcadas **CAMBIAR**.
