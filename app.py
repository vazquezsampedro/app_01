import streamlit as st
import pandas as pd
import os

from logic import (
    cargar_clientes,
    cargar_pisos,
    match_pisos_con_clientes,
    match_clientes_con_pisos,
)

# --------------------------------
# Configuración general
# --------------------------------
st.set_page_config(page_title="NOVA Real Estate", layout="wide")
st.markdown("## 🏠 NOVA Real Estate | Plataforma Inmobiliaria de IA")

# --------------------------------
# Definición de archivos de datos
# --------------------------------
CLIENTES_FILE = "clientes.xlsx"
PISOS_FILE = "pisos.xlsx"

# --------------------------------
# Cargar los datos existentes o crear archivos vacíos si no existen
# --------------------------------
if os.path.exists(CLIENTES_FILE):
    df_clientes = cargar_clientes(CLIENTES_FILE)
else:
    df_clientes = pd.DataFrame()

if os.path.exists(PISOS_FILE):
    df_pisos = cargar_pisos(PISOS_FILE)
else:
    df_pisos = pd.DataFrame()

# --------------------------------
# Interfaz Streamlit
# --------------------------------
st.sidebar.header("🧭 Acciones disponibles")
accion = st.sidebar.radio("¿Qué deseas hacer?", [
    "Registrar Piso", "Registrar Cliente",
    "Buscar Clientes para un Piso", "Buscar Pisos para un Cliente"
])

# --------------------------------
# Registrar un piso
# --------------------------------
if accion == "Registrar Piso":
    st.subheader("📝 Registro de nuevo piso")
    with st.form("registro_piso"):
        col1, col2, col3 = st.columns(3)
        with col1:
            zona = st.selectbox("Zona", list(range(10)))
            precio = st.slider("Precio (€)", 40000, 400000, 100000, step=10000)
            tipo = st.selectbox("Tipo de Vivienda", ['Piso', 'Casa', 'Chalet', 'Adosado', 'Dúplex', 'Ático', 'Estudio'])
            estado = st.selectbox("Estado", ['Obra Nueva', 'Buen Estado', 'A Reformar'])
            calefaccion = st.selectbox("Calefacción", ['Geotermia', 'Gas', 'Electrica', 'Bomba de calor', 'No disponible'])
            planta = st.slider("Planta", 0, 10, 1)

        with col2:
            metros = st.slider("Metros Cuadrados", 30, 400, 90, step=5)
            habitaciones = st.slider("Habitaciones", 1, 5, 3)
            banos = st.slider("Baños", 1, 4, 2)
            situacion = st.selectbox("Situación", ['alquilado', 'nuda propiedad', 'ocupada ilegalmente', 'disponible'])
            ascensor = st.selectbox("Ascensor", ['Si', 'No'])
            cocina = st.selectbox("Cocina", ['Gas', 'Electrica'])

        with col3:
            balcon = st.selectbox("Balcón", ['Si', 'No'])
            terraza = st.selectbox("Terraza", ['Si', 'No'])
            patio = st.selectbox("Patio", ['Si', 'No'])
            bajo = st.selectbox("Bajo", ['Si', 'No'])
            garaje = st.selectbox("Garaje", ['Si', 'No'])
            trastero = st.selectbox("Trastero", ['Si', 'No'])

        submitted = st.form_submit_button("✅ Registrar Piso")
        if submitted:
            nuevo_piso = pd.DataFrame([{
                "Zona": zona,
                "Precio": precio,
                "Tipo de Vivienda": tipo,
                "Situacion": situacion,
                "Estado": estado,
                "Ascensor": ascensor,
                "Planta": planta,
                "Metros Cuadrados": metros,
                "Balcon": balcon,
                "Bajo": bajo,
                "Patio": patio,
                "Terraza": terraza,
                "Cocina": cocina,
                "Garaje": garaje,
                "Trastero": trastero,
                "Calefaccion": calefaccion,
                "Habitaciones": habitaciones,
                "Baños": banos
            }])
            df_pisos = pd.concat([df_pisos, nuevo_piso], ignore_index=True)
            df_pisos.to_excel(PISOS_FILE, index=False)
            st.success("✅ Piso registrado correctamente")

            st.subheader("🎯 Clientes compatibles")
            clientes = match_pisos_con_clientes(nuevo_piso.iloc[0], df_clientes)
            st.dataframe(clientes)

# --------------------------------
# Registrar un cliente
# --------------------------------
elif accion == "Registrar Cliente":
    st.subheader("🧍 Registro de nuevo cliente")
    with st.form("registro_cliente"):
        col1, col2 = st.columns(2)
        with col1:
            entrada = st.slider("Entrada (%)", 0, 30, 10, step=5)
            zona = st.selectbox("Zona Preferida", list(range(10)))
        with col2:
            habitaciones = st.slider("Habitaciones deseadas", 1, 5, 3)
            banos = st.slider("Baños deseados", 1, 4, 2)

        submitted = st.form_submit_button("✅ Registrar Cliente")
        if submitted:
            nuevo_cliente = pd.DataFrame([{
                "Entrada Cliente": entrada,
                "Zona": zona,
                "Precio": entrada * 10000,
                "Tipo de Vivienda": '',
                "Situacion": '',
                "Estado": '',
                "Ascensor": '',
                "Planta": 0,
                "Metros Cuadrados": 0,
                "Balcon": '',
                "Bajo": '',
                "Patio": '',
                "Terraza": '',
                "Cocina": '',
                "Garaje": '',
                "Trastero": '',
                "Calefaccion": '',
                "Habitaciones": habitaciones,
                "Baños": banos
            }])
            df_clientes = pd.concat([df_clientes, nuevo_cliente], ignore_index=True)
            df_clientes.to_excel(CLIENTES_FILE, index=False)
            st.success("✅ Cliente registrado correctamente")

            st.subheader("🏡 Pisos compatibles")
            pisos = match_clientes_con_pisos(nuevo_cliente.iloc[0], df_pisos)
            st.dataframe(pisos)

# --------------------------------
# Buscar clientes para un piso
# --------------------------------
elif accion == "Buscar Clientes para un Piso":
    if df_pisos.empty:
        st.warning("⚠️ No hay pisos registrados.")
    else:
        st.subheader("🔍 Selecciona un piso")
        idx = st.selectbox("ID Piso", df_pisos.index)
        piso = df_pisos.loc[idx]
        st.write(piso)
        clientes = match_pisos_con_clientes(piso, df_clientes)
        st.subheader("🎯 Clientes compatibles")
        st.dataframe(clientes)

# --------------------------------
# Buscar pisos para un cliente
# --------------------------------
elif accion == "Buscar Pisos para un Cliente":
    if df_clientes.empty:
        st.warning("⚠️ No hay clientes registrados.")
    else:
        st.subheader("🔍 Selecciona un cliente")
        idx = st.selectbox("ID Cliente", df_clientes.index)
        cliente = df_clientes.loc[idx]
        st.write(cliente)
        pisos = match_clientes_con_pisos(cliente, df_pisos)
        st.subheader("🏡 Pisos compatibles")
        st.dataframe(pisos)
