import streamlit as st

def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Configuración inicial
st.set_page_config(page_title="Simulador de Crédito Loansi", layout="centered")

# Datos de créditos
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
        "descripcion": "Crédito rotativo para personas en sectores informales.",
        "monto_min": 50000,
        "monto_max": 500000,
        "plazos": [4, 6, 8],
        "tasa_mensual": 2.0718,
        "tasa_anual_efectiva": 27.9,
        "aval_porcentaje": 0.12
    }
}

st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
    }
    
    .main-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    .select-label {
        color: white;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox > div {
        background-color: #27282B !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        background-color: #27282B !important;
        color: white !important;
        border: none !important;
    }
    
    .monto-section {
        margin: 2rem 0;
    }
    
    .monto-title {
        color: white;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    .monto-value {
        color: #3B82F6;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    .slider-container {
        margin: 2rem 0;
        position: relative;
    }
    
    .stSlider > div {
        padding: 1.5rem 0 !important;
    }
    
    div[data-testid="stSlider"] > div > div > div {
        background: #4B5563 !important;
        height: 6px !important;
        border-radius: 3px !important;
    }
    
    div[data-testid="stSlider"] [role="slider"] {
        width: 20px !important;
        height: 20px !important;
        background: #3B82F6 !important;
        border: 2px solid white !important;
        border-radius: 50% !important;
        top: -7px !important;
        z-index: 2 !important;
    }
    
    .stSlider [data-baseweb="slider"] div[role="slider"] div,
    .stSlider [data-baseweb="tooltip"] {
        display: none !important;
    }
    
    .minmax-values {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .progress-bar {
        position: absolute;
        left: 0;
        height: 6px;
        background: #FF4B4B;
        border-radius: 3px 0 0 3px;
    }
    
    .result-box {
        background: rgba(255,255,255,0.05);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .result-text {
        color: #B0B0B0;
        margin-bottom: 0.5rem;
    }
    
    .result-amount {
        color: #3B82F6;
        font-size: 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Título y selector
st.markdown('<h1 class="main-title">Simulador de Crédito Loansi</h1>', unsafe_allow_html=True)
st.markdown('<div class="select-label">Selecciona la línea de crédito</div>', unsafe_allow_html=True)
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), label_visibility="collapsed")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto
st.markdown('<div class="monto-section">', unsafe_allow_html=True)
st.markdown('<div class="monto-title">¿Cuánto necesitas?</div>', unsafe_allow_html=True)

container = st.container()
monto = st.slider(
    "",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    label_visibility="collapsed"
)

# Mostrar valor seleccionado ANTES del slider
container.markdown(f'<div class="monto-value">$ {format_number(monto)}</div>', unsafe_allow_html=True)

# Valores min/max y barra de progreso
progress = ((monto - detalles["monto_min"]) / (detalles["monto_max"] - detalles["monto_min"])) * 100
st.markdown(f"""
<style>
    div[data-testid="stSlider"] > div > div > div {{
        background: linear-gradient(to right, #FF4B4B {progress}%, #4B5563 {progress}%) !important;
    }}
</style>
<div class="slider-container">
    <div class="minmax-values">
        <span>{format_number(detalles["monto_min"])}</span>
        <span>{format_number(detalles["monto_max"])}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sección de plazo
st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
st.markdown('<div style="color: white; font-size: 1.3rem; margin-bottom: 1rem;">Selecciona el plazo</div>', unsafe_allow_html=True)
plazo = st.radio(
    "",
    options=detalles["plazos"],
    format_func=lambda x: f"{x} {'Meses' if tipo_credito == 'LoansiFlex' else 'Semanas'}",
    horizontal=True,
    label_visibility="collapsed"
)

# Cálculos
cuota = (monto * (detalles["tasa_mensual"] / 100)) / (1 - (1 + detalles["tasa_mensual"] / 100) ** -plazo)

# Mostrar resultado
st.markdown(f"""
<div class="result-box">
    <div class="result-text">Pagarás {plazo} cuotas por un valor aproximado de:</div>
    <div class="result-amount">$ {format_number(cuota)} {'Mensual' if tipo_credito == 'LoansiFlex' else 'Semanal'}</div>
</div>
""", unsafe_allow_html=True)
