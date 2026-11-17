"""Fragmentos de código como imagen estilo carbon.now.sh: ventana oscura con los tres botones de macOS.

- Fuente: JetBrains Mono (presentacion/fuentes/).
- Colores: solo la paleta del tema (ver DESIGN.md, sección "Ventanas de código").
- Sin esquinas redondeadas ni sombra: el diseño de la presentación los prohíbe.

La imagen se dibuja al tamaño exacto que ocupa en la lámina (en px de lámina) multiplicado por ESCALA,
así el tamaño de letra en la lámina es el mismo que se pide aquí (tam_px).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import PythonLexer, SLexer, TextLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text, Token

FUENTES = Path(__file__).resolve().parent / "fuentes"
ESCALA = 4   # 4 px de imagen por px de lámina (~384 ppp al tamaño real)

# ------------------------------------------------------------------ paleta (la misma de tema.py)
FONDO = "#000000"
BARRA = "#000000"
TEXTO = "#ffffff"
TEXTO_SUAVE = "#d6d5dd"       # operadores y puntuación
COMENTARIO = "#8a8a8a"
BERMELLON = "#ff4713"         # palabras clave
AMARILLO = "#ffce00"          # funciones y llamadas
ROSADO = "#fc9bb3"            # cadenas de texto
VERDE = "#008b5c"             # números
TITULO = "#8a8a8a"            # nombre del archivo en la barra
BOTONES = (BERMELLON, AMARILLO, VERDE)   # cerrar, minimizar, maximizar (versión de la paleta)

COLORES = [   # el primer prefijo de token que coincida gana
    (Comment, COMENTARIO),
    (String, ROSADO),
    (Number, VERDE),
    (Keyword, BERMELLON),
    (Operator.Word, BERMELLON),        # and, or, not, in
    (Name.Builtin.Pseudo, BERMELLON),  # self, True...
    (Name.Builtin, AMARILLO),
    (Name.Function, AMARILLO),
    (Name.Class, AMARILLO),
    (Name.Decorator, AMARILLO),
    (Operator, TEXTO_SUAVE),
    (Punctuation, TEXTO_SUAVE),
]
LEXERS = {"python": PythonLexer, "r": SLexer, "consola": TextLexer}

# Sin ligaduras: "<-" y ">=" se ven tal como se escriben (con Pillow + libraqm; sin raqm no hay ligaduras de todos modos).
try:
    from PIL import features as _features
    SIN_LIGADURAS = {"features": ["-liga", "-calt"]} if _features.check("raqm") else {}
except Exception:
    SIN_LIGADURAS = {}


def _fuente(estilo, tam):
    archivo = {"normal": "JetBrainsMono-Regular.ttf", "negrita": "JetBrainsMono-Bold.ttf",
               "italica": "JetBrainsMono-Italic.ttf"}[estilo]
    return ImageFont.truetype(str(FUENTES / archivo), tam)


def _color(tipo):
    for prefijo, color in COLORES:
        if tipo in prefijo:
            return color
    return TEXTO


def _tokens_por_linea(codigo, lenguaje):
    """Lista de líneas; cada línea es una lista de (texto, color, cursiva)."""
    tokens = list(lex(codigo, LEXERS[lenguaje]()))
    # Las llamadas (nombre seguido de "(") se pintan como funciones, igual que en Carbon.
    marcados = []
    for i, (tipo, valor) in enumerate(tokens):
        siguiente = next((v for t, v in tokens[i + 1:] if v.strip()), "")
        if tipo in Name and not (tipo in Name.Builtin) and siguiente.startswith("("):
            tipo = Name.Function
        marcados.append((tipo, valor))
    lineas = [[]]
    for tipo, valor in marcados:
        partes = valor.split("\n")
        for k, parte in enumerate(partes):
            if k > 0:
                lineas.append([])
            if parte:
                lineas[-1].append((parte, _color(tipo), tipo in Comment))
    if lineas and not lineas[-1]:
        lineas.pop()
    return lineas


def _envolver(linea, max_col):
    """Corta una línea larga en varias; la continuación lleva la sangría original + 4 espacios."""
    chars = [(c, color, it) for texto, color, it in linea for c in texto]
    if len(chars) <= max_col:
        return [linea]
    sangria = len("".join(c for c, _, _ in chars)) - len("".join(c for c, _, _ in chars).lstrip())
    prefijo = " " * min(sangria + 4, max_col // 2)
    salida, actual = [], chars
    primera = True
    while actual:
        limite = max_col if primera else max_col - len(prefijo)
        if len(actual) <= limite:
            corte = len(actual)
        else:
            espacio = max((i for i in range(limite // 2, limite) if actual[i][0] == " "), default=None)
            corte = espacio + 1 if espacio is not None else limite   # corta después del último espacio
        trozo, actual = actual[:corte], actual[corte:]
        if not primera:
            trozo = [(c, TEXTO, False) for c in prefijo] + trozo
        salida.append(_agrupar(trozo))
        primera = False
    return salida


def _agrupar(chars):
    grupos = []
    for c, color, it in chars:
        if grupos and grupos[-1][1] == color and grupos[-1][2] == it:
            grupos[-1][0] += c
        else:
            grupos.append([c, color, it])
    return [tuple(g) for g in grupos]


def _lineas_necesarias(codigo, lenguaje, ancho, tam):
    ancho_char = _fuente("normal", round(tam * ESCALA)).getlength("M") / ESCALA
    max_col = max(20, int((ancho - 32) / ancho_char))
    return sum(len(_envolver(l, max_col)) for l in _tokens_por_linea(codigo, lenguaje))


def ventana(codigo, ruta_png, ancho, alto=None, lenguaje="python", titulo="", tam=10.0, interlineado=1.45,
            aviso_corte="# ... (continúa en el script)"):
    """Dibuja la ventana y la guarda en ruta_png. ancho/alto/tam en px de lámina.

    alto=None ajusta la ventana al contenido; con alto fijo, las líneas que no caben se cortan y la
    última se reemplaza por aviso_corte. Devuelve (ancho, alto) en px de lámina.
    """
    if isinstance(codigo, (list, tuple)):
        codigo = "\n".join(codigo)
    if isinstance(tam, tuple):   # (mínimo, máximo): la letra más grande con la que cabe todo el fragmento
        tam_min, tam_max = tam
        tam = tam_min
        t = tam_max
        while t >= tam_min:
            if alto is None or _lineas_necesarias(codigo, lenguaje, ancho, t) * t * interlineado <= alto - 26 - 20:
                tam = t
                break
            t -= 0.5
    e = ESCALA
    barra, pad_x, pad_y = 26, 16, 10
    f_normal, f_italica = _fuente("normal", round(tam * e)), _fuente("italica", round(tam * e))
    ancho_char = f_normal.getlength("M") / e
    max_col = max(20, int((ancho - 2 * pad_x) / ancho_char))
    alto_linea = tam * interlineado

    lineas = []
    for linea in _tokens_por_linea(codigo, lenguaje):
        lineas.extend(_envolver(linea, max_col))
    if alto is not None:
        caben = int((alto - barra - 2 * pad_y) / alto_linea)
        if len(lineas) > caben:
            lineas = lineas[:caben - 1] + [[(aviso_corte, COMENTARIO, True)]]
    else:
        alto = barra + 2 * pad_y + len(lineas) * alto_linea

    img = Image.new("RGB", (round(ancho * e), round(alto * e)), FONDO)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, barra * e], fill=BARRA)
    for i, color in enumerate(BOTONES):   # los tres botones de la ventana de macOS
        cx, cy, r = (16 + i * 16) * e, (barra / 2 + 1) * e, 5 * e
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    if titulo:
        f_titulo = _fuente("normal", round(9 * e))
        d.text(((16 + 3 * 16 + 4) * e, (barra / 2 + 1) * e), titulo, font=f_titulo, fill=TITULO, anchor="lm")

    y = (barra + pad_y) * e
    for linea in lineas:
        x = pad_x * e
        for texto, color, italica in linea:
            fuente = f_italica if italica else f_normal
            d.text((x, y + alto_linea * e / 2), texto, font=fuente, fill=color, anchor="lm", **SIN_LIGADURAS)
            x += fuente.getlength(texto, **SIN_LIGADURAS)
        y += alto_linea * e
    Path(ruta_png).parent.mkdir(parents=True, exist_ok=True)
    img.save(ruta_png, dpi=(96 * e, 96 * e))
    return ancho, alto
