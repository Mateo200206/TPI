import pandas as pd
import pytest

from supermercado import (
    calcular_importe,
    resumen_por_producto,
    resumen_por_sucursal,
    resumen_general,
    ev_ingreso_x_sucu,
    bubble_sort,
)


@pytest.fixture
def df_base():
    df = pd.DataFrame({
        "PRSUC":  [1, 1, 1, 2, 2],
        "PRCOD":  [100, 100, 200, 100, 300],
        "PRCANT": [2, 3, 1, 5, 2],
        "PRPRE":  [50.0, 50.0, 100.0, 50.0, 30.0],
    })
    return calcular_importe(df)


# 1) Calculo de totales (importe = cantidad * precio)
def test_calcular_importe(df_base):
    assert list(df_base["PRIMPORTE"]) == [100.0, 150.0, 100.0, 250.0, 60.0]


# 2) Resumen por producto agrupa unidades e importe
def test_resumen_por_producto(df_base):
    res = resumen_por_producto(df_base)
    fila = res[(res["PRSUC"] == 1) & (res["PRCOD"] == 100)].iloc[0]
    assert fila["TOTUNI"] == 5
    assert fila["TOTPES"] == 250.0


# 3) Producto mas vendido (mayor importe) por sucursal
def test_producto_mas_vendido(df_base):
    res = resumen_por_sucursal(df_base)
    suc1 = res[res["PRSUC"] == 1].iloc[0]
    assert suc1["MYPROD"] == 100   # 250 > 100
    assert suc1["MNPROD"] == 200


# 4) Resumen general: cantidad de sucursales e importe total
def test_resumen_general(df_base):
    g = resumen_general(df_base)
    assert g["CANSUC"] == 2
    assert g["TOTALIMP"] == 660.0


# 5) Validacion: operacion invalida debe lanzar ValueError
def test_operacion_invalida(df_base):
    with pytest.raises(ValueError):
        ev_ingreso_x_sucu(df_base, 1, 100.0, operacion="potencia")


# 6) Manejo de datos: division por cero predicho -> None
def test_division_por_cero(df_base):
    r = ev_ingreso_x_sucu(df_base, 1, 0.0, operacion="division")
    assert r["RESULTADO_OPERACION"] is None


# 7) bubble_sort ordena por la columna indicada
def test_bubble_sort():
    data = [[3, "c"], [1, "a"], [2, "b"]]
    assert bubble_sort(data, 0) == [[1, "a"], [2, "b"], [3, "c"]]
