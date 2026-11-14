"""Programación lineal entera: PuLP (principal) y SciPy milp (verificación)."""
import operator
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # preámbulo: para importar comun/

import numpy as np
import pulp
from scipy.optimize import Bounds, LinearConstraint, milp

from comun.utilidades import armar_resultado, emitir, leer_yaml

d = leer_yaml("ple")
nombres, c, sentido, restr = d["variables"], d["objetivo"], d["sentido"], d["restricciones"]
enteras = d.get("enteras") or []
COMPARAR = {"<=": operator.le, ">=": operator.ge, "=": operator.eq}
assert len(c) == len(nombres), "objetivo debe tener un coeficiente por variable"

# --- Modelo en PuLP: igual que PL, pero las variables enteras llevan cat="Integer" ---
modelo = pulp.LpProblem("PLE", pulp.LpMaximize if sentido == "max" else pulp.LpMinimize)
x = {v: pulp.LpVariable(f"x{i}", lowBound=0, cat="Integer" if v in enteras else "Continuous")
     for i, v in enumerate(nombres)}
modelo += pulp.lpSum(ci * x[v] for ci, v in zip(c, nombres))
for r in restr:
    lado_izq = pulp.lpSum(a * x[v] for a, v in zip(r["coef"], nombres))
    modelo += COMPARAR[r["signo"]](lado_izq, r["rhs"])
modelo.solve(pulp.PULP_CBC_CMD(msg=False))

estado = pulp.LpStatus[modelo.status]
valor = pulp.value(modelo.objective) if estado == "Optimal" else None

# --- Verificación cruzada con SciPy milp (lb <= A x <= ub por restricción) ---
A = np.array([r["coef"] for r in restr], dtype=float)
lb = [r["rhs"] if r["signo"] in (">=", "=") else -np.inf for r in restr]
ub = [r["rhs"] if r["signo"] in ("<=", "=") else np.inf for r in restr]
k = -1 if sentido == "max" else 1                                      # milp solo minimiza
chk = milp(c=k * np.array(c, dtype=float), constraints=LinearConstraint(A, lb, ub),
           integrality=[1 if v in enteras else 0 for v in nombres], bounds=Bounds(0, np.inf))
valor_scipy = k * chk.fun if chk.success else None
coincide = valor is not None and valor_scipy is not None and abs(valor - valor_scipy) < 1e-6

res = armar_resultado("ple", estado, valor, {v: x[v].value() for v in nombres},
                      verificacion={"metodo": "scipy.optimize.milp", "valor": valor_scipy, "coincide": coincide})
filas = [[v, res["variables"][v]] for v in nombres] + [[f"Z óptimo ({sentido})", res["valor_objetivo"]]]
emitir(res, d["nombre"], ["Variable", "Valor"], filas)
