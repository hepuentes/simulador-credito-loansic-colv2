import streamlit as st

# Configuración inicial
st.set_page_config(page_title="Simulador de Crédito Loansi", layout="centered")

# Función para formatear números
def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Datos de las líneas de crédito
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

# Estilos CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
    }

    .main-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 600;
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

    /* Texto cuánto necesitas */
    .monto-title {
        color: white;
        font-size: 1.3rem;
        margin: 2rem 0 1rem 0;
    }

    /* Valor grande seleccionado */
    .monto-value {
        color: #3B82F6;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 2rem;
    }

    /* Slider y valores */
    .slider-container {
        position: relative;
        padding: 0.5rem 0;
    }

    /* Slider personalizado */
    .stSlider > div {
        padding: 1rem 0 !important;
    }

    .stSlider [data-baseweb="slider"] {
        margin-top: 1rem !important;
    }

    /* Barra del slider */
    div[data-testid="stSlider"] > div > div > div {
        background: #4B5563 !important;
        height: 6px !important;
        border-radius: 3px !important;
    }

    /* Botón del slider */
    div[data-testid="stSlider"] [role="slider"] {
        width: 20px !important;
        height: 20px !important;
        background: #3B82F6 !important;
        border: 2px solid white !important;
        border-radius: 50% !important;
        top: -7px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }

    /* Ocultar elementos innecesarios */
    .stSlider [data-baseweb="slider"] div[role="slider"] div,
    .stSlider [data-baseweb="tooltip"],
    .stSlider div[role="slider"] span {
        display: none !important;
    }

    /* Valores min/max */
    .minmax-values {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<h1 class="main-title">Simulador de Crédito Loansi</h1>', unsafe_allow_html=True)

# Selector de línea de crédito
st.markdown('<div style="color: white; margin-bottom: 0.5rem;">Selecciona la línea de crédito</div>', unsafe_allow_html=True)
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), label_visibility="collapsed")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto
st.markdown('<div class="monto-title">¿Cuánto necesitas?</div>', unsafe_allow_html=True)

# Slider y valor seleccionado
col1, col2 = st.columns([20,1])
with col1:
    monto = st.slider(
        "",
        min_value=detalles["monto_min"],
        max_value=detalles["monto_max"],
        step=50000,
        label_visibility="collapsed"
    )

    # Mostrar valor grande debajo del título
    st.markdown(f'<div class="monto-value">$ {format_number(monto)}</div>', unsafe_allow_html=True)

    # Valores min/max debajo del slider
    st.markdown(f"""
    <div class="minmax-values">
        <span>{format_number(detalles["monto_min"])}</span>
        <span>{format_number(detalles["monto_max"])}</span>
    </div>
    """, unsafe_allow_html=True)

# Barra de progreso roja
progress = ((monto - detalles["monto_min"]) / (detalles["monto_max"] - detalles["monto_min"])) * 100
st.markdown(f"""
<style>
    div[data-testid="stSlider"] > div > div > div {{
        background: linear-gradient(to right, #FF4B4B {progress}%, #4B5563 {progress}%) !important;
    }}
</style>
""", unsafe_allow_html=True)
