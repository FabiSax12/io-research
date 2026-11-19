"""Gráficos de la presentación (PNG) con el estilo del tema.

Cada función recibe la ruta de salida y devuelve un dict con los números que usa la lámina
(para escribir la "lectura del gráfico" a partir de los datos y no a mano).
El tamaño de la figura coincide con el espacio en la lámina (1 px de lámina = 1/96 in),
así que los tamaños de letra en pt equivalen a px * 0.75, igual que en el resto del tema.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle  # noqa: E402

import datos  # noqa: E402
from tema import AMARILLO, BERMELLON, GRIS_REJILLA, GRIS_VENTANA, NEGRO, ROSADO, SERIES, VERDE  # noqa: E402

FUENTES = Path(__file__).resolve().parent / "fuentes"
for ttf in FUENTES.glob("*.ttf"):
    font_manager.fontManager.addfont(str(ttf))

C = {k: "#" + v for k, v in dict(bermellon=BERMELLON, amarillo=AMARILLO, verde=VERDE, rosado=ROSADO,
                                   rejilla=GRIS_REJILLA, ventana=GRIS_VENTANA, negro=NEGRO).items()}
plt.rcParams.update({
    "font.family": "Onest", "font.size": 7.5, "text.color": "black", "axes.labelcolor": "black",
    "xtick.color": "black", "ytick.color": "black", "axes.edgecolor": "black", "axes.linewidth": 0.75,
    "hatch.color": "edge", "hatch.linewidth": 0.8, "savefig.dpi": 300,   # el rayado toma el color del borde
})
TAM_ETIQUETA = 7.5     # 10 px


def figura(w_px, h_px):
    fig, ax = plt.subplots(figsize=(w_px / 96, h_px / 96))
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color("black")
    ax.tick_params(length=0)
    return fig, ax


def rejilla_y(ax):
    ax.yaxis.grid(True, color=C["rejilla"], linewidth=0.6)
    ax.set_axisbelow(True)


def rejilla_x(ax):
    ax.xaxis.grid(True, color=C["rejilla"], linewidth=0.6)
    ax.set_axisbelow(True)


def leyenda(ax, **kw):
    ley = ax.legend(frameon=False, fontsize=TAM_ETIQUETA, loc=kw.pop("loc", "upper left"), ncol=kw.pop("ncol", 3),
                    handlelength=1.2, borderaxespad=0, **kw)
    return ley


def guardar(fig, ruta):
    fig.savefig(ruta, facecolor="white", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    return ruta


# ------------------------------------------------------------------ contexto: tamaño de cada modelo
def tamano_modelos(ruta, w=426, h=170):
    filas = datos.tamanos()
    fig, ax = figura(w, h)
    xs = range(len(filas))
    ax.bar([x - 0.2 for x in xs], [f[1] for f in filas], 0.38, color=SERIES[0], label="Variables")
    ax.bar([x + 0.2 for x in xs], [f[2] for f in filas], 0.38, color=SERIES[1], label="Restricciones")
    for x, f in zip(xs, filas):
        ax.text(x - 0.2, f[1], str(f[1]), ha="center", va="bottom", fontsize=TAM_ETIQUETA, fontweight="bold")
        ax.text(x + 0.2, f[2], str(f[2]), ha="center", va="bottom", fontsize=TAM_ETIQUETA, fontweight="bold")
    ax.set_xticks(list(xs), [f[0] for f in filas])
    rejilla_y(ax)
    ax.set_ylim(0, max(max(f[1], f[2]) for f in filas) * 1.25)
    leyenda(ax, loc="upper left")
    guardar(fig, ruta)
    mayor = max(filas, key=lambda f: f[1])
    return {"filas": filas, "mayor": mayor}


# ------------------------------------------------------------------ PL: región factible (solo 2 variables)
def region_pl(ruta, w=426, h=200):
    d = datos.yaml_de("pl")
    res = datos.resultado("pl")
    fig, ax = figura(w, h)
    if len(d["variables"]) != 2 or res is None or res["valor_objetivo"] is None:
        ax.text(0.5, 0.5, "La región factible se dibuja solo con 2 variables", ha="center", transform=ax.transAxes)
        guardar(fig, ruta)
        return {"optimo": None}
    x_opt = [res["variables"][v] for v in d["variables"]]
    lim = max(max(x_opt) * 1.8, 1)
    lim_x = lim_y = lim
    for r in d["restricciones"]:   # el gráfico abarca los cortes con los ejes
        a, b = r["coef"]
        if a > 0 and r["signo"] == "<=":
            lim_x = max(lim_x, min(r["rhs"] / a * 1.15, lim * 3))
        if b > 0 and r["signo"] == "<=":
            lim_y = max(lim_y, min(r["rhs"] / b * 1.15, lim * 3))
    # polígono factible por muestreo de la malla (sirve para cualquier combinación de signos)
    import numpy as np
    xs = np.linspace(0, lim_x, 400)
    ys = np.linspace(0, lim_y, 400)
    X, Y = np.meshgrid(xs, ys)
    ok = np.ones_like(X, dtype=bool)
    for r in d["restricciones"]:
        lhs = r["coef"][0] * X + r["coef"][1] * Y
        ok &= {"<=": lhs <= r["rhs"] + 1e-9, ">=": lhs >= r["rhs"] - 1e-9, "=": abs(lhs - r["rhs"]) < lim / 200}[r["signo"]]
    ax.contourf(X, Y, ok.astype(float), levels=[0.5, 1.5], colors=["#fff3f0"])
    colores = [SERIES[1], SERIES[2], SERIES[3], C["negro"]]
    for i, r in enumerate(d["restricciones"]):
        a, b = r["coef"]
        if abs(b) > 1e-12:
            ax.plot(xs, (r["rhs"] - a * xs) / b, color=colores[i % 4], linewidth=1.4, label=r["nombre"])
        else:
            ax.axvline(r["rhs"] / a, color=colores[i % 4], linewidth=1.4, label=r["nombre"])
    c1, c2 = d["objetivo"]
    if abs(c2) > 1e-12:   # recta de nivel de la función objetivo en el óptimo (escenario, línea discontinua)
        ax.plot(xs, (res["valor_objetivo"] - c1 * xs) / c2, color=SERIES[0], linewidth=1.4, linestyle="--",
                label=f"Z = {datos.fmt(res['valor_objetivo'])}")
    ax.plot(*x_opt, "o", color=SERIES[0], markersize=5, zorder=5)
    ax.annotate(f"Óptimo ({datos.fmt(x_opt[0])}, {datos.fmt(x_opt[1])})", x_opt, xytext=(6, 6),
                textcoords="offset points", fontsize=TAM_ETIQUETA, fontweight="bold")
    ax.set_xlim(0, lim_x)
    ax.set_ylim(0, lim_y)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel(d["variables"][0], fontsize=TAM_ETIQUETA)
    ax.set_ylabel(d["variables"][1], fontsize=TAM_ETIQUETA)
    rejilla_y(ax)
    leyenda(ax, loc="upper right", ncol=1)
    guardar(fig, ruta)
    return {"optimo": res["valor_objetivo"], "x": x_opt}


# ------------------------------------------------------------------ PLE: relajación lineal (cota, rayada) vs óptimo entero
def relajacion_ple(ruta, w=426, h=170):
    cota, _ = datos.relajacion_ple()
    res = datos.resultado("ple")
    entero = res["valor_objetivo"] if res else None
    fig, ax = figura(w, h)
    ax.barh([1], [cota or 0], 0.55, color="white", edgecolor=SERIES[0], hatch="////", linewidth=0.8,
            label="Relajación lineal (cota)")
    ax.barh([0], [entero or 0], 0.55, color=SERIES[0], label="Óptimo entero (PuLP)")
    for yv, val in ((1, cota), (0, entero)):
        ax.text((val or 0), yv, f"  {datos.fmt(val)}", va="center", fontsize=9, fontweight="bold")
    ax.set_yticks([0, 1], ["Entero", "Relajación PL"])
    ax.axvline(0, color="black", linewidth=1)
    rejilla_x(ax)
    ax.set_xlim(0, max(cota or 1, entero or 1) * 1.25)
    ax.spines["bottom"].set_visible(False)
    leyenda(ax, loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2)
    guardar(fig, ruta)
    brecha = None if not (cota and entero) else abs(cota - entero) / abs(cota) * 100
    return {"cota": cota, "entero": entero, "brecha": brecha}


# ------------------------------------------------------------------ PLE: región factible con los puntos enteros
def region_ple(ruta, w=426, h=200):
    """Región de la relajación, puntos enteros factibles, óptimo entero, relajación y el redondeo (no factible)."""
    import math
    import numpy as np
    d = datos.yaml_de("ple")
    cota, x_rel = datos.relajacion_ple()
    res = datos.resultado("ple")
    entero = res["valor_objetivo"] if res else None
    brecha = None if not (cota and entero) else abs(cota - entero) / abs(cota) * 100
    fig, ax = figura(w, h)
    if len(d["variables"]) != 2 or res is None or x_rel is None:
        ax.text(0.5, 0.5, "La región se dibuja solo con 2 variables", ha="center", transform=ax.transAxes)
        guardar(fig, ruta)
        return {"cota": cota, "entero": entero, "brecha": brecha}
    x_ent = [res["variables"][v] for v in d["variables"]]
    factible = lambda p: all({"<=": sum(a * q for a, q in zip(r["coef"], p)) <= r["rhs"] + 1e-9,
                              ">=": sum(a * q for a, q in zip(r["coef"], p)) >= r["rhs"] - 1e-9,
                              "=": abs(sum(a * q for a, q in zip(r["coef"], p)) - r["rhs"]) < 1e-9}[r["signo"]]
                             for r in d["restricciones"]) and min(p) >= 0
    lim_x, lim_y = math.ceil(max(x_rel[0], x_ent[0]) * 1.5) + 1, math.ceil(max(x_rel[1], x_ent[1]) * 1.3) + 1
    xs = np.linspace(0, lim_x, 400)
    X, Y = np.meshgrid(xs, np.linspace(0, lim_y, 400))
    ok = np.ones_like(X, dtype=bool)
    for r in d["restricciones"]:
        lhs = r["coef"][0] * X + r["coef"][1] * Y
        ok &= {"<=": lhs <= r["rhs"] + 1e-9, ">=": lhs >= r["rhs"] - 1e-9, "=": abs(lhs - r["rhs"]) < 0.05}[r["signo"]]
    ax.contourf(X, Y, ok.astype(float), levels=[0.5, 1.5], colors=["#fff3f0"])
    colores = [SERIES[1], SERIES[2], SERIES[3], C["negro"]]
    for i, r in enumerate(d["restricciones"]):
        a, b = r["coef"]
        estilo = dict(color=colores[i % 4], linewidth=1.3, label=r["nombre"])
        if abs(b) > 1e-12:
            ax.plot(xs, (r["rhs"] - a * xs) / b, **estilo)
        else:
            ax.axvline(r["rhs"] / a, **estilo)
    puntos = [(i, j) for i in range(lim_x + 1) for j in range(lim_y + 1) if factible((i, j))]
    ax.plot(*zip(*puntos), "o", color=C["negro"], markersize=2.2, zorder=4, label="Puntos enteros factibles")
    ax.plot(*x_rel, "o", markerfacecolor="white", markeredgecolor=SERIES[0], markersize=6, zorder=5)
    ax.annotate(f"Relajación ({datos.fmt(x_rel[0])}; {datos.fmt(x_rel[1])}) Z = {datos.fmt(cota)}", x_rel,
                xytext=(6, 2), textcoords="offset points", fontsize=TAM_ETIQUETA,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
    ax.plot(*x_ent, "o", color=SERIES[0], markersize=6, zorder=6)
    ax.annotate(f"Óptimo entero ({datos.fmt(x_ent[0])}, {datos.fmt(x_ent[1])}) Z = {datos.fmt(entero)}", x_ent,
                xytext=(6, -10), textcoords="offset points", fontsize=TAM_ETIQUETA, fontweight="bold",
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
    redondeo = tuple(round(v) for v in x_rel)
    if not factible(redondeo):
        ax.plot(*redondeo, "x", color=C["negro"], markersize=7, markeredgewidth=1.8, zorder=6)
        ax.annotate(f"Redondeo {redondeo}: no factible", redondeo, xytext=(-6, 4), textcoords="offset points",
                    fontsize=TAM_ETIQUETA, ha="right", bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
    ax.set_xlim(0, lim_x)
    ax.set_ylim(0, lim_y)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel(d["variables"][0], fontsize=TAM_ETIQUETA)
    ax.set_ylabel(d["variables"][1], fontsize=TAM_ETIQUETA)
    rejilla_y(ax)
    leyenda(ax, loc="upper left", ncol=1, bbox_to_anchor=(1.02, 1))   # fuera del área: no tapa los puntos
    guardar(fig, ruta)
    return {"cota": cota, "entero": entero, "brecha": brecha}


# ------------------------------------------------------------------ transporte: barras apiladas por origen
def transporte_apilado(ruta, w=426, h=170):
    d = datos.yaml_de("transporte")
    res = datos.resultado("transporte")
    fig, ax = figura(w, h)
    origenes = d["origenes"]
    reales, ficticio = [], []
    for o in origenes:
        flujos = {k.split("->")[1]: v for k, v in (res or {"variables": {}})["variables"].items() if k.startswith(o + "->")}
        ficticio.append(sum(v for k, v in flujos.items() if k.startswith("Ficticio")))
        reales.append(sum(v for k, v in flujos.items() if not k.startswith("Ficticio")))
    ys = list(range(len(origenes)))[::-1]
    ax.barh(ys, reales, 0.55, color=SERIES[0], label="Enviado a clientes")
    ax.barh(ys, ficticio, 0.55, left=reales, color=SERIES[1], label="Al destino ficticio (no se envía)")
    for yv, r, f, o in zip(ys, reales, ficticio, d["oferta"]):
        ax.text(r + f, yv, f"  {datos.fmt(r + f)}", va="center", fontsize=9, fontweight="bold")
    ax.set_yticks(ys, origenes)
    ax.axvline(0, color="black", linewidth=1)
    ax.spines["bottom"].set_visible(False)
    rejilla_x(ax)
    ax.set_xlim(0, max(d["oferta"]) * 1.3)
    leyenda(ax, loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=2)
    guardar(fig, ruta)
    i = max(range(len(origenes)), key=lambda k: ficticio[k])
    return {"origenes": origenes, "reales": reales, "ficticio": ficticio, "con_sobrante": origenes[i] if ficticio[i] > 0 else None,
            "sobrante": ficticio[i]}


# ------------------------------------------------------------------ asignación: costo asignado por agente
def asignacion_barras(ruta, w=426, h=170):
    d = datos.yaml_de("asignacion")
    res = datos.resultado("asignacion")
    fig, ax = figura(w, h)
    etiquetas, costos, minimos = [], [], []
    for i, a in enumerate(d["agentes"]):
        tarea = next((k.split("->")[1] for k, v in (res or {"variables": {}})["variables"].items()
                      if k.startswith(a + "->") and v > 0.5), None)
        if tarea and not tarea.startswith("Ficticio"):
            costos.append(d["matriz"][i][d["tareas"].index(tarea)])
            etiquetas.append(f"{a}\n{tarea}")
        else:
            costos.append(0)
            etiquetas.append(f"{a}\nsin asignar")
        minimos.append(min(d["matriz"][i]))
    xs = range(len(costos))
    ax.bar(xs, costos, 0.5, color=SERIES[0], label="Valor de la tarea asignada")
    ax.plot(xs, minimos, "o", color="black", markersize=4, label="Mínimo de la fila")
    for x, c, m in zip(xs, costos, minimos):
        ax.text(x, c, datos.fmt(c), ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_xticks(list(xs), etiquetas)
    rejilla_y(ax)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_ylim(0, max(max(costos), max(minimos)) * 1.35)
    leyenda(ax, ncol=2)
    guardar(fig, ruta)
    return {"total": sum(costos), "sin_asignar": [e.split("\n")[0] for e in etiquetas if "sin asignar" in e]}


# ------------------------------------------------------------------ comparación Python / R / Solver
def comparacion(ruta, solver, w=426, h=180):
    nombres = [("pl", "PL"), ("ple", "PLE"), ("transporte", "Transp."), ("asignacion", "Asign."),
               ("transbordo", "Transb."), ("transbordo_desbalanceado", "Transb. desb.")]
    fig, ax = figura(w, h)
    pendientes = []
    for i, (p, et) in enumerate(nombres):
        py = (datos.resultado(p, "python") or {}).get("valor_objetivo")
        r = (datos.resultado(p, "r") or {}).get("valor_objetivo")
        sv = solver.get(p)
        base = py or 1
        for j, (val, color, nombre) in enumerate(((py, SERIES[0], "Python"), (r, SERIES[1], "R"), (sv, SERIES[2], "Solver"))):
            x = i + (j - 1) * 0.26
            etiqueta = nombre if i == 0 else None
            if val is None:   # pendiente: barra rayada (estimación) a la altura del valor de Python
                if nombre != "Solver" or p.startswith("transbordo"):
                    ax.bar(x, 100, 0.24, color="white", edgecolor=color, hatch="////", linewidth=0.8,
                           label=f"{nombre} (pendiente)" if (nombre, "p") not in pendientes else None)
                    pendientes.append((nombre, "p"))
            else:
                ax.bar(x, val / base * 100, 0.24, color=color, label=etiqueta)
    ax.set_xticks(range(len(nombres)), [n[1] for n in nombres])
    ax.set_ylim(0, 135)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0", "25", "50", "75", "100"])
    rejilla_y(ax)
    ax.axhline(0, color="black", linewidth=1)
    leyenda(ax, ncol=3)
    guardar(fig, ruta)
    return {"pendientes": sorted({n for n, _ in pendientes})}


# ------------------------------------------------------------------ transbordo: red con flujos
def red_transbordo(ruta, problema="transbordo", w=426, h=200, separar_etiquetas=False):
    d = datos.yaml_de(problema)
    res = datos.resultado(problema)
    flujos = (res or {}).get("variables", {})
    columnas = {"origen": 0, "transbordo": 1, "destino": 2}
    color_tipo = {"origen": C["amarillo"], "transbordo": C["rosado"], "destino": C["verde"]}
    nodos = list(d["nodos"])
    if any(k.endswith("->Ficticio") for k in flujos):
        nodos.append({"nombre": "Ficticio", "tipo": "destino"})
    elif any(k.startswith("Ficticio->") for k in flujos):
        nodos.insert(0, {"nombre": "Ficticio", "tipo": "origen"})
    pos = {}
    for t, col in columnas.items():
        grupo = [n["nombre"] for n in nodos if n["tipo"] == t]
        for i, k in enumerate(grupo):
            pos[k] = (col * 2.0, (len(grupo) - 1) / 2 - i)
    fig, ax = plt.subplots(figsize=(w / 96, h / 96))
    ax.axis("off")
    arcos = [(a["desde"], a["hasta"], a["costo"]) for a in d["arcos"]]
    arcos += [(k.split("->")[0], k.split("->")[1], 0) for k in flujos if "Ficticio" in k]
    for a, b, c in arcos:
        f = flujos.get(f"{a}->{b}", 0) or 0
        usado = f > 1e-9
        rad = 0.25 if columnas[next(n["tipo"] for n in nodos if n["nombre"] == a)] == columnas[next(n["tipo"] for n in nodos if n["nombre"] == b)] else 0.0
        flecha = FancyArrowPatch(pos[a], pos[b], arrowstyle="-|>", mutation_scale=8, shrinkA=11, shrinkB=11,
                                 connectionstyle=f"arc3,rad={rad}", color=C["bermellon"] if usado else C["rejilla"],
                                 linewidth=2.0 if usado else 0.9, linestyle="-" if "Ficticio" not in b + a else "--",
                                 zorder=1 if not usado else 2)
        ax.add_patch(flecha)
        # con separar_etiquetas, en los arcos diagonales de una sola columna la etiqueta va más cerca del origen,
        # para que no choque con la de otro arco que lo cruza (P1→T2 y P2→T1)
        t = 0.3 if separar_etiquetas and not rad and pos[a][1] != pos[b][1] and abs(pos[b][0] - pos[a][0]) == 2.0 else 0.4
        mx, my = (pos[a][0] * (1 - t) + pos[b][0] * t), (pos[a][1] * (1 - t) + pos[b][1] * t)
        etiqueta = f"{datos.fmt(c)}" + (f" [{datos.fmt(f)}]" if usado else "")
        ax.text(mx, my + (0.12 if rad else 0), etiqueta, fontsize=6.5, ha="center", va="center",
                fontweight="bold" if usado else "normal", zorder=3,
                bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
    for n in nodos:
        k = n["nombre"]
        color = C["rejilla"] if k == "Ficticio" else color_tipo[n["tipo"]]
        ax.add_patch(Rectangle((pos[k][0] - 0.22, pos[k][1] - 0.17), 0.44, 0.34, color=color, zorder=4))
        cantidad = n.get("oferta") or n.get("demanda")
        texto_color = "white" if n["tipo"] == "destino" and k != "Ficticio" else "black"
        ax.text(pos[k][0], pos[k][1], k, ha="center", va="center", fontsize=7.5, fontweight="bold", color=texto_color, zorder=5)
        if cantidad:
            lado = -0.3 if n["tipo"] == "origen" else 0.3
            ax.text(pos[k][0] + lado, pos[k][1], datos.fmt(cantidad), ha="right" if lado < 0 else "left", va="center",
                    fontsize=7, zorder=5)
    for t, col in columnas.items():
        ax.text(col * 2.0, max(p[1] for p in pos.values()) + 0.45,
                {"origen": "Orígenes (oferta)", "transbordo": "Transbordo", "destino": "Destinos (demanda)"}[t],
                ha="center", fontsize=7.5, fontweight="bold")
    ax.set_xlim(-0.75, 4.75)
    ys = [p[1] for p in pos.values()]
    ax.set_ylim(min(ys) - 0.4, max(ys) + 0.65)
    guardar(fig, ruta)
    via = sum(v for k, v in flujos.items() if k.split("->")[0] in [n["nombre"] for n in nodos if n["tipo"] == "transbordo"])
    return {"via_transbordo": via, "costo": (res or {}).get("valor_objetivo")}


# ------------------------------------------------------------------ transbordo: directo vs vía nodos (barras apiladas)
def destino_directo_vs_transbordo(ruta, w=426, h=150):
    d = datos.yaml_de("transbordo")
    res = datos.resultado("transbordo")
    flujos = (res or {}).get("variables", {})
    tipo = {n["nombre"]: n["tipo"] for n in d["nodos"]}
    destinos = [n["nombre"] for n in d["nodos"] if n["tipo"] == "destino"]
    directo = [sum(v for k, v in flujos.items() if k.endswith("->" + t) and tipo.get(k.split("->")[0]) == "origen") for t in destinos]
    via = [sum(v for k, v in flujos.items() if k.endswith("->" + t) and tipo.get(k.split("->")[0]) == "transbordo") for t in destinos]
    fig, ax = figura(w, h)
    ys = list(range(len(destinos)))[::-1]
    ax.barh(ys, via, 0.55, color=SERIES[0], label="Llega por un nodo de transbordo")
    if any(directo):   # sin envíos directos no se dibuja (ni se pone en la leyenda) una serie vacía
        ax.barh(ys, directo, 0.55, left=via, color=SERIES[1], label="Llega directo desde un origen")
    for yv, a, b in zip(ys, via, directo):
        ax.text(a + b, yv, f"  {datos.fmt(a + b)}", va="center", fontsize=9, fontweight="bold")
    ax.set_yticks(ys, destinos)
    ax.axvline(0, color="black", linewidth=1)
    ax.spines["bottom"].set_visible(False)
    rejilla_x(ax)
    ax.set_xlim(0, max(a + b for a, b in zip(via, directo)) * 1.3 or 1)
    leyenda(ax, loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2)
    guardar(fig, ruta)
    total = sum(via) + sum(directo)
    return {"pct_via": (sum(via) / total * 100) if total else None}


# ------------------------------------------------------------------ desbalanceo: curva de costo vs oferta total
def curva_desbalanceo(ruta, w=426, h=180):
    c = datos.curva_oferta()
    xs = [p[0] for p in c["puntos"]]
    ys = [p[1] for p in c["puntos"]]
    fig, ax = figura(w, h)
    bal = c["balance"]
    ax.axvspan(min(xs), bal, color=C["ventana"], linewidth=0, zorder=0)
    ax.axvspan(bal, max(xs), color=C["ventana"], linewidth=0, zorder=0)
    ax.text((min(xs) + bal) / 2, max(ys) * 1.08, "Falta oferta:\norigen ficticio", ha="center", fontsize=TAM_ETIQUETA)
    ax.text((bal + max(xs)) / 2, max(ys) * 1.08, "Sobra oferta:\ndestino ficticio", ha="center", fontsize=TAM_ETIQUETA)
    ax.plot(xs, ys, color=SERIES[0], linewidth=1.6, linestyle="--", label=f"Costo óptimo al variar la oferta de {c['nodo']}")
    ax.plot([bal], [dict(c["puntos"]).get(bal)], "o", color="black", markersize=5, zorder=5, label="Caso balanceado")
    ax.axvline(bal, color="black", linewidth=0.8)
    ax.axhline(0, color="black", linewidth=1)
    rejilla_y(ax)
    ax.set_xlabel("Oferta total (unidades)", fontsize=TAM_ETIQUETA)
    ax.set_ylim(0, max(ys) * 1.3)
    leyenda(ax, loc="lower right", ncol=1)
    guardar(fig, ruta)
    return {"balance": bal, "nodo": c["nodo"], "costo_bal": dict(c["puntos"]).get(bal), "min": min(ys), "max": max(ys)}


def generar_todos(carpeta, solver):
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    g = {}
    for nombre, funcion in (("tamanos", tamano_modelos), ("pl", region_pl), ("ple", region_ple),
                            ("transporte", transporte_apilado), ("asignacion", asignacion_barras),
                            ("red", lambda r: red_transbordo(r, separar_etiquetas=True)), ("directo", destino_directo_vs_transbordo),
                            ("desbalanceo", curva_desbalanceo)):
        ruta = carpeta / f"{nombre}.png"
        g[nombre] = {"ruta": ruta, **funcion(ruta)}
    ruta = carpeta / "red_desbalanceada.png"
    g["red_desb"] = {"ruta": ruta, **red_transbordo(ruta, "transbordo_desbalanceado")}
    ruta = carpeta / "comparacion.png"
    g["comparacion"] = {"ruta": ruta, **comparacion(ruta, solver)}
    return g
