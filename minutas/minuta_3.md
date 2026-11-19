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
  resultado), transbordo contra Solver, conclusiones, código, datos e IA, minutas y referencias. Son 51 láminas.
- Python y R coinciden en los cinco problemas. Kenneth revisó las tablas de resultados.
- Kenni ya tiene los resultados de Solver para los dos casos de transbordo. Falta pasarlos a la lámina de Solver y al
  gráfico comparativo, que todavía muestra la barra rayada.
- Pendientes marcados con "[completar]": enunciados de PL y PLE, opinión del equipo en la tabla de librerías, conclusión
  final y las tablas de cronograma de las minutas (láminas 40-41, 45 y 50).
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

- Las láminas 1, 2 y 36 a 51 (portada, índice, código, datos e IA, minutas con su cronograma y
  referencias) no se exponen. Fabián abre con la portada y cada quien presenta al siguiente al terminar.
- Se cambian los ejemplos de práctica de la minuta 2 por problemas propios: PL con la cooperativa cafetalera de
  Tarrazú (en lugar de las plantas de vidrio), PLE con el taller de bicicletas (458,57 contra 430, en lugar de 21
  contra 20) y transporte con la cooperativa lechera. Esto reemplaza el acuerdo de la minuta 2 sobre la lámina de
  enteros.
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
| Pasar los valores de Solver a la lámina 30 y al gráfico de la lámina 22 | 2026-11-17 | Kenni Rodríguez | Concluida |
| Completar los textos "[completar]" de la parte de cada quien | 2026-11-18 | Todos | Concluida |
| Ajustar el diagrama de red con nodos ficticios | 2026-11-18 | Yan Torres | Concluida |
| Completar el cronograma de las minutas (láminas 40-41, 45 y 50) | 2026-11-18 | Fabián Vargas | Concluida |
| Versión final de la presentación y exportación a PDF | 2026-11-18 | Fabián Vargas | En proceso |
| Revisión de erratas de la presentación completa | 2026-11-19 | Kenneth Araya | En proceso |
| Ensayo con cronómetro y prueba de los scripts en la laptop | 2026-11-19 | Todos | En proceso |
| Defensa | 2026-11-20 | Todos | En proceso |
