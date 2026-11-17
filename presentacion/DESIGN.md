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
| Franja de embargo | Fecha de la defensa en mayúsculas bermellón |
| *Chart takeaway:* | **Lectura del gráfico:** |
| *Forward-looking estimates may not come to pass.* | **Los resultados dependen de los datos de entrada y pueden variar.** |
| *Investment implications* | **Implicaciones para el modelo** |
| *Capital at risk* (pie) | USO ACADÉMICO. LOS RESULTADOS DEPENDEN DE LOS DATOS DE CADA MODELO. |
| Escenarios: probabilidades a 28 px | Costo óptimo del transbordo en tres casos (balanceado, sobra, falta oferta) |
| Mega forces: capital público vs. privado | Demanda que llega por un nodo de transbordo vs. directa, por destino |
| Cita con retrato amarillo | Definición de transbordo (Taha) con mosaico amarillo e iniciales; sin foto |
| Tabla táctica (asset class, View, Commentary) | Librería, Lenguaje, Valoración (medidor de −3 a +3), Comentario |
| Barras rayadas = estimaciones | Relajación lineal del PLE (cota) y resultados de R/Solver aún pendientes |
| Líneas discontinuas sobre ventana #ededf1 | Recta de nivel de Z (PL) y curva de costo en los casos desbalanceados |

Todos los textos fijos están en `tema.py` (`AVISO_PIE`, `APERTURA_FUENTE`, `ETIQUETA_LECTURA`, `TITULO_IMPLICACIONES`)
por si se quiere volver a la redacción original en inglés.

## Decisiones que la especificación no cubre

- **Código fuente**: va en Barlow Condensed 400 (11.5 px) sobre un recuadro #ededf1. La especificación no define
  una fuente monoespaciada y no se quiso salir de las dos familias.
- **Capturas** (`capturas/*.png`): `comun/utilidades.py` y `comun/utilidades.R` dibujan las tablas con encabezado negro,
  texto blanco y reglas horizontales negras; el diagrama de red de `parte2/python/transbordo.py` usa la paleta.
- **Matrices** (transbordo): se dibujan como tabla nativa desde el CSV para que se lean; las celdas con costo real van en bermellón.
- **Marcadores** de contenido pendiente: recuadro #ededf1 con "Pendiente" en negrita. Desaparecen solos cuando existe la captura.

## Fuentes

`fuentes/` trae los TTF estáticos de Google Fonts (licencia SIL OFL 1.1, ver `OFL-*.txt`): Onest 400/700/800 y
Barlow Condensed 400/700. Los gráficos las cargan desde esa carpeta. **Para que el PPTX se vea bien hay que instalarlas
en la computadora que abre la presentación** (Windows: clic derecho → Instalar para todos los usuarios; macOS: Catálogo
tipográfico). En el PPTX los titulares usan el nombre "Onest ExtraBold" (el peso 800).

## Lista de verificación

- [x] Fondo blanco en contenido, negro en portada
- [x] Pestaña de sección en todas las láminas de contenido (incluido el índice)
- [x] Todo gráfico con lectura y nota de fuente
- [x] Sin degradados, sombras (se quita el `<p:style>` de cada forma), esquinas redondeadas, fotos, íconos ni gráficos de pastel/3D
- [x] Texto del cuerpo en negro puro y alineado a la izquierda
- [x] Sin logo, nombre ni marca de BlackRock en las láminas
