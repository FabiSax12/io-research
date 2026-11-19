"""Programación lineal: PuLP (principal) y SciPy linprog (verificación)."""
import operator
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # preámbulo: para importar comun/

import pulp
from scipy.optimize import linprog

from comun.utilidades import armar_resultado, emitir, fmt, leer_yaml, limpiar

d = leer_yaml("pl")
nombres, c, sentido, restr = d["variables"], d["objetivo"], d["sentido"], d["restricciones"]
COMPARAR = {"<=": operator.le, ">=": operator.ge, "=": operator.eq}
assert len(c) == len(nombres), "objetivo debe tener un coeficiente por variable"

# --- Modelo en PuLP ---
modelo = pulp.LpProblem("PL", pulp.LpMaximize if sentido == "max" else pulp.LpMinimize)
x = {v: pulp.LpVariable(f"x{i}", lowBound=0) for i, v in enumerate(nombres)}
modelo += pulp.lpSum(ci * x[v] for ci, v in zip(c, nombres))          # función objetivo
for r in restr:
    lado_izq = pulp.lpSum(a * x[v] for a, v in zip(r["coef"], nombres))
    modelo += COMPARAR[r["signo"]](lado_izq, r["rhs"])                # restricción
modelo.solve(pulp.PULP_CBC_CMD(msg=False))

estado = pulp.LpStatus[modelo.status]
valor = pulp.value(modelo.objective) if estado == "Optimal" else None
sombra = [rc.pi for rc in modelo.constraints.values()] if estado == "Optimal" else []  # precios sombra (duales)

# --- Verificación cruzada con SciPy linprog ---
A_ub, b_ub, A_eq, b_eq = [], [], [], []
for r in restr:
    if r["signo"] == "<=":
        A_ub.append(r["coef"]); b_ub.append(r["rhs"])
    elif r["signo"] == ">=":
        A_ub.append([-a for a in r["coef"]]); b_ub.append(-r["rhs"])   # >= se pasa a <= multiplicando por -1
    else:
        A_eq.append(r["coef"]); b_eq.append(r["rhs"])
k = -1 if sentido == "max" else 1                                      # linprog solo minimiza
chk = linprog([k * ci for ci in c], A_ub=A_ub or None, b_ub=b_ub or None,
              A_eq=A_eq or None, b_eq=b_eq or None)
valor_scipy = k * chk.fun if chk.success else None
coincide = valor is not None and valor_scipy is not None and abs(valor - valor_scipy) < 1e-6

res = armar_resultado("pl", estado, valor, {v: x[v].value() for v in nombres},
                      verificacion={"metodo": "scipy.optimize.linprog", "valor": valor_scipy, "coincide": coincide},
                      precios_sombra=[limpiar(y) for y in sombra])
filas = ([[v, res["variables"][v]] for v in nombres] + [[f"Z óptimo ({sentido})", res["valor_objetivo"]]]
         + [[f"Sombra: {r['nombre']}", y] for r, y in zip(restr, res["precios_sombra"])])
emitir(res, d["nombre"], ["Variable", "Valor"], filas)
for r, y in zip(restr, res["precios_sombra"]):
    print(f"Precio sombra ({r['nombre']}): {fmt(y)}")
