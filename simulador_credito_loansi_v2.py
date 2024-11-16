import streamlit as st

# Función para formatear números
def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Configuración inicial
def get_plazo_display(plazo, tipo):
    if tipo == "LoansiFlex":
        return f"{plazo}\nMeses"
    return f"{plazo}\nSemanas"

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

COSTOS_ASOCIADOS = {
    "Pagaré Digital": 2800,
    "Carta de Instrucción": 2800,
    "Custodia TVE": 5600,
    "Consulta Datacrédito": 11000
}

total_costos_asociados = sum(COSTOS_ASOCIADOS.values())

def calcular_seguro_vida(plazo, seguro_vida_base):
    años = plazo // 12
    return seguro_vida_base * años if años >= 1 else 0

# Estilos
st.markdown("""
<style>
    .main {
        font-family: 'Inter', sans-serif;
        color: #FFFFFF;
        background-color: #1E1E1E;
    }

    /* Títulos */
    .section-title {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: left;
        margin: 2rem 0 1rem;
    }

    /* Monto display */
    .monto-display {
        color: #3B82F6;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: left;
        margin: 1rem 0;
    }

    /* Slider personalizado */
    .stSlider > div > div > div {
        background: #3B82F6 !important;
        border: 2px solid #FFFFFF !important;
        width: 2.5rem !important;
        height: 2.5rem !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        cursor: pointer !important;
    }

    .stSlider > div > div {
        background: linear-gradient(90deg, #3B82F6 var(--slider-progress), #4B5563 var(--slider-progress)) !important;
        height: 0.75rem !important;
        border-radius: 1rem !important;
    }

    /* Botones de plazo */
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: flex-start !important;
        gap: 1rem !important;
        margin: 1rem 0 !important;
    }

    .stRadio > label {
        background-color: #27272A;
        padding: 1.5rem !important;
        border-radius: 0.75rem !important;
        cursor: pointer !important;
        text-align: center !important;
        min-width: 100px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 0.5rem !important;
        transition: all 0.2s ease !important;
        border: 2px solid transparent !important;
    }

    .stRadio > label:hover {
        border-color: #3B82F6 !important;
    }

    .stRadio > label[data-checked="true"] {
        background-color: #3B82F6 !important;
        color: white !important;
    }

    /* Ocultar radio buttons */
    .stRadio input {
        position: absolute !important;
        opacity: 0 !important;
    }

    /* Resultado */
    .result-box {
        background-color: #27272A;
        border-radius: 1rem;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }

    .result-text {
        font-size: 1.2rem;
        color: #D1D5DB;
        margin-bottom: 1rem;
    }

    .result-amount {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# Layout
st.markdown("<h1>Simulador de Crédito Loansi</h1>", unsafe_allow_html=True)

# Selección de línea de crédito
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), key="select_credito")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto
st.markdown("<p class='section-title'>¿Cuánto necesitas?</p>", unsafe_allow_html=True)
monto = st.slider(
    "",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    key="monto_slider"
)
st.markdown(f"<div class='monto-display'>$ {format_number(monto)}</div>", unsafe_allow_html=True)

# Sección de plazo
st.markdown("<p class='section-title'>Selecciona el plazo</p>", unsafe_allow_html=True)
plazo = st.radio(
    "",
    options=detalles["plazos"],
    format_func=lambda x: get_plazo_display(x, tipo_credito),
    horizontal=True,
    key="plazo_radio"
)

frecuencia_pago = "Mensual" if tipo_credito == "LoansiFlex" else "Semanal"

# Cálculos
aval = monto * detalles["aval_porcentaje"]
seguro_vida = calcular_seguro_vida(plazo, detalles.get("seguro_vida_base", 0)) if tipo_credito == "LoansiFlex" else 0
total_financiar = monto + aval + total_costos_asociados + seguro_vida

if tipo_credito == "LoansiFlex":
    cuota = (total_financiar * (detalles["tasa_mensual"] / 100)) / (1 - (1 + detalles["tasa_mensual"] / 100) ** -plazo)
else:
    tasa_mensual = detalles["tasa_mensual"] / 100
    tasa_semanal = ((1 + tasa_mensual) ** 0.25) - 1
    cuota = round((total_financiar * tasa_semanal) / (1 - (1 + tasa_semanal) ** -plazo))

# Resultado
st.markdown(f"""
<div class="result-box">
    <p class="result-text">Pagarás {plazo} {frecuencia_pago.lower()} por un valor aproximado de:</p>
    <div class="result-amount">$ {format_number(cuota)} {frecuencia_pago}</div>
</div>
""", unsafe_allow_html=True)

# Detalles del crédito
with st.expander("Ver Detalles del Crédito"):
    total_interes = cuota * plazo - total_financiar
    total_pagar = cuota * plazo
    
    detalles_orden = [
        ("Monto Solicitado", f"$ {format_number(monto)} COP"),
        ("Plazo", f"{plazo} {'meses' if tipo_credito == 'LoansiFlex' else 'semanas'}"),
        ("Frecuencia de Pago", frecuencia_pago),
        ("Tasa de Interés Mensual", f"{detalles['tasa_mensual']}%"),
        ("Tasa Efectiva Anual (E.A.)", f"{detalles['tasa_anual_efectiva']}%"),
        ("Costo del Aval", f"$ {format_number(aval)} COP"),
        ("Costos Asociados", f"$ {format_number(total_costos_asociados)} COP"),
    ]
    
    if tipo_credito == "LoansiFlex":
        detalles_orden.append(("Seguro de Vida", f"$ {format_number(seguro_vida)} COP"))
    
    detalles_orden.extend([
        ("Total Intereses", f"$ {format_number(total_interes)} COP"),
        ("Total a Pagar", f"$ {format_number(total_pagar)} COP")
    ])
    
    for titulo, valor in detalles_orden:
        st.markdown(f"""
        <div class="detail-item">
            <span class="detail-label">{titulo}</span>
            <span class="detail-value">{valor}</span>
        </div>
        """, unsafe_allow_html=True)

# Mensaje legal
st.markdown("""
<div style='font-size: 0.8rem; color: #9CA3AF; margin-top: 2rem; padding: 1rem; background-color: rgba(255,255,255,0.05); border-radius: 0.5rem; line-height: 1.5;'>
    Loansi.co ofrece este Simulador conforme a la ley para propósitos informativos, sin que constituya una oferta o 
    compromiso de contratación. El simulador es orientativo y busca brindarte estimaciones generales. Los resultados 
    de la simulación no representan una garantía o asesoría en áreas comerciales, contables, fiscales o legales. 
    Los términos de la simulación se basan en las condiciones de mercado actuales. La tasa de interés aplicable será 
    la vigente en LOANSI SAS al momento de usar el simulador. Los demás elementos del crédito pueden cambiar y dependen 
    de factores externos, tu nivel de riesgo y capacidad de pago.
</div>
""", unsafe_allow_html=True)
