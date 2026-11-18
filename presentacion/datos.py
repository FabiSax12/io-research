"""Lectura de todo lo que alimenta la presentación: YAML de datos/, JSON de resultados/,
imágenes y salidas de consola de capturas/ y fragmentos de los scripts.

Nada de esto resuelve los problemas del curso (eso lo hacen los scripts de parte1/ y parte2/);
solo hay dos cálculos auxiliares para gráficos: la relajación lineal del PLE y la curva de
escenarios de oferta del transbordo.
"""
import json
import re
from pathlib import Path

import yaml
from scipy.optimize import linprog

RAIZ = Path(__file__).resolve().parents[1]
DATOS, RESULTADOS, CAPTURAS = (RAIZ / c for c in ("datos", "resultados", "capturas"))
PROBLEMAS = ["pl", "ple", "transporte", "asignacion", "transbordo", "transbordo_desbalanceado"]


def yaml_de(problema):
    with open(DATOS / f"{problema}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def es_ejemplo(problema):
    with open(DATOS / f"{problema}.yaml", encoding="utf-8") as f:
        return any(linea.startswith("# EJEMPLO") for linea in f.readlines()[:5])


def resultado(problema, lenguaje="python"):
    ruta = RESULTADOS / f"{problema}_{lenguaje}.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


def captura(nombre):
    """Ruta de capturas/<nombre> si existe; None si todavía no se generó."""
    ruta = CAPTURAS / nombre
    return ruta if ruta.exists() else None


def consola(problema, lenguaje="python", max_lineas=14):
    ruta = CAPTURAS / f"{problema}_{lenguaje}.txt"
    if not ruta.exists():
        return None
    lineas = [l for l in ruta.read_text(encoding="utf-8").splitlines() if not l.startswith("Archivos:")]
    return lineas[:max_lineas]


def fmt(x):
    if x is None:
        return "n/d"
    if isinstance(x, (int, float)):
        return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:.2f}"
    return str(x)


def fragmento(ruta_relativa, desde=None, hasta=None, max_lineas=24):
    """Líneas del script que van en la lámina: sin docstring, imports ni preámbulo, sin la parte de salida.

    desde / hasta: texto de la línea donde empieza el fragmento y de la línea donde termina (sin incluirla).
    Sin 'desde' arranca en la lectura del YAML; sin 'hasta' termina al armar el resultado.
    """
    ruta = RAIZ / ruta_relativa
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    inicio = 0
    for i, l in enumerate(lineas):
        if (desde and desde in l) or (not desde and (re.match(r"^\s*(d|nombre)\s*(=|<-)", l) or "leer_yaml(" in l)):
            inicio = i
            break
    salida = []
    for l in lineas[inicio:]:
        if salida and hasta and hasta in l:
            break
        if re.match(r"^\s*res\s*(=|<-)\s*armar_resultado", l) or "Resultado (JSON" in l:
            break
        if "preámbulo" in l:
            continue
        salida.append(re.sub(r"#\s*-{5,}\s*", "# ", l.rstrip()))   # acorta los separadores largos
    while salida and not salida[-1].strip():
        salida.pop()
    if len(salida) > max_lineas:
        salida = salida[:max_lineas - 1] + ["# ... (continúa en el script)"]
    return salida


# ------------------------------------------------------------------ tamaños de los modelos (gráfico de contexto)
def tamanos():
    """(problema, n.º de variables, n.º de restricciones) tal como los resuelven los scripts."""
    filas = []
    for p, etiqueta in (("pl", "PL"), ("ple", "PLE"), ("transporte", "Transporte"), ("asignacion", "Asignación"),
                        ("transbordo", "Transbordo")):
        d = yaml_de(p)
        if p in ("pl", "ple"):
            v, r = len(d["variables"]), len(d["restricciones"])
        elif p == "transporte":
            m, n = len(d["origenes"]), len(d["destinos"])
            m += sum(d["oferta"]) < sum(d["demanda"])     # origen ficticio
            n += sum(d["oferta"]) > sum(d["demanda"])     # destino ficticio
            v, r = m * n, m + n
        elif p == "asignacion":
            k = max(len(d["agentes"]), len(d["tareas"]))
            v, r = k * k, 2 * k
        else:
            v, r = len(d["arcos"]), len(d["nodos"])
        filas.append((etiqueta, v, r))
    return filas


# ------------------------------------------------------------------ PLE: relajación lineal (cota)
def relajacion_ple():
    d = yaml_de("ple")
    k = -1 if d["sentido"] == "max" else 1
    A_ub, b_ub, A_eq, b_eq = [], [], [], []
    for r in d["restricciones"]:
        if r["signo"] == "<=":
            A_ub.append(r["coef"]); b_ub.append(r["rhs"])
        elif r["signo"] == ">=":
            A_ub.append([-a for a in r["coef"]]); b_ub.append(-r["rhs"])
        else:
            A_eq.append(r["coef"]); b_eq.append(r["rhs"])
    sol = linprog([k * c for c in d["objetivo"]], A_ub=A_ub or None, b_ub=b_ub or None,
                  A_eq=A_eq or None, b_eq=b_eq or None)
    return (k * sol.fun, list(sol.x)) if sol.success else (None, None)


# ------------------------------------------------------------------ transbordo: modelo de red con ficticio
def resolver_transbordo(nodos, arcos):
    """Modelo de red con balanceo por nodo ficticio (mismo criterio que parte2/python/transbordo.py)."""
    oferta = {n["nombre"]: n.get("oferta", 0) for n in nodos}
    demanda = {n["nombre"]: n.get("demanda", 0) for n in nodos}
    tipo = {n["nombre"]: n["tipo"] for n in nodos}
    costo = {(a["desde"], a["hasta"]): a["costo"] for a in arcos}
    dif = sum(oferta.values()) - sum(demanda.values())
    if dif > 1e-9:
        oferta["Ficticio"], demanda["Ficticio"] = 0, dif
        costo.update({(k, "Ficticio"): 0 for k in tipo if tipo[k] == "origen"})
    elif dif < -1e-9:
        oferta["Ficticio"], demanda["Ficticio"] = -dif, 0
        costo.update({("Ficticio", k): 0 for k in tipo if tipo[k] == "destino"})
    lista = list(costo)
    nombres = list(oferta)
    A = [[(1 if a[0] == k else 0) - (1 if a[1] == k else 0) for a in lista] for k in nombres]
    b = [oferta[k] - demanda[k] for k in nombres]
    sol = linprog([costo[a] for a in lista], A_eq=A, b_eq=b)
    if not sol.success:
        return None, {}
    return sol.fun, {f"{a[0]}->{a[1]}": x for a, x in zip(lista, sol.x)}


def curva_oferta(problema="transbordo", nodo=None, paso=5):
    """Costo óptimo cuando la oferta de un origen varía; marca dónde el modelo queda desbalanceado."""
    d = yaml_de(problema)
    origenes = [n for n in d["nodos"] if n["tipo"] == "origen"]
    nodo = nodo or origenes[0]["nombre"]
    base = next(n for n in origenes if n["nombre"] == nodo)["oferta"]
    demanda_total = sum(n.get("demanda", 0) for n in d["nodos"])
    otros = sum(n["oferta"] for n in origenes if n["nombre"] != nodo)
    puntos = []
    for s in range(max(0, base - 4 * paso), base + 8 * paso + 1, paso):
        nodos = [dict(n, oferta=s) if n["nombre"] == nodo else n for n in d["nodos"]]
        valor, _ = resolver_transbordo(nodos, d["arcos"])
        puntos.append((s + otros, valor))
    return {"nodo": nodo, "puntos": puntos, "balance": demanda_total, "base": base + otros}


def escenarios_transbordo():
    """Costo óptimo del ejemplo en tres casos: balanceado, sobra oferta, falta oferta."""
    d = yaml_de("transbordo")
    origenes = [n for n in d["nodos"] if n["tipo"] == "origen"]
    o1 = origenes[0]
    total_o = sum(n["oferta"] for n in origenes)
    total_d = sum(n.get("demanda", 0) for n in d["nodos"])
    casos = []
    for etiqueta, delta in (("balanceado", 0), ("sobra", 20), ("falta", -20)):
        nodos = [dict(n, oferta=n["oferta"] + delta) if n is o1 else n for n in d["nodos"]]
        valor, flujos = resolver_transbordo(nodos, d["arcos"])
        casos.append({"caso": etiqueta, "oferta": total_o + delta, "demanda": total_d, "valor": valor,
                      "ficticio": sum(v for k, v in flujos.items() if "Ficticio" in k)})
    return casos
