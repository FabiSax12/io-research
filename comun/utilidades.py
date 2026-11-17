"""Utilidades mínimas de I/O compartidas por los scripts de Python.

Leer YAML, guardar JSON, imprimir la solución y guardar la tabla como PNG.
Si existe la variable de entorno IO_DIR, se lee de IO_DIR/datos y se escribe
en IO_DIR/resultados y IO_DIR/capturas (lo usan los tests).
"""
import json
import os
import sys
from numbers import Number
from pathlib import Path

import matplotlib
import yaml

matplotlib.use("Agg")  # sin ventanas: solo guardar imágenes
import matplotlib.pyplot as plt  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):  # acentos correctos en consolas de Windows
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parents[1]
BASE = Path(os.environ.get("IO_DIR", RAIZ))
LENGUAJE = "python"


def leer_yaml(nombre):
    """Lee datos/<nombre>.yaml y devuelve el contenido como dict."""
    with open(BASE / "datos" / f"{nombre}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ruta_salida(carpeta, archivo):
    """Devuelve BASE/carpeta/archivo y crea la carpeta si no existe."""
    ruta = BASE / carpeta / archivo
    ruta.parent.mkdir(parents=True, exist_ok=True)
    return ruta


def fmt(x):
    """Número sin decimales sobrantes (2.0 -> '2', 2.5 -> '2.5')."""
    if isinstance(x, Number):
        return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:.4f}".rstrip("0")
    return str(x)


def limpiar(x):
    """Redondea a 6 decimales y evita el -0.0."""
    return None if x is None else round(float(x), 6) + 0.0


def armar_resultado(problema, estado, valor, variables, ajustes=(), verificacion=None, **extra):
    """Diccionario con el esquema común a Python y R (se guarda como JSON)."""
    if verificacion:  # tipos nativos: numpy devuelve np.float64 / np.bool_, que json no acepta
        verificacion = {**verificacion, "valor": limpiar(verificacion["valor"]),
                        "coincide": bool(verificacion["coincide"])}
    return {
        "problema": problema,
        "lenguaje": LENGUAJE,
        "estado": estado,
        "valor_objetivo": limpiar(valor),
        "variables": {k: limpiar(v) for k, v in variables.items()},
        "ajustes": list(ajustes),
        "verificacion": verificacion,
        **extra,
    }


def _registrar_fuentes():
    """Usa Onest (fuente del tema de la presentación) si está en presentacion/fuentes; si no, la de matplotlib."""
    from matplotlib import font_manager
    carpeta = RAIZ / "presentacion" / "fuentes"
    for ttf in sorted(carpeta.glob("Onest-*.ttf")):
        font_manager.fontManager.addfont(str(ttf))
    if any(f.name == "Onest" for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = "Onest"


_registrar_fuentes()


def tabla_png(ruta, titulo, columnas, filas):
    """Guarda una tabla (lista de filas) como imagen PNG lista para las láminas.

    Estilo del tema de la presentación: encabezado negro con texto blanco en negrita,
    reglas horizontales negras de 1.5 px, sin líneas verticales ni sombras.
    """
    fig, ax = plt.subplots(figsize=(max(5, 1.7 * len(columnas)), 0.8 + 0.4 * (len(filas) + 1)))
    ax.axis("off")
    ax.set_title(titulo, fontsize=11, fontweight="bold", loc="left")
    tabla = ax.table(cellText=[[fmt(c) for c in fila] for fila in filas],
                     colLabels=columnas, loc="center", cellLoc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)
    for (fila, _), celda in tabla.get_celld().items():
        celda.visible_edges = "closed" if fila == 0 else "B"   # filas: solo la regla inferior
        celda.set_edgecolor("#000000")
        celda.set_linewidth(1.1)            # ~1.5 px a 150 dpi
        if fila == 0:
            celda.set_facecolor("#000000")
            celda.set_text_props(fontweight="bold", color="#ffffff")
    fig.savefig(ruta, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def emitir(res, titulo, columnas, filas):
    """Imprime la solución, guarda resultados/<problema>_python.json y la tabla PNG."""
    print(f"=== {titulo} ===")
    print(f"Estado: {res['estado']}")
    print(f"Valor óptimo: {fmt(res['valor_objetivo']) if res['valor_objetivo'] is not None else 'n/d'}")
    print("Solución (variables distintas de cero):")
    for nombre, valor in res["variables"].items():
        if valor is not None and abs(valor) > 1e-9:
            print(f"  {nombre} = {fmt(valor)}")
    for aviso in res["ajustes"]:
        print(f"Ajuste: {aviso}")
    if res["verificacion"]:
        v = res["verificacion"]
        print(f"Verificación ({v['metodo']}): {fmt(v['valor'])} -> {'coincide' if v['coincide'] else 'NO COINCIDE'}")

    nombre = f"{res['problema']}_{LENGUAJE}"
    with open(ruta_salida("resultados", f"{nombre}.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    optimo = f" | óptimo = {fmt(res['valor_objetivo'])}" if res["valor_objetivo"] is not None else ""
    tabla_png(ruta_salida("capturas", f"{nombre}_tabla.png"), f"{titulo} ({LENGUAJE}){optimo}", columnas, filas)
