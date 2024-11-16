st.markdown("""
<style>
    /* Tema oscuro base */
    .stApp {
        background-color: #1E1E1E;
    }

    /* Título principal */
    .main-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 2rem 0 3rem 0;
    }

    /* Selector de línea de crédito */
    .stSelectbox > div > div {
        background-color: #27282B !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem !important;
        border-radius: 0.5rem !important;
    }

    /* Container del monto */
    .monto-container {
        position: relative;
        margin: 3rem 0;
    }

    /* Texto "¿Cuánto necesitas?" */
    .monto-title {
        color: white;
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }

    /* Valores min/max del slider */
    .minmax-values {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 0.9rem;
        position: absolute;
        width: 100%;
        top: -1.5rem;
    }

    /* Slider personalizado */
    .stSlider > div {
        padding: 2rem 0 !important;
    }

    .stSlider div[data-baseweb="slider"] > div {
        background: linear-gradient(to right, #FF4B4B 50%, #4B5563 50%) !important;
        height: 0.4rem !important;
        border-radius: 0.2rem !important;
    }

    .stSlider div[role="slider"] {
        background: #3B82F6 !important;
        border: 2px solid white !important;
        width: 1.5rem !important;
        height: 1.5rem !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        top: -0.55rem !important;
        z-index: 2 !important;
    }

    /* Ocultar elementos del slider */
    .stSlider div[data-baseweb="slider"] div[role="slider"] div,
    .stSlider div[data-baseweb="tooltip"],
    .stSlider div[role="slider"] span {
        display: none !important;
    }

    /* Valor del monto seleccionado */
    .monto-value {
        color: #3B82F6;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-title">Simulador de Crédito Loansi</h1>', unsafe_allow_html=True)

# Selector de línea de crédito
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), key="select_credito")
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Sección de monto
st.markdown("""
<div class="monto-container">
    <div class="monto-title">¿Cuánto necesitas?</div>
    <div class="minmax-values">
        <span>$ 1.000.000</span>
        <span>$ 20.000.000</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Slider
monto = st.slider("", 
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    key="monto_slider",
    label_visibility="collapsed"
)

# Mostrar valor seleccionado
st.markdown(f'<div class="monto-value">$ {format_number(monto)}</div>', unsafe_allow_html=True)
