"""Láminas de las minutas, armadas con lo que lee minutas.py.

Por cada minuta, en el orden de plantilla.md: datos y presentes con la agenda, anotaciones importantes,
resumen de acuerdos y cronograma. Lo que no cabe en una lámina pasa a la siguiente: el texto se mide con
las mismas fuentes del tema para saber cuántas líneas ocupa.
"""
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

import minutas
from tema import (BASE, BLANCO, MARGEN, NEGRO, REGLA_X, TITULAR, TOPE, EXH_X, EXH_W, COL_IZQ_X, COL_IZQ_W,
                  rect, regla_h, regla_v, texto, titular)

FUENTES = Path(__file__).resolve().parent / "fuentes"
TAM, LINEA = 12, 15            # letra del cuerpo y alto de línea (px)
HUECO = 6                      # espacio entre viñetas
Y_CUERPO = TOPE + 84           # primera línea bajo el titular
HOLGURA = 0.96                 # ancho útil real frente al medido (LibreOffice y PowerPoint no miden igual)


@lru_cache(maxsize=None)
def _fuente(negrita, tam):
    return ImageFont.truetype(str(FUENTES / ("Onest-Bold.ttf" if negrita else "Onest-Regular.ttf")), tam * 4)


def lineas(trs, ancho, tam=TAM):
    """Cuántas líneas ocupan los tramos [(texto, negrita)] en un cuadro de ancho px (corte por palabras)."""
    ancho *= 4 * HOLGURA
    n, x = 1, 0.0
    for t, neg in trs:
        f = _fuente(neg, tam)
        for palabra in t.replace("\n", " ").split(" "):
            w = f.getlength(palabra + " ")
            if x + w - f.getlength(" ") > ancho and x > 0:
                n, x = n + 1, 0.0
            x += w
    return n


# ------------------------------------------------------------------ encabezado de cada lámina
def _cabecera(m, mi, seccion, pagina=None):
    """Lámina nueva con rótulo de la minuta, titular de la sección y regla."""
    etiqueta = f"Minuta {mi['numero']} · {mi['tema']} · {mi['fecha']}"
    lam = m.nueva("minutas", f"Minuta {mi['numero']}: {seccion}", grupo="minutas")
    texto(lam, MARGEN, TOPE, 880, 16, etiqueta, tam=12, negrita=True)
    pag = f" ({pagina[0]}/{pagina[1]})" if pagina and pagina[1] > 1 else ""
    titular(lam, MARGEN, TOPE + 20, 880, seccion + pag, tam=34, h=40)
    regla_h(lam, MARGEN, TOPE + 68, 880)
    return lam


# ------------------------------------------------------------------ lámina 1: datos, presentes y agenda
def _datos(m, mi):
    lam = m.nueva("minutas", f"Minuta {mi['numero']}", grupo="minutas")
    texto(lam, COL_IZQ_X, TOPE, COL_IZQ_W + 400, 16, f"Minuta de reunión · {mi['curso']}", tam=12, negrita=True)
    titular(lam, COL_IZQ_X, TOPE + 20, 880, f"Minuta {mi['numero']}: {mi['tema']}", tam=34, h=40)
    regla_v(lam, REGLA_X, TOPE + 84, BASE - TOPE - 84)

    y = Y_CUERPO
    for et, valor in (("Fecha", mi["fecha"]), ("Hora de inicio", mi["inicio"]), ("Hora de finalización", mi["fin"])):
        regla_h(lam, COL_IZQ_X, y, COL_IZQ_W)
        texto(lam, COL_IZQ_X, y + 7, 170, 18, et, tam=13, negrita=True)
        texto(lam, COL_IZQ_X + 180, y + 7, COL_IZQ_W - 180, 18, valor, tam=13)
        y += 30
    regla_h(lam, COL_IZQ_X, y, COL_IZQ_W)

    y += 24
    texto(lam, COL_IZQ_X, y, COL_IZQ_W, 20, "Presentes", tam=15, fuente=TITULAR)
    y += 30
    for asistio, nombre in mi["presentes"]:
        rect(lam, COL_IZQ_X, y + 2, 13, 13, NEGRO if asistio else None, borde=None if asistio else NEGRO, grosor=1.5)
        texto(lam, COL_IZQ_X + 24, y, COL_IZQ_W - 24, 18, nombre + ("" if asistio else " (ausente)"), tam=13)
        y += 26

    y = Y_CUERPO
    texto(lam, EXH_X, y, EXH_W, 20, "Agenda tratada", tam=15, fuente=TITULAR)
    y += 30
    for i, punto in enumerate(mi["agenda"], 1):
        regla_h(lam, EXH_X, y, EXH_W)
        h = max(40, lineas([(punto, False)], EXH_W - 44, 13) * 17 + 18)
        texto(lam, EXH_X, y + 8, 32, 26, str(i), tam=20, fuente=TITULAR)
        texto(lam, EXH_X + 44, y + 9, EXH_W - 44, h - 12, punto, tam=13, interlineado=1.3)
        y += h
    regla_h(lam, EXH_X, y, EXH_W)


# ------------------------------------------------------------------ tablas con alto de fila medido
def _alturas(filas, anchos, tam):
    return [max(lineas([(c, i == 0)], w - 16, tam) for i, (c, w) in enumerate(zip(f, anchos))) * round(tam * 1.25) + 16
            for f in filas]


def _dibujar_tabla(lam, x, y, anchos, encabezado, filas, tam=TAM):
    """Encabezado negro, filas con regla de 1.5 px y primera columna en negrita. Devuelve la y final."""
    rect(lam, x, y, sum(anchos), 26, NEGRO)
    cx = x
    for t, w in zip(encabezado, anchos):
        texto(lam, cx + 8, y, w - 16, 26, t, tam=12, negrita=True, color=BLANCO, anclar="medio")
        cx += w
    y += 26
    for fila, h in zip(filas, _alturas(filas, anchos, tam)):
        cx = x
        for i, (t, w) in enumerate(zip(fila, anchos)):
            texto(lam, cx + 8, y + 8, w - 16, h - 10, t, tam=tam, negrita=(i == 0), interlineado=1.25)
            cx += w
        y += h
        regla_h(lam, x, y - 1.5, sum(anchos))
    return y


def _paginas_tabla(filas, anchos, alto, tam):
    """Reparte las filas en páginas que caben en alto px (después del encabezado de 26 px)."""
    paginas, actual, usado = [], [], 26
    for fila, h in zip(filas, _alturas(filas, anchos, tam)):
        if actual and usado + h > alto:
            paginas.append(actual)
            actual, usado = [], 26
        actual.append(fila)
        usado += h
    return paginas + [actual]


def _cronograma(m, mi):
    anchos = [330, 100, 150, 300]
    paginas = _paginas_tabla(mi["cronograma"], anchos, BASE - Y_CUERPO, TAM)
    for i, filas in enumerate(paginas, 1):
        lam = _cabecera(m, mi, "Cronograma", (i, len(paginas)))
        _dibujar_tabla(lam, MARGEN, Y_CUERPO, anchos, ["Actividad", "Plazo", "Responsable", "Condición"], filas)


# ------------------------------------------------------------------ anotaciones y acuerdos (viñetas en columnas)
def _anchos_tabla(tabla, ancho):
    """Reparte el ancho según el texto más largo de cada columna (mínimo 60 px)."""
    pesos = [max(min(len(f[i]), 40) for f in tabla) + 6 for i in range(len(tabla[0]))]
    return [max(60, ancho * p / sum(pesos)) for p in pesos]


def _alto_item(it, ancho):
    if "tabla" in it:
        return 26 + sum(_alturas(it["tabla"][1:], _anchos_tabla(it["tabla"], ancho), 11.5)) + HUECO
    sangria = 11 + (16 if it["nivel"] else 0)
    return lineas(it["tramos"], ancho - sangria) * LINEA + HUECO


def _dibujar_item(lam, it, x, y, ancho):
    if "tabla" in it:
        anchos = _anchos_tabla(it["tabla"], ancho)
        _dibujar_tabla(lam, x, y, anchos, it["tabla"][0], it["tabla"][1:], tam=11.5)
        return
    sangria = 16 if it["nivel"] else 0
    texto(lam, x + sangria, y, ancho - sangria, _alto_item(it, ancho) - HUECO,
          [[(t, {"negrita": n}) for t, n in it["tramos"]]], tam=TAM, interlineado=1.25, vinetas=True)


def _empaquetar(items, alturas, ncols, limite):
    """Reparte los items en páginas de ncols columnas de alto limite; cada item es (item, y dentro de la columna)."""
    paginas, col, y = [[[] for _ in range(ncols)]], 0, 0
    for it, h in zip(items, alturas):
        if y + h > limite and y > 0:
            col, y = col + 1, 0
            if col == ncols:
                paginas.append([[] for _ in range(ncols)])
                col = 0
        paginas[-1][col].append((it, y))
        y += h
    return paginas


def _vinetas(m, mi, clave, titulo):
    items = mi[clave]
    if not items:
        return
    # con una tabla en la sección se usa una sola columna ancha para que la tabla respire
    ncols = 1 if any("tabla" in it for it in items) else 2
    ancho = 880 if ncols == 1 else 420
    alturas = [_alto_item(it, ancho) for it in items]
    paginas = _empaquetar(items, alturas, ncols, BASE - Y_CUERPO)
    if len(paginas) == 1 and ncols == 2:      # una sola lámina: columnas parejas en vez de llenar la primera
        for limite in range(40, BASE - Y_CUERPO, 4):
            candidata = _empaquetar(items, alturas, ncols, limite)
            if len(candidata) == 1:
                paginas = candidata
                break
    for i, pagina in enumerate(paginas, 1):
        lam = _cabecera(m, mi, titulo, (i, len(paginas)))
        for c, colocados in enumerate(pagina):
            x = MARGEN + c * (ancho + 40)
            for it, dy in colocados:
                _dibujar_item(lam, it, x, Y_CUERPO + dy, ancho)
        if ncols == 2 and pagina[1]:
            regla_v(lam, REGLA_X, Y_CUERPO, BASE - Y_CUERPO)


# ------------------------------------------------------------------ punto de entrada
def agregar(m):
    """Agrega al mazo las láminas de todas las minutas de minutas/ (leídas en este momento)."""
    for mi in minutas.leer_todas():
        _datos(m, mi)
        _vinetas(m, mi, "anotaciones", "Anotaciones importantes")
        _vinetas(m, mi, "acuerdos", "Resumen de acuerdos")
        if mi["cronograma"]:
            _cronograma(m, mi)
