import streamlit as st
import time
import json
import os
from utils.json_database import load_database as load_json_db, save_database as save_json_db

def show_login():
    """
    Mostra la schermata di login e registrazione.
    Gestisce l'autenticazione degli utenti e la registrazione di nuovi account.
    """
    # Assicuriamoci che lo stato di autenticazione sia corretto all'inizio
    if not st.session_state.get('is_authenticated', False):
        st.session_state.is_authenticated = False
    
    # Verifica se mostrare la schermata di benvenuto
    if not st.session_state.get('show_login_screen', False):
        from main import show_welcome_screen
        show_welcome_screen()
        return

    # Stile CSS per la pagina di login
    st.markdown("""
    <style>
        /* Stile generale della pagina */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
        }
        
        /* Reset di alcuni stili Streamlit */
        div.block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Stile dei form input */
        div[data-baseweb="input"] {
            border-radius: 6px !important;
            border: 1px solid #e2e8f0 !important;
            transition: all 0.2s ease !important;
            padding: 5px 10px !important;
            background-color: white !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #1a56db !important;
            box-shadow: 0 0 0 2px rgba(26, 86, 219, 0.1) !important;
        }
        
        /* Stile dei bottoni */
        .stButton button {
            background-color: #0066ff !important; /* Blu più acceso */
            color: white !important;
            font-weight: 500 !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.6rem 1rem !important;
            font-size: 15px !important;
            transition: all 0.2s ease !important;
        }
        .stButton button:hover {
            background-color: #0055cc !important; /* Blu più scuro per hover */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12) !important;
        }
        
        /* Stile per le tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent !important;
            border-bottom: 1px solid #e2e8f0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            color: #64748b !important;
            padding: 1rem 1.5rem !important;
            border-radius: 0 !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #1a56db !important;
            border-bottom: 2px solid #1a56db !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Contenitore principale
    container = st.container()
    
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Box principale
            st.markdown("""
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            """, unsafe_allow_html=True)
            
            # Logo dell'azienda centrato
            st.markdown('<div style="text-align: center; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
            from main import show_company_logo
            show_company_logo(size="medium", with_text=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Tabs per login e registrazione
            tab1, tab2 = st.tabs(["Accedi", "Registrati"])
            
            # Tab Login
            with tab1:
                st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Accedi al tuo account</h3>", unsafe_allow_html=True)
                
                with st.form("login_form"):
                    # Email
                    email = st.text_input("Email", placeholder="email@esempio.com")
                    
                    # Password
                    password = st.text_input("Password", type="password", placeholder="••••••••")
                    
                    # Pulsante Login
                    login_btn = st.form_submit_button("Accedi", use_container_width=True)
                    
                    if login_btn:
                        # Impostiamo immediatamente is_authenticated a False per sicurezza
                        st.session_state.is_authenticated = False
                        
                        if not email or not password:
                            st.error("Inserisci email e password.")
                        else:
                            # Carica il database più recente
                            load_database()
                            
                            # Debug per verificare gli utenti nel database
                            if not st.session_state.users:
                                st.error("Nessun utente trovato. Prova a registrarti.")
                            
                            # Verifica le credenziali - richiede match esatto
                            if email in st.session_state.users and st.session_state.users[email] == password:
                                with st.spinner("Accesso in corso..."):
                                    time.sleep(0.5)  # Simulazione caricamento
                                    st.session_state.is_authenticated = True
                                    st.session_state.current_user_email = email
                                    st.session_state.current_page = 'home'
                                    st.rerun()
                            else:
                                # Mostra messaggio di errore e NON permette l'accesso
                                st.error("Credenziali non valide. Verifica email e password.")
                                # Assicuriamoci che l'utente non sia autenticato
                                st.session_state.is_authenticated = False
                                # Forza il display dello stato
                                st.write(f"Stato autenticazione: Non autenticato")
            
            # Tab Registrazione
            with tab2:
                st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Crea un nuovo account</h3>", unsafe_allow_html=True)
                
                with st.form("register_form"):
                    # Email
                    new_email = st.text_input("Email", placeholder="email@esempio.com")
                    
                    # Password
                    new_password = st.text_input("Password", type="password", placeholder="••••••••", 
                                               help="Usa almeno 8 caratteri con lettere, numeri e simboli")
                    
                    # Conferma Password
                    confirm_password = st.text_input("Conferma Password", type="password", placeholder="••••••••")
                    
                    # Condizioni d'uso
                    terms = st.checkbox("Accetto i Termini di Servizio e la Privacy Policy")
                    
                    # Pulsante Registrazione
                    register_btn = st.form_submit_button("Registrati", use_container_width=True)
                    
                    if register_btn:
                        # Validazione
                        if not new_email or not new_password or not confirm_password:
                            st.error("Compila tutti i campi richiesti.")
                        elif '@' not in new_email or '.' not in new_email:
                            st.error("Inserisci un indirizzo email valido.")
                        elif len(new_password) < 8:
                            st.error("La password deve contenere almeno 8 caratteri.")
                        elif new_password != confirm_password:
                            st.error("Le password non corrispondono.")
                        elif not terms:
                            st.error("Devi accettare i Termini di Servizio.")
                        else:
                            # Carica il database più recente
                            load_database()
                            
                            # Verifica se l'email è già registrata
                            if new_email in st.session_state.users:
                                st.error("Email già registrata. Prova ad accedere.")
                            else:
                                # Registra il nuovo utente
                                st.session_state.users[new_email] = new_password
                                save_database()
                                st.success("Account creato con successo! Ora puoi accedere.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Footer
            st.markdown("""
            <div style="text-align: center; margin-top: 1rem;">
                <p style="color: #64748b; font-size: 0.8rem;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" 
                         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
                         style="display: inline; vertical-align: middle; margin-right: 5px;">
                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                    Connessione protetta con crittografia SSL
                </p>
                <p style="color: #64748b; font-size: 0.8rem; margin-top: 0.5rem;">
                    CiaoHost © 2025 - Tutti i diritti riservati
                </p>
            </div>
            """, unsafe_allow_html=True)

def load_database():
    """Carica il database dal file JSON"""
    try:
        data = load_json_db()
        
        # Assegna i dati alla session state
        st.session_state.properties = data.get('properties', {})
        st.session_state.users = data.get('users', {})
        
        # Stampa debug informazioni (visibile solo durante lo sviluppo)
        print(f"Database caricato. Utenti trovati: {len(st.session_state.users)}")
        
        # Verifica se ci sono utenti nel database
        if not st.session_state.users:
            print("ATTENZIONE: Nessun utente trovato nel database.")
            
    except Exception as e:
        error_msg = f"Errore durante il caricamento del database: {e}"
        print(error_msg)
        st.error(error_msg)
        
        # In caso di errore, inizializza con valori vuoti
        st.session_state.properties = {}
        st.session_state.users = {}
        
        # Salva il database vuoto
        save_database()

def save_database():
    """Salva il database nel file JSON"""
    try:
        save_json_db({
            'properties': st.session_state.properties,
            'users': st.session_state.users
        })
    except Exception as e:
        st.error(f"Errore durante il salvataggio del database: {e}")