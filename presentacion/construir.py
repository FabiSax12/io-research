"""Arma presentacion/salida/presentacion_io.pptx con el tema de DESIGN.md.

No resuelve modelos: lee resultados/ y capturas/ (los genera run_all.py) y dibuja los gráficos.
Para reconstruir todo desde cero usar reconstruir.py.
"""
import sys
from pathlib import Path

from pptx import Presentation

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import contenido as K  # noqa: E402
import datos  # noqa: E402
import graficos  # noqa: E402
import ventana_codigo  # noqa: E402
from tema import (AMARILLO, BASE, BLANCO, COL_IZQ_W, COL_IZQ_X, EXH_W, EXH_X, GRIS_EMBARGO, GRIS_VENTANA,  # noqa: E402
                  MARGEN, NEGRO, NOTA, REGLA_X, SECCIONES, TITULAR, TOPE, BERMELLON, caja_implicaciones,
                  columnas_cuerpo, exhibicion, imagen, lectura, marcador, medidor, nota_fuente, ovalo, pestana, pie,
                  px, rect, regla_h, regla_v, texto, titular, ANCHO, ALTO)

SALIDA = AQUI / "salida"
GRAFICOS = SALIDA / "graficos"
CODIGO = SALIDA / "codigo"          # ventanas de código (PNG estilo carbon.now.sh)
_contador_ventanas = [0]


def ventana(lam, codigo_txt, x, y, w, h, lenguaje, titulo, tam=10.0):
    """Inserta un fragmento de código como ventana estilo Carbon (ver ventana_codigo.py)."""
    _contador_ventanas[0] += 1
    ruta = CODIGO / f"ventana_{_contador_ventanas[0]:02d}.png"
    ventana_codigo.ventana(codigo_txt, ruta, w, h, lenguaje, titulo, tam=tam)
    return lam.shapes.add_picture(str(ruta), px(x), px(y), px(w), px(h))
f = datos.fmt


# ================================================================== valores calculados para los textos
def modelo_texto(d):
    """Modelo algebraico corto a partir de un YAML de PL/PLE."""
    termino = lambda cs: " + ".join(f"{c}{v}" if c != 1 else v for c, v in zip(cs, d["variables"]) if c)
    lineas = [f"{d['sentido']} Z = {termino(d['objetivo'])}"]
    for r in d["restricciones"]:
        lineas.append(f"{termino(r['coef'])} {r['signo'].replace('<=', '≤').replace('>=', '≥')} {r['rhs']}")
    tipo = " enteras" if d.get("enteras") else ""
    lineas.append(f"{', '.join(d['variables'])} ≥ 0{tipo}")
    return "\n".join(lineas)


def solucion_texto(res):
    if not res:
        return "[pendiente: correr run_all.py]"
    return ", ".join(f"{k} = {f(v)}" for k, v in res["variables"].items() if v)


def valores(g):
    v = {}
    pl, ple = datos.yaml_de("pl"), datos.yaml_de("ple")
    rpl, rple = datos.resultado("pl"), datos.resultado("ple")
    v.update(pl_nombre=pl["nombre"], pl_modelo=modelo_texto(pl), pl_optimo=f((rpl or {}).get("valor_objetivo")),
             pl_solucion=solucion_texto(rpl), pl_x1=f((g["pl"].get("x") or [None, None])[0]),
             pl_x2=f((g["pl"].get("x") or [None, None])[1]))
    v.update(ple_nombre=ple["nombre"], ple_modelo=modelo_texto(ple), ple_optimo=f((rple or {}).get("valor_objetivo")),
             ple_solucion=solucion_texto(rple), ple_cota=f(g["ple"]["cota"]),
             ple_brecha=f"{g['ple']['brecha']:.1f}" if g["ple"]["brecha"] is not None else "n/d")
    tr, rtr = datos.yaml_de("transporte"), datos.resultado("transporte")
    v.update(tr_nombre=tr["nombre"], tr_oferta=sum(tr["oferta"]), tr_demanda=sum(tr["demanda"]),
             tr_optimo=f((rtr or {}).get("valor_objetivo")),
             tr_ajuste=" ".join((rtr or {}).get("ajustes") or ["Oferta y demanda ya están balanceadas."]))
    gt = g["transporte"]
    v["tr_lectura"] = (f"{gt['con_sobrante']} es la única planta que no envía todo: le sobran {f(gt['sobrante'])} unidades, "
                       f"que el modelo manda al destino ficticio." if gt["con_sobrante"] else
                       "todas las plantas envían su oferta completa; el modelo está balanceado.")
    asg, ras = datos.yaml_de("asignacion"), datos.resultado("asignacion")
    v.update(as_nombre=asg["nombre"], as_dim=f"{len(asg['agentes'])} × {len(asg['tareas'])}",
             as_sentido="minimizar costo" if asg["sentido"] == "min" else "maximizar rendimiento",
             as_optimo=f((ras or {}).get("valor_objetivo")),
             as_ajuste=" ".join((ras or {}).get("ajustes") or ["La matriz ya es cuadrada."]))
    sin = g["asignacion"]["sin_asignar"]
    v["as_lectura"] = (f"el total es {f(g['asignacion']['total'])}; {', '.join(sin)} queda sin tarea porque la matriz tiene más agentes que tareas."
                       if sin else f"cada agente recibe una tarea y el total es {f(g['asignacion']['total'])}.")
    v.update(mayor_nombre=g["tamanos"]["mayor"][0].lower(), mayor_vars=g["tamanos"]["mayor"][1])

    # comparación entre lenguajes
    pend = g["comparacion"]["pendientes"]
    v["estado_comparacion"] = ("Python ya corrió los seis problemas y su verificación interna coincide. "
                               + (f"Faltan: {' y '.join(pend)}." if pend else "R y Solver coinciden con Python."))
    v["comparacion_lectura"] = ("las barras sólidas coinciden en 100; las rayadas son resultados que todavía hay que correr."
                                if pend else "las tres herramientas dan el mismo óptimo en todos los problemas.")

    # transbordo
    tb, rtb = datos.yaml_de("transbordo"), datos.resultado("transbordo")
    tipos = {"origen": "orígenes", "transbordo": "transbordos", "destino": "destinos"}
    v.update(tb_nombre=tb["nombre"], tb_narcos=len(tb["arcos"]), tb_optimo=f((rtb or {}).get("valor_objetivo")),
             tb_via=f(g["red"]["via_transbordo"]),
             tb_nodos="; ".join(f"{len([n for n in tb['nodos'] if n['tipo'] == t])} {nombre} "
                                f"({', '.join(n['nombre'] for n in tb['nodos'] if n['tipo'] == t)})" for t, nombre in tipos.items()) + ".",
             tb_B=f((rtb or {}).get("buffer", {}).get("B")), tb_M=f((rtb or {}).get("buffer", {}).get("M")),
             tb_n=len(tb["nodos"]), tb_buffer=f(((rtb or {}).get("verificacion") or {}).get("valor")),
             pct_via=f(g["directo"]["pct_via"]))
    sv = K.SOLVER.get("transbordo")
    v["solver_lectura"] = (f"Solver da {f(sv)}, igual que Python y R." if sv is not None and abs(sv - (rtb or {}).get("valor_objetivo", -1)) < 1e-6
                           else f"Solver da {f(sv)}; revisar contra {v['tb_optimo']}." if sv is not None
                           else f"[completar: correr Solver; el óptimo esperado es {v['tb_optimo']}.]")
    esc = {c["caso"]: c for c in datos.escenarios_transbordo()}
    v.update(o_bal=esc["balanceado"]["oferta"], d_bal=esc["balanceado"]["demanda"],
             f_sobra=f(esc["sobra"]["ficticio"]), f_falta=f(esc["falta"]["ficticio"]))
    v["_escenarios"] = esc
    rdb = datos.resultado("transbordo_desbalanceado")
    v.update(desb_ajuste=" ".join((rdb or {}).get("ajustes") or []), desb_optimo=f((rdb or {}).get("valor_objetivo")),
             curva_nodo=g["desbalanceo"]["nodo"], curva_bal=g["desbalanceo"]["balance"], curva_costo=f(g["desbalanceo"]["costo_bal"]))
    return v


def llenar(obj, v):
    """Reemplaza {clave} en strings, listas y dicts."""
    if isinstance(obj, str):
        return obj.format(**v)
    if isinstance(obj, list):
        return [llenar(o, v) for o in obj]
    if isinstance(obj, tuple):
        return tuple(llenar(o, v) for o in obj)
    if isinstance(obj, dict):
        return {k: llenar(o, v) for k, o in obj.items()}
    return obj


# ================================================================== tipos de lámina
class Mazo:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = px(ANCHO), px(ALTO)
        self.vacia = self.prs.slide_layouts[6]
        self.indice = []   # (sección, titular, número de lámina)

    def nueva(self, seccion=None, titulo=None, fondo=BLANCO):
        lam = self.prs.slides.add_slide(self.vacia)
        lam.background.fill.solid()
        lam.background.fill.fore_color.rgb = __import__("tema").rgb(fondo)
        n = len(self.prs.slides)
        if seccion:
            pestana(lam, seccion)
            pie(lam, n)
            self.indice.append((seccion, titulo, n))
        return lam


def portada(m):
    lam = m.nueva(fondo=NEGRO)
    rect(lam, MARGEN, MARGEN, 560, 400, AMARILLO)
    texto(lam, MARGEN + 32, MARGEN + 32, 500, 200, [K.PORTADA["anio"]] + K.PORTADA["titulo"].split("\n"), tam=64,
          fuente=TITULAR, interlineado=1.0)
    texto(lam, MARGEN + 32, MARGEN + 246, 480, 80, K.PORTADA["subtitulo"], tam=22, negrita=True, interlineado=1.15)
    texto(lam, MARGEN + 32, MARGEN + 344, 480, 40, [f"{K.CURSO} · {K.SEMESTRE}", K.PROFESOR], tam=13, interlineado=1.3)
    a, b, c = K.INSTITUCION
    texto(lam, 640, MARGEN + 300, 280, 100, [[(a, {})], [(b, {"negrita": True})], [(c, {})]], tam=22, color=BLANCO,
          interlineado=1.0)
    rect(lam, MARGEN, 470, ANCHO - 2 * MARGEN, 30, GRIS_EMBARGO)
    texto(lam, MARGEN + 14, 470, 800, 30, K.FECHA_DEFENSA, tam=12, negrita=True, color=BERMELLON, mayusculas=True,
          anclar="medio")


def indice(m, lam, integrantes):
    """Se dibuja al final, cuando ya se conocen los números de lámina."""
    rect(lam, MARGEN, TOPE, 420, BASE - TOPE, AMARILLO)
    texto(lam, MARGEN + 24, TOPE + 20, 380, 50, "Contenido", tam=42, fuente=TITULAR, interlineado=1.0)
    grupos = []
    for sec, _, n in m.indice[1:]:
        if grupos and grupos[-1][0] == sec:
            grupos[-1][2] = n
        else:
            grupos.append([sec, n, n])
    descripciones = {"contexto": "Introducción", "herramientas": "Librerías de Python y R",
                     "parte1": "PL, PLE, transporte y asignación", "parte2": "Problema de transbordo",
                     "resumen": "Conclusiones, minutas y referencias"}
    y = TOPE + 100
    for sec, a, b in grupos:
        regla_h(lam, MARGEN + 24, y - 8, 372)
        texto(lam, MARGEN + 24, y, 250, 40, [[(SECCIONES[sec]["etiqueta"], {"negrita": True})], [(descripciones[sec], {})]],
              tam=13)
        texto(lam, MARGEN + 300, y, 96, 20, f"{a}–{b}" if a != b else str(a), tam=13, negrita=True, alinear="der")
        y += 56
    texto(lam, 500, TOPE + 20, 420, 30, "Equipo", tam=15, fuente=TITULAR)
    texto(lam, 500, TOPE + 46, 420, 120, integrantes or ["[completar: integrantes]"], tam=13)
    texto(lam, 500, TOPE + 170, 420, 30, "Enunciado", tam=15, fuente=TITULAR)
    texto(lam, 500, TOPE + 196, 420, 160, [
        "Parte I: resolver con librerías de Python y R un problema de PL, PLE, transporte y asignación (3 o más restricciones cada uno).",
        "Parte II: investigar el problema de transbordo, plantear su modelo matricial, resolverlo con R, Python y Solver, y "
        "analizar el caso desbalanceado.",
    ], tam=12, espacio_despues=6)


def dividida(m, seccion, c, grafico, alto_grafico=None, sin_grafico=False):
    """Titular y dos columnas a la izquierda, regla de 4 px, exhibición a la derecha.

    sin_grafico=True deja vacío el espacio del gráfico para dibujar algo nativo encima (p. ej. una matriz).
    """
    lam = m.nueva(seccion, c["titular"])
    titular(lam, COL_IZQ_X, TOPE, COL_IZQ_W, c["titular"], h=135)
    columnas_cuerpo(lam, TOPE + 150, c["izq"], c["der"])
    regla_v(lam, REGLA_X, TOPE, BASE - TOPE)
    e = c["exhibicion"]
    exhibicion(lam, seccion, e["titulo"], e["subtitulo"], grafico, e["lectura"], e["fuente"], e.get("implicaciones"),
               alto_grafico=alto_grafico, dibujar_grafico=not sin_grafico)
    return lam


def matriz_nativa(lam, ruta_csv, x, y, w, h):
    """Dibuja la matriz ampliada del CSV como tabla del tema (encabezado negro, reglas de 1.5 px)."""
    import csv
    if not ruta_csv.exists():
        marcador(lam, x, y, w, h, "correr python run_all.py transbordo para generar la matriz.")
        return
    with open(ruta_csv, encoding="utf-8-sig") as fh:
        filas = list(csv.reader(fh))
    nc, nf = len(filas[0]), len(filas)
    ancho = w / (nc + 0.8)                       # la primera columna (nombres) mide 1.8 celdas
    xs = [x] + [x + ancho * (1.8 + k) for k in range(nc - 1)]
    anchos = [ancho * 1.8] + [ancho] * (nc - 1)
    alto = min(22, h / nf)
    for i, fila in enumerate(filas):
        fy = y + i * alto
        if i == 0:
            rect(lam, x, fy, w, alto, NEGRO)
        for j, celda in enumerate(fila):
            cx, cw = xs[j], anchos[j]
            negrita = i == 0 or j == 0 or i == nf - 1 or j == nc - 1
            color = BLANCO if i == 0 else (BERMELLON if celda not in ("M", "0") and 0 < i < nf - 1 and 0 < j < nc - 1 else NEGRO)
            texto(lam, cx + 2, fy, cw - 4, alto, celda, tam=9 if i == 0 else 10.5, negrita=negrita, color=color,
                  anclar="medio", alinear="izq" if j == 0 else "der")
        if i > 0:
            regla_h(lam, x, fy + alto - 1.5, w, grosor=1.5 if i in (nf - 2, nf - 1) else 0.75)


def codigo(m, seccion, titulo, fragmentos):
    """Dos fragmentos de código (Python y R) lado a lado. fragmentos: [(ruta, desde, hasta), ...]."""
    lam = m.nueva(seccion, titulo)
    titular(lam, MARGEN, TOPE, 880, titulo, h=50)
    w = (ANCHO - 2 * MARGEN - 28) / 2
    y = TOPE + 62
    alto = BASE - 40 - y
    for i, (ruta, desde, hasta) in enumerate(fragmentos):
        x = MARGEN + i * (w + 28)
        python = ruta.endswith(".py")
        lineas = datos.fragmento(ruta, desde, hasta, max_lineas=60)   # la ventana corta lo que no cabe
        ventana(lam, lineas or ["(sin fragmento)"], x, y, w, alto, "python" if python else "r",
                f"{'Python' if python else 'R'} · {ruta}")
        if i == 0:
            regla_v(lam, x + w + 12, y, alto)
    nota_fuente(lam, MARGEN, BASE - 28, 880, "Fragmentos tomados de los scripts del repositorio, sin preámbulo ni la parte de salida (JSON y PNG).")
    return lam


def capturas(m, seccion, titulo, paneles, lectura_txt, fuente, pesos=None):
    """Dos o tres capturas de capturas/ lado a lado; un marcador si alguna falta."""
    lam = m.nueva(seccion, titulo)
    titular(lam, MARGEN, TOPE, 880, titulo, h=50)
    n = len(paneles)
    pesos = pesos or [1.35] + [1] * (n - 1)     # por defecto la primera captura (tabla de Python) es la más ancha
    util = ANCHO - 2 * MARGEN - 28 * (n - 1)
    alto = BASE - TOPE - 90 - 74
    x = MARGEN
    for i, (t, sub, ruta, falta) in enumerate(paneles):
        w = util * pesos[i] / sum(pesos)
        texto(lam, x, TOPE + 62, w, 20, t, tam=15, fuente=TITULAR)
        texto(lam, x, TOPE + 82, w, 16, sub, tam=12)
        y = TOPE + 106
        if ruta is None:
            marcador(lam, x, y, w, alto - 20, falta)
        elif isinstance(ruta, Path) and ruta.suffix == ".csv":   # matriz dibujada como tabla del tema
            matriz_nativa(lam, ruta, x, y, w, alto - 20)
        elif isinstance(ruta, list):   # salida de consola, como ventana de terminal
            ventana(lam, ruta, x, y, w, alto - 20, "consola", "Terminal", tam=8.5)
        else:
            imagen(lam, ruta, x, y, w, alto - 20)
        if i < n - 1:
            regla_v(lam, x + w + 12, TOPE + 62, alto + 24)
        x += w + 28
    lectura(lam, MARGEN, BASE - 66, 880, lectura_txt, h=20)
    nota_fuente(lam, MARGEN, BASE - 40, 880, fuente)
    return lam


def panel_resultado(problema, lenguaje):
    ruta = datos.captura(f"{problema}_{lenguaje}_tabla.png")
    comando = (f"python run_all.py {problema}" if lenguaje == "python" else
               f"Rscript (R 4.2+) y luego python run_all.py {problema}")
    return (f"Tabla de solución en {'Python' if lenguaje == 'python' else 'R'}",
            "Solución y valor óptimo", ruta, f"correr {comando} para generar esta captura.")


def panel_consola(problema):
    lineas = datos.consola(problema, max_lineas=40)
    return ("Salida de consola", "Lo que imprime el script de Python", lineas, f"correr python run_all.py {problema}.")


def tabla_herramientas(m, c):
    lam = m.nueva("herramientas", c["titular"])
    titular(lam, MARGEN, TOPE, 880, c["titular"], h=50)
    # leyenda sobre la tabla, alineada a la derecha
    lx, ly, lw = ANCHO - MARGEN - 380, TOPE + 54, 380
    rect(lam, lx, ly, lw, 54, None, borde=NEGRO, grosor=1.5)
    texto(lam, lx + 10, ly + 7, lw - 20, 14, c["leyenda"], tam=10, negrita=True)
    texto(lam, MARGEN, ly + 4, 460, 50, "Cada medidor va de −3 a +3; la celda de color es nuestra valoración "
          "después de usar la librería y el punto, la que teníamos antes.", tam=12)
    from tema import GRIS_NEUTRO, ROSADO
    items = [(ROSADO, "Desaconsejada", 96), (GRIS_NEUTRO, "Neutral", 70), (AMARILLO, "Recomendada", 92)]
    ix = lx + 10
    for color, et, ancho in items:
        rect(lam, ix, ly + 31, 12, 12, color)
        texto(lam, ix + 17, ly + 30, ancho - 17, 14, et, tam=10)
        ix += ancho
    ovalo(lam, ix + 3, ly + 34, 6, NEGRO)
    texto(lam, ix + 14, ly + 30, 100, 14, "Valoración previa", tam=10)
    # encabezado negro
    y = TOPE + 118
    cols = [(MARGEN, 150, "Librería"), (MARGEN + 160, 60, "Lenguaje"), (MARGEN + 230, 130, "Valoración"), (MARGEN + 380, 500, "Comentario")]
    rect(lam, MARGEN, y, 880, 24, NEGRO)
    for x, w, t in cols:
        texto(lam, x + 8, y, w, 24, t, tam=12, negrita=True, color=BLANCO, anclar="medio")
    y += 24
    alto_fila = (BASE - 58 - y) / len(c["filas"])
    for nombre, leng, val, prev, com in c["filas"]:
        texto(lam, MARGEN + 8, y + 5, 150, alto_fila - 6, nombre, tam=13, negrita=True)
        texto(lam, MARGEN + 168, y + 6, 60, alto_fila - 6, leng, tam=12)
        medidor(lam, MARGEN + 238, y + 3, val, prev)
        texto(lam, MARGEN + 388, y + 4, 492, alto_fila - 4, com, tam=11.5)
        y += alto_fila
        regla_h(lam, MARGEN, y - 1.5, 880)
    lectura(lam, MARGEN, BASE - 52, 880, c["lectura"], h=18)
    nota_fuente(lam, MARGEN, BASE - 30, 880, c["fuente"])


def fuerzas(m, c, grafico):
    """Cita destacada con mosaico amarillo + barras apiladas (estilo 'mega forces')."""
    lam = m.nueva("parte2", c["titular"])
    titular(lam, COL_IZQ_X, TOPE, COL_IZQ_W, c["titular"], h=130)
    y = TOPE + 140
    rect(lam, COL_IZQ_X, y, 64, 80, AMARILLO)
    texto(lam, COL_IZQ_X + 8, y + 50, 50, 26, c["iniciales"], tam=22, fuente=TITULAR)
    texto(lam, COL_IZQ_X + 78, y, COL_IZQ_W - 78, 66, f"“{c['cita']}”", tam=14, negrita=True, interlineado=1.15)
    texto(lam, COL_IZQ_X + 78, y + 68, COL_IZQ_W - 78, 14, c["autor"], tam=10, fuente=NOTA)
    regla_h(lam, COL_IZQ_X, y + 94, COL_IZQ_W)
    mitad = len(c["situaciones"]) // 2
    columnas_cuerpo(lam, y + 106, c["situaciones"][:mitad], c["situaciones"][mitad:])
    regla_v(lam, REGLA_X, TOPE, BASE - TOPE)
    e = c["exhibicion"]
    exhibicion(lam, "parte2", e["titulo"], e["subtitulo"], grafico, e["lectura"], e["fuente"], None, alto_grafico=230)


def tabla_texto(m, seccion, titular_txt, encabezados, filas, anchos, lectura_txt=None, fuente=None, tam=12, alto_max=80):
    lam = m.nueva(seccion, titular_txt)
    titular(lam, MARGEN, TOPE, 880, titular_txt, h=50)
    y = TOPE + 70
    rect(lam, MARGEN, y, 880, 26, NEGRO)
    x = MARGEN
    for t, w in zip(encabezados, anchos):
        texto(lam, x + 8, y, w - 16, 26, t, tam=12, negrita=True, color=BLANCO, anclar="medio")
        x += w
    y += 26
    disponible = BASE - y - (64 if lectura_txt else 30)
    alto = min(disponible / max(len(filas), 1), alto_max)
    for fila in filas:
        x = MARGEN
        for i, (t, w) in enumerate(zip(fila, anchos)):
            texto(lam, x + 8, y + 8, w - 16, alto - 10, t, tam=tam, negrita=(i == 0))
            x += w
        y += alto
        regla_h(lam, MARGEN, y - 1.5, 880)
    if lectura_txt:
        lectura(lam, MARGEN, BASE - 52, 880, lectura_txt, h=18)
    if fuente:
        nota_fuente(lam, MARGEN, BASE - 30, 880, fuente)
    return lam


def escenarios(m, c, esc):
    lam = m.nueva("parte2", c["titular"])
    titular(lam, MARGEN, TOPE, 560, c["titular"], h=95)
    texto(lam, MARGEN, TOPE + 100, 560, 50, c["intro"], tam=13)
    y = TOPE + 170
    regla_h(lam, MARGEN, y, 880)
    for clave, caso, linea in c["casos"]:
        valor = esc[clave]["valor"]
        texto(lam, MARGEN, y + 14, 140, 36, f(valor), tam=28, fuente=TITULAR)
        texto(lam, MARGEN + 160, y + 14, 200, 36, caso, tam=15, fuente=TITULAR, anclar="medio")
        texto(lam, MARGEN + 380, y + 14, 500, 36, linea, tam=12.5, anclar="medio")
        y += 64
        regla_h(lam, MARGEN, y, 880)
    texto(lam, MARGEN, y + 12, 880, 30, c["nota"], tam=11.5)
    nota_fuente(lam, MARGEN, BASE - 30, 880, c["fuente"])


def conclusiones(m, c):
    lam = m.nueva("resumen", c["titular"])
    titular(lam, COL_IZQ_X, TOPE, COL_IZQ_W, c["titular"], h=95)
    columnas_cuerpo(lam, TOPE + 110, c["izq"], c["der"])
    regla_v(lam, REGLA_X, TOPE, BASE - TOPE)
    caja_implicaciones(lam, EXH_X, TOPE, EXH_W, 120, "resumen", c["implicaciones"], titulo="Implicaciones del trabajo")
    texto(lam, EXH_X, TOPE + 140, EXH_W, 20, "Resultados clave", tam=15, fuente=TITULAR)
    filas = [("PL", "pl"), ("PLE", "ple"), ("Transporte", "transporte"), ("Asignación", "asignacion"),
             ("Transbordo", "transbordo"), ("Transbordo desbalanceado", "transbordo_desbalanceado")]
    y = TOPE + 166
    rect(lam, EXH_X, y, EXH_W, 24, NEGRO)
    for x, t in ((EXH_X + 8, "Problema"), (EXH_X + 200, "Python"), (EXH_X + 280, "R"), (EXH_X + 350, "Solver")):
        texto(lam, x, y, 120, 24, t, tam=12, negrita=True, color=BLANCO, anclar="medio")
    y += 24
    for et, p in filas:
        r = datos.resultado(p, "r")
        texto(lam, EXH_X + 8, y + 5, 190, 18, et, tam=12, negrita=True)
        texto(lam, EXH_X + 200, y + 5, 70, 18, f((datos.resultado(p) or {}).get("valor_objetivo")), tam=12)
        texto(lam, EXH_X + 280, y + 5, 70, 18, f(r["valor_objetivo"]) if r else "pend.", tam=12)
        sv = K.SOLVER.get(p, "—")
        texto(lam, EXH_X + 350, y + 5, 70, 18, "—" if sv == "—" else (f(sv) if sv is not None else "pend."), tam=12)
        y += 28
        regla_h(lam, EXH_X, y - 1.5, EXH_W)
    nota_fuente(lam, EXH_X, y + 8, EXH_W, "Valores óptimos de resultados/*.json; Solver se reporta a mano en contenido.SOLVER.")


def minutas(m, c):
    mins = datos.minutas()
    filas = []
    for mi in mins:
        if mi["cronograma"]:
            filas = [fl for fl in mi["cronograma"] if any(fl)]
            break
    if not filas:
        filas = [["[completar: actividad]", "[fecha]", "[responsable]", "[en proceso / concluida]"]] * 3
    lam = tabla_texto(m, "resumen", c["titular"], ["Actividad", "Plazo", "Responsable", "Condición"], filas[:7],
                      [380, 140, 200, 160], tam=12, alto_max=36)
    resumen = "  ·  ".join(f"{mi['archivo'].replace('.md', '').replace('_', ' ').capitalize()}: {mi['fecha']} "
                           f"({mi['inicio']}–{mi['fin']})" for mi in mins) or "[completar: minutas]"
    texto(lam, MARGEN, BASE - 54, 880, 18, [[("Reuniones: ", {"negrita": True}), (resumen, {})]], tam=11.5)
    nota_fuente(lam, MARGEN, BASE - 30, 880, c["nota"])


def referencias(m):
    lam = m.nueva("resumen", "Referencias")
    titular(lam, MARGEN, TOPE, 880, "Referencias", h=50)
    regla_h(lam, MARGEN, TOPE + 62, 880)
    texto(lam, MARGEN, TOPE + 76, 880, BASE - TOPE - 76, K.REFERENCIAS, tam=12, espacio_despues=7)


# ================================================================== armado
def construir(destino=None):
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    g = graficos.generar_todos(GRAFICOS, K.SOLVER)
    v = valores(g)
    m = Mazo()

    portada(m)
    lam_indice = m.nueva("contexto", "Contenido")
    dividida(m, "contexto", llenar(K.INTRO, v), g["tamanos"]["ruta"], alto_grafico=190)

    tabla_herramientas(m, K.HERRAMIENTAS)
    c = K.USO_LIBRERIAS
    lam = m.nueva("herramientas", c["titular"])
    titular(lam, COL_IZQ_X, TOPE, COL_IZQ_W, c["titular"], h=135)
    columnas_cuerpo(lam, TOPE + 150, c["izq"], c["der"])
    regla_v(lam, REGLA_X, TOPE, BASE - TOPE)
    texto(lam, EXH_X, TOPE, EXH_W, 20, "PuLP frente a lpSolve", tam=15, fuente=TITULAR)
    texto(lam, EXH_X, TOPE + 20, EXH_W, 16, "El mismo modelo de PL en las dos librerías", tam=12)
    ventana(lam, [
        "m = pulp.LpProblem(\"PL\", pulp.LpMaximize)",
        "x = [pulp.LpVariable(f\"x{i}\", lowBound=0) for i in range(2)]",
        "m += 3*x[0] + 5*x[1]          # objetivo",
        "m += x[0] <= 4                # restricciones",
        "m += 2*x[1] <= 12",
        "m += 3*x[0] + 2*x[1] <= 18",
        "m.solve(pulp.PULP_CBC_CMD(msg=False))",
    ], EXH_X, TOPE + 44, EXH_W, 166, "python", "Python · PuLP")
    ventana(lam, [
        "A <- matrix(c(1,0, 0,2, 3,2), nrow = 3, byrow = TRUE)",
        "sol <- lp(\"max\", c(3, 5), A, rep(\"<=\", 3), c(4, 12, 18))",
        "sol$objval; sol$solution",
        "# PLE: int.vec · transporte: lp.transport() · asignación: lp.assign()",
    ], EXH_X, TOPE + 220, EXH_W, 124, "r", "R · lpSolve")
    nota_fuente(lam, EXH_X, TOPE + 354, EXH_W, "Ejemplo ilustrativo (plantas de vidrio, Hillier y Lieberman). El código completo está en parte1/.")

    for p in ("pl", "ple", "transporte", "asignacion"):
        c = llenar(K.PARTE1[p], v)
        dividida(m, "parte1", c, g[p]["ruta"], alto_grafico=190)
        codigo(m, "parte1", f"{c['titular']}: código", list(c["codigo"]))
        capturas(m, "parte1", f"{c['titular']}: resultados",
                 [panel_resultado(p, "python"), panel_resultado(p, "r"), panel_consola(p)],
                 f"Python y R resuelven el mismo YAML; el valor óptimo es {f((datos.resultado(p) or {}).get('valor_objetivo'))}.",
                 f"Capturas de run_all.py: capturas/{p}_python_tabla.png, {p}_r_tabla.png y {p}_python.txt, a partir de datos/{p}.yaml.")
    dividida(m, "parte1", llenar(K.COMPARACION, v), g["comparacion"]["ruta"], alto_grafico=180)

    fuerzas(m, llenar(K.QUE_ES, v), g["directo"]["ruta"])
    c = K.RELACION
    tabla_texto(m, "parte2", c["titular"], c["encabezados"], c["filas"], [150, 330, 400], c["lectura"], c["fuente"])
    dividida(m, "parte2", llenar(K.EJEMPLO, v), g["red"]["ruta"], alto_grafico=190)
    lam = dividida(m, "parte2", llenar(K.MATRICIAL, v), None, alto_grafico=190, sin_grafico=True)
    matriz_nativa(lam, datos.CAPTURAS / "transbordo_matriz_python.csv", EXH_X, TOPE + 42, EXH_W, 190)
    codigo(m, "parte2", "Transbordo: código", K.CODIGO_TRANSBORDO)
    capturas(m, "parte2", "Transbordo: resultados",
             [panel_resultado("transbordo", "python"), panel_resultado("transbordo", "r"), panel_consola("transbordo")],
             f"el modelo de red y el modelo matricial con buffer dan {v['tb_optimo']} en Python.",
             "Capturas de run_all.py: capturas/transbordo_python_tabla.png, transbordo_r_tabla.png y transbordo_python.txt, a partir de datos/transbordo.yaml.")
    dividida(m, "parte2", llenar(K.SOLVER_LAMINA, v), datos.captura("transbordo_solver.png") or "transbordo_solver.png",
             alto_grafico=190)
    escenarios(m, llenar(K.VARIANTES, v), v["_escenarios"])
    dividida(m, "parte2", llenar(K.DESBALANCEADO, v), g["desbalanceo"]["ruta"], alto_grafico=190)
    capturas(m, "parte2", "Transbordo desbalanceado: resultados",
             [("Red con destino ficticio", "Flujo óptimo; discontinua = arco ficticio", g["red_desb"]["ruta"], ""),
              ("Matriz ampliada con ficticio", "Costos; última fila y columna = demanda y oferta + B",
               datos.CAPTURAS / "transbordo_desbalanceado_matriz_python.csv", ""),
              panel_resultado("transbordo_desbalanceado", "python")],
             f"el ficticio absorbe el excedente a costo 0 y el costo óptimo es {v['desb_optimo']}.",
             "Elaboración propia con PuLP 3 sobre datos/transbordo_desbalanceado.yaml; matriz de "
             "capturas/transbordo_desbalanceado_matriz_python.csv y tabla de capturas/transbordo_desbalanceado_python_tabla.png.",
             pesos=[0.95, 1.45, 0.9])

    conclusiones(m, K.CONCLUSIONES)
    minutas(m, K.MINUTAS)
    referencias(m)

    integrantes = next((mi["presentes"] for mi in datos.minutas() if mi["presentes"]), [])
    indice(m, lam_indice, integrantes)

    destino = Path(destino or SALIDA / "presentacion_io.pptx")
    destino.parent.mkdir(parents=True, exist_ok=True)
    m.prs.save(destino)
    avisos = [p for p in datos.PROBLEMAS if datos.es_ejemplo(p)]
    if avisos:
        print(f"Aviso: datos de EJEMPLO todavía en {', '.join(avisos)} (quitar la línea '# EJEMPLO' al cargar los reales).")
    print(f"Presentación: {destino} ({len(m.prs.slides)} láminas)")
    return destino


if __name__ == "__main__":
    construir(sys.argv[1] if len(sys.argv) > 1 else None)
