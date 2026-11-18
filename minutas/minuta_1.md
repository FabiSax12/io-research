# Minuta de reunión: División de trabajo

**Curso:** Investigación de Operaciones, TEC, II Semestre 2026
**Fecha:** 2026-11-09
**Hora de inicio:** 20:00
**Hora de finalización:** 20:48

## Presentes

- [x] Fabián Vargas
- [x] Yan Torres
- [x] Kenni Rodríguez
- [x] Kenneth Araya

## Agenda tratada

1. Qué se entrega y cómo se evalúa.
2. Reparto de las partes entre los cuatro integrantes.
3. Reparto de la exposición.
4. Herramientas y forma de trabajo.
5. Cronograma de actividades y próximas reuniones.

## Anotaciones importantes

- El entregable es una presentación de PowerPoint. El código y los resultados son apoyo, pero deben poder pegarse en
  las láminas y correrse en la defensa.
- Parte I: un problema de programación lineal (PL), uno entero (PLE), uno de transporte y uno de asignación.
  Parte II: un problema de transbordo, balanceado y desbalanceado, que también se resuelve con Excel Solver.
- Se usa **Python (PuLP, SciPy)** y **R (lpSolve)** para resolver cada problema en dos lenguajes y comparar resultados.
- Cada problema se define en un archivo de datos aparte; los scripts solo lo leen. Son cortos y con comentarios en
  español.
- **Reparto del trabajo técnico:** Fabián, PL y PLE; Yan, transporte; Kenneth, asignación; Kenni, transbordo y Solver.
  La revisión bibliográfica y la comparación de librerías son de todos.
- **Reparto de la exposición:** la carga no coincide con el trabajo técnico, porque transbordo tiene casi el triple de
  láminas que transporte o asignación. Para que todos hablen lo mismo (unos 5 minutos cada uno) se reparte así:
  - Fabián: contexto, PL y PLE.
  - Yan: tabla de librerías, transporte, comparación Python/R/Solver y conclusiones.
  - Kenneth: asignación, qué es un transbordo, diferencias con transporte y el ejemplo de red.
  - Kenni: modelo matricial con buffer, código, resultados, Solver y caso desbalanceado.
- Duda: mínimo de restricciones por modelo. Se acordó usar al menos 3 en todos.
- Duda: si Excel Solver aguanta el transbordo completo (límite de 200 celdas variables). Kenni lo verifica.

## Resumen de acuerdos

- Cada responsable avisa al grupo si se atrasa más de un día.
- Resultados y capturas con el mismo formato en todas las partes.
- Reunión de revisión de información el 2026-11-13 y de presentación el 2026-11-17. Todos leen la teoría de su parte
  antes de la primera.
- Quien expone una lámina que no resolvió recibe de su autor el resultado y una explicación breve del modelo.

## Cronograma

| ACTIVIDAD | PLAZO | RESPONSABLE | CONDICIÓN |
|-----------|-------|-------------|-----------|
| Elegir los cinco problemas y redactar sus enunciados | 2026-11-09 | Todos | Cada integrante propone el de su parte |
| Lectura de teoría y documentación de librerías | 2026-11-11 | Todos | Tabla comparativa con recomendación por librería |
| Reunión de revisión de información (minuta 2) | 2026-11-13 | Todos | Cada quien trae lo leído y lo resuelto |
| PL y PLE en Python y R | 2026-11-13 | Fabián Vargas | Datos finales de ambos problemas |
| Transporte en Python y R | 2026-11-14 | Yan Torres | Formato de datos definido |
| Asignación en Python y R | 2026-11-14 | Kenneth Araya | Formato de datos definido |
| Transbordo en Python y R, balanceado y desbalanceado | 2026-11-14 | Kenni Rodríguez | Formato de datos definido |
| Transbordo en Excel Solver (dos archivos) | 2026-11-15 | Kenni Rodríguez | Matriz de transbordo lista |
| Comparación de resultados entre Python, R y Solver | 2026-11-15 | Kenneth Araya | Los cinco problemas resueltos; los resultados se entregan a Yan, que los expone |
| Presentación, textos y gráficos | 2026-11-16 | Fabián Vargas | Resultados y capturas listos |
| Reunión de presentación y preparación de la defensa (minuta 3) | 2026-11-17 | Todos | Diapositivas completas |
| Ensayo general con cronómetro | 2026-11-19 | Todos | Un ensayo por persona, unos 5 minutos cada uno |
| Defensa | 2026-11-20 | Todos | Cada integrante expone su parte |
