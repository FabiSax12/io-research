# DESIGN.md: tema "BlackRock Outlook" (homenaje no oficial)

Este documento fija el diseño de la presentación. El código lo aplica en `tema.py` (constantes y primitivas),
`graficos.py` (gráficos) y `construir.py` (tipos de lámina). Si cambia algo del diseño, cambiarlo aquí y en `tema.py`.

## Especificación (textual, tal como la dio el equipo)

> Create a presentation in the 'BlackRock Outlook' theme, an unofficial homage to an investment institute's annual
> global outlook. Background: white (#ffffff) on content slides, black (#000000) on the cover. Typography: 'Onest'
> (Google Fonts) 800 for headlines at 42 to 48px with 1.0 leading, 800 at 15px for chart titles, 400 at 11.5 to 13px
> for body in pure black; source notes and disclaimers in 'Barlow Condensed' 400 at 10px. Signature: each content
> slide has a color-coded section tab flush with the top edge, 196 by 24px, bold 12px sentence-case label: yellow
> #ffce00 with black text for Investment environment, vermilion #ff4713 with white text for Themes, green #008b5c with
> white text for Mega forces, pink #fc9bb3 with black text for Views, black for Summary. Split pages: headline and two
> body columns left, a 4px black vertical rule, exhibit right. Exhibit stack: bold chart title, a plain subtitle with
> units and dates, the chart, a 'Chart takeaway:' line with the label bold, a Barlow Condensed source note opening with
> 'Forward-looking estimates may not come to pass.' in bold, then an Investment implications box: 9px top bar in the
> section color over a tint (#fff3f0, #e8fff7, #fffbef), bold 14px heading, two bullets. Charts: vermilion #ff4713 for
> the lead series, then #ffce00, #008b5c, #fc9bb3; #d6d5dd gridlines, black baseline, hatched bars for estimates,
> dashed scenario lines over a #ededf1 forecast window. Cover: a #ffce00 block on a black field with the year and
> 'Global Outlook' at 64px 800, a 22px bold subtitle, the institute name stacked with the middle word bold, and a
> #e3e3ea embargo strip in #ff4713 bold capitals. Contents: a yellow panel, bold sections with page ranges. Scenarios:
> probabilities at 28px 800 beside one-line cases, 1.5px black rules. Mega forces: stacked horizontal bars (public vs.
> private capital) with direct totals, and a bold pull quote with a yellow portrait tile. Tactical views table: black
> header row (asset class, View, Commentary), 1.5px black row rules, and a seven-cell conviction meter per asset:
> #d6d5dd cells with a taller center cell, the active cell pink for underweight, #595959 for neutral, yellow for
> overweight, a 10px bold label beneath ('+1', 'Neutral', '-1'), a black dot on the previous view, and a legend box
> above. Footer: a capitals 'Capital at risk' disclaimer bottom-left in 10px #8a8a8a Barlow Condensed, page number
> bottom-right. Strictly avoid: the BlackRock logo, wordmark or name on slides, claiming affiliation with BlackRock,
> Inc., gradients, drop shadows, rounded corners, photos, icons, centered body text, pie or 3D charts, gray body copy,
> colors outside the palette, content slides without a section tab, charts without a takeaway line and source note.

## Unidades

Lámina 16:9 de 960 × 540 px (10 × 5.625 in). 1 px = 9525 EMU; un tamaño en px pasa a pt multiplicando por 0.75.
Los gráficos se dibujan con `figsize = (ancho_px / 96, alto_px / 96)` para que el tamaño de letra coincida con el de la lámina.
El interlineado "1.0" es exacto (igual al tamaño de la letra), no el "sencillo" de PowerPoint.

## Adaptación al trabajo de Investigación de Operaciones

El diseño es fijo; lo que cambia es el contenido. Estas son las únicas traducciones:

| Elemento del diseño | En esta presentación |
|---|---|
| Pestaña amarilla *Investment environment* | **Contexto** (contenido, introducción) |
| Pestaña rosada *Views* | **Herramientas** (librerías de Python y R) |
| Pestaña bermellón *Themes* | **Parte I** (PL, PLE, transporte, asignación) |
| Pestaña verde *Mega forces* | **Parte II** (transbordo) |
| Pestaña negra *Summary* | **Resumen** (conclusiones, minutas, referencias) |
| Portada: año + *Global Outlook* | "2026 / Trabajo de investigación" a 64 px 800 |
| Nombre del instituto apilado | Instituto / **Tecnológico** / de Costa Rica (solo texto, sin logo) |
| Franja de embargo | **Se quitó** a pedido del equipo (la portada no lleva fecha de defensa) |
| *Chart takeaway:* | **Lectura del gráfico:** |
| *Forward-looking estimates may not come to pass.* | **Se quitó**: la nota de fuente muestra solo la fuente |
| *Investment implications* | **Implicaciones para el modelo** |
| *Capital at risk* (pie) | **Se quitó**: el pie muestra solo el número de lámina |
| Escenarios: probabilidades a 28 px | Costo óptimo del transbordo en tres casos (balanceado, sobra, falta oferta) |
| Mega forces: capital público vs. privado | Demanda que llega por un nodo de transbordo vs. directa, por destino |
| Cita con retrato amarillo | Definición de transbordo (Taha) con mosaico amarillo e iniciales; sin foto |
| Tabla táctica (asset class, View, Commentary) | Librería, Lenguaje, Valoración (medidor de −3 a +3), Comentario |
| Barras rayadas = estimaciones | Relajación lineal del PLE (cota) y resultados de R/Solver aún pendientes |
| Líneas discontinuas sobre ventana #ededf1 | Recta de nivel de Z (PL) y curva de costo en los casos desbalanceados |

Todos los textos fijos están en `tema.py` (`ETIQUETA_LECTURA`, `TITULO_IMPLICACIONES`)
por si se quiere volver a la redacción original en inglés.

## Decisiones que la especificación no cubre

- **Código fuente**: ver "Ventanas de código" más abajo.
- **Capturas** (`capturas/*.png`): `comun/utilidades.py` y `comun/utilidades.R` dibujan las tablas con encabezado negro,
  texto blanco y reglas horizontales negras; el diagrama de red de `parte2/python/transbordo.py` usa la paleta.
- **Matrices** (transbordo): se dibujan como tabla nativa desde el CSV para que se lean; las celdas con costo real van en bermellón.
- **Índice**: solo secciones con rango de láminas y el equipo; sin resumen del enunciado (pedido del equipo).
- **Código**: una lámina por lenguaje (primero Python, después R) para que la ventana use todo el ancho; la letra se
  ajusta sola entre 10 y 13.5 px para que entre el fragmento completo.
- **Resultados de la Parte I y del transbordo**: dos columnas; a la izquierda la tabla de Python sobre la de R, a la
  derecha la salida de consola. Las capturas se recortan (sin margen blanco) antes de insertarlas.
- **Tabla de librerías**: columnas Librería, Lenguaje, Qué resuelve, Rol en el trabajo, Recomendación (medidor de
  −3 a +3) y Comentario; la leyenda de arriba explica el medidor con un ejemplo.
- **Marcadores** de contenido pendiente: recuadro #ededf1 con "Pendiente" en negrita. Desaparecen solos cuando existe la captura.

## Ventanas de código (estilo carbon.now.sh)

Pedido del equipo: todo fragmento de código se muestra como una ventana de editor, al estilo de carbon.now.sh, con
los tres botones de la ventana de macOS. Lo dibuja `ventana_codigo.py` como PNG (4× el tamaño en la lámina).

| Elemento | Valor |
|---|---|
| Fuente | JetBrains Mono 400 (cursiva en comentarios), 10 px en código y 8.5 px en la terminal; sin ligaduras |
| Fondo de la ventana y barra | #000000 |
| Botones (cerrar, minimizar, maximizar) | #ff4713, #ffce00, #008b5c: la versión de la paleta del rojo, amarillo y verde de macOS |
| Título en la barra | Lenguaje · ruta del script, JetBrains Mono 9 px #8a8a8a |
| Palabras clave (`for`, `if`, `function`, `True`) | #ff4713 |
| Funciones y llamadas (`lpSum(`, `lp(`) | #ffce00 |
| Cadenas | #fc9bb3 |
| Números | #008b5c |
| Comentarios | #8a8a8a cursiva |
| Operadores y puntuación | #d6d5dd |
| Resto del texto | #ffffff |

Se usa en las láminas de código (Python a la izquierda, R a la derecha), en la salida de consola (ventana "Terminal")
y en el ejemplo PuLP frente a lpSolve. Las líneas largas se cortan con sangría francesa; si el fragmento no cabe, la
última línea dice `# ... (continúa en el script)`.

Diferencias con Carbon, a propósito: **sin esquinas redondeadas y sin sombra**, porque la especificación del tema
los prohíbe. Los botones sí son círculos (son el detalle que identifica la ventana).

## Fuentes

`fuentes/` trae los TTF estáticos de Google Fonts (licencia SIL OFL 1.1, ver `OFL-*.txt`): Onest 400/700/800,
Barlow Condensed 400/700 y JetBrains Mono 400/700/cursiva. JetBrains Mono solo se usa dentro de las imágenes de
código, así que no hace falta instalarla para abrir el PPTX. Los gráficos las cargan desde esa carpeta. **Para que el PPTX se vea bien hay que instalarlas
en la computadora que abre la presentación** (Windows: clic derecho → Instalar para todos los usuarios; macOS: Catálogo
tipográfico). En el PPTX los titulares usan el nombre "Onest ExtraBold" (el peso 800).

## Lista de verificación

- [x] Fondo blanco en contenido, negro en portada
- [x] Pestaña de sección en todas las láminas de contenido (incluido el índice)
- [x] Todo gráfico con lectura y nota de fuente
- [x] Sin degradados, sombras (se quita el `<p:style>` de cada forma), esquinas redondeadas, fotos, íconos ni gráficos de pastel/3D
- [x] Texto del cuerpo en negro puro y alineado a la izquierda
- [x] Sin logo, nombre ni marca de BlackRock en las láminas
