# Estilos actualizados
st.markdown("""
<style>
    /* Base */
    .stApp {
        background-color: #1E1E1E;
    }

    /* Título */
    .main-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 2rem 0 3rem 0;
    }

    /* Selector de crédito */
    .stSelectbox [data-baseweb="select"] {
        background-color: #27282B !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        color: white !important;
        background: #27282B !important;
        border: none !important;
        cursor: pointer !important;
    }

    /* Contenedor de monto */
    .monto-question {
        color: white;
        font-size: 1.3rem;
        margin: 2.5rem 0 1rem 0;
    }

    /* Slider y valores */
    .slider-values {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 0.9rem;
        opacity: 0.8;
        margin-bottom: 0.5rem;
    }
    
    .stSlider > div {
        padding: 0 !important;
    }

    /* Personalización del slider */
    .stSlider [data-baseweb="slider"] {
        height: 6px !important;
    }
    
    div[data-testid="stSlider"] > div > div > div {
        background: linear-gradient(to right, #FF4B4B var(--progress), #4B5563 var(--progress)) !important;
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
        cursor: pointer !important;
    }

    /* Ocultar elementos innecesarios del slider */
    .stSlider [data-baseweb="slider"] div[role="slider"] div,
    .stSlider [data-baseweb="tooltip"] {
        display: none !important;
    }

    /* Valor seleccionado */
    .monto-selected {
        color: #3B82F6;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 2rem 0 3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<h1 class="main-title">Simulador de Crédito Loansi</h1>', unsafe_allow_html=True)

# Selector de línea de crédito
tipo_credito = st.selectbox("Selecciona la línea de crédito", 
                           options=LINEAS_DE_CREDITO.keys(), 
                           key="select_credito",
                           label_visibility="visible")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto
st.markdown('<div class="monto-question">¿Cuánto necesitas?</div>', unsafe_allow_html=True)

# Valores min/max
st.markdown(f"""
<div class="slider-values">
    <span>$ {format_number(detalles['monto_min'])}</span>
    <span>$ {format_number(detalles['monto_max'])}</span>
</div>
""", unsafe_allow_html=True)

# Ajustar el progress del slider
col1, col2 = st.columns([20,1])
with col1:
    monto = st.slider("", 
        min_value=detalles["monto_min"],
        max_value=detalles["monto_max"],
        step=50000,
        key="monto_slider",
        label_visibility="collapsed"
    )

# Mostrar el valor seleccionado
progress = (monto - detalles["monto_min"]) / (detalles["monto_max"] - detalles["monto_min"]) * 100
st.markdown(f"""
<style>
    div[data-testid="stSlider"] > div > div > div {{
        background: linear-gradient(to right, #FF4B4B {progress}%, #4B5563 {progress}%) !important;
    }}
</style>
<div class="monto-selected">$ {format_number(monto)}</div>
""", unsafe_allow_html=True)
