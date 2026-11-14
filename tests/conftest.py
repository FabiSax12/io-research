"""Ayudas para los tests: corren los scripts reales sobre datos temporales (variable IO_DIR)."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from run_all import PROBLEMAS, buscar_rscript  # noqa: E402

RSCRIPT = buscar_rscript()
LENGUAJES = ["python", pytest.param("r", marks=pytest.mark.skipif(RSCRIPT is None, reason="Rscript no está instalado"))]


def ejecutar(tmp_path, problema, datos, lenguaje, copiar_yaml=False):
    """Escribe datos/<problema>.yaml en tmp_path, corre el script y devuelve el JSON resultante.

    `datos` es un dict (se guarda como YAML). Con copiar_yaml=True `datos` es una ruta a un YAML existente.
    """
    (tmp_path / "datos").mkdir(exist_ok=True)
    destino = tmp_path / "datos" / f"{problema}.yaml"
    if copiar_yaml:
        destino.write_bytes(Path(datos).read_bytes())
    else:
        destino.write_text(yaml.safe_dump(datos, allow_unicode=True, sort_keys=False), encoding="utf-8")
    carpeta, script = PROBLEMAS[problema]
    if lenguaje == "python":
        comando = [sys.executable, str(RAIZ / carpeta / "python" / f"{script}.py")]
    else:
        comando = [RSCRIPT, str(RAIZ / carpeta / "r" / f"{script}.R")]
    if carpeta == "parte2":
        comando.append(problema)
    env = {**os.environ, "IO_DIR": str(tmp_path), "PYTHONUTF8": "1"}
    proceso = subprocess.run(comando, capture_output=True, env=env, timeout=180)
    salida = (proceso.stdout + proceso.stderr).decode("utf-8", errors="replace")
    assert proceso.returncode == 0, f"{lenguaje}/{problema} falló:\n{salida}"
    resultado = json.loads((tmp_path / "resultados" / f"{problema}_{lenguaje}.json").read_text(encoding="utf-8"))
    resultado["_consola"] = salida
    return resultado


def distintas_de_cero(resultado):
    """Variables con valor distinto de cero, redondeadas, para comparar con lo esperado."""
    return {k: round(v, 6) for k, v in resultado["variables"].items() if v is not None and abs(v) > 1e-9}
