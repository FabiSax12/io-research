"""Textos de la presentación. Editar aquí; el diseño vive en tema.py y el armado en construir.py.

Convenciones:
- "{clave}" se reemplaza con un número calculado de resultados/ o de los gráficos (ver construir.valores()).
- Un párrafo que empieza con "## " sale en negrita (subtítulo dentro de una columna).
- "[completar: ...]" marca texto que el equipo debe escribir o confirmar antes de exponer.
"""

CURSO = "Investigación de Operaciones"
SEMESTRE = "II Semestre 2026"
INSTITUCION = ("Instituto", "Tecnológico", "de Costa Rica")     # la palabra del medio va en negrita
PROFESOR = "Prof. Esteban José Ballestero Alfaro"

# Resultados de Excel Solver: escribir el valor óptimo que dio Solver al terminar el paso manual.
# None = todavía no se corrió (la lámina muestra un marcador y el gráfico una barra rayada).
SOLVER = {"transbordo": 820, "transbordo_desbalanceado": 610}

PORTADA = {
    "anio": "2026",
    "titulo": "Trabajo de\ninvestigación",
    "subtitulo": "Programación lineal, transporte, asignación y transbordo resueltos con Python, R y Excel Solver",
}

# ------------------------------------------------------------------ contexto
INTRO = {
    "titular": "Tres variantes de un mismo problema",
    "izq": [
        "## Transporte",
        "Mueve bienes de orígenes con oferta a destinos con demanda al menor costo total de envío.",
        "## Asignación",
        "Reparte tareas entre agentes, uno a uno, para minimizar costo o maximizar rendimiento. "
        "Es un transporte con ofertas y demandas iguales a 1.",
    ],
    "der": [
        "## Transbordo",
        "Permite que el flujo pase por nodos intermedios (bodegas, centros de distribución) antes de llegar "
        "al destino. Es el tema de la Parte II.",
        "## Cómo lo resolvimos",
        "Cada problema vive en un YAML de datos/. Los scripts de Python y R leen el mismo archivo, "
        "así que los dos lenguajes resuelven exactamente el mismo modelo.",
    ],
    "exhibicion": {
        "titulo": "Tamaño de los modelos resueltos",
        "subtitulo": "Variables de decisión y restricciones por problema, después de balancear (unidades)",
        "lectura": "el modelo más grande es {mayor_nombre}, con {mayor_vars} variables; ninguno pasa de 20, "
                   "así que el reto es modelar bien, no la escala.",
        "fuente": None,
        "implicaciones": [
            "Todos cumplen el mínimo de 3 restricciones que pide el enunciado.",
            "El balanceo (nodos ficticios) agrega variables: hay que contarlas al explicar el modelo.",
        ],
    },
}

# ------------------------------------------------------------------ herramientas (tabla de valoración)
# Tabla de librerías. Cada fila: (librería, lenguaje, qué resuelve, rol en el trabajo, recomendación, expectativa, comentario)
# recomendación y expectativa van de -3 (no la recomendamos) a +3 (la recomendamos) para los problemas de este curso:
# recomendación = después de probarla (celda de color); expectativa = lo que pensábamos antes (punto negro).
HERRAMIENTAS = {
    "titular": "Librerías que investigamos",
    "intro": "¿Con qué resolver cada tipo de problema? Comparamos siete herramientas según qué problemas cubren y qué "
             "tan fácil fue escribir los modelos. La columna Recomendación resume nuestra opinión en una escala de −3 a +3.",
    "leyenda": "Cómo leer la columna Recomendación",
    "filas": [
        ("PuLP", "Python", "PL · PLE · Transp. · Asig.", "Solución principal", 2, 1,
         "El modelo se escribe casi igual que en la pizarra; trae el solver CBC."),
        ("SciPy", "Python", "PL · PLE · Asig.", "Verificación", 1, 1,
         "linprog y milp trabajan con matrices; linear_sum_assignment resuelve asignación."),
        ("OR-Tools", "Python", "PL · PLE · Redes", "Solo investigada", 1, 2,
         "Muy completa, pero pide más código del necesario para modelos de clase."),
        ("Pyomo", "Python", "PL · PLE", "Solo investigada", 0, 1,
         "Pensada para modelos grandes; hay que instalar el solver aparte."),
        ("lpSolve", "R", "PL · PLE · Transp. · Asig.", "Solución principal", 2, 1,
         "lp(), lp.transport() y lp.assign(): una llamada por tipo de problema."),
        ("ompr + ROI", "R", "PL · PLE", "Solo investigada", 0, 0,
         "Sintaxis parecida a PuLP, pero con muchas dependencias que instalar."),
        ("Excel Solver", "Excel", "PL · PLE · Transp. · Asig.", "Transbordo (Parte II)", 1, 0,
         "Simplex LP; muestra la matriz completa. Máximo 200 celdas variables."),
    ],
    "lectura": "PuLP (Python) y lpSolve (R) cubren los cuatro tipos con poco código, por eso son las que usamos; SciPy verifica los resultados.",
    "fuente": "Documentación oficial de PuLP, SciPy, lpSolve y Excel Solver (ver referencias).",
}

USO_LIBRERIAS = {
    "titular": "El mismo patrón en las cuatro librerías",
    "izq": [
        "## 1. Datos",
        "Coeficientes, lados derechos y sentido (max o min) salen del YAML.",
        "## 2. Variables",
        "PuLP: LpVariable(lowBound=0, cat=\"Integer\"). lpSolve: vector de coeficientes; int.vec marca las enteras.",
    ],
    "der": [
        "## 3. Objetivo y restricciones",
        "PuLP las suma con lpSum; lpSolve recibe la matriz A, los signos y el vector b.",
        "## 4. Resolver y leer",
        "modelo.solve(PULP_CBC_CMD()) o lp(...). Se lee el estado, el valor óptimo y las variables.",
    ],
}

# ------------------------------------------------------------------ parte I (un bloque por problema)
PARTE1 = {
    "pl": {
        "titular": "Programación lineal",
        "izq": ["## Problema", "{pl_nombre}. Una cooperativa de Tarrazú decide cuántos quintales producir de café "
                "Tradicional (x1) y Premium (x2). Ganancia: ₡30 000 y ₡50 000 por quintal (Z en miles de colones).",
                "## Modelo", "{pl_modelo}"],
        "der": ["## Restricciones", "100 qq de grano verde; 280 h de tostadora (2 h y 4 h por qq); "
                "máximo 50 qq de Premium; contrato de al menos 20 qq de Tradicional.",
                "## Librerías", "Python: PuLP (CBC) y SciPy linprog para verificar. R: lpSolve::lp().",
                "## Resultado", "Z = {pl_optimo} con {pl_solucion}."],
        "exhibicion": {
            "titulo": "Región factible y solución óptima",
            "subtitulo": "Restricciones del modelo y recta de nivel de Z en el óptimo",
            "lectura": "el óptimo está en el vértice ({pl_x1}, {pl_x2}), donde se cruzan dos restricciones activas; Z = {pl_optimo}.",
            "fuente": None,
            "implicaciones": ["Activas: grano y tostadora. Demanda y contrato tienen holgura (precio sombra 0).",
                              "Precios sombra: un quintal más de grano o una hora más de tostadora vale ₡10 000."],
        },
        "codigo": [("parte1/python/pl.py", "--- Modelo en PuLP", "--- Verificación"), ("parte1/r/pl.R", None, None)],
    },
    "ple": {
        "titular": "Programación lineal entera",
        "izq": ["## Problema", "{ple_nombre}. Un taller de Cartago decide cuántas bicicletas de montaña (x1) y "
                "urbanas (x2) armar; deben ser enteras. Ganancia: ₡70 000 y ₡50 000 (Z en miles de colones).",
                "## Modelo", "{ple_modelo}"],
        "der": ["## Restricciones", "19 h de soldadura (3 h y 2 h); 17 h de pintura (1 h y 3 h); "
                "4 cuadros de montaña; cupo de ensamblaje para 8 bicicletas.",
                "## Librerías", "Python: PuLP con cat=\"Integer\" (ramificación y acotamiento en CBC) y SciPy milp. "
                "R: lpSolve::lp() con int.vec.",
                "## Resultado", "Z = {ple_optimo} con {ple_solucion}."],
        "exhibicion": {
            "titulo": "Óptimo entero frente a la relajación lineal",
            "subtitulo": "Valor de Z sin y con la condición de integralidad",
            "lectura": "exigir enteros baja Z de {ple_cota} a {ple_optimo} ({ple_brecha} % menos); la relajación es una cota.",
            "fuente": "La barra rayada es una cota, no una solución factible.",
            "implicaciones": ["Redondear no sirve: (3, 5) no es factible y (3, 4) da 410; exigir enteros cuesta {ple_brecha} %.",
                              "x1 ≤ 4 tiene holgura en la relajación (3,29) pero es activa en el óptimo entero."],
        },
        "codigo": [("parte1/python/ple.py", "--- Modelo en PuLP", "--- Verificación"), ("parte1/r/ple.R", None, None)],
    },
    "transporte": {
        "titular": "Problema de transporte",
        "izq": ["## Problema", "{tr_nombre}. Una cooperativa lechera envía leche desde sus plantas de San Carlos, "
                "Zarcero y Cartago (200, 150 y 150 miles de litros) a sus centros de San José, Alajuela y Heredia "
                "(180, 170 y 100). xij = miles de litros de la planta i al centro j (Z en miles de colones).",
                "## Modelo", "Min Z = 8x11 + 5x12 + 6x13 + 7x21 + 4x22 + 5x23 + 4x31 + 9x32 + 7x33",
                "Oferta: x11 + x12 + x13 ≤ 200; x21 + x22 + x23 ≤ 150; x31 + x32 + x33 ≤ 150",
                "Demanda: x11 + x21 + x31 = 180; x12 + x22 + x32 = 170; x13 + x23 + x33 = 100; xij ≥ 0"],
        "der": ["## Balanceo", "{tr_ajuste}",
                "## Librerías", "Python: PuLP. R: lpSolve::lp.transport().",
                "## Resultado", "Costo mínimo = {tr_optimo} (₡2 140 000). Cartago abastece a San José y Zarcero a "
                "Alajuela; San Carlos reparte el resto y le sobran 50 mil litros."],
        "exhibicion": {
            "titulo": "Uso de la oferta por planta",
            "subtitulo": "Unidades enviadas a clientes y asignadas al destino ficticio, por origen",
            "lectura": "{tr_lectura}",
            "fuente": None,
            "implicaciones": ["Lo que va al ficticio es oferta que se queda en la planta.",
                              "El ficticio tiene costo 0, así que no altera el costo total."],
        },
        "codigo": [("parte1/python/transporte.py", "--- Modelo en PuLP", None), ("parte1/r/transporte.R", "--- Modelo:", None)],
    },
    "asignacion": {
        "titular": "Problema de asignación",
        "izq": ["## Problema", "{as_nombre}. Matriz de {as_dim} ({as_sentido}).",
                "## Modelo", "x_ij ∈ {{0,1}}; cada agente hace a lo sumo una tarea y cada tarea la hace un agente. "
                "Con ofertas y demandas enteras, el PL ya tiene un óptimo entero (Winston, 2004, sec. 7.3 y 7.5)."],
        "der": ["## Ajuste", "{as_ajuste}",
                "## Librerías", "Python: PuLP (y verificación con variables binarias). R: lpSolve::lp.assign().",
                "## Resultado", "Valor óptimo = {as_optimo}."],
        "exhibicion": {
            "titulo": "Asignación óptima por agente",
            "subtitulo": "Valor de la tarea asignada y mínimo de cada fila de la matriz",
            "lectura": "{as_lectura}",
            "fuente": None,
            "implicaciones": ["No siempre gana el mínimo de cada fila: dos agentes no pueden tomar la misma tarea.",
                              "Las tareas ficticias marcan a quién no se le asigna trabajo."],
        },
        "codigo": [("parte1/python/asignacion.py", "--- Verificación: modelo de PL", None),
                   ("parte1/r/asignacion.R", "--- Modelo de asignación", None)],
    },
}

COMPARACION = {
    "titular": "Tres herramientas, un solo óptimo",
    "izq": ["## Cómo se comparó", "run_all.py corre cada problema en los dos lenguajes y compara el valor óptimo con tolerancia de 1e-6.",
            "## Verificación interna", "Cada script además resuelve el modelo con un segundo método (SciPy, variables binarias o el modelo con buffer)."],
    "der": ["## Estado", "{estado_comparacion}",
            "## Solver", "Excel Solver (Simplex LP) sobre la matriz con buffer da el mismo óptimo en transbordo y en transbordo desbalanceado."],
    "exhibicion": {
        "titulo": "Valor óptimo relativo al de Python",
        "subtitulo": "Índice, Python = 100, por problema y herramienta",
        "lectura": "{comparacion_lectura}",
        "fuente": "Barras rayadas: resultado aún no generado.",
        "implicaciones": ["Si los tres coinciden, el modelo está bien planteado, no solo bien programado.",
                          "Una diferencia apunta a datos distintos o a un error de balanceo."],
    },
}

# fragmentos de código del transbordo: (script, línea donde empieza, línea donde termina)
CODIGO_TRANSBORDO = [("parte2/python/transbordo.py", "3. Modelo de red", "5. Resultado"),
                     ("parte2/r/transbordo.R", "3. Modelo de red", "5. Resultado")]

# ------------------------------------------------------------------ parte II
QUE_ES = {
    "titular": "¿Qué es un problema de transbordo?",
    "cita": "Un problema de transbordo es un problema de transporte en el que la mercancía puede pasar por "
            "nodos intermedios antes de llegar a su destino.",
    "autor": "Paráfrasis de Taha (2017), p. 224",
    "iniciales": "HT",
    "situaciones": [
        "## Situaciones que modela",
        "Cadenas de suministro con bodegas o centros de distribución; cross-docking; redes de combustible "
        "con terminales; carga aérea con aeropuertos hub; redes de agua o energía con estaciones intermedias.",
        "## Elementos",
        "Nodos de origen (oferta), de transbordo (entra = sale) y de destino (demanda); arcos con costo unitario.",
    ],
    "exhibicion": {
        "titulo": "Cómo llega la demanda a cada destino",
        "subtitulo": "Unidades por destino según su último tramo, ejemplo de la Parte II",
        "lectura": "el {pct_via} % de la demanda llega a través de un nodo de transbordo: la ruta directa P1→D1 existe, pero es más cara.",
        "fuente": None,
    },
}

RELACION = {
    "titular": "Transporte y transbordo",
    "encabezados": ["Aspecto", "Transporte", "Transbordo"],
    "filas": [
        ("Rutas", "Solo directas, de origen a destino", "Pueden pasar por nodos intermedios, y en general por cualquier nodo"),
        ("Nodos", "Cada nodo solo ofrece o solo demanda", "Hay nodos de transbordo con oferta neta 0 (lo que entra, sale)"),
        ("Restricciones", "Oferta por fila y demanda por columna", "Conservación de flujo en cada nodo: sale − entra = oferta − demanda"),
        ("Matriz", "m × n (orígenes × destinos)", "n × n con todos los nodos; costo 0 en la diagonal y M donde no hay arco"),
        ("Relación", "Caso particular del transbordo sin nodos intermedios",
         "Se convierte en transporte agregando un buffer B a filas y columnas (Taha, 2017, p. 224)"),
    ],
    "lectura": "todo problema de transbordo se puede resolver como uno de transporte; la diferencia está en armar la matriz.",
    "fuente": "Taha (2017), p. 224 y sec. 22.1 (material web); Hillier y Lieberman (2021), cap. 9; Winston (2004), sec. 7.6; Khurana (2015).",
}

EJEMPLO = {
    "titular": "Nuestro ejemplo de transbordo",
    "izq": ["## Enunciado", "{tb_nombre}. Una empresa envía producto desde dos plantas (P1, P2) a tres clientes (D1, D2, D3), casi siempre a través de dos centros de distribución (T1, T2); también existe un envío directo P1→D1, más caro.",
            "## Nodos", "{tb_nodos}"],
    "der": ["## Arcos", "{tb_narcos} rutas posibles con costo unitario; las que no existen no se pueden usar (costo M en la matriz).",
            "## Resultado", "Costo mínimo = {tb_optimo}. Flujo por los nodos de transbordo: {tb_via} unidades."],
    "exhibicion": {
        "titulo": "Red del ejemplo y flujo óptimo",
        "subtitulo": "Costo unitario por arco; [flujo] en los arcos usados (unidades)",
        "lectura": "todo el flujo pasa por T1 o T2; el arco directo P1→D1 (costo 12) queda sin usar.",
        "fuente": None,
        "implicaciones": ["Los arcos grises existen pero no conviene usarlos.",
                          "Los nodos rosados no ofrecen ni demandan: solo redistribuyen."],
    },
}

MATRICIAL = {
    "titular": "Modelo matricial paso a paso",
    "izq": ["## 1. Clasificar nodos", "Orígenes, transbordos y destinos; todo nodo es fila (envía) y columna (recibe).",
            "## 2. Balancear", "Si Σoferta ≠ Σdemanda, agregar un nodo ficticio (ver variantes).",
            "## 3. Buffer", "B = flujo total = {tb_B}. Es lo máximo que puede pasar por un nodo."],
    "der": ["## 4. Costos", "c_ij del arco; 0 en la diagonal (x_ii = buffer sin usar); M = {tb_M} si no hay arco.",
            "## 5. Oferta y demanda", "Fila i: oferta_i + B. Columna j: demanda_j + B.",
            "## 6. Resolver", "min Σ c_ij x_ij con Σ_j x_ij = oferta_i + B, Σ_i x_ij = demanda_j + B, x_ij ≥ 0."],
    "exhibicion": {
        "titulo": "Matriz de costos ampliada",
        "subtitulo": "{tb_n} × {tb_n} nodos, buffer B = {tb_B}, M = {tb_M}",
        "lectura": "las celdas M bloquean rutas que no existen; con el buffer el modelo da {tb_buffer} = {tb_optimo} del modelo de red.",
        "fuente": None,
        "implicaciones": ["M se elige mayor que cualquier plan sin arcos ficticios para que nunca convenga.",
                          "La misma matriz se carga en Excel para Solver."],
    },
}

SOLVER_LAMINA = {
    "titular": "Solución con Excel Solver",
    "izq": ["## Archivo", "parte2/solver/transbordo.xlsx lo genera el script de Python: matriz, celdas de decisión y fórmulas.",
            "## Objetivo", "Celda de costo total (SUMAPRODUCTO de costos × envíos), minimizar."],
    "der": ["## Restricciones", "Suma de cada fila = oferta + B; suma de cada columna = demanda + B; no negatividad.",
            "## Método", "Simplex LP. La hoja Instrucciones trae las celdas exactas y el óptimo esperado ({tb_optimo})."],
    "exhibicion": {
        "titulo": "Resultado de Solver",
        "subtitulo": "Captura de la hoja resuelta",
        "lectura": "{solver_lectura}",
        "fuente": None,
        "implicaciones": ["Solver no se automatiza: se corre a mano y se guarda la captura.",
                          "Guardar el libro resuelto con otro nombre; el script sobrescribe transbordo.xlsx."],
    },
}

SOLVER_DESB_LAMINA = {
    "titular": "Solver: caso desbalanceado",
    "izq": ["## Archivo", "parte2/solver/transbordo_desbalanceado.xlsx: la misma hoja con una fila y una columna más para el nodo Ficticio."],
    "der": ["## Qué cambia", "El ficticio absorbe el excedente de oferta a costo 0; B se calcula con el total ya balanceado.",
            "## Método", "Mismo modelo: minimizar el costo total con suma de fila = oferta + B y suma de columna = demanda + B (Simplex LP)."],
    "exhibicion": {
        "titulo": "Resultado de Solver (desbalanceado)",
        "subtitulo": "Hoja resuelta con el nodo Ficticio",
        "lectura": "{solver_desb_lectura}",
        "fuente": None,
        "implicaciones": ["El flujo hacia el ficticio son las unidades de oferta que no salen del origen.",
                          "Guardar el libro resuelto con otro nombre; el script sobrescribe el archivo."],
    },
}

VARIANTES = {
    "titular": "¿Hay transbordos desbalanceados?",
    "intro": "Sí. Igual que en transporte, si la oferta total no coincide con la demanda total el modelo no tiene "
             "solución factible hasta balancearlo con un nodo ficticio de costo 0.",
    "casos": [
        ("balanceado", "Oferta = demanda", "Sin ajustes: se resuelve tal cual. Oferta {o_bal}, demanda {d_bal}."),
        ("sobra", "Oferta > demanda", "Destino ficticio con demanda = excedente ({f_sobra}) y arcos de costo 0 desde cada origen."),
        ("falta", "Oferta < demanda", "Origen ficticio con oferta = faltante ({f_falta}) y arcos de costo 0 hacia cada destino."),
    ],
    "nota": "Costo óptimo del ejemplo en cada caso (variando la oferta de P1 en ±20 unidades). "
            "B se calcula después de balancear, con el total ya igualado.",
    "fuente": "Taha (2017), pp. 209-210; Khurana (2015).",
}

DESBALANCEADO = {
    "titular": "Cómo se resuelve el caso desbalanceado",
    "izq": ["## Sobra oferta", "Se agrega un destino ficticio (una columna más). Lo que recibe es oferta que no sale del origen.",
            "## Falta oferta", "Se agrega un origen ficticio. Lo que envía es demanda que queda sin atender; "
            "si eso tiene un costo (penalización), se usa en lugar de 0."],
    "der": ["## Enunciado", "Misma red del ejemplo anterior, pero la demanda baja: D2 pasa de 40 a 30 y D3 de 30 a 20. "
            "P1 y P2 siguen ofreciendo 60 y 40, así que sobran 20 unidades. ¿Cómo enviar al menor costo?",
            "## Nuestro caso", "{desb_ajuste} Costo = {desb_optimo}."],
    "exhibicion": {
        "titulo": "Costo óptimo según la oferta disponible",
        "subtitulo": "Costo total al variar la oferta de {curva_nodo}; demanda fija de {curva_bal} unidades",
        "lectura": "con oferta de sobra el costo no cambia ({curva_costo}); si falta, baja solo porque se envía menos, no porque la red sea más barata.",
        "fuente": None,
        "implicaciones": ["Un costo menor con faltante es engañoso: hay demanda sin cubrir.",
                          "Conviene reportar las unidades del ficticio junto al costo."],
    },
}

# ------------------------------------------------------------------ resumen
CONCLUSIONES = {
    "titular": "Lo que nos llevamos",
    "izq": ["## Parte I", "Los cuatro tipos de problema se resuelven con el mismo patrón: datos, variables, objetivo, restricciones. "
            "PuLP y lpSolve cubren todo el curso.",
            "## Verificación", "Resolver con dos lenguajes y un segundo método detecta errores de planteamiento."],
    "der": ["## Parte II", "El transbordo generaliza al transporte; con el buffer B se resuelve con las mismas herramientas.",
            "## Desbalanceo", "Se corrige con un nodo ficticio de costo 0, igual que en transporte.",
            "## Conclusión", "Con problemas propios (café, bicicletas, leche y una red de transbordo) vimos que, "
            "si el modelo está bien planteado, Python, R y Solver llegan al mismo óptimo: la herramienta cambia la "
            "sintaxis, no la respuesta. Lo que más trabajo cuesta es pasar el enunciado a variables y restricciones."],
    "implicaciones": ["Modelar bien (nodos, arcos, balance) importa más que la herramienta elegida.",
                      "El modelo de red es más corto de escribir; el matricial es el que se presenta en clase."],
}

REFERENCIAS = [
    "Hillier, F. S. y Lieberman, G. J. (2021). Introduction to Operations Research (11.ª ed.). McGraw-Hill.",
    "Taha, H. A. (2017). Operations Research: An Introduction (10.ª ed., edición global). Pearson.",
    "Winston, W. L. (2004). Operations Research: Applications and Algorithms (4.ª ed.). Brooks/Cole.",
    "Mitchell, S., O'Sullivan, M. y Dunning, I. (2011). PuLP: A Linear Programming Toolkit for Python. University of Auckland. https://coin-or.github.io/pulp/ (este proyecto usa la serie 3.x)",
    "Virtanen, P. et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. Nature Methods, 17, 261–272. https://doi.org/10.1038/s41592-019-0686-2",
    "Huangfu, Q. y Hall, J. A. J. (2018). Parallelizing the dual revised simplex method. Mathematical Programming Computation, 10, 119–142. (HiGHS) https://doi.org/10.1007/s12532-017-0130-5",
    "Berkelaar, M. et al. (2024). lpSolve: Interface to 'Lp_solve' v. 5.5 to Solve Linear/Integer Programs. CRAN. https://CRAN.R-project.org/package=lpSolve",
    "Schumacher, D. (2023). ompr: Model and Solve Mixed Integer Linear Programs. CRAN. https://CRAN.R-project.org/package=ompr",
    "Microsoft (s. f.). Definir y resolver un problema con Solver. Soporte de Microsoft. https://support.microsoft.com/es-es/office/definir-y-resolver-un-problema-con-solver-5d1a388f-079d-43ac-a7eb-f63e45925040 (consultado 19/11/2026)",
    "Khurana, A. (2015). Variants of transshipment problem. European Transportation Research Review, 7, 11. https://doi.org/10.1007/s12544-015-0154-8",
]
