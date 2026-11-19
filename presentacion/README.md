# Presentación (generada con código)

La presentación del trabajo se arma con Python (python-pptx + matplotlib) a partir de lo que producen los scripts
del repositorio. El diseño está en [DESIGN.md](DESIGN.md).

## Reconstruir

Desde la raíz del repositorio:

```bash
python presentacion/reconstruir.py              # corre run_all.py, dibuja los gráficos y arma el PPTX
python presentacion/reconstruir.py --sin-modelos  # usa resultados/ y capturas/ que ya existen
python presentacion/reconstruir.py --pdf          # además PDF y miniaturas PNG (necesita LibreOffice)
```

Atajos: `presentacion/reconstruir.sh` (Linux/macOS) y `presentacion\reconstruir.bat` (Windows), con los mismos argumentos.

Resultado: `presentacion/salida/presentacion_io.pptx` (más `.pdf` y `previews/` con `--pdf`). La carpeta `salida/`
no se versiona: se regenera cada vez.

Antes de abrir el PPTX, instalar las fuentes de `presentacion/fuentes/` (Onest y Barlow Condensed).

## Archivos

| Archivo | Qué contiene | Quién lo toca |
|---|---|---|
| `contenido.py` | Todos los textos de las láminas, la tabla de librerías, las referencias y `SOLVER` (óptimos de Excel) | Todo el equipo |
| `construir.py` | Tipos de lámina y orden de la presentación | Integración |
| `graficos.py` | Gráficos (PNG) con el estilo del tema | Integración |
| `ventana_codigo.py` | Dibuja los fragmentos de código como ventanas estilo carbon.now.sh (JetBrains Mono, botones de macOS) | Solo si cambia el diseño |
| `datos.py` | Lee YAML, JSON, capturas y fragmentos de código | Integración |
| `minutas.py` | Lee `minutas/minuta_*.md` (estructura de `plantilla.md`): datos, presentes, agenda, anotaciones, acuerdos y cronograma | Solo si cambia la plantilla |
| `laminas_minutas.py` | Dibuja las láminas de cada minuta y reparte en varias láminas lo que no cabe | Integración |
| `tema.py` | Paleta, tipografía, retícula y primitivas (pestaña, pie, exhibición, medidor) | Solo si cambia el diseño |
| `reconstruir.py` | Script único que rehace todo | Nadie |

## Qué sale automáticamente y qué falta completar

Sale solo, a partir de `datos/`, `resultados/` y `capturas/`: modelos, valores óptimos, lecturas de los gráficos,
tablas de solución, salidas de consola, matriz ampliada, red de transbordo, fragmentos de código, comparación entre
lenguajes, minutas con su cronograma e índice con números de lámina.

**Minutas**: se leen de `minutas/minuta_*.md` al reconstruir. Para actualizarlas basta editar el `.md` y volver a correr
`reconstruir.py`; cada minuta genera sus láminas (datos y agenda, anotaciones, acuerdos y cronograma) en el orden de la plantilla.

Queda marcado para completar (buscar `[completar` en `contenido.py` o los recuadros grises "Pendiente" en las láminas):

1. **Datos reales**: los YAML de `datos/` todavía son de ejemplo. Al cambiarlos, la presentación se actualiza sola.
2. **R**: instalar R 4.2+ y correr `python run_all.py`; aparecen las tablas de R y la comparación se completa.
3. **Excel Solver**: resolver `parte2/solver/transbordo.xlsx`, guardar la captura como `capturas/transbordo_solver.png`
   y escribir el óptimo en `SOLVER` dentro de `contenido.py`.
4. Enunciados de cada problema, nombre del profesor, valoración de librerías, conclusión propia y fuentes extra.

## Orden de las láminas (49)

Portada · Contenido · Introducción · Librerías (tabla) · Patrón PuLP/lpSolve ·
por cada problema de la Parte I (PL, PLE, transporte, asignación): planteamiento + gráfico, código en Python, código en R,
resultados (tablas de Python y R a la izquierda, consola a la derecha) ·
Comparación Python/R/Solver · ¿Qué es transbordo? · Transporte vs. transbordo · Ejemplo (red) · Modelo matricial paso a paso ·
Código en Python · Código en R · Resultados · Solver · Variantes desbalanceadas · Caso desbalanceado · Resultados desbalanceado · Solver desbalanceado ·
Conclusiones · Minutas (tres, con anotaciones, acuerdos y cronograma; láminas 36 a 48) · Referencias (última lámina, como pide el enunciado).
