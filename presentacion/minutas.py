"""Lee las minutas de minutas/ con la estructura de plantilla.md.

Cada minuta queda como un dict:
    numero, tema, curso, fecha, inicio, fin,
    presentes   [(asistio, nombre)],
    agenda      [texto],
    anotaciones y acuerdos   [item],   item = {"nivel": 0|1, "tramos": [(texto, negrita)]} o {"tabla": [[celda]]},
    cronograma  [[actividad, plazo, responsable, condicion]]  (sin filas vacías).
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "minutas"


def tramos(texto):
    """Separa **negrita** del resto; quita la cursiva (*x*) y el código (`x`), que el tema no usa."""
    texto = re.sub(r"(?<!\*)\*(?!\*)([^*]+)(?<!\*)\*(?!\*)", r"\1", texto).replace("`", "")
    partes = re.split(r"\*\*(.+?)\*\*", texto)
    return [(p, i % 2 == 1) for i, p in enumerate(partes) if p]


def _celdas(linea):
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def _es_separador(celdas):
    return all(re.fullmatch(r":?-{2,}:?", c) for c in celdas if c)


def _tabla(lineas):
    """Filas de una tabla markdown sin la línea de guiones; encabezado incluido."""
    filas = [_celdas(l) for l in lineas]
    return [f for f in filas if not _es_separador(f)]


def _items(lineas):
    """Viñetas (con un nivel de sub-viñetas), líneas de continuación y tablas de una sección."""
    items, bloque_tabla = [], []
    for linea in lineas + [""]:
        if linea.strip().startswith("|"):
            bloque_tabla.append(linea)
            continue
        if bloque_tabla:
            items.append({"tabla": _tabla(bloque_tabla)})
            bloque_tabla = []
        v = re.match(r"^(\s*)- (.+)$", linea)
        if v:
            items.append({"nivel": 1 if len(v.group(1)) >= 2 else 0, "texto": v.group(2).strip()})
        elif linea.strip() and items and "texto" in items[-1]:     # continuación de la viñeta anterior
            items[-1]["texto"] += " " + linea.strip()
    for it in items:
        if "texto" in it:
            it["tramos"] = tramos(it.pop("texto"))
    return items


def leer(ruta):
    t = Path(ruta).read_text(encoding="utf-8")
    secciones = {}
    for bloque in re.split(r"^## ", t, flags=re.M)[1:]:
        titulo, _, cuerpo = bloque.partition("\n")
        secciones[titulo.strip()] = cuerpo.splitlines()
    titulo = re.search(r"^# (.+)$", t, flags=re.M).group(1)
    campo = lambda nombre: (re.search(rf"\*\*{nombre}:\*\*\s*(.+)", t) or [None, ""])[1].strip()
    cronograma = [f for f in _tabla([l for l in secciones.get("Cronograma", []) if l.strip().startswith("|")])[1:]
                  if any(f)]
    return {
        "numero": int(re.findall(r"\d+", Path(ruta).stem)[0]),
        "tema": titulo.split(":", 1)[1].strip() if ":" in titulo else titulo,
        "curso": campo("Curso"), "fecha": campo("Fecha"),
        "inicio": campo("Hora de inicio"), "fin": campo("Hora de finalización"),
        "presentes": [(m[1].lower() == "x", m[2].strip()) for l in secciones.get("Presentes", [])
                      if (m := re.match(r"^- \[([ xX])\] (.+)$", l))],
        "agenda": [m[1].strip() for l in secciones.get("Agenda tratada", []) if (m := re.match(r"^\d+\.\s+(.+)$", l))],
        "anotaciones": _items(secciones.get("Anotaciones importantes", [])),
        "acuerdos": _items(secciones.get("Resumen de acuerdos", [])),
        "cronograma": cronograma,
    }


def leer_todas():
    """Todas las minuta_N.md de la carpeta, ordenadas por número (la plantilla no se incluye)."""
    rutas = sorted(CARPETA.glob("minuta_*.md"), key=lambda p: int(re.findall(r"\d+", p.stem)[0]))
    return [leer(r) for r in rutas]
