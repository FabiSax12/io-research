"""Problema de transporte con PuLP. Si oferta != demanda agrega un nodo ficticio de costo 0."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # preámbulo: para importar comun/

import pulp

from comun.utilidades import armar_resultado, emitir, leer_yaml

d = leer_yaml("transporte")
origenes, destinos = list(d["origenes"]), list(d["destinos"])
oferta, demanda = list(d["oferta"]), list(d["demanda"])
costo = [list(fila) for fila in d["costos"]]
assert len(costo) == len(origenes) and all(len(f) == len(destinos) for f in costo), "matriz de costos mal dimensionada"
assert len(oferta) == len(origenes) and len(demanda) == len(destinos), "oferta/demanda mal dimensionadas"

# --- Balanceo: el exceso se absorbe con un nodo ficticio de costo 0 ---
ajustes = []
dif = sum(oferta) - sum(demanda)
if dif > 1e-9:
    destinos.append("Ficticio"); demanda.append(dif)
    for fila in costo:
        fila.append(0)
    ajustes.append(f"Oferta ({sum(oferta)}) > demanda ({sum(demanda) - dif}): se agregó el destino ficticio con demanda {dif} y costo 0")
elif dif < -1e-9:
    origenes.append("Ficticio"); oferta.append(-dif)
    costo.append([0] * len(destinos))
    ajustes.append(f"Demanda ({sum(demanda)}) > oferta ({sum(oferta) + dif}): se agregó el origen ficticio con oferta {-dif} y costo 0")

# --- Modelo en PuLP ---
m, n = len(origenes), len(destinos)
modelo = pulp.LpProblem("Transporte", pulp.LpMinimize)
x = {(i, j): pulp.LpVariable(f"x{i}_{j}", lowBound=0) for i in range(m) for j in range(n)}
modelo += pulp.lpSum(costo[i][j] * x[i, j] for i, j in x)
for i in range(m):
    modelo += pulp.lpSum(x[i, j] for j in range(n)) == oferta[i]     # se despacha toda la oferta
for j in range(n):
    modelo += pulp.lpSum(x[i, j] for i in range(m)) == demanda[j]    # se cubre toda la demanda
modelo.solve(pulp.PULP_CBC_CMD(msg=False))

estado = pulp.LpStatus[modelo.status]
valor = pulp.value(modelo.objective) if estado == "Optimal" else None
envios = {f"{origenes[i]}->{destinos[j]}": x[i, j].value() for i, j in x}

res = armar_resultado("transporte", estado, valor, envios, ajustes)
filas = [[origenes[i]] + [res["variables"][f"{origenes[i]}->{destinos[j]}"] for j in range(n)] + [oferta[i]] for i in range(m)]
filas.append(["Demanda"] + demanda + [sum(demanda)])
emitir(res, d["nombre"], ["Envíos"] + destinos + ["Oferta"], filas)
