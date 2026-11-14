"""Transbordo: (1) modelo de red con conservación de flujo y (2) modelo matricial con buffer.

Uso:  python parte2/python/transbordo.py [nombre_del_yaml]     (por defecto: transbordo)
Si oferta != demanda agrega un nodo ficticio. Genera además la matriz ampliada
(CSV + PNG), el diagrama de la red y el archivo de Excel para Solver.
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # preámbulo: para importar comun/

import matplotlib
import networkx as nx
import pulp
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter as col

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from comun.utilidades import armar_resultado, emitir, fmt, leer_yaml, ruta_salida, tabla_png  # noqa: E402

nombre = sys.argv[1] if len(sys.argv) > 1 else "transbordo"
d = leer_yaml(nombre)

# ---------------------------------------------------------------- 1. Datos
tipo = {n["nombre"]: n["tipo"] for n in d["nodos"]}
oferta = {n["nombre"]: n.get("oferta", 0) for n in d["nodos"]}
demanda = {n["nombre"]: n.get("demanda", 0) for n in d["nodos"]}
costo = {(a["desde"], a["hasta"]): a["costo"] for a in d["arcos"]}
assert all(a in tipo and b in tipo for a, b in costo), "hay arcos con nodos que no están en 'nodos'"

# ---------------------------------------------------------------- 2. Balanceo (oferta vs demanda)
ajustes = []
dif = sum(oferta.values()) - sum(demanda.values())
origenes = [k for k in tipo if tipo[k] == "origen"]
destinos = [k for k in tipo if tipo[k] == "destino"]
if dif > 1e-9:                      # sobra oferta: destino ficticio que recibe el excedente
    tipo["Ficticio"], oferta["Ficticio"], demanda["Ficticio"] = "destino", 0, dif
    costo.update({(o, "Ficticio"): 0 for o in origenes})
    ajustes.append(f"Oferta ({sum(oferta.values())}) > demanda ({sum(demanda.values()) - dif}): "
                   f"se agregó el nodo destino Ficticio con demanda {dif} y arcos de costo 0 desde cada origen")
elif dif < -1e-9:                   # falta oferta: origen ficticio que cubre el faltante
    tipo["Ficticio"], oferta["Ficticio"], demanda["Ficticio"] = "origen", -dif, 0
    costo.update({("Ficticio", t): 0 for t in destinos})
    ajustes.append(f"Demanda ({sum(demanda.values())}) > oferta ({sum(oferta.values()) + dif}): "
                   f"se agregó el nodo origen Ficticio con oferta {-dif} y arcos de costo 0 hacia cada destino")
ORDEN = {"origen": 0, "transbordo": 1, "destino": 2}
nodos = sorted(tipo, key=lambda k: ORDEN[tipo[k]])     # orígenes, transbordos, destinos
n = len(nodos)

# ---------------------------------------------------------------- 3. Modelo de red (conservación de flujo)
red = pulp.LpProblem("Transbordo_red", pulp.LpMinimize)
flujo = {a: pulp.LpVariable(f"f{i}", lowBound=0) for i, a in enumerate(costo)}
red += pulp.lpSum(costo[a] * flujo[a] for a in costo)
for k in nodos:                     # sale - entra = oferta - demanda
    sale = pulp.lpSum(flujo[a] for a in costo if a[0] == k)
    entra = pulp.lpSum(flujo[a] for a in costo if a[1] == k)
    red += sale - entra == oferta[k] - demanda[k]
red.solve(pulp.PULP_CBC_CMD(msg=False))
estado = pulp.LpStatus[red.status]
valor_red = pulp.value(red.objective) if estado == "Optimal" else None

# ---------------------------------------------------------------- 4. Modelo matricial con buffer
B = max(sum(oferta.values()), sum(demanda.values()))             # buffer = flujo total
cota = B * (n - 1) * max(costo.values())                         # ningún plan sin M cuesta más que esto
M = 10 ** len(str(int(cota)))                                    # potencia de 10 mayor que cota
C = [[0 if i == j else costo.get((i, j), M) for j in nodos] for i in nodos]
oferta_amp = [oferta[k] + B for k in nodos]                      # fila: oferta + B
demanda_amp = [demanda[k] + B for k in nodos]                    # columna: demanda + B

buf = pulp.LpProblem("Transbordo_buffer", pulp.LpMinimize)
x = {(i, j): pulp.LpVariable(f"x{i}_{j}", lowBound=0) for i in range(n) for j in range(n)}
buf += pulp.lpSum(C[i][j] * x[i, j] for i, j in x)
for i in range(n):
    buf += pulp.lpSum(x[i, j] for j in range(n)) == oferta_amp[i]
for j in range(n):
    buf += pulp.lpSum(x[i, j] for i in range(n)) == demanda_amp[j]
buf.solve(pulp.PULP_CBC_CMD(msg=False))
valor_buf = pulp.value(buf.objective) if pulp.LpStatus[buf.status] == "Optimal" else None
if valor_buf is not None and valor_buf >= M:                     # usó un arco inexistente: no hay plan factible
    estado, valor_buf = "Infeasible", None

coincide = valor_red is not None and valor_buf is not None and abs(valor_red - valor_buf) < 1e-6

# ---------------------------------------------------------------- 5. Resultado (JSON, consola, tabla PNG)
res = armar_resultado(nombre, estado, valor_red, {f"{a}->{b}": flujo[a, b].value() for a, b in costo}, ajustes,
                      {"metodo": "transporte con buffer", "valor": valor_buf, "coincide": coincide},
                      buffer={"B": B, "M": M})
print(f"Buffer B = {fmt(B)}, M = {fmt(M)}")
print(f"Modelo de red: {fmt(valor_red) if valor_red is not None else 'n/d'} | "
      f"Modelo con buffer: {fmt(valor_buf) if valor_buf is not None else 'n/d'}")
filas = [[f"{a} -> {b}", costo[a, b], res["variables"][f"{a}->{b}"]] for a, b in costo if flujo[a, b].value() > 1e-9]
filas.append(["Costo total", "", res["valor_objetivo"]])
emitir(res, d["nombre"], ["Arco", "Costo unitario", "Flujo"], filas)

# ---------------------------------------------------------------- 6. Matriz ampliada (CSV + PNG)
encabezado = ["De / A"] + nodos + ["Oferta"]
cuerpo = [[nodos[i]] + ["M" if C[i][j] == M else fmt(C[i][j]) for j in range(n)] + [fmt(oferta_amp[i])] for i in range(n)]
cuerpo.append(["Demanda"] + [fmt(v) for v in demanda_amp] + [""])
with open(ruta_salida("capturas", f"{nombre}_matriz_python.csv"), "w", newline="", encoding="utf-8-sig") as f:
    csv.writer(f).writerows([encabezado] + cuerpo)
tabla_png(ruta_salida("capturas", f"{nombre}_matriz_python.png"),
          f"Matriz de costos ampliada (B = {fmt(B)}, M = {fmt(M)})", encabezado, cuerpo)

# ---------------------------------------------------------------- 7. Diagrama de la red (columnas por tipo)
G = nx.DiGraph(list(costo))
pos = {}
for t, columna in ORDEN.items():
    grupo = [k for k in nodos if tipo[k] == t]
    for i, k in enumerate(grupo):
        pos[k] = (columna * 3, (len(grupo) - 1) / 2 - i)
colores = {"origen": "#9ecae1", "transbordo": "#fdd49e", "destino": "#a1d99b"}
usados = [a for a in costo if flujo[a].value() > 1e-9]
fig, ax = plt.subplots(figsize=(10, 6))
nx.draw_networkx_nodes(G, pos, node_color=["#d9d9d9" if k == "Ficticio" else colores[tipo[k]] for k in G],
                       node_size=1800, edgecolors="black", ax=ax)
nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
estilo = dict(node_size=1800, arrowsize=15, connectionstyle="arc3,rad=0.12", ax=ax)
nx.draw_networkx_edges(G, pos, edgelist=[a for a in costo if a not in usados], edge_color="#999999", **estilo)
nx.draw_networkx_edges(G, pos, edgelist=usados, edge_color="#d62728", width=2.2, **estilo)
etiquetas = {a: f"{fmt(costo[a])}" + (f"  [{fmt(flujo[a].value())}]" if a in usados else "") for a in costo}
nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_size=8, label_pos=0.35, rotate=False,
                             connectionstyle="arc3,rad=0.12", ax=ax, bbox=dict(fc="white", ec="none", alpha=0.8))
for t, columna in ORDEN.items():
    ax.text(columna * 3, max(y for _, y in pos.values()) + 0.8, {"origen": "Orígenes", "transbordo": "Transbordo", "destino": "Destinos"}[t],
            ha="center", fontweight="bold")
ax.set_title(f"{d['nombre']}: costo por arco (rojo = arco usado, [flujo])", fontsize=11)
ax.axis("off")
fig.savefig(ruta_salida("capturas", f"{nombre}_red.png"), dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------------------------------------------------------------- 8. Excel para Solver (el paso de Solver es manual)
wb = Workbook()
ws = wb.active
ws.title = "Modelo"
negrita, azul = Font(bold=True), PatternFill("solid", fgColor="DBE7F5")
ws["A1"], ws["A1"].font = "Transbordo como problema de transporte con buffer", Font(bold=True, size=13)
ws["A2"], ws["B2"] = "B (buffer)", B
ws["A3"], ws["B3"] = "M (arco inexistente)", M

f_cost = 5                                                        # fila del encabezado de costos
ws.cell(f_cost, 1, "MATRIZ DE COSTOS").font = negrita
for j, k in enumerate(nodos):
    ws.cell(f_cost, 2 + j, k).font = negrita
    ws.cell(f_cost, 2 + j).fill = azul
for i, k in enumerate(nodos):
    ws.cell(f_cost + 1 + i, 1, k).font = negrita
    for j in range(n):
        ws.cell(f_cost + 1 + i, 2 + j, "=$B$3" if C[i][j] == M else C[i][j])
r_cost = f"B{f_cost + 1}:{col(n + 1)}{f_cost + n}"

f_dec = f_cost + n + 3                                            # fila del encabezado de decisión
ws.cell(f_dec, 1, "CELDAS DE DECISIÓN (variables de Solver)").font = negrita
for j, k in enumerate(nodos):
    ws.cell(f_dec + 1, 2 + j, k).font = negrita
    ws.cell(f_dec + 1, 2 + j).fill = azul
ws.cell(f_dec + 1, n + 2, "Suma fila").font = negrita
ws.cell(f_dec + 1, n + 3, "Oferta").font = negrita
for i, k in enumerate(nodos):
    fila = f_dec + 2 + i
    ws.cell(fila, 1, k).font = negrita
    for j in range(n):
        ws.cell(fila, 2 + j, 0).fill = PatternFill("solid", fgColor="FFF2CC")
    ws.cell(fila, n + 2, f"=SUM(B{fila}:{col(n + 1)}{fila})")
    ws.cell(fila, n + 3, oferta_amp[i])
f_sum, f_dem = f_dec + 2 + n, f_dec + 3 + n
ws.cell(f_sum, 1, "Suma columna").font = negrita
ws.cell(f_dem, 1, "Demanda").font = negrita
for j in range(n):
    ws.cell(f_sum, 2 + j, f"=SUM({col(2 + j)}{f_dec + 2}:{col(2 + j)}{f_dec + 1 + n})")
    ws.cell(f_dem, 2 + j, demanda_amp[j])
r_dec = f"B{f_dec + 2}:{col(n + 1)}{f_dec + 1 + n}"
c_total = f"B{f_dem + 2}"
ws.cell(f_dem + 2, 1, "COSTO TOTAL").font = negrita
ws[c_total] = f"=SUMPRODUCT({r_cost},{r_dec})"
ws[c_total].font = negrita
ws.column_dimensions["A"].width = 24
for j in range(2, n + 4):
    ws.column_dimensions[col(j)].width = 12


def absoluto(rango):  # B7:F9 -> Modelo!$B$7:$F$9
    return "Modelo!" + re.sub(r"([A-Z]+)(\d+)", r"$\1$\2", rango)


r_suma_fila = f"{col(n + 2)}{f_dec + 2}:{col(n + 2)}{f_dec + 1 + n}"
r_oferta = f"{col(n + 3)}{f_dec + 2}:{col(n + 3)}{f_dec + 1 + n}"
r_suma_col = f"B{f_sum}:{col(n + 1)}{f_sum}"
r_demanda = f"B{f_dem}:{col(n + 1)}{f_dem}"
ins = wb.create_sheet("Instrucciones")
lineas = [
    ("PARÁMETROS DE SOLVER (Datos > Solver)", True),
    ("", False),
    (f"1. Establecer objetivo: {absoluto(c_total)}", False),
    ("2. Para: Mín", False),
    (f"3. Cambiando las celdas de variables: {absoluto(r_dec)}", False),
    ("4. Sujeto a las restricciones (botón Agregar):", False),
    (f"     {absoluto(r_suma_fila)} = {absoluto(r_oferta)}      (suma de cada fila = oferta)", False),
    (f"     {absoluto(r_suma_col)} = {absoluto(r_demanda)}      (suma de cada columna = demanda)", False),
    ("5. Marcar 'Convertir variables sin restricciones en no negativas' (no negatividad).", False),
    ("6. Método de resolución: Simplex LP.", False),
    ("7. Resolver y conservar la solución.", False),
    ("", False),
    ("CÓMO LEER EL RESULTADO", True),
    ("- Celdas fuera de la diagonal con valor > 0: unidades enviadas por ese arco.", False),
    ("- Diagonal: buffer sin usar (no es un envío real).", False),
    (f"- Si el costo total es >= M ({fmt(M)}), el plan usa un arco inexistente: revisar los datos.", False),
    (f"- Valor óptimo esperado (calculado con Python): {fmt(valor_buf) if valor_buf is not None else 'n/d'}", False),
    ("", False),
    ("AJUSTES DE BALANCEO", True),
] + [(a, False) for a in ajustes or ["Sin ajustes: oferta = demanda."]] + [
    ("", False),
    ("Nota: si Solver no aparece, activarlo en Archivo > Opciones > Complementos > Solver.", False),
    ("Guardar la versión resuelta con otro nombre para no perderla si se vuelve a generar este archivo.", False),
]
for i, (texto, titulo) in enumerate(lineas, start=1):
    ins.cell(i, 1, texto).font = Font(bold=titulo)
ins.column_dimensions["A"].width = 110
wb.save(ruta_salida("parte2/solver", f"{nombre}.xlsx"))
print(f"Archivos: capturas/{nombre}_matriz_python.csv/.png, capturas/{nombre}_red.png, parte2/solver/{nombre}.xlsx")
