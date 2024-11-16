# Función para formatear números (al inicio del código)
def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Estilos actualizados
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

    .selector-label {
        color: white;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .stSelectbox [data-baseweb="select"] {
        background-color: #27282B !important;
    }

    .monto-title {
        color: white;
        font-size: 1.3rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Valor seleccionado (arriba del slider) */
    .monto-value {
        color: #3B82F6;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 1rem 0 2rem 0;
    }

    /* Contenedor del slider */
    .slider-container {
        position: relative;
        padding: 0 0.5rem;
    }

    /* Valores min/max debajo del slider */
    .minmax-values {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Ocultar elementos innecesarios del slider */
    .stSlider [data-baseweb="slider"] div[role="slider"] div,
    .stSlider [data-baseweb="tooltip"] {
        display: none !important;
    }

    /* Estilizar el slider */
    div[data-testid="stSlider"] > div > div > div {
        position: relative;
        height: 6px !important;
        background: linear-gradient(to right, #FF4B4B var(--progress, 50%), #4B5563 var(--progress, 50%)) !important;
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
        cursor: pointer !important;
    }
</style>
""", unsafe_allow_html=True)

# Título y selector
st.markdown('<h1 class="main-title">Simulador de Crédito Loansi</h1>', unsafe_allow_html=True)
st.markdown('<div class="selector-label">Selecciona la línea de crédito</div>', unsafe_allow_html=True)
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), key="select_credito", label_visibility="collapsed")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto
st.markdown('<div class="monto-title">¿Cuánto necesitas?</div>', unsafe_allow_html=True)

# Valor seleccionado (antes del slider)
monto = st.slider(
    "",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    key="monto_slider",
    label_visibility="collapsed"
)

# Mostrar el valor seleccionado
st.markdown(f"""
<div class="monto-value">$ {format_number(monto)}</div>
""", unsafe_allow_html=True)

# Valores min/max debajo del slider
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
