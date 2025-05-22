import pandas as pd


# -------------------
# 1. Cargar datos
# -------------------

def cargar_clientes(path='clientes.xlsx'):
    return pd.read_excel(path)

def cargar_pisos(path='pisos.xlsx'):
    return pd.read_excel(path)

# -------------------------------
# 2. Lógica de matching básica
# -------------------------------

def match_pisos_con_clientes(piso, df_clientes):
    return df_clientes[
        (df_clientes["Zona"] == piso["Zona"]) &
        ((df_clientes["Entrada Cliente"] * 10000) >= piso["Precio"]) &
        (df_clientes["Habitaciones"] >= piso["Habitaciones"])
    ]

def match_clientes_con_pisos(cliente, df_pisos):
    return df_pisos[
        (df_pisos["Zona"] == cliente["Zona"]) &
        (df_pisos["Precio"] <= cliente["Entrada Cliente"] * 10000) &
        (df_pisos["Habitaciones"] >= cliente["Habitaciones"])
    ]

def registrar_piso(form_data, df_pisos, df_clientes):
    nuevo_piso = pd.DataFrame([form_data])
    df_pisos = pd.concat([df_pisos, nuevo_piso], ignore_index=True)
    clientes_compatibles = match_pisos_con_clientes(nuevo_piso.iloc[0], df_clientes)
    return df_pisos, clientes_compatibles

def registrar_cliente(form_data, df_clientes, df_pisos):
    nuevo_cliente = pd.DataFrame([form_data])
    df_clientes = pd.concat([df_clientes, nuevo_cliente], ignore_index=True)
    pisos_compatibles = match_clientes_con_pisos(nuevo_cliente.iloc[0], df_pisos)
    return df_clientes, pisos_compatibles


