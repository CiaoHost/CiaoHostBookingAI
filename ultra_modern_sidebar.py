import streamlit as st
import json
import random

def get_current_user():
    """Ottiene l'username dell'utente loggato"""
    try:
        # Carica il database utenti
        with open("c:/Users/DEADSHOT/Desktop/ciaohostreale/ciaohostluss/DatabaseCiaoHostProprieta.json", "r") as f:
            data = json.load(f)
            users = data.get("users", {})
        
        # Ottieni l'email dell'utente loggato dal session state
        current_email = st.session_state.get('current_user_email', '')
        
        if current_email and current_email in users:
            # Estrai il nome utente dall'email (parte prima della @)
            username = current_email.split('@')[0]
            return username
        else:
            return "Utente"
    except:
        return "Utente"

def get_user_avatar(email):
    """Genera un avatar consistente per ogni utente basato sull'email"""
    avatars = [
        "�", "�", "🧑", "👴", "👵", "👱‍♂️", "�‍♀️", "�‍🦰", 
        "�👩‍🦰", "�‍🦱", "👩‍�", "👨‍🦲", "�‍🦲", "👨‍🦳", "👩‍🦳",
        "�", "👨‍🦴", "👩‍🦴", "👨‍�", "👩‍�", "🧑‍�", "�‍🎓", 
        "👩‍🎓", "🧑‍�", "👨‍⚕️", "👩‍⚕️", "🧑‍⚕️", "👨‍🏫", "👩‍🏫"
    ]
    # Usa l'email come seed per avere sempre lo stesso avatar per lo stesso utente
    if email:
        random.seed(hash(email))
        avatar = random.choice(avatars)
        random.seed()  # Reset del seed
        return avatar
    return "�"

def create_ultra_modern_sidebar():
    """Crea una sidebar semplice e funzionale"""
    
    # CSS per la sidebar semplice
    st.markdown("""
    <style>
    /* Simple Sidebar Styling */
    [data-testid="stSidebar"] {
        background: #1e293b !important;
        border-right: 1px solid rgba(255,255,255,0.1) !important;
        width: 260px !important;
    }
    
    [data-testid="stSidebar"] > div {
        background: transparent !important;
        padding: 1rem !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #e2e8f0 !important;
        margin-bottom: 0.5rem !important;
        padding: 0.5rem !important;
        border-radius: 0.5rem !important;
        font-size: 0.875rem !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(59, 130, 246, 0.2) !important;
        border-color: rgba(59, 130, 246, 0.3) !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #94a3b8 !important;
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #94a3b8 !important;
        font-size: 0.875rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Force title color override */
    [data-testid="stSidebar"] .element-container h3 {
        color: #94a3b8 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #94a3b8 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1) !important;
        margin: 1rem 0 !important;
    }
    
    [data-testid="stSidebar"] strong {
        color: #64748b !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: block;
        margin-bottom: 0.5rem !important;
    }
    
    /* Logo styling */
    [data-testid="stSidebar"] img {
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Advanced User Profile Section */
    .user-profile-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1)) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        margin: 8px 0 !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .user-profile-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .user-profile-card:hover::before {
        left: 100%;
    }
    
    .user-avatar-advanced {
        width: 48px !important;
        height: 48px !important;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 20px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        animation: avatarPulse 3s ease-in-out infinite !important;
    }
    
    @keyframes avatarPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }
        50% { transform: scale(1.05); box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4); }
    }
    
    .user-info-advanced {
        flex: 1 !important;
        margin-left: 12px !important;
    }
    
    .user-name-advanced {
        color: white !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        margin: 0 0 4px 0 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    .user-status-advanced {
        color: #94a3b8 !important;
        font-size: 11px !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }
    
    .status-dot {
        width: 8px !important;
        height: 8px !important;
        background: #10b981 !important;
        border-radius: 50% !important;
        animation: statusPulse 2s ease-in-out infinite !important;
        box-shadow: 0 0 6px rgba(16, 185, 129, 0.6) !important;
    }
    
    @keyframes statusPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.2); }
    }
    
    .user-profile-content {
        display: flex !important;
        align-items: center !important;
        position: relative !important;
        z-index: 1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def show_navigation_breadcrumb():
    """Mostra un breadcrumb moderno per la navigazione"""
    
    # Mappa delle pagine con icone e descrizioni
    page_info = {
        'home': {'icon': '🏠', 'title': 'Home', 'subtitle': 'Benvenuto in CiaoHost'},
        'ai': {'icon': '🤖', 'title': 'Assistente AI', 'subtitle': 'Chat intelligente per supporto'},
        'search_properties': {'icon': '🔍', 'title': 'Ricerca Immobili', 'subtitle': 'Trova la proprietà perfetta'},
        'subscriptions': {'icon': '💼', 'title': 'Abbonamenti', 'subtitle': 'Scegli il piano giusto per te'},
        'dashboard': {'icon': '📊', 'title': 'Dashboard Intelligente', 'subtitle': 'Panoramica completa delle tue performance'},
        'ai_management': {'icon': '🤖', 'title': 'AI Gestionale', 'subtitle': 'Assistente AI specializzato per la gestione immobiliare'},
        'cleaning_management': {'icon': '🧹', 'title': 'Gestione Pulizie', 'subtitle': 'Organizza e monitora le pulizie'},
        'dynamic_pricing': {'icon': '💰', 'title': 'Prezzi Dinamici', 'subtitle': 'Ottimizza i prezzi automaticamente'},
        'fiscal_management': {'icon': '👥', 'title': 'Gestione Utenti', 'subtitle': 'Amministra utenti e permessi'},
        'property_management': {'icon': '🏢', 'title': 'Gestione Immobili', 'subtitle': 'Gestisci il tuo portafoglio immobiliare'},
        'report_builder': {'icon': '📈', 'title': 'Report Builder', 'subtitle': 'Crea report personalizzati'},
        'settings': {'icon': '⚙️', 'title': 'Impostazioni', 'subtitle': 'Configura le tue preferenze'}
    }
    
    # Ottieni la pagina corrente
    current_page = st.session_state.get('current_page', 'home')
    page_data = page_info.get(current_page, page_info['home'])
    
    # Mostra il breadcrumb
    st.markdown(f"""
    <div class="modern-breadcrumb">
        <div class="breadcrumb-content">
            <div class="breadcrumb-icon">{page_data['icon']}</div>
            <div class="breadcrumb-info">
                <h1 class="breadcrumb-title">{page_data['title']}</h1>
                <p class="breadcrumb-subtitle">{page_data['subtitle']}</p>
            </div>
        </div>
    </div>
    
    <style>
    .modern-breadcrumb {{
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9));
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    .breadcrumb-content {{
        display: flex;
        align-items: center;
        gap: 16px;
    }}
    
    .breadcrumb-icon {{
        font-size: 32px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }}
    
    .breadcrumb-title {{
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #1e293b, #475569);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .breadcrumb-subtitle {{
        font-size: 12px;
        color: #64748b;
        margin: 2px 0 0 0;
        font-weight: 500;
    }}
    </style>
    """, unsafe_allow_html=True)

def render_ultra_modern_sidebar():
    """Renderizza la sidebar semplice e funzionale"""
    
    # Applica gli stili
    create_ultra_modern_sidebar()
    
    # Logo e titolo
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo.png", width=80)
    with col2:
        st.markdown('<h3 style="color: #94a3b8 !important; margin-bottom: 0;">CiaoHost</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8 !important; font-style: italic; margin-top: 0;">Gestione Intelligente</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sezione Principale
    st.markdown("**PRINCIPALE**")
    
    # Pulsanti di navigazione principali
    nav_items = [
        {"key": "home", "icon": "🏠", "text": "Home", "page": "home"},
        {"key": "ai", "icon": "🤖", "text": "Assistente AI", "page": "ai"},
        {"key": "search", "icon": "🔍", "text": "Ricerca Immobili", "page": "search_properties"},
        {"key": "subscriptions", "icon": "💼", "text": "Abbonamenti", "page": "subscriptions"}
    ]
    
    for item in nav_items:
        if st.button(
            f"{item['icon']} {item['text']}", 
            key=f"sidebar_{item['key']}", 
            use_container_width=True
        ):
            st.session_state.current_page = item['page']
            st.rerun()
    
    # Sezione Premium (solo se abbonamento attivo)
    if st.session_state.get('subscription_purchased', False):
        st.markdown("---")
        st.markdown("**PREMIUM**")
        
        premium_items = [
            {"key": "dashboard", "icon": "📊", "text": "Dashboard", "page": "dashboard"},
            {"key": "cleaning", "icon": "🧹", "text": "Gestione Pulizie", "page": "cleaning_management"},
            {"key": "pricing", "icon": "💰", "text": "Prezzi Dinamici", "page": "dynamic_pricing"},
            {"key": "users", "icon": "👥", "text": "Gestione Utenti", "page": "fiscal_management"},
            {"key": "properties", "icon": "🏢", "text": "Gestione Immobili", "page": "property_management"},
            {"key": "reports", "icon": "📈", "text": "Report Builder", "page": "report_builder"},
            {"key": "settings", "icon": "⚙️", "text": "Impostazioni", "page": "settings"}
        ]
        
        for item in premium_items:
            if st.button(
                f"{item['icon']} {item['text']}", 
                key=f"sidebar_premium_{item['key']}", 
                use_container_width=True
            ):
                st.session_state.current_page = item['page']
                st.rerun()
    
    # Spazio per spingere il logout in basso
    st.markdown("<br>" * 3, unsafe_allow_html=True)
    
    # Info utente avanzata
    st.markdown("---")
    current_username = get_current_user()
    current_email = st.session_state.get('current_user_email', '')
    avatar = get_user_avatar(current_email)
    
    # Card utente moderna
    st.markdown(f"""
    <div class="user-profile-card">
        <div class="user-profile-content">
            <div class="user-avatar-advanced">{avatar}</div>
            <div class="user-info-advanced">
                <div class="user-name-advanced">{current_username}</div>
                <div class="user-status-advanced">
                    <div class="status-dot"></div>
                    <span>Online</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pulsante Logout
    if st.button("🚪 Logout", key="sidebar_logout", use_container_width=True):
        # Reset dello stato di autenticazione
        for key in list(st.session_state.keys()):
            if key.startswith(('is_authenticated', 'current_page', 'subscription_purchased')):
                del st.session_state[key]
        st.rerun()

