import streamlit as st

# Función para formatear números
def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Datos de líneas de crédito
LINEAS_DE_CREDITO = {
    "LoansiFlex": {
        "descripcion": "Crédito de libre inversión para empleados, independientes, personas naturales y pensionados.",
        "monto_min": 1000000,
        "monto_max": 20000000,
        "plazos": [12, 24, 36, 48, 60],
        "tasa_mensual": 1.9715,
        "tasa_anual_efectiva": 26.4,
        "aval_porcentaje": 0.10,
        "seguro_vida_base": 150000
    },
    "Microflex": {
        "descripcion": "Crédito rotativo para personas en sectores informales, orientado a cubrir necesidades de liquidez rápida con pagos semanales.",
        "monto_min": 50000,
        "monto_max": 500000,
        "plazos": [4, 6, 8],
        "tasa_mensual": 2.0718,
        "tasa_anual_efectiva": 27.9,
        "aval_porcentaje": 0.12
    }
}

# Configuración de la página
st.set_page_config(page_title="Simulador de Crédito Loansi", layout="wide")

# Estilos
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
    }
    
    .main-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 600;
        text-align: left;
        margin: 2rem 0;
    }

    /* Selector de crédito */
    .stSelectbox > div {
        background-color: #27282B !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        background-color: #27282B !important;
        border: none !important;
        color: white !important;
    }

    /* Sección de monto */
    .monto-title {
        color: white;
        font-size: 1.3rem;
        margin: 2rem 0 1rem 0;
    }

    .minmax-container {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 0.9rem;
        margin: 0 0.5rem;
    }

    /* Slider personalizado */
    .stSlider {
        padding-top: 1rem !important;
    }

    .stSlider > div > div > div {
        background: linear-gradient(to right, #FF4B4B 50%, #4B5563 50%);
        height: 6px !important;
    }

    .stSlider [role="slider"] {
        width: 20px !important;
        height: 20px !important;
        background: #3B82F6 !important;
        border: 2px solid white !important;
        border-radius: 50% !important;
        top: -7px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }

    /* Ocultar elementos del slider */
    .stSlider [data-baseweb="slider"] div[role="slider"] div,
    .stSlider [data-baseweb="tooltip"],
    .stSlider div[role="slider"] span {
        display: none !important;
    }

    /* Valor seleccionado */
    .monto-value {
        color: #3B82F6;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: left;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<h1 class="main-title">Simulador de Crédito Loansi</h1>', unsafe_allow_html=True)

# Selector de línea de crédito
tipo_credito = st.selectbox(
    "Selecciona la línea de crédito",
    options=LINEAS_DE_CREDITO.keys(),
    key="select_credito"
)
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto
st.markdown('<p class="monto-title">¿Cuánto necesitas?</p>', unsafe_allow_html=True)

# Valores min/max antes del slider
st.markdown(f"""
<div class="minmax-container">
    <span>$ {format_number(detalles['monto_min'])}</span>
    <span>$ {format_number(detalles['monto_max'])}</span>
</div>
""", unsafe_allow_html=True)

# Slider
monto = st.slider(
    "",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    key="monto_slider",
    label_visibility="collapsed"
)

# Mostrar valor seleccionado
st.markdown(f'<div class="monto-value">$ {format_number(monto)}</div>', unsafe_allow_html=True)

# Sección de plazo
st.markdown(
    '<p style="color: white; font-size: 1.3rem; margin: 2rem 0;">Selecciona el plazo</p>',
    unsafe_allow_html=True
)

# Radio buttons para el plazo
plazo = st.radio(
    "",
    options=detalles["plazos"],
    format_func=lambda x: f"{x} {'Meses' if tipo_credito == 'LoansiFlex' else 'Semanas'}",
    horizontal=True,
    label_visibility="collapsed"
)

# Mostrar cuota aproximada
cuota = 120088  # Este valor sería calculado según tus fórmulas
st.markdown(f"""
<div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;">
    <p style="color: #A0AEC0; margin-bottom: 0.5rem;">Pagarás {plazo} {'meses' if tipo_credito == 'LoansiFlex' else 'semanas'} por un valor aproximado de:</p>
    <p style="color: #3B82F6; font-size: 2rem; font-weight: 700;">$ {format_number(cuota)} {"Mensual" if tipo_credito == "LoansiFlex" else "Semanal"}</p>
</div>
""", unsafe_allow_html=True)

# Botón para ver detalles
with st.expander("Ver Detalles del Crédito"):
    st.markdown("""
    <div style="color: white;">
        <p>Aquí irían los detalles del crédito...</p>
    </div>
    """, unsafe_allow_html=True)
