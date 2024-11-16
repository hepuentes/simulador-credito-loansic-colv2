import streamlit as st

def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Datos base
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

st.markdown("""
<style>
    /* Tema oscuro */
    .stApp {
        background-color: #1E1E1E;
    }

    /* Selector de crédito */
    .stSelectbox > div > div {
        background-color: #27282B !important;
        color: white !important;
        border: none !important;
    }

    /* Slider */
    .slider-container {
        position: relative;
        padding: 2rem 0;
    }

    .stSlider > div {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
    }

    .stSlider div[data-baseweb="slider"] > div {
        background: #4B5563 !important;
        height: 0.4rem !important;
    }

    .stSlider div[role="slider"] {
        background: #3B82F6 !important;
        border: 2px solid white !important;
        width: 1.8rem !important;
        height: 1.8rem !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        top: -0.7rem !important;
    }

    /* Texto del monto */
    .monto-grande {
        color: #3B82F6;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1.5rem 0;
    }

    /* Valores min/max */
    .valores-minmax {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 0.9rem;
        margin-top: -2rem;
    }

    /* Botones de plazo */
    .stRadio > label {
        background: #27282B !important;
        border: none !important;
        color: white !important;
        padding: 1rem 2rem !important;
        border-radius: 0.5rem !important;
        margin: 0.2rem !important;
        min-width: 120px !important;
        text-align: center !important;
    }

    .stRadio > label[data-checked="true"] {
        background: #3B82F6 !important;
    }

    /* Texto de cuotas */
    .resultado-container {
        background: rgba(255,255,255,0.05);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
    }

    .texto-cuota {
        color: #B0B0B0;
        margin-bottom: 0.5rem;
    }

    .valor-cuota {
        color: #3B82F6;
        font-size: 2rem;
        font-weight: bold;
    }

    .detalle-container {
        background: #27282B;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }

    /* Ocultar elementos del slider */
    .stSlider div[data-baseweb="slider"] div[role="slider"] div,
    .stSlider div[data-baseweb="tooltip"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: white; font-size: 2rem; margin-bottom: 2rem;'>Simulador de Crédito Loansi</h1>", unsafe_allow_html=True)

# Selección de línea de crédito
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), key="select_credito")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Monto
st.markdown("<p style='color: white; font-size: 1.2rem; margin: 2rem 0 1rem;'>¿Cuánto necesitas?</p>", unsafe_allow_html=True)

# Mostrar valores min/max
st.markdown(f"""
<div class="valores-minmax">
    <span>$ {format_number(detalles['monto_min'])}</span>
    <span>$ {format_number(detalles['monto_max'])}</span>
</div>
""", unsafe_allow_html=True)

# Slider y monto
monto = st.slider(
    "",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    key="monto_slider",
    label_visibility="collapsed"
)

st.markdown(f"<div class='monto-grande'>$ {format_number(monto)}</div>", unsafe_allow_html=True)

# Plazo
st.markdown("<p style='color: white; font-size: 1.2rem; margin: 2rem 0 1rem;'>Selecciona el plazo</p>", unsafe_allow_html=True)
plazo = st.radio(
    "",
    options=detalles["plazos"],
    format_func=lambda x: f"{x} {'Meses' if tipo_credito == 'LoansiFlex' else 'Semanas'}",
    horizontal=True,
    key="plazo_radio",
    label_visibility="collapsed"
)

# Cálculos
frecuencia_pago = "Mensual" if tipo_credito == "LoansiFlex" else "Semanal"
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
<div class="resultado-container">
    <div class="texto-cuota">Pagarás {plazo} {frecuencia_pago.lower()} por un valor aproximado de:</div>
    <div class="valor-cuota">$ {format_number(cuota)} {frecuencia_pago}</div>
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
        ("Costos Asociados", f"$ {format_number(total_costos_asociados)} COP")
    ]
    
    if tipo_credito == "LoansiFlex":
        detalles_orden.append(("Seguro de Vida", f"$ {format_number(seguro_vida)} COP"))
    
    detalles_orden.extend([
        ("Total Intereses", f"$ {format_number(total_interes)} COP"),
        ("Total a Pagar", f"$ {format_number(total_pagar)} COP")
    ])
    
    for titulo, valor in detalles_orden:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span style="color: #B0B0B0;">{titulo}</span>
            <span style="color: white; font-weight: 500;">{valor}</span>
        </div>
        """, unsafe_allow_html=True)
