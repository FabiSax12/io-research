"""Textos de la presentación. Editar aquí; el diseño vive en tema.py y el armado en construir.py.

Convenciones:
- "{clave}" se reemplaza con un número calculado de resultados/ o de los gráficos (ver construir.valores()).
- Un párrafo que empieza con "## " sale en negrita (subtítulo dentro de una columna).
- "[completar: ...]" marca texto que el equipo debe escribir o confirmar antes de exponer.
"""

CURSO = "Investigación de Operaciones"
SEMESTRE = "II Semestre 2026"
INSTITUCION = ("Instituto", "Tecnológico", "de Costa Rica")     # la palabra del medio va en negrita
PROFESOR = "[completar: nombre del profesor]"
FECHA_DEFENSA = "Defensa: 19 o 20 de noviembre de 2026, por Zoom"

# Resultados de Excel Solver: escribir el valor óptimo que dio Solver al terminar el paso manual.
# None = todavía no se corrió (la lámina muestra un marcador y el gráfico una barra rayada).
SOLVER = {"transbordo": None, "transbordo_desbalanceado": None}

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
        "fuente": "Elaboración propia a partir de datos/*.yaml y de los modelos que arman los scripts del repositorio.",
        "implicaciones": [
            "Todos cumplen el mínimo de 3 restricciones que pide el enunciado.",
            "El balanceo (nodos ficticios) agrega variables: hay que contarlas al explicar el modelo.",
        ],
    },
}

# ------------------------------------------------------------------ herramientas (tabla de valoración)
# valor y previo van de -3 a +3: valoración del equipo para este curso (facilidad + cobertura de los 4 tipos).
# previo = lo que esperábamos antes de probarla (punto negro). Ajustar a la experiencia real del equipo.
HERRAMIENTAS = {
    "titular": "Librerías que investigamos",
    "leyenda": "Valoración del equipo para los problemas del curso, de -3 a +3",
    "filas": [
        ("PuLP", "Python", 2, 1, "Modelado algebraico legible; trae CBC. Cubre PL, PLE, transporte y asignación. Es nuestra opción principal en Python."),
        ("SciPy (optimize)", "Python", 1, 1, "linprog y milp (HiGHS) usan matrices; linear_sum_assignment resuelve asignación directa. La usamos para verificar."),
        ("OR-Tools", "Python", 1, 2, "Muy completa (LP, MIP, flujo de costo mínimo), pero más verbosa para modelos de clase."),
        ("Pyomo", "Python", 0, 1, "Potente para modelos grandes; requiere instalar un solver aparte. Excesiva para este trabajo."),
        ("lpSolve", "R", 2, 1, "lp(), lp.transport() y lp.assign() resuelven los cuatro tipos con una llamada cada uno."),
        ("ompr + ROI", "R", 0, 0, "Sintaxis algebraica tipo PuLP en R, pero con más dependencias que instalar."),
        ("Excel Solver", "Excel", 1, 0, "Simplex LP integrado; útil para mostrar la matriz. Límite de 200 celdas variables."),
    ],
    "lectura": "PuLP y lpSolve resuelven los cuatro tipos de problema con poco código; SciPy sirve como verificación independiente.",
    "fuente": "Valoración cualitativa del equipo [completar: confirmar con la experiencia de cada integrante]. "
              "Documentación oficial de cada librería (ver referencias).",
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
        "izq": ["## Problema", "{pl_nombre}. [completar: enunciado en una o dos oraciones.]",
                "## Modelo", "{pl_modelo}"],
        "der": ["## Librerías", "Python: PuLP (CBC) y SciPy linprog para verificar. R: lpSolve::lp().",
                "## Resultado", "Z = {pl_optimo} con {pl_solucion}."],
        "exhibicion": {
            "titulo": "Región factible y solución óptima",
            "subtitulo": "Restricciones del modelo y recta de nivel de Z en el óptimo",
            "lectura": "el óptimo está en el vértice ({pl_x1}, {pl_x2}), donde se cruzan dos restricciones activas; Z = {pl_optimo}.",
            "fuente": "Elaboración propia con PuLP 3 (CBC) y SciPy linprog sobre datos/pl.yaml.",
            "implicaciones": ["La línea discontinua es la función objetivo en su mejor valor posible.",
                              "Las restricciones que no tocan el vértice tienen holgura."],
        },
        "codigo": [("parte1/python/pl.py", "--- Modelo en PuLP", "--- Verificación"), ("parte1/r/pl.R", None, None)],
    },
    "ple": {
        "titular": "Programación lineal entera",
        "izq": ["## Problema", "{ple_nombre}. [completar: enunciado.]", "## Modelo", "{ple_modelo}"],
        "der": ["## Librerías", "Python: PuLP con cat=\"Integer\" (ramificación y acotamiento en CBC) y SciPy milp. "
                "R: lpSolve::lp() con int.vec.",
                "## Resultado", "Z = {ple_optimo} con {ple_solucion}."],
        "exhibicion": {
            "titulo": "Óptimo entero frente a la relajación lineal",
            "subtitulo": "Valor de Z sin y con la condición de integralidad",
            "lectura": "exigir enteros baja Z de {ple_cota} a {ple_optimo} ({ple_brecha} % menos); la relajación es una cota.",
            "fuente": "Elaboración propia con PuLP 3 (CBC) y SciPy milp/linprog sobre datos/ple.yaml. La barra rayada es una cota, no una solución factible.",
            "implicaciones": ["Redondear la solución de PL no garantiza el óptimo entero.",
                              "La brecha mide cuánto cuesta la integralidad."],
        },
        "codigo": [("parte1/python/ple.py", "--- Modelo en PuLP", "--- Verificación"), ("parte1/r/ple.R", None, None)],
    },
    "transporte": {
        "titular": "Problema de transporte",
        "izq": ["## Problema", "{tr_nombre}. Oferta total {tr_oferta}, demanda total {tr_demanda}.",
                "## Modelo", "min Σ c_ij x_ij, con Σ_j x_ij = oferta_i, Σ_i x_ij = demanda_j y x_ij ≥ 0."],
        "der": ["## Balanceo", "{tr_ajuste}",
                "## Librerías", "Python: PuLP. R: lpSolve::lp.transport().",
                "## Resultado", "Costo mínimo = {tr_optimo}."],
        "exhibicion": {
            "titulo": "Uso de la oferta por planta",
            "subtitulo": "Unidades enviadas a clientes y asignadas al destino ficticio, por origen",
            "lectura": "{tr_lectura}",
            "fuente": "Elaboración propia con PuLP 3 sobre datos/transporte.yaml.",
            "implicaciones": ["Lo que va al ficticio es oferta que se queda en la planta.",
                              "El ficticio tiene costo 0, así que no altera el costo total."],
        },
        "codigo": [("parte1/python/transporte.py", "--- Modelo en PuLP", None), ("parte1/r/transporte.R", "--- Modelo:", None)],
    },
    "asignacion": {
        "titular": "Problema de asignación",
        "izq": ["## Problema", "{as_nombre}. Matriz de {as_dim} ({as_sentido}).",
                "## Modelo", "x_ij ∈ {{0,1}}; cada agente hace a lo sumo una tarea y cada tarea la hace un agente. "
                "Como PL, la matriz es totalmente unimodular y el óptimo sale entero."],
        "der": ["## Ajuste", "{as_ajuste}",
                "## Librerías", "Python: PuLP (y verificación con variables binarias). R: lpSolve::lp.assign().",
                "## Resultado", "Valor óptimo = {as_optimo}."],
        "exhibicion": {
            "titulo": "Asignación óptima por agente",
            "subtitulo": "Valor de la tarea asignada y mínimo de cada fila de la matriz",
            "lectura": "{as_lectura}",
            "fuente": "Elaboración propia con PuLP 3 sobre datos/asignacion.yaml.",
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
            "## Pendiente", "[completar: correr Rscript (R 4.2+) y Solver, y actualizar contenido.SOLVER.]"],
    "exhibicion": {
        "titulo": "Valor óptimo relativo al de Python",
        "subtitulo": "Índice, Python = 100, por problema y herramienta",
        "lectura": "{comparacion_lectura}",
        "fuente": "Elaboración propia con run_all.py (resultados/*.json). Barras rayadas: resultado aún no generado.",
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
    "autor": "Paráfrasis de Taha (2017), cap. 5",
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
        "fuente": "Elaboración propia con PuLP 3 sobre datos/transbordo.yaml.",
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
         "Se convierte en transporte agregando un buffer B a filas y columnas (Taha, 2017)"),
    ],
    "lectura": "todo problema de transbordo se puede resolver como uno de transporte; la diferencia está en armar la matriz.",
    "fuente": "Taha (2017), cap. 5; Hillier y Lieberman (2021), cap. 9; Winston (2004), sec. 7.6.",
}

EJEMPLO = {
    "titular": "Nuestro ejemplo de transbordo",
    "izq": ["## Enunciado", "{tb_nombre}. [completar: contexto del ejemplo.]",
            "## Nodos", "{tb_nodos}"],
    "der": ["## Arcos", "{tb_narcos} rutas posibles con costo unitario; las que no existen no se pueden usar (costo M en la matriz).",
            "## Resultado", "Costo mínimo = {tb_optimo}. Flujo por los nodos de transbordo: {tb_via} unidades."],
    "exhibicion": {
        "titulo": "Red del ejemplo y flujo óptimo",
        "subtitulo": "Costo unitario por arco; [flujo] en los arcos usados (unidades)",
        "lectura": "todo el flujo pasa por T1 o T2; el arco directo P1→D1 (costo 12) queda sin usar.",
        "fuente": "Elaboración propia con PuLP 3 sobre datos/transbordo.yaml; la red la dibuja graficos.py.",
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
        "fuente": "Elaboración propia: capturas/transbordo_matriz_python.png generada por parte2/python/transbordo.py.",
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
        "subtitulo": "Captura de la hoja resuelta (capturas/transbordo_solver.png)",
        "lectura": "{solver_lectura}",
        "fuente": "Elaboración propia con Excel Solver (Simplex LP) sobre parte2/solver/transbordo.xlsx.",
        "implicaciones": ["Solver no se automatiza: se corre a mano y se guarda la captura.",
                          "Guardar el libro resuelto con otro nombre; el script sobrescribe transbordo.xlsx."],
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
    "fuente": "Elaboración propia: modelo de red resuelto con SciPy linprog (datos.py) sobre datos/transbordo.yaml; Taha (2017), cap. 5.",
}

DESBALANCEADO = {
    "titular": "Cómo se resuelve el caso desbalanceado",
    "izq": ["## Sobra oferta", "Se agrega un destino ficticio. Lo que recibe es oferta que no sale del origen.",
            "## Falta oferta", "Se agrega un origen ficticio. Lo que envía es demanda que queda sin atender; "
            "si eso tiene un costo (penalización), se usa en lugar de 0."],
    "der": ["## En la matriz", "El ficticio es una fila o columna más; B se calcula con el total ya balanceado.",
            "## Nuestro caso", "{desb_ajuste} Costo = {desb_optimo}."],
    "exhibicion": {
        "titulo": "Costo óptimo según la oferta disponible",
        "subtitulo": "Costo total al variar la oferta de {curva_nodo}; demanda fija de {curva_bal} unidades",
        "lectura": "con oferta de sobra el costo no cambia ({curva_costo}); si falta, baja solo porque se envía menos, no porque la red sea más barata.",
        "fuente": "Elaboración propia: modelo de red con nodo ficticio resuelto con SciPy linprog (datos.py) sobre datos/transbordo.yaml.",
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
            "[completar: conclusión propia del equipo.]"],
    "implicaciones": ["Modelar bien (nodos, arcos, balance) importa más que la herramienta elegida.",
                      "El modelo de red es más corto de escribir; el matricial es el que se presenta en clase."],
}

MINUTAS = {
    "titular": "Minutas y cronograma",
    "nota": "Minutas completas en la carpeta de archivos del subgrupo en Teams (minutas/*.md en el repositorio).",
}

REFERENCIAS = [
    "Hillier, F. S. y Lieberman, G. J. (2021). Introduction to Operations Research (11.ª ed.). McGraw-Hill.",
    "Taha, H. A. (2017). Operations Research: An Introduction (10.ª ed.). Pearson.",
    "Winston, W. L. (2004). Operations Research: Applications and Algorithms (4.ª ed.). Brooks/Cole.",
    "Mitchell, S., O'Sullivan, M. y Dunning, I. (2011). PuLP: A Linear Programming Toolkit for Python. University of Auckland. https://coin-or.github.io/pulp/",
    "Virtanen, P. et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. Nature Methods, 17, 261–272.",
    "Huangfu, Q. y Hall, J. A. J. (2018). Parallelizing the dual revised simplex method. Mathematical Programming Computation, 10, 119–142. (HiGHS)",
    "Berkelaar, M. et al. (2024). lpSolve: Interface to 'Lp_solve' v. 5.5 to Solve Linear/Integer Programs. CRAN. https://CRAN.R-project.org/package=lpSolve",
    "Schumacher, D. (2023). ompr: Model and Solve Mixed Integer Linear Programs. CRAN. https://CRAN.R-project.org/package=ompr",
    "Microsoft (s. f.). Definir y resolver un problema con Solver. Soporte de Microsoft Excel.",
    "[completar: otras fuentes consultadas por el equipo]",
]
