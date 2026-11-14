"""Parte II: transbordo. Red P -> T -> D con un arco directo P -> D más caro (7 contra 2 + 3)."""
import csv

import pytest
from openpyxl import load_workbook

from conftest import LENGUAJES, distintas_de_cero, ejecutar


def red(oferta, demanda, arcos=None):
    arcos = arcos if arcos is not None else [("P", "T", 2), ("T", "D", 3), ("P", "D", 7)]
    return {"nombre": "t",
            "nodos": [{"nombre": "P", "tipo": "origen", "oferta": oferta},
                      {"nombre": "T", "tipo": "transbordo"},
                      {"nombre": "D", "tipo": "destino", "demanda": demanda}],
            "arcos": [{"desde": a, "hasta": b, "costo": c} for a, b, c in arcos]}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_transbordo_balanceado_red_y_buffer_coinciden(tmp_path, lenguaje):
    # Por T cuesta 2 + 3 = 5 por unidad (el directo cuesta 7): 10 unidades -> 50
    res = ejecutar(tmp_path, "transbordo", red(10, 10), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(50)
    assert res["verificacion"]["valor"] == pytest.approx(50)
    assert res["verificacion"]["coincide"] is True
    assert distintas_de_cero(res) == {"P->T": 10, "T->D": 10}
    assert res["ajustes"] == []
    # buffer B = 10; cota = 10 * (3 - 1) * 7 = 140, así que M = 1000
    assert res["buffer"] == {"B": 10, "M": 1000}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_transbordo_sobra_oferta_agrega_destino_ficticio(tmp_path, lenguaje):
    # oferta 10 > demanda 6: 6 * 5 = 30 y los 4 sobrantes van al destino ficticio a costo 0
    res = ejecutar(tmp_path, "transbordo", red(10, 6), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(30)
    assert res["verificacion"]["coincide"] is True
    assert distintas_de_cero(res) == {"P->T": 6, "T->D": 6, "P->Ficticio": 4}
    assert len(res["ajustes"]) == 1 and "Ficticio" in res["ajustes"][0]


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_transbordo_falta_oferta_agrega_origen_ficticio(tmp_path, lenguaje):
    # oferta 6 < demanda 10: 6 * 5 = 30 y el origen ficticio cubre 4 unidades a costo 0
    res = ejecutar(tmp_path, "transbordo", red(6, 10), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(30)
    assert res["verificacion"]["coincide"] is True
    assert distintas_de_cero(res) == {"P->T": 6, "T->D": 6, "Ficticio->D": 4}
    assert "Ficticio" in res["ajustes"][0]


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_transbordo_sin_camino_es_infactible(tmp_path, lenguaje):
    # No hay ruta hacia D: ambos modelos deben decir que no hay solución (el buffer tendría que usar M)
    res = ejecutar(tmp_path, "transbordo", red(10, 10, arcos=[("P", "T", 2)]), lenguaje)
    assert res["estado"] == "Infeasible"
    assert res["valor_objetivo"] is None


def test_transbordo_python_genera_matriz_excel_y_diagrama(tmp_path):
    ejecutar(tmp_path, "transbordo", red(10, 6), "python")
    capturas = tmp_path / "capturas"
    assert (capturas / "transbordo_red.png").stat().st_size > 0
    assert (capturas / "transbordo_matriz_python.png").stat().st_size > 0

    with open(capturas / "transbordo_matriz_python.csv", encoding="utf-8-sig", newline="") as f:
        filas = list(csv.reader(f))
    assert filas[0] == ["De / A", "P", "T", "D", "Ficticio", "Oferta"]
    assert filas[1] == ["P", "0", "2", "7", "0", "20"]                 # P: B = 10, oferta 10 + 10
    assert filas[2] == ["T", "M", "0", "3", "M", "10"]                 # arcos que no existen = M
    assert filas[-1] == ["Demanda", "10", "10", "16", "14", ""]        # demanda + B (D = 6 + 10, Ficticio = 4 + 10)

    wb = load_workbook(tmp_path / "parte2" / "solver" / "transbordo.xlsx")
    assert wb.sheetnames == ["Modelo", "Instrucciones"]
    hoja = wb["Modelo"]
    formulas = [c.value for fila in hoja.iter_rows() for c in fila if isinstance(c.value, str) and c.value.startswith("=")]
    assert any(f.startswith("=SUMPRODUCT(") for f in formulas)
    assert "=$B$3" in formulas                                          # los M apuntan a la celda de M
    instrucciones = "\n".join(str(c.value) for fila in wb["Instrucciones"].iter_rows() for c in fila if c.value)
    for texto in ("Simplex LP", "no negativas", "Mín", "Establecer objetivo", "Cambiando las celdas de variables"):
        assert texto in instrucciones
