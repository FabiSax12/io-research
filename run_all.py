"""Corre los problemas en Python y en R y compara los resultados.

    python run_all.py                  # todo
    python run_all.py transporte       # solo uno (o varios: python run_all.py pl ple)

Problemas: pl, ple, transporte, asignacion, transbordo, transbordo_desbalanceado.
Guarda la salida de consola en capturas/<problema>_<python|r>.txt y los JSON en resultados/.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PROBLEMAS = {  # nombre del problema (= nombre del YAML) -> (carpeta, nombre del script)
    "pl": ("parte1", "pl"),
    "ple": ("parte1", "ple"),
    "transporte": ("parte1", "transporte"),
    "asignacion": ("parte1", "asignacion"),
    "transbordo": ("parte2", "transbordo"),
    "transbordo_desbalanceado": ("parte2", "transbordo"),  # mismo script, otro YAML
}
TOLERANCIA = 1e-6


def buscar_rscript():
    """Rscript del PATH o, si no está, de las rutas típicas de Windows, macOS y Linux."""
    encontrado = shutil.which("Rscript")
    if encontrado:
        return encontrado
    candidatos = []
    if os.name == "nt":
        for var in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            base = os.environ.get(var)
            if base:
                for sub in ("R", "Programs/R"):
                    candidatos += list(Path(base, sub).glob("R-*/bin/Rscript.exe"))
                    candidatos += list(Path(base, sub).glob("R-*/bin/x64/Rscript.exe"))
        version = lambda p: [int(x) for x in re.findall(r"R-(\d+(?:\.\d+)*)", str(p))[0].split(".")]
        candidatos.sort(key=version, reverse=True)  # la versión más reciente primero
    else:
        candidatos = [Path(p) for p in ("/usr/local/bin/Rscript", "/opt/homebrew/bin/Rscript", "/usr/bin/Rscript",
                                        "/Library/Frameworks/R.framework/Resources/bin/Rscript")]
    return next((str(c) for c in candidatos if c.exists()), None)


def coinciden(a, b, tolerancia=TOLERANCIA):
    """True si ambos valores existen y son iguales dentro de la tolerancia (relativa para valores grandes)."""
    return a is not None and b is not None and abs(a - b) <= tolerancia * max(1.0, abs(a), abs(b))


def es_ejemplo(problema):
    """True si el YAML todavía tiene la marca '# EJEMPLO' al inicio."""
    with open(RAIZ / "datos" / f"{problema}.yaml", encoding="utf-8") as f:
        return any(linea.startswith("# EJEMPLO") for _, linea in zip(range(5), f))


def correr(problema, lenguaje, rscript):
    """Ejecuta un script, guarda su consola en capturas/*.txt y devuelve (código, JSON o None)."""
    carpeta, script = PROBLEMAS[problema]
    argumentos = [problema] if carpeta == "parte2" else []  # el transbordo recibe el nombre del YAML
    if lenguaje == "python":
        comando = [sys.executable, str(RAIZ / carpeta / "python" / f"{script}.py")]
    else:
        comando = [rscript, str(RAIZ / carpeta / "r" / f"{script}.R")]
    json_ruta = RAIZ / "resultados" / f"{problema}_{lenguaje}.json"
    json_ruta.unlink(missing_ok=True)  # evita comparar con un resultado viejo si esta corrida falla
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    proceso = subprocess.run(comando + argumentos, cwd=RAIZ, capture_output=True, env=env)
    texto = (proceso.stdout + proceso.stderr).decode("utf-8", errors="replace")
    salida = RAIZ / "capturas" / f"{problema}_{lenguaje}.txt"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text(texto, encoding="utf-8")
    resultado = json.loads(json_ruta.read_text(encoding="utf-8")) if proceso.returncode == 0 and json_ruta.exists() else None
    return proceso.returncode, texto, resultado


def numero(v):
    return f"{v:.6g}" if isinstance(v, (int, float)) else str(v)


def marca(ok):
    return "-" if ok is None else ("sí" if ok else "NO")


def imprimir_tabla(filas):
    encabezado = ["Problema", "Óptimo Python", "Óptimo R", "Py = R", "Verif. Python", "Verif. R"]
    todas = [encabezado] + filas
    anchos = [max(len(str(f[i])) for f in todas) for i in range(len(encabezado))]
    linea = "-+-".join("-" * a for a in anchos)
    print("\n" + " | ".join(h.ljust(a) for h, a in zip(encabezado, anchos)))
    print(linea)
    for f in filas:
        print(" | ".join(str(c).ljust(a) for c, a in zip(f, anchos)))
    print("\nVerif.: PL = SciPy linprog, PLE = SciPy milp, asignación = PuLP, transbordo = modelo de red vs modelo con buffer.")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    pedidos = sys.argv[1:] or list(PROBLEMAS)
    desconocidos = [p for p in pedidos if p not in PROBLEMAS]
    if desconocidos:
        sys.exit(f"Problema(s) desconocido(s): {', '.join(desconocidos)}. Opciones: {', '.join(PROBLEMAS)}")

    for p in pedidos:
        if es_ejemplo(p):
            print(f"ADVERTENCIA: datos/{p}.yaml todavía tiene datos de EJEMPLO (reemplazar por el problema del grupo).")

    rscript = buscar_rscript()
    if rscript is None:
        print("\nERROR: no se encontró Rscript. Instalar R (https://cran.r-project.org) y agregarlo al PATH,\n"
              "o instalarlo en la ruta por defecto (Windows: C:\\Program Files\\R\\R-x.y.z). "
              "Se corre solo la parte de Python.\n")

    filas, hay_error = [], False
    for problema in pedidos:
        resultados = {}
        for lenguaje in ("python", "r"):
            if lenguaje == "r" and rscript is None:
                resultados[lenguaje] = None
                continue
            print(f"\n##### {problema} ({lenguaje})")
            codigo, texto, resultado = correr(problema, lenguaje, rscript)
            print(texto.rstrip())
            if codigo != 0 or resultado is None:
                print(f"!!! Falló {problema} en {lenguaje} (código {codigo}); ver capturas/{problema}_{lenguaje}.txt")
            resultados[lenguaje] = resultado

        py, r = resultados["python"], resultados["r"]
        vp, vr = (py or {}).get("valor_objetivo"), (r or {}).get("valor_objetivo")
        igual = coinciden(vp, vr) if r is not None else None   # sin R no hay comparación
        verif = lambda x: None if not x or not x.get("verificacion") else x["verificacion"]["coincide"]
        filas.append([problema, "falló" if py is None else numero(vp if vp is not None else "n/d"),
                      "n/d" if r is None else numero(vr if vr is not None else "n/d"), marca(igual), marca(verif(py)), marca(verif(r))])
        hay_error |= r is None or py is None or not igual or verif(py) is False or verif(r) is False

    imprimir_tabla(filas)
    sys.exit(1 if hay_error else 0)


if __name__ == "__main__":
    main()
