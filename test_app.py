import streamlit as st
import pandas as pd
import os

from test_logic import (
    cargar_clientes,
    cargar_pisos,
    match_pisos_con_clientes,
    match_clientes_con_pisos,
)

# --------------------------------
# 0. Configuración general
# --------------------------------
# --------------------------------
# 0. Configuración general de la página y personalización de la interfaz
# --------------------------------

# Parámetros personalizables
PAGE_TITLE = "SaaS Real Estate"
PAGE_ICON = "🏠"
LAYOUT = "wide"  # Opciones: "centered", "wide"
INITIAL_SIDEBAR_STATE = "expanded"  # Opciones: "auto", "expanded", "collapsed"
BACKGROUND_COLOR = "#3C484B" # 3C484B
HEADER_COLOR = "#FFFFFF"
HEADER_TEXT = "SaaS Real Estate | Plataforma Inmobiliaria de IA"
HEADER_ICON = "🏠"
HEADER_FONT_SIZE = "2.2rem"
HEADER_FONT_WEIGHT = "700"
HEADER_MARGIN = "0.5em 0 1.5em 0"
FONT_FAMILY = "Segoe UI, sans-serif"

# Configuración de la página
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
)

# Estilos personalizados con CSS
st.markdown(
    f"""
    <style>
        body {{
            background-color: {BACKGROUND_COLOR};
            font-family: {FONT_FAMILY};
        }}
        .main > div:first-child {{
            padding-top: 1.5rem;
        }}
        .nova-header {{
            color: {HEADER_COLOR};
            font-size: {HEADER_FONT_SIZE};
            font-weight: {HEADER_FONT_WEIGHT};
            margin: {HEADER_MARGIN};
            display: flex;
            align-items: center;
            gap: 0.5em;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Encabezado personalizado
st.markdown(
    f'<div class="nova-header">{HEADER_ICON} {HEADER_TEXT}</div>',
    unsafe_allow_html=True,
)


# --------------------------------
# 1. Definición de archivos de datos
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
# --------------------------------
# Sidebar personalizada
# --------------------------------

# Parámetros personalizables para la sidebar
SIDEBAR_BG_COLOR = "#2E383B" # Color de fondo de la sidebar
SIDEBAR_HEADER_COLOR = "#F9FAFB" # Color del encabezado
SIDEBAR_HEADER_TEXT = "Acciones disponibles" # Texto del encabezado
SIDEBAR_HEADER_ICON = "🔎" 
SIDEBAR_HEADER_FONT_SIZE = "1.4rem" # Tamaño de la fuente del encabezado
SIDEBAR_HEADER_FONT_WEIGHT = "600" # Peso de la fuente del encabezado
SIDEBAR_HEADER_MARGIN = "0em 0 0em 0" # Margen del encabezado
SIDEBAR_FONT_FAMILY = "Segoe UI, sans-serif" # Familia de fuente de la sidebar
SIDEBAR_RADIO_LABEL_COLOR = "#FFFFFF" # Color del texto de las opciones
SIDEBAR_RADIO_BG_COLOR = "#3C4345" # Color de fondo de las opciones
SIDEBAR_RADIO_SELECTED_BG = "#f9ca24" # Color de fondo de la opción seleccionada
SIDEBAR_RADIO_SELECTED_COLOR = "#fff" # Color del texto de la opción seleccionada
SIDEBAR_WIDTH = "320px"  # Ejemplo: "320px", "400px"

# Opciones disponibles para la acción
ACCIONES = [
    "Registrar Piso",           # Registrar un nuevo piso
    "Registrar Cliente",        # Registrar un nuevo cliente
    "Buscar Clientes para un Piso",  # Buscar clientes compatibles con un piso
    "Buscar Pisos para un Cliente"   # Buscar pisos compatibles con un cliente
]

# Estilos personalizados para la sidebar
st.markdown(
    f"""
    <style>
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {SIDEBAR_BG_COLOR};
            font-family: {SIDEBAR_FONT_FAMILY};
            width: {SIDEBAR_WIDTH};
            min-width: {SIDEBAR_WIDTH};
            max-width: {SIDEBAR_WIDTH};
        }}
        .nova-sidebar-header {{
            color: {SIDEBAR_HEADER_COLOR};
            font-size: {SIDEBAR_HEADER_FONT_SIZE};
            font-weight: {SIDEBAR_HEADER_FONT_WEIGHT};
            margin: {SIDEBAR_HEADER_MARGIN};
            display: flex;
            align-items: center;
            gap: 0.5em;
        }}
        section[data-testid="stSidebar"] label {{
            color: {SIDEBAR_RADIO_LABEL_COLOR};
        }}
        section[data-testid="stSidebar"] .stRadio > div {{
            background: {SIDEBAR_RADIO_BG_COLOR};
            border-radius: 0.5em;
            padding: 0.5em;
        }}
        section[data-testid="stSidebar"] .stRadio [aria-checked="true"] {{
            background: {SIDEBAR_RADIO_SELECTED_BG};
            color: {SIDEBAR_RADIO_SELECTED_COLOR};
            border-radius: 0.5em;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Encabezado personalizado de la sidebar
st.sidebar.markdown(
    f'<div class="nova-sidebar-header">{SIDEBAR_HEADER_ICON} {SIDEBAR_HEADER_TEXT}</div>',
    unsafe_allow_html=True,
)

# Selector de acción en la sidebar
accion = st.sidebar.radio(
    "¿Qué deseas hacer?",
    ACCIONES
)

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
