"""Tema visual de la presentación (ver presentacion/DESIGN.md).

Todas las medidas del diseño están en px sobre una lámina de 960 x 540 px (16:9, 10 x 5.625 in),
así que 1 px = 9525 EMU y un tamaño de letra en px se convierte a pt multiplicando por 0.75.
Este módulo solo contiene constantes y primitivas de dibujo; el contenido está en contenido.py.
"""
from pathlib import Path

from lxml import etree
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

# ------------------------------------------------------------------ paleta (nada fuera de esta lista)
BLANCO = "ffffff"
NEGRO = "000000"
AMARILLO = "ffce00"
BERMELLON = "ff4713"
VERDE = "008b5c"
ROSADO = "fc9bb3"
GRIS_REJILLA = "d6d5dd"     # rejillas de gráficos y celdas del medidor
GRIS_NEUTRO = "595959"      # celda activa "neutral" del medidor
GRIS_PIE = "8a8a8a"         # número de lámina del pie
GRIS_EMBARGO = "e3e3ea"     # franja de embargo de la portada
GRIS_VENTANA = "ededf1"     # ventana de pronóstico / escenario
TINTE_BERMELLON = "fff3f0"
TINTE_VERDE = "e8fff7"
TINTE_AMARILLO = "fffbef"

SERIES = ["#" + c for c in (BERMELLON, AMARILLO, VERDE, ROSADO)]   # orden de las series en gráficos

# ------------------------------------------------------------------ tipografía
TITULAR = "Onest ExtraBold"   # Onest 800 (nombre de la fuente estática de Google Fonts)
CUERPO = "Onest"              # Onest 400; con bold=True da Onest 700
NOTA = "Barlow Condensed"     # notas de fuente, avisos legales y pie de página

# ------------------------------------------------------------------ secciones (pestaña de color)
# El diseño original define cinco tipos de sección; aquí se renombran a las secciones del trabajo.
SECCIONES = {
    "contexto":     {"etiqueta": "Contexto",     "fondo": AMARILLO,  "texto": NEGRO,  "tinte": TINTE_AMARILLO},
    "parte1":       {"etiqueta": "Parte I",      "fondo": BERMELLON, "texto": BLANCO, "tinte": TINTE_BERMELLON},
    "parte2":       {"etiqueta": "Parte II",     "fondo": VERDE,     "texto": BLANCO, "tinte": TINTE_VERDE},
    "herramientas": {"etiqueta": "Herramientas", "fondo": ROSADO,    "texto": NEGRO,  "tinte": TINTE_BERMELLON},
    "resumen":      {"etiqueta": "Resumen",      "fondo": NEGRO,     "texto": BLANCO, "tinte": TINTE_AMARILLO},
}

# ------------------------------------------------------------------ textos fijos del diseño (en español)
ETIQUETA_LECTURA = "Lectura:"
TITULO_IMPLICACIONES = "Implicaciones para el modelo"

# ------------------------------------------------------------------ retícula
ANCHO, ALTO = 960, 540
MARGEN = 40
COL_IZQ_X, COL_IZQ_W = 40, 412          # titular y dos columnas de texto
REGLA_X = 470                           # regla vertical negra de 4 px
EXH_X, EXH_W = 494, 426                 # exhibición (gráfico) a la derecha
TOPE = 46                               # primera línea de contenido bajo la pestaña
BASE = 492                              # último px útil sobre el pie


def px(v):
    return Emu(int(round(v * 9525)))


def pt(px_):
    return Pt(px_ * 0.75)


def rgb(hexa):
    return RGBColor.from_string(hexa.lstrip("#"))


def _sin_estilo(forma):
    """Quita el <p:style> que python-pptx agrega: así no hereda sombras ni bordes del tema de Office."""
    estilo = forma._element.find(qn("p:style"))
    if estilo is not None:
        forma._element.remove(estilo)
    return forma


def rect(lamina, x, y, w, h, relleno, borde=None, grosor=1.0):
    """Rectángulo de esquinas rectas, sin sombra ni degradado."""
    r = _sin_estilo(lamina.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(x), px(y), px(w), px(h)))
    if relleno is None:
        r.fill.background()
    else:
        r.fill.solid()
        r.fill.fore_color.rgb = rgb(relleno)
    if borde is None:
        r.line.fill.background()
    else:
        r.line.color.rgb = rgb(borde)
        r.line.width = px(grosor)
    return r


def ovalo(lamina, x, y, d, relleno):
    o = _sin_estilo(lamina.shapes.add_shape(MSO_SHAPE.OVAL, px(x), px(y), px(d), px(d)))
    o.fill.solid()
    o.fill.fore_color.rgb = rgb(relleno)
    o.line.fill.background()
    return o


def regla_h(lamina, x, y, w, grosor=1.5, color=NEGRO):
    return rect(lamina, x, y, w, grosor, color)


def regla_v(lamina, x, y, h, grosor=4, color=NEGRO):
    return rect(lamina, x, y, grosor, h, color)


def texto(lamina, x, y, w, h, parrafos, tam=12, fuente=CUERPO, color=NEGRO, negrita=False,
          interlineado=None, alinear="izq", anclar="arriba", espacio_despues=0, vinetas=False, mayusculas=False,
          sangria_francesa=0):
    """Cuadro de texto sin márgenes internos.

    parrafos: str, lista de str, o lista de párrafos donde cada párrafo es una lista de
    tramos (texto, dict de estilo) con claves opcionales: negrita, cursiva, color, fuente, tam.
    Con vinetas=True cada párrafo lleva una viñeta "•" con sangría francesa.
    sangria_francesa: px de sangría francesa sin viñeta (lista de referencias APA).
    """
    caja = lamina.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = caja.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"arriba": MSO_ANCHOR.TOP, "medio": MSO_ANCHOR.MIDDLE, "abajo": MSO_ANCHOR.BOTTOM}[anclar]
    if isinstance(parrafos, str):
        parrafos = [parrafos]
    for i, par in enumerate(parrafos):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"izq": PP_ALIGN.LEFT, "der": PP_ALIGN.RIGHT, "centro": PP_ALIGN.CENTER}[alinear]
        if interlineado:   # interlineado exacto: 1.0 = tamaño de la letra (no el "sencillo" de la fuente)
            p.line_spacing = pt(tam * interlineado)
        if espacio_despues:
            p.space_after = pt(espacio_despues)
        tramos = [(par, {})] if isinstance(par, str) else par
        if vinetas:
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(px(11)))
            pPr.set("indent", str(-px(11)))
            bu = etree.SubElement(pPr, qn("a:buChar"))
            bu.set("char", "•")
        elif sangria_francesa:
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(px(sangria_francesa)))
            pPr.set("indent", str(-px(sangria_francesa)))
        for contenido, estilo in tramos:
            r = p.add_run()
            r.text = contenido.upper() if mayusculas else contenido
            f = r.font
            f.name = estilo.get("fuente", fuente)
            f.size = pt(estilo.get("tam", tam))
            f.bold = estilo.get("negrita", negrita)
            f.italic = estilo.get("cursiva", False)
            f.color.rgb = rgb(estilo.get("color", color))
    return caja


def imagen(lamina, ruta, x, y, w, h, alinear="izq", recortar=False):
    """Inserta una imagen ajustada (sin deformar) dentro de la caja x, y, w, h.

    recortar=True quita el margen blanco de la imagen (las capturas de tablas traen mucho) para que se vea más grande.
    """
    from PIL import Image, ImageChops
    if recortar:
        with Image.open(ruta) as im:
            rgb = im.convert("RGB")
            caja = ImageChops.difference(rgb, Image.new("RGB", rgb.size, "white")).getbbox()
            if caja:
                m = 12
                caja = (max(caja[0] - m, 0), max(caja[1] - m, 0), min(caja[2] + m, rgb.width), min(caja[3] + m, rgb.height))
                destino = Path(__file__).resolve().parent / "salida" / "recortes"
                destino.mkdir(parents=True, exist_ok=True)
                ruta = destino / Path(ruta).name
                rgb.crop(caja).save(ruta)
    with Image.open(ruta) as im:
        iw, ih = im.size
    escala = min(w / iw, h / ih)
    ancho, alto = iw * escala, ih * escala
    dx = 0 if alinear == "izq" else (w - ancho) / 2
    return lamina.shapes.add_picture(str(ruta), px(x + dx), px(y), px(ancho), px(alto))


def marcador(lamina, x, y, w, h, mensaje):
    """Caja de contenido pendiente (placeholder) en gris de ventana, texto negro."""
    rect(lamina, x, y, w, h, GRIS_VENTANA)
    texto(lamina, x + 12, y + 10, w - 24, h - 20,
          [[("Pendiente  ", {"negrita": True}), (mensaje, {})]], tam=12, anclar="medio")


# ------------------------------------------------------------------ elementos de cada lámina de contenido
def pestana(lamina, seccion):
    s = SECCIONES[seccion]
    rect(lamina, MARGEN, 0, 196, 24, s["fondo"])
    texto(lamina, MARGEN + 10, 0, 180, 24, s["etiqueta"], tam=12, negrita=True, color=s["texto"], anclar="medio")


def pie(lamina, numero):
    texto(lamina, ANCHO - MARGEN - 60, 512, 60, 14, str(numero), tam=10, fuente=NOTA, color=GRIS_PIE, alinear="der")


def titular(lamina, x, y, w, contenido, tam=42, h=None):
    return texto(lamina, x, y, w, h or tam * 3.2, contenido, tam=tam, fuente=TITULAR, interlineado=1.0)


def columnas_cuerpo(lamina, y, izquierda, derecha, x=COL_IZQ_X, w=COL_IZQ_W, h=None, tam=12):
    """Dos columnas de texto del cuerpo (listas de párrafos). Un párrafo que empieza con '## ' va en negrita."""
    ancho = (w - 20) / 2
    for i, col in enumerate((izquierda, derecha)):
        pars = []
        for p in col:
            if isinstance(p, str) and p.startswith("## "):
                pars.append([(p[3:], {"negrita": True})])
            else:
                pars.append(p)
        texto(lamina, x + i * (ancho + 20), y, ancho, h or (BASE - y), pars, tam=tam, espacio_despues=6)


def nota_fuente(lamina, x, y, w, fuente, h=30):
    if not fuente:
        return
    texto(lamina, x, y, w, h, [[(fuente, {})]],
          tam=10, fuente=NOTA, interlineado=1.0)


def cita_pie(lamina, cita):
    """Cita corta al pie, abajo a la izquierda: gris, ~9,5 pt (formato de la minuta 2)."""
    if not cita:
        return
    texto(lamina, MARGEN, 484, 800, 42, [[(cita, {})]], tam=12.5, fuente=NOTA, color=GRIS_PIE,
          interlineado=1.0, anclar="abajo")


def lectura(lamina, x, y, w, mensaje, h=32):
    texto(lamina, x, y, w, h, [[(ETIQUETA_LECTURA + " ", {"negrita": True}), (mensaje, {})]], tam=11.5)


def caja_implicaciones(lamina, x, y, w, h, seccion, vinetas, titulo=TITULO_IMPLICACIONES):
    s = SECCIONES[seccion]
    rect(lamina, x, y, w, h, s["tinte"])
    rect(lamina, x, y, w, 9, s["fondo"])
    texto(lamina, x + 12, y + 17, w - 24, 20, titulo, tam=14, negrita=True)
    texto(lamina, x + 12, y + 39, w - 24, h - 45, vinetas[:2], tam=11.5, vinetas=True, espacio_despues=3)


def exhibicion(lamina, seccion, titulo, subtitulo, grafico, lectura_txt, fuente, implicaciones=None,
               x=EXH_X, y=TOPE, w=EXH_W, alto_grafico=None, dibujar_grafico=True):
    """Pila de la exhibición: título, subtítulo, gráfico, lectura, nota de fuente y caja de implicaciones."""
    alto_caja = 100 if implicaciones else 0
    if alto_grafico is None:
        alto_grafico = (BASE - y) - 20 - 18 - 36 - 34 - (alto_caja + 8 if implicaciones else 0) - 8
    texto(lamina, x, y, w, 20, titulo, tam=15, fuente=TITULAR)
    lineas_sub = 1 if len(subtitulo) * 6.2 < w else 2      # estimación del ancho de Onest a 12 px
    texto(lamina, x, y + 20, w, 16 * lineas_sub, subtitulo, tam=12, interlineado=1.2)
    gy = y + 28 + 15 * lineas_sub
    if alto_grafico is not None:
        alto_grafico -= 15 * (lineas_sub - 1)
    if not dibujar_grafico:
        pass
    elif grafico is not None and Path(grafico).exists():
        imagen(lamina, grafico, x, gy, w, alto_grafico)
    else:
        marcador(lamina, x, gy, w, alto_grafico, f"generar {Path(str(grafico)).name if grafico else 'gráfico'}")
    ly = gy + alto_grafico + 6
    lectura(lamina, x, ly, w, lectura_txt)
    nota_fuente(lamina, x, ly + 34, w, fuente)
    if implicaciones:
        caja_implicaciones(lamina, x, BASE - alto_caja, w, alto_caja, seccion, implicaciones)


def medidor(lamina, x, y, valor, previo=None, celda=14, hueco=2, alto=12, alto_centro=18):
    """Medidor de convicción de siete celdas (-3 .. +3). La celda central es más alta.

    valor < 0 -> celda activa rosada; 0 -> gris #595959; > 0 -> amarilla. Punto negro en la valoración previa.
    """
    for i, v in enumerate(range(-3, 4)):
        cx = x + i * (celda + hueco)
        h = alto_centro if v == 0 else alto
        cy = y + (alto_centro - h) / 2
        color = GRIS_REJILLA
        if v == valor:
            color = ROSADO if v < 0 else (GRIS_NEUTRO if v == 0 else AMARILLO)
        rect(lamina, cx, cy, celda, h, color)
        if previo is not None and v == previo:
            ovalo(lamina, cx + celda / 2 - 3, cy + h / 2 - 3, 6, NEGRO)
    etiqueta = "Neutral" if valor == 0 else f"{valor:+d}"
    ax = x + (valor + 3) * (celda + hueco) + celda / 2
    texto(lamina, ax - 30, y + alto_centro + 1, 60, 12, etiqueta, tam=10, negrita=True, alinear="centro")
    return 7 * celda + 6 * hueco
