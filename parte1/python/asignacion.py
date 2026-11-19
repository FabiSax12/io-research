"""Asignación (PL): linear_sum_assignment (principal) y PuLP (verificación)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # preámbulo: para importar comun/

import numpy as np
import pulp
from scipy.optimize import linear_sum_assignment

from comun.utilidades import armar_resultado, emitir, leer_yaml

d = leer_yaml("asignacion")
agentes, tareas = list(d["agentes"]), list(d["tareas"])
matriz = [list(fila) for fila in d["matriz"]]
maximizar = d["sentido"] == "max"
assert len(matriz) == len(agentes) and all(len(f) == len(tareas) for f in matriz), "matriz mal dimensionada"

# --- Si no es cuadrada: filas o columnas ficticias con valor 0 ---
ajustes = []
sobran = len(tareas) - len(agentes)
for k in range(sobran):                                   # más tareas que agentes
    agentes.append(f"Ficticio {k + 1}"); matriz.append([0] * len(tareas))
for k in range(-sobran):                                  # más agentes que tareas
    tareas.append(f"Ficticio {k + 1}")
    for fila in matriz:
        fila.append(0)
if sobran:
    k, cosa = abs(sobran), ("agente ficticio" if sobran > 0 else "tarea ficticia")
    ajustes.append(f"Matriz {len(d['agentes'])}x{len(d['tareas'])} no cuadrada: se "
                   + (f"agregó 1 {cosa} (Ficticio 1)" if k == 1 else f"agregaron {k} {cosa.replace(' ', 's ')}s (Ficticio 1 a {k})")
                   + " con valor 0; quien queda asignado ahí no recibe trabajo")

# --- Método húngaro de SciPy ---
costo = np.array(matriz, dtype=float)
filas_opt, cols_opt = linear_sum_assignment(costo, maximize=maximizar)
valor = costo[filas_opt, cols_opt].sum()
asignado = set(zip(filas_opt.tolist(), cols_opt.tolist()))

# --- Verificación: modelo de PL con variables binarias en PuLP ---
n = len(agentes)
modelo = pulp.LpProblem("Asignacion", pulp.LpMaximize if maximizar else pulp.LpMinimize)
x = {(i, j): pulp.LpVariable(f"x{i}_{j}", cat="Binary") for i in range(n) for j in range(n)}
modelo += pulp.lpSum(matriz[i][j] * x[i, j] for i, j in x)
for i in range(n):
    modelo += pulp.lpSum(x[i, j] for j in range(n)) == 1   # cada agente hace una tarea
for j in range(n):
    modelo += pulp.lpSum(x[i, j] for i in range(n)) == 1   # cada tarea la hace un agente
modelo.solve(pulp.PULP_CBC_CMD(msg=False))
valor_pulp = pulp.value(modelo.objective)

res = armar_resultado("asignacion", "Optimal", valor,
                      {f"{agentes[i]}->{tareas[j]}": int((i, j) in asignado) for i in range(n) for j in range(n)},
                      ajustes, {"metodo": "PuLP (binarias)", "valor": valor_pulp, "coincide": abs(valor - valor_pulp) < 1e-6})
filas = [[agentes[i], tareas[j] if "Ficticio" not in tareas[j] else "(sin tarea)", matriz[i][j]]
         for i, j in sorted(asignado) if "Ficticio" not in agentes[i]]
filas.append(["Total", "", res["valor_objetivo"]])
emitir(res, d["nombre"], ["Agente", "Tarea", "Valor"], filas)
