"""Parte I. Los valores esperados se calcularon a mano (ver el comentario de cada caso)."""
import pytest

from conftest import LENGUAJES, distintas_de_cero, ejecutar


def restr(coef, signo, rhs):
    return {"nombre": "r", "coef": coef, "signo": signo, "rhs": rhs}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_pl_maximizar(tmp_path, lenguaje):
    # max x + 2y  s.a. x <= 3, y <= 2, x + y <= 4  ->  (2, 2), Z = 6
    datos = {"nombre": "t", "sentido": "max", "variables": ["x", "y"], "objetivo": [1, 2],
             "restricciones": [restr([1, 0], "<=", 3), restr([0, 1], "<=", 2), restr([1, 1], "<=", 4)]}
    res = ejecutar(tmp_path, "pl", datos, lenguaje)
    assert res["estado"] == "Optimal"
    assert res["valor_objetivo"] == pytest.approx(6)
    assert distintas_de_cero(res) == {"x": 2, "y": 2}
    if lenguaje == "python":
        assert res["verificacion"]["coincide"] is True  # SciPy linprog coincide con PuLP


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_pl_minimizar_con_igual_y_mayor_igual(tmp_path, lenguaje):
    # min x + y  s.a. x + y >= 4, x - y = 0, x <= 5  ->  (2, 2), Z = 4
    datos = {"nombre": "t", "sentido": "min", "variables": ["x", "y"], "objetivo": [1, 1],
             "restricciones": [restr([1, 1], ">=", 4), restr([1, -1], "=", 0), restr([1, 0], "<=", 5)]}
    res = ejecutar(tmp_path, "pl", datos, lenguaje)
    assert res["valor_objetivo"] == pytest.approx(4)
    assert distintas_de_cero(res) == {"x": 2, "y": 2}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_pl_infactible(tmp_path, lenguaje):
    # x <= 1 y x >= 3 no se pueden cumplir a la vez
    datos = {"nombre": "t", "sentido": "max", "variables": ["x"], "objetivo": [1],
             "restricciones": [restr([1], "<=", 1), restr([1], ">=", 3), restr([1], "<=", 10)]}
    res = ejecutar(tmp_path, "pl", datos, lenguaje)
    assert res["estado"] == "Infeasible"
    assert res["valor_objetivo"] is None


ENTERO = {"nombre": "t", "sentido": "max", "variables": ["x", "y"], "objetivo": [5, 4],
          "restricciones": [restr([6, 4], "<=", 24), restr([1, 2], "<=", 6), restr([0, 1], "<=", 2)]}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_ple_todas_enteras(tmp_path, lenguaje):
    # La relajación lineal da (3; 1.5) con Z = 21. Con x, y enteras el óptimo es (4, 0), Z = 20
    # (se revisaron a mano (3,1)=19, (2,2)=18 y (4,0)=20; (4,1) viola la madera).
    res = ejecutar(tmp_path, "ple", {**ENTERO, "enteras": ["x", "y"]}, lenguaje)
    assert res["valor_objetivo"] == pytest.approx(20)
    assert distintas_de_cero(res) == {"x": 4}
    if lenguaje == "python":
        assert res["verificacion"]["coincide"] is True  # SciPy milp coincide con PuLP


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_ple_solo_algunas_enteras(tmp_path, lenguaje):
    # Con solo x entera, el óptimo de la relajación (3; 1.5) ya tiene x entera: Z = 21 y y sigue fraccionaria
    res = ejecutar(tmp_path, "ple", {**ENTERO, "enteras": ["x"]}, lenguaje)
    assert res["valor_objetivo"] == pytest.approx(21)
    assert distintas_de_cero(res) == {"x": 3, "y": 1.5}


# ----------------------------------------------------------------------------- Transporte
def transporte(oferta, demanda, costos):
    return {"nombre": "t", "origenes": [f"S{i + 1}" for i in range(len(oferta))],
            "destinos": [f"D{j + 1}" for j in range(len(demanda))],
            "oferta": oferta, "demanda": demanda, "costos": costos}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_transporte_2x2_balanceado(tmp_path, lenguaje):
    # Con t = envío S1->D2: costo = 85 + 4t, mínimo en t = 0: S1->D1 20, S2->D1 5, S2->D2 25, Z = 85
    res = ejecutar(tmp_path, "transporte", transporte([20, 30], [25, 25], [[2, 3], [4, 1]]), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(85)
    assert distintas_de_cero(res) == {"S1->D1": 20, "S2->D1": 5, "S2->D2": 25}
    assert res["ajustes"] == []


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_transporte_sobra_oferta_agrega_destino_ficticio(tmp_path, lenguaje):
    # oferta 50 > demanda 40: D1 se abastece desde S1 (costo 1), D2 desde S2 (costo 2); a S1 le sobran 10
    res = ejecutar(tmp_path, "transporte", transporte([30, 20], [20, 20], [[1, 4], [3, 2]]), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(60)
    assert distintas_de_cero(res) == {"S1->D1": 20, "S2->D2": 20, "S1->Ficticio": 10}
    assert len(res["ajustes"]) == 1 and "ficticio" in res["ajustes"][0].lower()


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_transporte_falta_oferta_agrega_origen_ficticio(tmp_path, lenguaje):
    # demanda 50 > oferta 40: el origen ficticio (costo 0) cubre 10 unidades de D1
    res = ejecutar(tmp_path, "transporte", transporte([20, 20], [30, 20], [[1, 4], [3, 2]]), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(60)
    assert distintas_de_cero(res) == {"S1->D1": 20, "S2->D2": 20, "Ficticio->D1": 10}
    assert len(res["ajustes"]) == 1 and "ficticio" in res["ajustes"][0].lower()


# ----------------------------------------------------------------------------- Asignación
def asignacion(matriz, sentido="min"):
    return {"nombre": "t", "sentido": sentido, "agentes": [f"A{i + 1}" for i in range(len(matriz))],
            "tareas": [f"T{j + 1}" for j in range(len(matriz[0]))], "matriz": matriz}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_asignacion_cuadrada(tmp_path, lenguaje):
    # La diagonal cuesta 1 y todo lo demás 9: óptimo A1->T1, A2->T2, A3->T3, Z = 3
    res = ejecutar(tmp_path, "asignacion", asignacion([[1, 9, 9], [9, 1, 9], [9, 9, 1]]), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(3)
    assert distintas_de_cero(res) == {"A1->T1": 1, "A2->T2": 1, "A3->T3": 1}
    assert res["ajustes"] == []
    if lenguaje == "python":
        assert res["verificacion"]["coincide"] is True


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_asignacion_mas_agentes_que_tareas_agrega_tarea_ficticia(tmp_path, lenguaje):
    # 3 agentes, 2 tareas: A1->T2 (1) + A2->T1 (2) = 3; A3 queda sin tarea (columna ficticia)
    res = ejecutar(tmp_path, "asignacion", asignacion([[4, 1], [2, 3], [5, 5]]), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(3)
    assert distintas_de_cero(res) == {"A1->T2": 1, "A2->T1": 1, "A3->Ficticio 1": 1}
    assert len(res["ajustes"]) == 1 and "ficticio" in res["ajustes"][0].lower()


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_asignacion_mas_tareas_que_agentes_agrega_agente_ficticio(tmp_path, lenguaje):
    # 2 agentes, 3 tareas: A1->T2 (1) + A2->T1 (2) = 3; T3 la hace el agente ficticio
    res = ejecutar(tmp_path, "asignacion", asignacion([[4, 1, 7], [2, 3, 6]]), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(3)
    assert distintas_de_cero(res) == {"A1->T2": 1, "A2->T1": 1, "Ficticio 1->T3": 1}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_asignacion_maximizar(tmp_path, lenguaje):
    # rendimientos [[5,1],[2,6]]: A1->T1 (5) + A2->T2 (6) = 11 contra 1 + 2 = 3 de la otra asignación
    res = ejecutar(tmp_path, "asignacion", asignacion([[5, 1], [2, 6]], "max"), lenguaje)
    assert res["valor_objetivo"] == pytest.approx(11)
    assert distintas_de_cero(res) == {"A1->T1": 1, "A2->T2": 1}


@pytest.mark.parametrize("lenguaje", LENGUAJES)
def test_pl_precios_sombra(tmp_path, lenguaje):
    # max x + 2y  s.a. x <= 3, y <= 2, x + y <= 4  ->  activas y <= 2 y x + y <= 4.
    # Duales: columna de x: y3 = 1; columna de y: y2 + y3 = 2 -> y2 = 1; x <= 3 tiene holgura -> y1 = 0.
    datos = {"nombre": "t", "sentido": "max", "variables": ["x", "y"], "objetivo": [1, 2],
             "restricciones": [restr([1, 0], "<=", 3), restr([0, 1], "<=", 2), restr([1, 1], "<=", 4)]}
    res = ejecutar(tmp_path, "pl", datos, lenguaje)
    assert res["precios_sombra"] == pytest.approx([0, 1, 1])
