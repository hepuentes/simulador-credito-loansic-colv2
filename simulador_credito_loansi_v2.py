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
        "descripcion": "Crédito rotativo para personas en sectores informales.",
        "monto_min": 50000,
        "monto_max": 500000,
        "plazos": [4, 6, 8],
        "tasa_mensual": 2.0718,
        "tasa_anual_efectiva": 27.9,
        "aval_porcentaje": 0.12
    }
}

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
        text-align: center;
        margin: 2rem 0;
    }

    .select-label {
        color: white;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    /* Selector de crédito */
    .stSelectbox > div {
        background-color: #27282B !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        background-color: #27282B !important;
        color: white !important;
        border: none !important;
    }

    /* Título y valor */
    .monto-title {
        color: white;
        font-size: 1.3rem;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }

    .monto-value {
        color: #3B82F6;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0 2rem 0;
    }

    /* Slider */
    .stSlider > div {
        padding: 0 !important;
        margin: 1rem 0;
    }

    div[data-testid="stSlider"] > div > div > div {
        background: #4B5563 !important;
        height: 6px !important;
        border-radius: 3px !important;
    }

    div[data-testid="stSlider"] [role="slider"] {
        width: 24px !important;
        height: 24px !important;
        background: #3B82F6 !important;
        border: 2px solid white !important;
        border-radius: 50% !important;
        top: -9px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }

    /* Ocultar elementos del slider */
    .stSlider [data-baseweb="slider"] div[role="slider"] div,
    .stSlider [data-baseweb="tooltip"] {
        display: none !important;
    }

    /* Valores min/max */
    .minmax-values {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 0.9rem;
        margin: 0.5rem 1rem;
    }

    /* Botones de plazo */
    .stRadio > label {
        background-color: #27282B !important;
        border: none !important;
        color: white !important;
        padding: 1rem 2rem !important;
        border-radius: 0.5rem !important;
        margin: 0.2rem !important;
    }

    .stRadio > label[data-checked="true"] {
        background-color: #3B82F6 !important;
    }

    /* Resultado */
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

# Título
st.markdown('<h1 class="main-title">Simulador de Crédito Loansi</h1>', unsafe_allow_html=True)

# Selector de línea de crédito
st.markdown('<div class="select-label">Selecciona la línea de crédito</div>', unsafe_allow_html=True)
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), label_visibility="collapsed")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto
st.markdown('<div class="monto-title">¿Cuánto necesitas?</div>', unsafe_allow_html=True)

# Slider y valor seleccionado en contenedor
container = st.container()
monto = container.slider(
    "",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    label_visibility="collapsed"
)

# Mostrar valor centrado antes del slider
st.markdown(f'<div class="monto-value">$ {format_number(monto)}</div>', unsafe_allow_html=True)

# Barra de progreso y valores min/max
progress = ((monto - detalles["monto_min"]) / (detalles["monto_max"] - detalles["monto_min"])) * 100
st.markdown(f"""
<style>
    div[data-testid="stSlider"] > div > div > div {{
        background: linear-gradient(to right, #FF4B4B {progress}%, #4B5563 {progress}%) !important;
    }}
</style>
<div class="minmax-values">
    <span>{format_number(detalles["monto_min"])}</span>
    <span>{format_number(detalles["monto_max"])}</span>
</div>
""", unsafe_allow_html=True)

# Sección de plazo
st.markdown('<div class="monto-title">Selecciona el plazo</div>', unsafe_allow_html=True)
plazo = st.radio(
    "",
    options=detalles["plazos"],
    format_func=lambda x: f"{x} {'Meses' if tipo_credito == 'LoansiFlex' else 'Semanas'}",
    horizontal=True,
    label_visibility="collapsed"
)

# Cálculos
frecuencia_pago = "Mensual" if tipo_credito == "LoansiFlex" else "Semanal"
aval = monto * detalles["aval_porcentaje"]
seguro_vida = detalles.get("seguro_vida_base", 0) * (plazo // 12) if tipo_credito == "LoansiFlex" else 0
total_financiar = monto + aval + seguro_vida

# Cálculo de cuota
if tipo_credito == "LoansiFlex":
    cuota = (total_financiar * (detalles["tasa_mensual"] / 100)) / (1 - (1 + detalles["tasa_mensual"] / 100) ** -plazo)
else:
    tasa_mensual = detalles["tasa_mensual"] / 100
    tasa_semanal = ((1 + tasa_mensual) ** 0.25) - 1
    cuota = round((total_financiar * tasa_semanal) / (1 - (1 + tasa_semanal) ** -plazo))

# Mostrar resultado
st.markdown(f"""
<div class="result-box">
    <div class="result-text">Pagarás {plazo} cuotas por un valor aproximado de:</div>
    <div class="result-amount">$ {format_number(cuota)} {frecuencia_pago}</div>
</div>
""", unsafe_allow_html=True)

# Mensaje legal
st.markdown("""
<div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
    <p style="color: #9CA3AF; font-size: 0.8rem; line-height: 1.4;">
        Loansi.co ofrece este Simulador conforme a la ley para propósitos informativos, sin que constituya una oferta o 
        compromiso de contratación. El simulador es orientativo y busca brindarte estimaciones generales. Los resultados 
        de la simulación no representan una garantía o asesoría en áreas comerciales, contables, fiscales o legales. 
        Los términos de la simulación se basan en las condiciones de mercado actuales. La tasa de interés aplicable será 
        la vigente en LOANSI SAS al momento de usar el simulador. Los demás elementos del crédito pueden cambiar y dependen 
        de factores externos, tu nivel de riesgo y capacidad de pago.
    </p>
</div>
""", unsafe_allow_html=True)
