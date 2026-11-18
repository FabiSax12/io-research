# Minuta de reunión: Presentación

**Curso:** Investigación de Operaciones, TEC, II Semestre 2026
**Fecha:** 2026-11-17
**Hora de inicio:** 18:00
**Hora de finalización:** 18:45

## Presentes

- [x] Fabián Vargas
- [x] Yan Torres
- [x] Kenni Rodríguez
- [x] Kenneth Araya

## Agenda tratada

1. Revisión de la presentación, lámina por lámina.
2. Resultados de Python, R y Excel Solver, y textos pendientes.
3. Orden de exposición y preguntas probables.
4. Plan de ensayos.

## Anotaciones importantes

- Estructura: portada, índice, contexto, tabla de librerías, un bloque por problema (enunciado, modelo, código y
  resultado), transbordo contra Solver, conclusiones y referencias. Son 36 láminas.
- Python y R coinciden en los cinco problemas. Kenneth revisó las tablas de resultados.
- Kenni ya tiene los resultados de Solver para los dos casos de transbordo. Falta pasarlos a la lámina de Solver y al
  gráfico comparativo, que todavía muestra la barra rayada.
- Pendientes marcados con "[completar]": enunciados de PL y PLE, opinión del equipo en la tabla de librerías, conclusión
  final y la tabla de cronograma de la lámina 35.
- Ajustes de forma: menos texto en las láminas de transporte y asignación, y nodos ficticios en el diagrama de
  transbordo desbalanceado.
- Los scripts corrieron sin errores en otra computadora (Windows con R 4.2) tras instalar los paquetes.
- **Equilibrio de la exposición:** se contaron las láminas con peso según su contenido (conceptual y con gráfico, 1;
  resultados y tablas, 0.75; código, 0.5). Con el reparto de la minuta 1 el tiempo queda en unos 6 puntos por persona.

## Resumen de acuerdos

- Orden de exposición, unos 5 minutos cada uno:

  | Orden | Integrante | Láminas | Contenido |
  |-------|------------|---------|-----------|
  | 1 | Fabián | 3 y 6-13 | Contexto, PL y PLE |
  | 2 | Yan | 4-5, 14-17, 22 y 34 | Librerías, transporte, comparación de resultados y conclusiones |
  | 3 | Kenneth | 18-21 y 23-25 | Asignación, qué es un transbordo, diferencias con transporte y ejemplo de red |
  | 4 | Kenni | 26-33 | Modelo matricial con buffer, código, resultados, Solver y caso desbalanceado |

- Las láminas 1, 2, 35 y 36 (portada, índice, cronograma y referencias) no se exponen. Fabián abre con la portada y
  cada quien presenta al siguiente al terminar.
- Todos deben poder explicar el modelo de los demás.
- Preguntas probables: por qué el óptimo entero es menor que la relajación (Fabián); por qué el destino ficticio cuesta
  cero y por qué se eligió PuLP y lpSolve y no OR-Tools (Yan); en qué se diferencia transbordo de transporte y por qué
  la asignación no siempre toma el mínimo de la fila (Kenneth); para qué sirve M y qué pasa si el modelo está
  desbalanceado (Kenni).
- Se lleva la presentación en PowerPoint y PDF, y los scripts listos en una laptop. Si falla el equipo, se muestran las
  capturas de resultados incluidas en la presentación.

## Cronograma

| ACTIVIDAD | PLAZO | RESPONSABLE | CONDICIÓN |
|-----------|-------|-------------|-----------|
| Pasar los valores de Solver a la lámina 30 y al gráfico de la lámina 22 | 2026-11-17 | Kenni Rodríguez | Resultados de los dos archivos de Excel |
| Completar los textos "[completar]" de la parte de cada quien | 2026-11-18 | Todos | Antes de la versión final |
| Ajustar el diagrama de red con nodos ficticios | 2026-11-18 | Yan Torres | Caso desbalanceado resuelto |
| Completar el cronograma de la lámina 35 | 2026-11-18 | Fabián Vargas | Fechas de las tres minutas |
| Versión final de la presentación y exportación a PDF | 2026-11-18 | Fabián Vargas | Textos completos |
| Revisión de erratas de la presentación completa | 2026-11-19 | Kenneth Araya | PDF exportado |
| Ensayo con cronómetro y prueba de los scripts en la laptop | 2026-11-19 | Todos | Presentación final cerrada; cada uno en unos 5 minutos |
| Defensa | 2026-11-20 | Todos | Cada integrante responde sobre cualquier parte |
