#!/usr/bin/env python3
import pandas as pd


def leer_csv(path):
    return pd.read_csv(path)


def bubble_sort(data, col_index):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j][col_index] > data[j + 1][col_index]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def ordenar_por_sucursal(df):
    data = df.values.tolist()
    col_index = df.columns.get_loc("PRSUC")
    data_ordenada = bubble_sort(data, col_index)
    return pd.DataFrame(data_ordenada, columns=df.columns)


def calcular_importe(df):
    df = df.copy()
    df["PRIMPORTE"] = df["PRCANT"] * df["PRPRE"]
    return df


def resumen_por_producto(df):
    i, n = 0, len(df)
    resultados = []
    while i < n:
        sucursal = df.loc[i, "PRSUC"]
        producto = df.loc[i, "PRCOD"]
        totuni, totpeso = 0, 0
        while i < n and df.loc[i, "PRSUC"] == sucursal and df.loc[i, "PRCOD"] == producto:
            totuni  += df.loc[i, "PRCANT"]
            totpeso += df.loc[i, "PRIMPORTE"]
            i += 1
        resultados.append({"PRSUC": sucursal, "PRCOD": producto,
                            "TOTUNI": totuni, "TOTPES": totpeso})
    return pd.DataFrame(resultados)


def ev_ingreso_x_sucu(df, sucursal_input, importe_predicho, operacion="suma"):
    i, n = 0, len(df)
    total_sucursal = 0.0

    while i < n:
        if df.loc[i, "PRSUC"] == sucursal_input:
            total_sucursal += df.loc[i, "PRIMPORTE"]
        i += 1

    total_real = round(total_sucursal, 2)
    diferencia = round(total_real - importe_predicho, 2)
    diferencia_pct = round((diferencia / total_real) * 100, 2) if total_real != 0 else 0

    ops = {
        "suma": round(total_real + importe_predicho, 2),
        "resta": round(total_real - importe_predicho, 2),
        "multiplicacion": round(total_real * importe_predicho, 2),
        "division": round(total_real / importe_predicho, 2) if importe_predicho != 0 else None,
    }

    if operacion not in ops:
        raise ValueError(f"Operacion invalida. Elegir entre: {list(ops.keys())}")

    resultado_operacion = ops[operacion]

    return {
        "SUCURSAL": sucursal_input,
        "TOTAL_REAL": total_real,
        "TOTAL_PREDICHO": importe_predicho,
        "DIFERENCIA": diferencia,
        "DIFERENCIA_PCT": diferencia_pct,
        "PREDICHO_VS_REAL": "mayor" if importe_predicho > total_real else "menor" if importe_predicho < total_real else "igual",
        "OPERACION": operacion,
        "RESULTADO_OPERACION": resultado_operacion,
    }




def resumen_por_sucursal(df):
    i, n = 0, len(df)
    resultados = []
    while i < n:
        sucursal = df.loc[i, "PRSUC"]
        totsuc, myprod, myimpor, mnprod, mnimpor = 0, None, 0, None, None
        while i < n and df.loc[i, "PRSUC"] == sucursal:
            producto = df.loc[i, "PRCOD"]
            totuni, totimpor = 0, 0
            while i < n and df.loc[i, "PRSUC"] == sucursal and df.loc[i, "PRCOD"] == producto:
                totuni  += df.loc[i, "PRCANT"]
                totimpor += df.loc[i, "PRIMPORTE"]
                i += 1
            totsuc += totuni
            if myimpor == 0 or totimpor > myimpor:
                myimpor, myprod = totimpor, producto
            if mnimpor is None or totimpor < mnimpor:
                mnimpor, mnprod = totimpor, producto
        resultados.append({"PRSUC": sucursal, "TOTSUC": totsuc,
                            "MYPROD": myprod, "MYIMPOR": myimpor,
                            "MNPROD": mnprod, "MNIMPOR": mnimpor})
    return pd.DataFrame(resultados)


def resumen_general(df):
    i, n = 0, len(df)
    cansuc, totalimp = 0, 0
    while i < n:
        sucursal = df.loc[i, "PRSUC"]
        totsucursal = 0
        cansuc += 1
        while i < n and df.loc[i, "PRSUC"] == sucursal:
            totsucursal += df.loc[i, "PRIMPORTE"]
            i += 1
        totalimp += totsucursal
    return {"CANSUC": cansuc, "TOTALIMP": round(totalimp, 2)}


def procesar(path, ordenado=True):
    df = leer_csv(path)
    if not ordenado:
        df = ordenar_por_sucursal(df)
    df = calcular_importe(df)
    productos  = resumen_por_producto(df)
    sucursales = resumen_por_sucursal(df)
    general    = resumen_general(df)
    return productos, sucursales, general


if __name__ == "__main__":
    path = input("Indique el path del csv: ")
    ordenado = input("El archivo está ordenado? (Y/N): ").upper() == "Y"
    productos, sucursales, general = procesar(path, ordenado)
    print("\nPor producto:")
    print(productos.to_string(index=False))
    print("\nPor sucursal:")
    print(sucursales.to_string(index=False))
    print("\nTotal sucursales:", general["CANSUC"])
    print("Compra total:    $", general["TOTALIMP"])

