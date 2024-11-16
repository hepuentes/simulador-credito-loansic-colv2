import streamlit as st

# Función para formatear números
def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Datos base
LINEAS_DE_CREDITO = {
    "LoansiFlex": {
        "descripcion": "Crédito de libre inversión para empleados, independientes, personas naturales y pensionados.",
        "monto_min": 1000000,
        "monto_max": 20000000,
        "plazo_min": 12,
        "plazo_max": 60,
        "tasa_mensual": 1.9715,
        "tasa_anual_efectiva": 26.4,
        "aval_porcentaje": 0.10,
        "seguro_vida_base": 150000,
        "plazos": [12, 24, 36, 48, 60]
    },
    "Microflex": {
        "descripcion": "Crédito rotativo para personas en sectores informales, orientado a cubrir necesidades de liquidez rápida con pagos semanales.",
        "monto_min": 50000,
        "monto_max": 500000,
        "plazo_min": 4,
        "plazo_max": 8,
        "tasa_mensual": 2.0718,
        "tasa_anual_efectiva": 27.9,
        "aval_porcentaje": 0.12,
        "plazos": [4, 6, 8]
    }
}

st.markdown("""
<style>
    /* Estilos base */
    .main {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Slider personalizado */
    .custom-slider {
        background: #f0f2f5;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .monto-display {
        font-size: 2rem;
        font-weight: 700;
        color: #1a73e8;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Botones de plazo */
    .plazo-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 20px 0;
    }
    
    .plazo-button {
        background-color: #f0f2f5;
        border: none;
        padding: 10px 20px;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .plazo-button.active {
        background-color: #1a73e8;
        color: white;
    }
    
    /* Resultado */
    .result-box {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .legal-text {
        font-size: 0.8rem;
        color: #666;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 2rem;
        line-height: 1.4;
    }
    
    /* Mejoras visuales generales */
    .stSlider > div > div > div {
        background-color: #1a73e8 !important;
    }
    
    .stSlider > div > div {
        background-color: #e8f0fe !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Simulador de Crédito Loansi</h1>", unsafe_allow_html=True)

# Selección de línea de crédito
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), key="select_credito")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto con slider moderno
st.markdown("<h3>¿Cuánto necesitas?</h3>", unsafe_allow_html=True)
monto = st.slider(
    "",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    key="monto_slider"
)
st.markdown(f"<div class='monto-display'>$ {format_number(monto)}</div>", unsafe_allow_html=True)

# Sección de plazo con botones tipo pills
st.markdown("<h3>Selecciona el plazo</h3>", unsafe_allow_html=True)
plazos = detalles["plazos"]
plazo = st.radio(
    "",
    plazos,
    format_func=lambda x: f"{x} {'meses' if tipo_credito == 'LoansiFlex' else 'semanas'}",
    horizontal=True,
    key="plazo_radio"
)

# Cálculos y resultados (mantener el código existente para cálculos)
aval = monto * detalles["aval_porcentaje"]
seguro_vida = calcular_seguro_vida(plazo, detalles.get("seguro_vida_base", 0)) if tipo_credito == "LoansiFlex" else 0
total_financiar = monto + aval + total_costos_asociados + seguro_vida

if tipo_credito == "LoansiFlex":
    cuota = (total_financiar * (detalles["tasa_mensual"] / 100)) / (1 - (1 + detalles["tasa_mensual"] / 100) ** -plazo)
else:
    tasa_mensual = detalles["tasa_mensual"] / 100
    tasa_semanal = ((1 + tasa_mensual) ** 0.25) - 1
    cuota = round((total_financiar * tasa_semanal) / (1 - (1 + tasa_semanal) ** -plazo))

# Mostrar resultado
st.markdown(f"""
<div class="result-box">
    <p class="result-text">Pagarás {plazo} cuotas por un valor aproximado de:</p>
    <div class="result-amount">$ {format_number(cuota)} {frecuencia_pago}</div>
</div>
""", unsafe_allow_html=True)

# Detalles del crédito (mantener el código existente)
with st.expander("Ver Detalles del Crédito"):
    # ... (mantener el código existente para detalles)
    pass

# Mensaje legal
st.markdown("""
<div class="legal-text">
    Loansi.co ofrece este Simulador conforme a la ley para propósitos informativos, sin que constituya una oferta o 
    compromiso de contratación. El simulador es orientativo y busca brindarte estimaciones generales. Los resultados 
    de la simulación no representan una garantía o asesoría en áreas comerciales, contables, fiscales o legales. 
    Los términos de la simulación se basan en las condiciones de mercado actuales. La tasa de interés aplicable será 
    la vigente en LOANSI SAS al momento de usar el simulador. Los demás elementos del crédito pueden cambiar y dependen 
    de factores externos, tu nivel de riesgo y capacidad de pago.
</div>
""", unsafe_allow_html=True)