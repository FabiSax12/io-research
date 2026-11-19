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
  resultado), transbordo contra Solver, conclusiones, minutas y referencias. Son 49 láminas: 35 de contenido, 13 de
  minutas (36 a 48) y la de referencias (49).
- Python y R coinciden en los seis problemas (PL 3800, PLE 430, transporte 2140, asignación 100, transbordo 820 y
  transbordo desbalanceado 610). Kenneth revisó las tablas de resultados.
- Solver da 820 y 610 para los dos casos de transbordo, igual que Python y R. Los resultados ya están en las láminas
  30 y 34 y en el gráfico comparativo.
- Los textos que estaban pendientes quedaron resueltos: enunciados, opinión del equipo en la tabla de
  librerías, conclusión final (lámina 35) y cronograma, que va en las láminas de las minutas.
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
  | 2 | Yan | 4-5, 14-17, 22 y 35 | Librerías, transporte, comparación de resultados y conclusiones |
  | 3 | Kenneth | 18-21 y 23-25 | Asignación, qué es un transbordo, diferencias con transporte y ejemplo de red |
  | 4 | Kenni | 26-34 | Modelo matricial con buffer, código, resultados, Solver y caso desbalanceado |

- Las láminas 1, 2 y 36 a 49 (portada, índice, minutas con cronograma y referencias) no se exponen. Fabián abre con la
  portada y cada quien presenta al siguiente al terminar.
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
| Pasar los valores de Solver a las láminas 30 y 34 y al gráfico de la lámina 22 | 2026-11-17 | Kenni Rodríguez | Resultados de los dos archivos de Excel |
| Completar los textos pendientes de la parte de cada quien | 2026-11-18 | Todos | Antes de la versión final |
| Ajustar el diagrama de red con nodos ficticios | 2026-11-18 | Yan Torres | Caso desbalanceado resuelto |
| Completar el cronograma en las láminas de las minutas (36 a 48) | 2026-11-18 | Fabián Vargas | Fechas de las tres minutas |
| Versión final de la presentación y exportación a PDF | 2026-11-18 | Fabián Vargas | Textos completos |
| Revisión de erratas de la presentación completa | 2026-11-19 | Kenneth Araya | PDF exportado |
| Ensayo con cronómetro y prueba de los scripts en la laptop | 2026-11-19 | Todos | Presentación final cerrada; cada uno en unos 5 minutos |
| Defensa | 2026-11-20 | Todos | Cada integrante responde sobre cualquier parte |
