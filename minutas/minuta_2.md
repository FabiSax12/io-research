# Minuta de reunión: Revisión de información

**Curso:** Investigación de Operaciones, TEC, II Semestre 2026
**Fecha:** 2026-11-13
**Hora de inicio:** 16:00
**Hora de finalización:** 16:41

## Presentes

- [x] Fabián Vargas
- [x] Yan Torres
- [x] Kenni Rodríguez
- [x] Kenneth Araya

## Agenda tratada

1. Fuentes leídas y referencias para la presentación.
2. Comparación de librerías.
3. Problemas de práctica resueltos y sus resultados.
4. Dudas de modelado y ajustes al cronograma.
5. Preparación de cada quien para su parte de la exposición.

## Anotaciones importantes

- **Fuentes:** Hillier y Lieberman, *Introducción a la investigación de operaciones* (PL, transporte, asignación y
  redes); Taha, *Investigación de operaciones* (ramificación y acotamiento, transbordo); documentación oficial de PuLP 3,
  SciPy, lpSolve, OR-Tools, Pyomo y ompr; ayuda de Excel sobre Solver.
- **Librerías:** PuLP y lpSolve cubren los cuatro tipos de problema con poco código, así que son la solución principal.
  SciPy verifica. OR-Tools y Pyomo piden más código del necesario; ompr necesita muchas dependencias.
- **Versiones:** PuLP 4 cambió la API (`lowBound`, `PULP_CBC_CMD`). Se trabaja con PuLP 3 y se anota la versión en la
  lámina de librerías.
- **Problemas resueltos:**
  - PL (cooperativa cafetalera, café Tradicional y Premium): óptimo en (60, 40) con Z = 3800 (₡3 800 000 de ganancia
    semanal); coincide con PuLP, SciPy y lpSolve.
  - PLE (taller de bicicletas de montaña y urbanas): la relajación da (3,29; 4,57) con Z ≈ 458,57, pero el óptimo
    entero es (4, 3) con Z = 430. Redondear no sirve: (3, 5) no es factible y (3, 4) da 410; va a una lámina.
  - Transporte desbalanceado (distribución de leche, oferta 500, demanda 450): destino ficticio con demanda 50 y
    costo 0; costo mínimo 2140.
  - Asignación de 4 técnicos a 3 órdenes de trabajo: se agrega una orden ficticia de valor 0; valor óptimo 100 y
    Andrea queda sin orden.
  - Transbordo (2 plantas, 2 centros de distribución y 3 clientes): se modela como transporte con todos los nodos en
    filas y columnas, buffer B = 100 y un costo M donde no hay arco; óptimo 820 en Python y R. El caso desbalanceado
    (oferta 100, demanda 80) da 610. Luego se verificó con Solver: 820 y 610.
- **Dudas:** si M causa problemas numéricos en Solver (Kenni prueba con M = 1000; el modelo final usa M = 10 000) y
  cómo explicar en la defensa que el nodo de transbordo tiene oferta y demanda cero.
- **Exposición:** cada quien confirma qué láminas le tocan según el reparto de la minuta 1. Kenneth, que expone la
  teoría de transbordo, pide a Kenni un resumen de una página sobre nodos y conservación de flujo. Yan, que expone la
  comparación entre Python, R y Solver, la armará con los resultados que le pase Kenneth.

## Resumen de acuerdos

- Referencias: los libros de Hillier y Taha más la documentación de cada librería, en formato APA (Kenneth).
- Se mantiene PuLP + lpSolve como solución principal, SciPy como verificación y Solver solo para transbordo.
- El ejemplo de PLE (458,57 contra 430) se usa en la lámina de enteros.
- Cada integrante revisa el código de otra persona antes de incluirlo en la presentación.
- Se mantiene el reparto de exposición de la minuta 1: Fabián (contexto, PL, PLE), Yan (librerías, transporte,
  comparación, conclusiones), Kenneth (asignación y teoría de transbordo), Kenni (modelo matricial, Solver y
  desbalanceado).

## Cronograma

| ACTIVIDAD | PLAZO | RESPONSABLE | CONDICIÓN |
|-----------|-------|-------------|-----------|
| Entregar enunciados definitivos de los cinco problemas | 2026-11-13 | Todos | Concluida |
| Confirmar versiones de las librerías y probar la instalación | 2026-11-13 | Fabián Vargas | Concluida |
| Lista de referencias en formato APA | 2026-11-14 | Kenneth Araya | Concluida |
| Probar el costo M en Excel Solver | 2026-11-14 | Kenni Rodríguez | Concluida |
| Resolver transporte y asignación con datos finales | 2026-11-14 | Yan Torres y Kenneth Araya | Concluida |
| Resumen de una página sobre nodos y conservación de flujo | 2026-11-14 | Kenni Rodríguez | Concluida |
| Revisión cruzada de scripts | 2026-11-15 | Todos | Concluida |
