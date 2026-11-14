"""Corre los datos de ejemplo de datos/ en Python y R y exige que den el mismo óptimo."""
import pytest

from conftest import RAIZ, RSCRIPT, ejecutar
from run_all import PROBLEMAS, coinciden


@pytest.mark.skipif(RSCRIPT is None, reason="Rscript no está instalado")
@pytest.mark.parametrize("problema", list(PROBLEMAS))
def test_python_y_r_coinciden_en_los_ejemplos(tmp_path, problema):
    origen = RAIZ / "datos" / f"{problema}.yaml"
    py = ejecutar(tmp_path, problema, origen, "python", copiar_yaml=True)
    r = ejecutar(tmp_path, problema, origen, "r", copiar_yaml=True)
    assert py["estado"] == r["estado"] == "Optimal"
    assert coinciden(py["valor_objetivo"], r["valor_objetivo"])
    assert py["ajustes"] and r["ajustes"] if problema in ("transporte", "asignacion", "transbordo_desbalanceado") else True


@pytest.mark.parametrize("problema", list(PROBLEMAS))
def test_ejemplos_python_tienen_verificacion_interna(tmp_path, problema):
    res = ejecutar(tmp_path, problema, RAIZ / "datos" / f"{problema}.yaml", "python", copiar_yaml=True)
    if problema in ("transporte",):
        assert res["verificacion"] is None
    else:
        assert res["verificacion"]["coincide"] is True


def test_coinciden_usa_tolerancia():
    assert coinciden(100.0, 100.0 + 1e-9)
    assert not coinciden(100.0, 100.5)
    assert not coinciden(None, 1.0)
