import streamlit as st

def apply_animations():
    """Applica animazioni avanzate all'interfaccia utente"""
    
    # CSS per animazioni avanzate
    st.markdown("""
    <style>
    /* Animazioni di base */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes zoomIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Applicazione delle animazioni agli elementi */
    
    /* Animazione per il titolo principale */
    h1, .stTitle {
        animation: fadeIn 1s ease-out;
    }
    
    /* Animazione per i sottotitoli */
    h2, h3, .stSubheader {
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Animazione per i paragrafi */
    p, .stText {
        animation: fadeIn 1.2s ease-out;
    }
    
    /* Animazione per i pulsanti */
    .stButton > button {
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08) !important;
    }
    
    .stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    .stButton > button::after {
        content: "";
        display: block;
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        pointer-events: none;
        background-image: radial-gradient(circle, #fff 10%, transparent 10.01%);
        background-repeat: no-repeat;
        background-position: 50%;
        transform: scale(10, 10);
        opacity: 0;
        transition: transform 0.5s, opacity 1s;
    }
    
    .stButton > button:active::after {
        transform: scale(0, 0);
        opacity: 0.3;
        transition: 0s;
    }
    
    /* Animazione per le card */
    .dashboard-card, div[data-testid="stVerticalBlock"] > div {
        animation: zoomIn 0.8s ease-out;
        transition: all 0.3s ease !important;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Animazione per le metriche */
    div[data-testid="stMetric"] {
        animation: slideInRight 0.8s ease-out;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: scale(1.03) !important;
    }
    
    /* Animazione per i grafici */
    div[data-testid="stVegaLiteChart"], div[data-testid="stArrowVegaLiteChart"] {
        animation: fadeIn 1.5s ease-out;
        transition: all 0.5s ease !important;
    }
    
    /* Animazione per le tabelle */
    div[data-testid="stTable"], div[data-testid="stDataFrame"] {
        animation: fadeIn 1.2s ease-out;
        transition: all 0.3s ease !important;
    }
    
    /* Animazione per le immagini */
    img {
        animation: zoomIn 1s ease-out;
        transition: all 0.5s ease !important;
    }
    
    img:hover {
        transform: scale(1.05) !important;
    }
    
    /* Animazione per i selettori */
    div[data-testid="stSelectbox"], div[data-testid="stMultiselect"] {
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Animazione per gli input */
    div[data-testid="stTextInput"], div[data-testid="stNumberInput"], div[data-testid="stDateInput"], div[data-testid="stTimeInput"], div[data-testid="stTextArea"] {
        animation: slideInRight 0.8s ease-out;
    }
    
    /* Animazione per i checkbox */
    div[data-testid="stCheckbox"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Animazione per i radio */
    div[data-testid="stRadio"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Animazione per i slider */
    div[data-testid="stSlider"] {
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Animazione per i file uploader */
    div[data-testid="stFileUploader"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Animazione per i messaggi di successo */
    div[data-testid="stSuccessMessage"] {
        animation: pulse 2s infinite;
    }
    
    /* Animazione per i messaggi di errore */
    div[data-testid="stErrorMessage"] {
        animation: shake 0.5s;
    }
    
    /* Animazione per i messaggi di info */
    div[data-testid="stInfoMessage"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Animazione per i messaggi di warning */
    div[data-testid="stWarningMessage"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Animazione per la sidebar */
    [data-testid="stSidebar"] {
        animation: slideInLeft 0.5s ease-out;
    }
    
    /* Animazione per gli elementi della sidebar */
    [data-testid="stSidebar"] > div > div > div > div > div {
        animation: fadeIn 1s ease-out;
        animation-fill-mode: both;
    }
    
    /* Animazione per i tab */
    button[role="tab"] {
        transition: all 0.3s ease !important;
    }
    
    button[role="tab"]:hover {
        transform: translateY(-2px) !important;
    }
    
    /* Animazione per i contenuti dei tab */
    div[role="tabpanel"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Effetto shimmer per elementi in caricamento */
    .shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite linear;
    }
    
    /* Animazione per gli elementi in hover */
    .hover-float:hover {
        animation: float 2s ease-in-out infinite;
    }
    
    /* Animazione per gli elementi che ruotano */
    .rotate {
        animation: rotate 2s linear infinite;
    }
    
    /* Animazione per gli elementi che pulsano */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Animazione per gli elementi che rimbalzano */
    .bounce {
        animation: bounce 2s infinite;
    }
    
    /* Animazione per gli elementi che fluttuano */
    .float {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Animazione per gli elementi che appaiono gradualmente */
    .fade-in {
        animation: fadeIn 1s ease-out;
    }
    
    /* Animazione per gli elementi che entrano da sinistra */
    .slide-in-left {
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Animazione per gli elementi che entrano da destra */
    .slide-in-right {
        animation: slideInRight 0.8s ease-out;
    }
    
    /* Animazione per gli elementi che si ingrandiscono */
    .zoom-in {
        animation: zoomIn 0.8s ease-out;
    }
    
    /* Effetto di transizione per tutti gli elementi */
    * {
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def add_animated_welcome():
    """Aggiunge un'animazione di benvenuto"""
    
    st.markdown("""
    <style>
    @keyframes welcomeAnimation {
        0% { opacity: 0; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .welcome-animation {
        animation: welcomeAnimation 1.5s ease-out;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    }
    
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    </style>
    
    <div class="welcome-animation">
        <div class="welcome-title">Benvenuto in CiaoHost AI Manager</div>
        <div class="welcome-subtitle">La piattaforma intelligente per la gestione dei tuoi immobili</div>
    </div>
    """, unsafe_allow_html=True)

def add_animated_cards():
    """Aggiunge stili per card animate"""
    
    st.markdown("""
    <style>
    @keyframes cardEntrance {
        from {
            opacity: 0;
            transform: translateY(25px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        animation: cardEntrance 0.8s ease-out;
        animation-fill-mode: both;
    }
    
    .animated-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #3b82f6;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1e293b;
    }
    
    .card-text {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Animazione sequenziale per le card */
    .animated-card:nth-child(1) {
        animation-delay: 0.1s;
    }
    
    .animated-card:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .animated-card:nth-child(3) {
        animation-delay: 0.3s;
    }
    
    .animated-card:nth-child(4) {
        animation-delay: 0.4s;
    }
    </style>
    """, unsafe_allow_html=True)

def add_animated_buttons():
    """Aggiunge stili per pulsanti animati"""
    
    st.markdown("""
    <style>
    .animated-button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        display: inline-block;
        text-align: center;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .animated-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
    
    .animated-button:active {
        transform: translateY(1px);
    }
    
    .animated-button::after {
        content: "";
        display: block;
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        pointer-events: none;
        background-image: radial-gradient(circle, rgba(255, 255, 255, 0.3) 10%, transparent 10.01%);
        background-repeat: no-repeat;
        background-position: 50%;
        transform: scale(10, 10);
        opacity: 0;
        transition: transform 0.5s, opacity 1s;
    }
    
    .animated-button:active::after {
        transform: scale(0, 0);
        opacity: 0.3;
        transition: 0s;
    }
    </style>
    """, unsafe_allow_html=True)

def add_animated_progress():
    """Aggiunge stili per barre di progresso animate"""
    
    st.markdown("""
    <style>
    @keyframes progressAnimation {
        0% { width: 0%; }
    }
    
    .progress-container {
        background-color: #f1f5f9;
        border-radius: 10px;
        height: 10px;
        width: 100%;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #3b82f6 0%, #1e40af 100%);
        animation: progressAnimation 1.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)

def add_animated_charts():
    """Aggiunge stili per grafici animati"""
    
    st.markdown("""
    <style>
    @keyframes chartAnimation {
        0% { opacity: 0; transform: scaleY(0); }
        100% { opacity: 1; transform: scaleY(1); }
    }
    
    .chart-container {
        animation: fadeIn 1.5s ease-out;
        padding: 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .chart-bar {
        background: linear-gradient(90deg, #3b82f6 0%, #1e40af 100%);
        border-radius: 5px;
        margin: 0.5rem 0;
        height: 30px;
        animation: chartAnimation 1.5s ease-out;
        transform-origin: left;
    }
    </style>
    """, unsafe_allow_html=True)

def add_animated_icons():
    """Aggiunge stili per icone animate"""
    
    st.markdown("""
    <style>
    @keyframes iconPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    @keyframes iconRotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes iconBounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
    
    .icon-pulse {
        animation: iconPulse 2s infinite;
        display: inline-block;
    }
    
    .icon-rotate {
        animation: iconRotate 3s linear infinite;
        display: inline-block;
    }
    
    .icon-bounce {
        animation: iconBounce 2s infinite;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

def add_animated_notifications():
    """Aggiunge stili per notifiche animate"""
    
    st.markdown("""
    <style>
    @keyframes notificationSlideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes notificationSlideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: notificationSlideIn 0.5s ease-out, notificationSlideOut 0.5s ease-in 4.5s;
        animation-fill-mode: forwards;
    }
    
    .notification-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .notification-error {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        color: white;
    }
    
    .notification-info {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
    }
    
    .notification-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def add_all_animations():
    """Applica tutte le animazioni"""
    apply_animations()
    add_animated_cards()
    add_animated_buttons()
    add_animated_progress()
    add_animated_charts()
    add_animated_icons()
    add_animated_notifications()