
import streamlit as st
import google.generativeai as genai
import os
import json
import pandas as pd
from dotenv import load_dotenv
import time
import random
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from attached_assets.cleaning_management import (
    show_cleaning_calendar,
    show_cleaning_services,
    show_scheduling,
    show_automated_messages
)
# Note: The 'attached_assets.cleaning_management' module has dependencies
# on a 'utils' directory (e.g., 'utils.database') and potentially a 'data' subdirectory.
# Ensure these are correctly structured for the imports and file access to work.

# import attached_assets.dashboard_creator as dashboard_creator
# import attached_assets.dashboard_creator as dashboard_creator
# import attached_assets.data_insights as data_insights
import attached_assets.dynamic_pricing as dynamic_pricing
# import attached_assets.fiscal_management as fiscal_management
from property_management import show_property_management
# import attached_assets.report_builder as report_builder
import attached_assets.settings as settings

# Funzione per mostrare l'effetto coriandoli usando direttamente Streamlit
def show_confetti():
    """
    Mostra un effetto coriandoli semplice ma visibile usando direttamente Streamlit
    """
    # Salva lo stato per sapere se mostrare i coriandoli
    if 'show_confetti' not in st.session_state:
        st.session_state.show_confetti = True
    
    if st.session_state.show_confetti:
        # Crea un container per i coriandoli
        confetti_container = st.empty()
        
        # Genera coriandoli colorati (emoji)
        confetti_symbols = ["🎉", "🎊", "🥳"]
        
        # Crea righe di coriandoli con emoji
        for _ in range(5):  # 5 righe di coriandoli
            row = ""
            for _ in range(15):  # 15 emoji per riga
                row += confetti_symbols[int(random.random() * len(confetti_symbols))] + " "
            confetti_container.markdown(f"<h1 style='text-align: center; line-height: 1;'>{row}</h1>", unsafe_allow_html=True)
        
        # Mostra un messaggio di congratulazioni
        st.balloons()  # Usa anche l'effetto palloncini integrato di Streamlit
        st.success("🎉 Congratulazioni! Abbonamento attivato con successo! 🎉")
        
        # Disattiva i coriandoli dopo averli mostrati una volta
        st.session_state.show_confetti = False

# Sezione per mostrare il logo aziendale
def show_footer():
    """
    Mostra il footer con copyright in tutte le pagine
    """
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;">
        <p style="color: #64748b; font-size: 0.8rem;">
            CiaoHost © 2025 - Tutti i diritti riservati
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_company_logo(size="medium", with_text=True):
    """
    Mostra il logo aziendale con dimensioni personalizzabili
    
    Parametri:
    - size: "small" (80px), "medium" (150px), "large" (200px)
    - with_text: se True, mostra anche il testo "CiaoHost" accanto al logo
    """
    # Dimensioni del logo in base al parametro size (aumentate)
    sizes = {
        "small": 120,
        "medium": 200,
        "large": 280
    }
    width = sizes.get(size, 200)  # Default a medium se size non è valido
    
    # Percorso del logo
    logo_path = "logo.png"
    
    # Verifica se il file esiste
    if os.path.exists(logo_path):
        # Usa il logo reale
        if with_text:
            # Verifica se siamo nella pagina di login
            if st.session_state.get('current_page') == 'login':
                # Layout più centrato per la pagina di login
                cols = st.columns([1, 2])
                with cols[0]:
                    st.image(logo_path, width=width)
                with cols[1]:
                    st.markdown(f"""
                    <h1 style="color: #4361ee; font-size: {int(width/3)}px; margin-top: {int(width/4)}px; text-align: center;">CiaoHost</h1>
                    """, unsafe_allow_html=True)
            else:
                # Layout normale per le altre pagine
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(logo_path, width=width)
                with cols[1]:
                    st.markdown(f"""
                    <h1 style="color: #4361ee; font-size: {int(width/3)}px; margin-top: {int(width/4)}px;">CiaoHost</h1>
                    """, unsafe_allow_html=True)
        else:
            st.image(logo_path, width=width)
    else:
        # Fallback al logo generato con CSS
        if with_text:
            # Verifica se siamo nella pagina di login per il layout
            if st.session_state.get('current_page') == 'login':
                # Layout più centrato per la pagina di login
                cols = st.columns([1, 2])
                with cols[0]:
                    st.markdown(f"""
                    <div style="background-color: #4361ee; color: white; width: {width}px; height: {width}px; 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                margin: 0 auto; text-align: center; line-height: {width}px; font-weight: bold; 
                                font-size: {int(width/3)}px;">
                        CH
                    </div>
                    """, unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"""
                    <h1 style="color: #4361ee; font-size: {int(width/3)}px; margin-top: {int(width/4)}px; text-align: center;">CiaoHost</h1>
                    """, unsafe_allow_html=True)
            else:
                # Layout normale per le altre pagine
                cols = st.columns([1, 3])
                with cols[0]:
                    st.markdown(f"""
                    <div style="background-color: #4361ee; color: white; width: {width}px; height: {width}px; 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                margin: 0 auto; text-align: center; line-height: {width}px; font-weight: bold; 
                                font-size: {int(width/3)}px;">
                        CH
                    </div>
                    """, unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"""
                    <h1 style="color: #4361ee; font-size: {int(width/3)}px; margin-top: {int(width/4)}px;">CiaoHost</h1>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #4361ee; color: white; width: {width}px; height: {width}px; 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        margin: 0 auto; text-align: center; line-height: {width}px; font-weight: bold; 
                        font-size: {int(width/3)}px;">
                CH
            </div>
            """, unsafe_allow_html=True)

# Puoi chiamare show_company_logo() dove preferisci nel layout, ad esempio subito dopo l'inizio di main()

API_KEY = "AIzaSyB-Lgs26JGbdxdJFVk1-1JQFd2lUfyFXwM"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Errore durante la configurazione di Gemini: {e}")
    model = None

CONTESTO_IMMOBILIARE = """
Sei un esperta guida turistica dell'azienda chiamata CiaoHost, devi offrire supporto ai clienti e hai queste capacità:
1. Aiutare i clienti a prenotare un soggiorno negli immobili disponibili
2. Andare ad aiutare per avere informazioni su un' immobile dove stanno soggiornando
3. Andare a costruire un trip plan nel caso soggiornino da qualche parte e vogliano avere delle informazioni su cosa fare e cosa visitare

In caso ti domandino chi sei o cosa fai rispondi in modo intelligente, da ora in poi sei CiaoHost AI e sei stato costruito da CiaoHost,
devi simulare il tutto. Ma non devi sempre ribadire chi sei, solo in caso te lo chiedono. In più se ti do un immobile devi dirmi se è disponibile o meno e non devi assolutamente dire l'id dell'immobile.

IMPORTANTE: Se l'utente esprime la volontà di prenotare un soggiorno (usando frasi come "vorrei prenotare", "voglio affittare", "cerco un alloggio", ecc.), devi SEMPRE rispondere con questo messaggio:

"✨ Sono felice di aiutarti con la prenotazione!

Per prenotare un immobile, usa il comando /prenota seguito dal nome dell'immobile.
Esempio: /prenota Villa Bella

Questo avvierà il processo di prenotazione guidato dove ti chiederò:
• Data di check-in
• Data di check-out
• Numero di ospiti
• Ora di arrivo
• Eventuali richieste speciali

La tua prenotazione verrà salvata nel nostro sistema e riceverai una conferma."

Formatta le risposte con:
• Liste puntate per i concetti chiave
• Tabelle comparative quando utile
• Evidenziazione termini tecnici (es. cap rate)
"""

CONTESTO_GESTIONALE = """
Sei un esperto di gestione immobiliare dell'azienda chiamata CiaoHost, devi offrire supporto ai clienti e hai queste capacità:
1. Analizzare dati di mercato e generare report
2. Creare contratti d'affitto/vendita personalizzati
3. Calcolare ROI, Tasso Capitalizzazione e metriche finanziarie
4. Generare descrizioni accattivanti per annunci immobiliari
5. Rispondere a domande tecniche su normative e pratiche notarili
6. Aiutare i clienti a prenotare un soggiorno negli immobili disponibili

In caso ti domandino chi sei o cosa fai rispondi in modo intelligente, da ora in poi sei CiaoHost AI e sei stato costruito da CiaoHost,
devi simulare il tutto. Ma non devi sempre ribadire chi sei, solo in caso te lo chiedono. In più se ti do un immobile devi dirmi se è disponibile o meno e non devi assolutamente dire l'id dell'immobile.

Formatta le risposte con:
• Liste puntate per i concetti chiave
• Tabelle comparative quando utile
• Evidenziazione termini tecnici (es. cap rate, ROI, yield)
"""

DB_FILE = "DatabaseCiaoHostProprieta.json"
BOOKINGS_DB_FILE = "DatabaseCiaoHostPrenotazioni.json"
ADMIN_CREDENTIALS = {"username": "admin", "password": "root"}

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'properties' not in st.session_state:
    st.session_state.properties = {}
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'user_states' not in st.session_state:
    st.session_state.user_states = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'current_user_email' not in st.session_state:
    st.session_state.current_user_email = None
if 'admin_state' not in st.session_state:
    st.session_state.admin_state = {'mode': None, 'step': None}
if 'data' not in st.session_state:
    st.session_state.data = None
if 'dashboard_panels' not in st.session_state:
    st.session_state.dashboard_panels = []
if 'saved_dashboards' not in st.session_state:
    st.session_state.saved_dashboards = {}
if 'subscription_purchased' not in st.session_state:
    st.session_state.subscription_purchased = False

from utils.json_database import load_database as load_json_db, save_database as save_json_db, get_all_properties

def load_database():
    try:
        data = load_json_db()
        st.session_state.properties = data.get('properties', {})
        st.session_state.users = data.get('users', {})
    except Exception as e:
        st.error(f"Errore durante il caricamento del database: {e}")
        st.session_state.properties = {}
        st.session_state.users = {}
        save_database()

def save_database():
    try:
        save_json_db({
            'properties': st.session_state.properties,
            'users': st.session_state.users
        })
    except Exception as e:
        st.error(f"Errore durante il salvataggio del database: {e}")

def handle_booking(message_text):
    """Gestisce il processo di prenotazione attraverso la chat"""
    from datetime import datetime
    import uuid
    from utils.booking_database import save_bookings_database
    
    booking_state = st.session_state.get('booking_state', {})
    
    # Inizializza lo stato di prenotazione se non esiste
    if 'booking_state' not in st.session_state:
        st.session_state.booking_state = {
            'active': False,
            'step': None,
            'property_id': None,
            'property_name': None,
            'data': {}
        }
        booking_state = st.session_state.booking_state
    
    # Controlla se il messaggio è un comando di prenotazione
    if message_text.lower().startswith("/prenota "):
        property_name = message_text[9:].strip()
        
        # Cerca la proprietà nel database
        property_found = False
        property_id = None
        
        for pid, prop in st.session_state.properties.items():
            if prop.get('name', '').lower() == property_name.lower():
                property_found = True
                property_id = pid
                property_name = prop.get('name')
                break
        
        if property_found:
            # Inizia il processo di prenotazione
            booking_state['active'] = True
            booking_state['step'] = 'check_in_date'
            booking_state['property_id'] = property_id
            booking_state['property_name'] = property_name
            booking_state['data'] = {
                'property_id': property_id,
                'property_name': property_name
            }
            
            return f"🏠 Hai selezionato: **{property_name}**\n\nPer completare la prenotazione, ho bisogno di alcune informazioni.\n\nPer prima cosa, quando vorresti fare il check-in? (formato: GG/MM/AAAA)"
        else:
            return f"❌ Mi dispiace, non ho trovato nessun immobile con il nome '{property_name}'. Puoi verificare il nome e riprovare."
    
    # Se c'è una prenotazione attiva, gestisci i vari passaggi
    if booking_state.get('active', False):
        current_step = booking_state.get('step')
        
        if current_step == 'check_in_date':
            # Salva la data di check-in
            try:
                # Semplice validazione del formato data
                if len(message_text.split('/')) != 3:
                    return "❌ Formato data non valido. Usa il formato GG/MM/AAAA."
                
                booking_state['data']['check_in_date'] = message_text
                booking_state['step'] = 'check_out_date'
                return "📅 Quando vorresti fare il check-out? (formato: GG/MM/AAAA)"
            except:
                return "❌ Formato data non valido. Usa il formato GG/MM/AAAA."
        
        elif current_step == 'check_out_date':
            # Salva la data di check-out
            try:
                # Semplice validazione del formato data
                if len(message_text.split('/')) != 3:
                    return "❌ Formato data non valido. Usa il formato GG/MM/AAAA."
                
                booking_state['data']['check_out_date'] = message_text
                booking_state['step'] = 'guests'
                return "👥 Quante persone soggiorneranno? (inserisci un numero)"
            except:
                return "❌ Formato data non valido. Usa il formato GG/MM/AAAA."
        
        elif current_step == 'guests':
            # Salva il numero di ospiti
            try:
                num_guests = int(message_text)
                if num_guests <= 0:
                    return "❌ Il numero di ospiti deve essere maggiore di zero."
                
                booking_state['data']['guests'] = num_guests
                booking_state['step'] = 'check_in_time'
                return "🕒 A che ora prevedi di arrivare per il check-in? (formato: HH:MM)"
            except:
                return "❌ Inserisci un numero valido per il numero di ospiti."
        
        elif current_step == 'check_in_time':
            # Salva l'ora di check-in
            booking_state['data']['check_in_time'] = message_text
            booking_state['step'] = 'special_requests'
            return "📝 Hai richieste speciali? (se non ne hai, scrivi 'nessuna')"
        
        elif current_step == 'special_requests':
            # Salva le richieste speciali e completa la prenotazione
            booking_state['data']['special_requests'] = message_text
            booking_state['step'] = 'confirmation'
            
            # Prepara il riepilogo della prenotazione
            property_name = booking_state['data']['property_name']
            check_in = booking_state['data']['check_in_date']
            check_out = booking_state['data']['check_out_date']
            guests = booking_state['data']['guests']
            check_in_time = booking_state['data']['check_in_time']
            special_requests = booking_state['data']['special_requests']
            
            summary = f"""
📋 **Riepilogo Prenotazione**

🏠 **Immobile**: {property_name}
📅 **Check-in**: {check_in} alle {check_in_time}
📅 **Check-out**: {check_out}
👥 **Ospiti**: {guests}
📝 **Richieste speciali**: {special_requests}

Confermi la prenotazione? (sì/no)
"""
            return summary
        
        elif current_step == 'confirmation':
            if message_text.lower() in ['sì', 'si', 'yes', 'y', 's']:
                # Salva la prenotazione nel database
                booking_data = booking_state['data']
                booking_data['status'] = 'Confermata'
                booking_data['created_at'] = datetime.now().isoformat()
                
                # Aggiungi la prenotazione al database
                if 'bookings' not in st.session_state:
                    st.session_state.bookings = {}
                
                booking_id = str(uuid.uuid4())
                st.session_state.bookings[booking_id] = booking_data
                
                # Salva il database delle prenotazioni
                try:
                    save_bookings_database({
                        'bookings': st.session_state.bookings
                    })
                except Exception as e:
                    st.error(f"Errore durante il salvataggio delle prenotazioni: {e}")
                
                # Resetta lo stato di prenotazione
                st.session_state.booking_state = {
                    'active': False,
                    'step': None,
                    'property_id': None,
                    'property_name': None,
                    'data': {}
                }
                
                return f"""
✅ **Prenotazione confermata!**

La tua prenotazione per {booking_data['property_name']} è stata registrata con successo.
Numero di prenotazione: {booking_id[:8]}

Ti invieremo una email di conferma con tutti i dettagli.
Grazie per aver scelto CiaoHost!
"""
            else:
                # Annulla la prenotazione
                st.session_state.booking_state = {
                    'active': False,
                    'step': None,
                    'property_id': None,
                    'property_name': None,
                    'data': {}
                }
                
                return "❌ Prenotazione annullata. Se desideri prenotare un altro immobile, usa il comando /prenota seguito dal nome dell'immobile."
    
    return None

def handle_admin_access(message_text):
    admin_state = st.session_state.admin_state

    if message_text.lower().strip() == "/admin":
        admin_state['mode'] = 'auth'
        admin_state['step'] = 'username'
        return "👤 Inserisci username admin:"

    if admin_state.get('mode') == 'auth':
        if admin_state.get('step') == 'username':
            if message_text == ADMIN_CREDENTIALS['username']:
                admin_state['step'] = 'password'
                return "🔑 Inserisci password:"
            else:
                admin_state['mode'] = None
                admin_state['step'] = None
                return "❌ Username errato! Riprova con /admin."

        elif admin_state.get('step') == 'password':
            if message_text == ADMIN_CREDENTIALS['password']:
                admin_state['mode'] = 'active'
                admin_state['step'] = None
                return """🔓 Accesso admin consentito!
Comandi disponibili:
  • /add_property <nome> <tipo> <prezzo> <località> <telefono> <servizi_comma_separated>
    Esempio: /add_property "Villa Sole" B&B 120 Roma +390123456 "WiFi,Piscina"
  • /list_properties
  • /list_users
  • /delete_property <id>
  • /exit_admin (per uscire dalla modalità admin)"""
            else:
                admin_state['mode'] = None
                admin_state['step'] = None
                return "❌ Password errata! Riprova con /admin."

    if admin_state.get('mode') == 'active':
        cmd_parts = message_text.lower().strip().split(maxsplit=1)
        command = cmd_parts[0]

        if command == "/add_property":
            try:
                # Nuovo formato che supporta spazi nel nome della proprietà
                # Formato: /add_property "Nome Proprietà" Tipo Prezzo Località Telefono "Servizi1,Servizi2"
                command_pattern = r'/add_property\s+"([^"]+)"\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.+)'
                import re
                match = re.match(command_pattern, message_text.strip())
                
                if not match:
                    return """❌ Formato errato. Usa: 
/add_property "Nome Proprietà" Tipo Prezzo Località Telefono "Servizi1,Servizi2"

Esempio: /add_property "Villa Bella" B&B 120 Roma +390123456 "WiFi,Piscina"
                    
Nota: Il nome della proprietà deve essere tra virgolette."""
                
                name, prop_type, price_str, location, phone, services_str = match.groups()
                
                try:
                    price_value = float(price_str.replace('€', '').replace(',', '.').strip())
                except ValueError:
                    return "❌ Errore: Il prezzo deve essere un numero valido (es. 150.50)."
                
                # Rimuovi le virgolette dai servizi se presenti
                services_str = services_str.strip('"')

                prop_id = str(len(st.session_state.properties) + 1)
                while prop_id in st.session_state.properties:
                    prop_id = str(int(prop_id) + 1)

                # Creiamo una proprietà con tutti i campi necessari
                from datetime import datetime
                import uuid
                
                # Utilizziamo la funzione add_property per aggiungere la proprietà
                from utils.json_database import add_property
                
                property_data = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "type": prop_type,
                    "city": location,
                    "address": "",  # Campo vuoto, può essere aggiornato in seguito
                    "bedrooms": 1,  # Valore predefinito
                    "bathrooms": 1.0,  # Valore predefinito
                    "max_guests": 2,  # Valore predefinito
                    "base_price": price_value,
                    "cleaning_fee": 30.0,  # Valore predefinito
                    "check_in_instructions": "",
                    "wifi_details": "",
                    "checkout_instructions": "",
                    "amenities": [s.strip() for s in services_str.split(',')],
                    "photos": [],
                    "status": "Attivo",
                    "phone": phone,
                    "description": "",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                
                success = add_property(property_data)
                
                if not success:
                    return "❌ Errore durante l'aggiunta della proprietà."
                    
                # Ricarica il database
                load_database()
                return f"✅ Proprietà '{name}' aggiunta con successo!"
            except Exception as e:
                return f"❌ Errore durante l'aggiunta: {str(e)}"

        elif command == "/list_properties":
            if not st.session_state.properties:
                return "ℹ️ Nessuna proprietà nel database."
            
            prop_list_str = "Elenco Proprietà:\n"
            for pid, prop in st.session_state.properties.items():
                prop_list_str += (f"  • ID {pid}: {prop.get('name', 'N/A')} ({prop.get('type', 'N/A')}) "
                                  f"a {prop.get('location', 'N/A')} - €{prop.get('price', 0):,.2f} "
                                  f"- Status: {prop.get('status', 'N/A')}\n")
            return prop_list_str
            
        elif command == "/list_users":
            if not st.session_state.users:
                return "ℹ️ Nessun utente registrato nel database."
            
            user_list_str = "Elenco Utenti Registrati:\n"
            for email, password in st.session_state.users.items():
                user_list_str += f"  • Email: {email} - Password: {password}\n"
            return user_list_str

        elif command == "/delete_property":
            try:
                if len(cmd_parts) < 2 or not cmd_parts[1]:
                     return "❌ Formato corretto: /delete_property <id>"
                prop_id_to_delete = cmd_parts[1].strip()
                
                if prop_id_to_delete in st.session_state.properties:
                    deleted_prop_name = st.session_state.properties[prop_id_to_delete].get('name', 'Sconosciuta')
                    del st.session_state.properties[prop_id_to_delete]
                    save_database()
                    return f"✅ Immobile '{deleted_prop_name}' (ID: {prop_id_to_delete}) eliminato!"
                return f"❌ Immobile con ID {prop_id_to_delete} non trovato."
            except Exception as e:
                return f"❌ Errore durante l'eliminazione: {str(e)}"
        
        elif command == "/exit_admin":
            admin_state['mode'] = None
            admin_state['step'] = None
            return "🚪 Modalità admin disattivata."
        
        elif message_text.startswith("/"):
            return "❓ Comando admin non riconosciuto. Comandi validi: /add_property, /list_properties, /list_users, /delete_property, /exit_admin."

    return None

def show_property_search():
    # Mostra un'animazione di caricamento
    from loading_animations import show_loading_animation
    show_loading_animation("Caricamento immobili...", duration=1.5)
    
    st.markdown("""
        <h1 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 1rem;">
            <span style="color: #4361ee;">🔍</span> Ricerca Immobili
        </h1>
        <p style="font-size: 1.1rem; color: #6c757d; margin-bottom: 2rem;">
            Trova la proprietà perfetta per le tue esigenze
        </p>
    """, unsafe_allow_html=True)
    
    properties = st.session_state.get('properties', {})

    if not properties:
        st.markdown("""
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center; margin: 2rem 0;">
                <img src="https://cdn-icons-png.flaticon.com/512/6134/6134065.png" style="width: 100px; margin-bottom: 1rem;">
                <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">Nessun immobile disponibile</h3>
                <p style="color: #6c757d;">Al momento non ci sono immobili nel database. Riprova più tardi.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # Mostriamo tutte le proprietà, indipendentemente dallo stato
    available_properties = properties.copy()

    if not available_properties:
        st.markdown("""
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center; margin: 2rem 0;">
                <img src="https://cdn-icons-png.flaticon.com/512/6134/6134065.png" style="width: 100px; margin-bottom: 1rem;">
                <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">Nessun immobile disponibile</h3>
                <p style="color: #6c757d;">Al momento non ci sono immobili disponibili. Riprova più tardi.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # Advanced search filters in Booking.com style
    st.markdown("""
        <div class="search-bar">
            <h3 style="font-size: 1.4rem; margin-bottom: 1.2rem; color: var(--primary-color); font-weight: 700;">
                Trova l'alloggio perfetto
            </h3>
    """, unsafe_allow_html=True)
    
    # Date selection in same row (2 columns)
    col_dates1, col_dates2 = st.columns(2)
    
    with col_dates1:
        check_in = st.date_input("Check-in", value=None, format="DD/MM/YYYY")
    
    with col_dates2:
        check_out = st.date_input("Check-out", value=None, format="DD/MM/YYYY")
    
    # Main search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Search with search icon
        st.markdown("""
        <style>
        .search-container .stTextInput > div:first-child { 
            position: relative;
        }
        .search-container .stTextInput input {
            padding-left: 40px !important;
        }
        .search-icon {
            position: absolute;
            left: 15px;
            top: 12px;
            color: var(--primary-color);
            z-index: 1;
            font-size: 18px;
        }
        </style>
        <div class="search-container">
            <div class="search-icon">🔍</div>
        </div>
        """, unsafe_allow_html=True)
        search_term = st.text_input("", placeholder="Nome, tipo o località...", key="prop_search_term").lower()
    
    with col2:
        # Extract unique property types
        property_types = list(set([prop.get('type', 'Non specificato') for prop in available_properties.values()]))
        property_types.insert(0, "Tutti i tipi")
        selected_type = st.selectbox("Tipo di Alloggio", property_types)
    
    with col3:
        # Extract unique locations
        locations = list(set([prop.get('location', 'Non specificato') for prop in available_properties.values()]))
        locations.insert(0, "Tutte le località")
        
        # Se c'è una destinazione selezionata, la impostiamo come default
        default_index = 0
        if st.session_state.get('destination_selected'):
            if st.session_state.destination_selected in locations:
                default_index = locations.index(st.session_state.destination_selected)
            # Rimuoviamo la destinazione selezionata per evitare problemi in futuro
            st.session_state.pop('destination_selected', None)
        
        selected_location = st.selectbox("Destinazione", locations, index=default_index)
    
    # Additional filter options in collapsible section
    with st.expander("Filtri avanzati"):
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            # Price range slider
            prices = [prop.get('price', 0) for prop in available_properties.values()]
            min_price, max_price = min(prices), max(prices)
            
            # Assicuriamoci che min_price e max_price siano diversi
            if min_price == max_price:
                if min_price == 0:
                    max_price = 100  # Se entrambi sono 0, impostiamo max_price a 100
                else:
                    # Altrimenti, impostiamo max_price a min_price + 10% (o almeno +50)
                    max_price = min_price + max(50, int(min_price * 0.1))
            
            price_range = st.slider(
                "Fascia di Prezzo (€)",
                min_value=int(min_price),
                max_value=int(max_price),
                value=(int(min_price), int(max_price)),
                step=50
            )
            
            # Guest selection
            guests = st.number_input("Numero di ospiti", min_value=1, max_value=10, value=2)
        
        with col_adv2:
            # Services filter with multiselect
            all_services = set()
            for prop in available_properties.values():
                services = prop.get('services', [])
                all_services.update(services)
            
            if not all_services:
                all_services = {"Wi-Fi", "Parcheggio", "Aria condizionata", "Piscina", "Vista panoramica", 
                              "Colazione inclusa", "TV", "Terrazza"}
            
            selected_services = st.multiselect(
                "Servizi Desiderati",
                options=sorted(list(all_services)),
                default=[]
            )
            
            # Property rating
            min_rating = st.select_slider(
                "Valutazione minima",
                options=["Qualsiasi", "7+", "8+", "9+"],
                value="Qualsiasi"
            )
    
    # Chiusura del div senza pulsante di ricerca
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_properties = {}
    for pid, prop in available_properties.items():
        # Text search filter
        text_match = True
        if search_term:
            text_match = (search_term in prop.get('name', '').lower() or
                         search_term in prop.get('type', '').lower() or
                         search_term in prop.get('location', '').lower())
        
        # Property type filter
        type_match = True
        if selected_type != "Tutti i tipi":
            type_match = prop.get('type', '') == selected_type
        
        # Location filter
        location_match = True
        if selected_location != "Tutte le località":
            location_match = prop.get('location', '') == selected_location
        
        # Price range filter
        price = prop.get('price', 0)
        price_match = price_range[0] <= price <= price_range[1]
        
        # Services filter
        services_match = True
        if selected_services:
            prop_services = set(prop.get('services', []))
            services_match = all(service in prop_services for service in selected_services)
        
        # Add to filtered properties if all conditions match
        if text_match and type_match and location_match and price_match and services_match:
            filtered_properties[pid] = prop
    
    # Display results count without sorting options
    st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <p style="font-size: 1.1rem; font-weight: 600; color: var(--primary-color);">
                <span style="color: var(--primary-color); font-weight: 700;">{len(filtered_properties)}</span> immobili trovati
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # No results message
    if not filtered_properties:
        st.markdown("""
            <div style="background-color: white; padding: 2.5rem; border-radius: 12px; box-shadow: var(--shadow-md); text-align: center; margin: 2rem 0; animation: fadeIn 0.5s ease-in-out;">
                <img src="https://cdn-icons-png.flaticon.com/512/6134/6134065.png" style="width: 120px; margin-bottom: 1.5rem; opacity: 0.9;">
                <h3 style="font-size: 1.6rem; margin-bottom: 1rem; color: var(--primary-color);">Nessun risultato</h3>
                <p style="color: #6c757d; font-size: 1.1rem;">Nessun immobile corrisponde ai criteri di ricerca. Prova a modificare i filtri.</p>
                <button style="margin-top: 1.5rem; background-color: var(--secondary-color); color: white; border: none; padding: 0.7rem 1.5rem; border-radius: 50px; font-weight: 500; cursor: pointer;">Resetta i filtri</button>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Display properties in a modern card format inspired by Booking.com
        # We'll use a single column layout for better mobile responsiveness
        
        # Add style for sequential card animation
        st.markdown("""
        <style>
        @keyframes propertyCardEntrance {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .property-card {
            animation: propertyCardEntrance 0.8s ease-out;
            animation-fill-mode: both;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Organizziamo le proprietà in righe di 3 elementi ciascuna
        property_rows = []
        current_row = []
        
        for prop_id, prop in filtered_properties.items():
            current_row.append((prop_id, prop))
            if len(current_row) == 3:
                property_rows.append(current_row)
                current_row = []
        
        # Aggiungiamo l'ultima riga anche se non completa
        if current_row:
            property_rows.append(current_row)
        
        for row_index, row in enumerate(property_rows):
            cols = st.columns(len(row))
            for i, (prop_id, prop) in enumerate(row):
                # Calcola il ritardo di animazione basato sulla posizione
                animation_delay = (row_index * len(row) + i) * 0.15
                
                prop_name = prop.get('name', 'Nome non disponibile')
                prop_type = prop.get('type', 'Tipo non specificato')
                prop_location = prop.get('location', 'Località non specificata')
                prop_price = prop.get('price', 0)
                prop_services = prop.get('services', [])
                prop_phone = prop.get('phone', 'Non disponibile')
                
                # Aggiungi stile inline per il ritardo di animazione
                st.markdown(f"""
                <style>
                .property-card-{row_index}-{i} {{
                    animation-delay: {animation_delay}s;
                }}
                </style>
                """, unsafe_allow_html=True)
                with cols[i]:
                    # Verifica se la proprietà è inattiva
                    is_inactive = prop.get("status", "").lower() == "inattivo"
                    
                    # Utilizziamo un approccio diverso per mostrare le proprietà inattive
                    if is_inactive:
                        # Badge per proprietà inattive
                        st.markdown("""
                            <div style="position: absolute; top: 10px; left: 10px; background-color: #ef4444; color: white; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; z-index: 10;">
                                Non disponibile
                            </div>
                        """, unsafe_allow_html=True)
                    # Card container con animazioni
                    opacity = "opacity: 0.8;" if is_inactive else ""
                    
                    # STRUTTURA A GRIGLIA PERFETTAMENTE ALLINEATA
                    # =========================================
                    
                    # Definiamo stili globali per garantire allineamento perfetto
                    st.markdown(f"""
                    <style>
                    .grid-container-{prop_id} {{
                        display: grid;
                        grid-template-columns: 1fr;
                        grid-gap: 0;
                        background: white;
                        border-radius: var(--radius-md);
                        box-shadow: var(--shadow-md);
                        margin-bottom: 30px;
                        overflow: hidden;
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }}
                    
                    .grid-container-{prop_id}:hover {{
                        transform: translateY(-5px);
                        box-shadow: var(--shadow-lg);
                    }}
                    
                    .property-header-{prop_id} {{
                        display: flex;
                        justify-content: space-between;
                        align-items: flex-start;
                        padding: 20px 20px 5px 20px;
                    }}
                    
                    .property-image-{prop_id} {{
                        width: 100%;
                        height: 250px;
                        object-fit: cover;
                        border-radius: 8px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    }}
                    
                    .property-info-grid-{prop_id} {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        grid-gap: 15px;
                    }}
                    
                    .property-info-item-{prop_id} {{
                        display: flex;
                        align-items: center;
                    }}
                    
                    .property-service-grid-{prop_id} {{
                        display: grid;
                        grid-template-columns: 1fr 1fr 1fr;
                        grid-gap: 10px;
                    }}
                    
                    .badge-{prop_id} {{
                        background-color: #3b82f6;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 20px;
                        font-weight: 600;
                        justify-self: end;
                    }}
                    
                    .price-container-{prop_id} {{
                        display: grid;
                        grid-template-columns: auto auto;
                        justify-content: space-between;
                        align-items: center;
                        background: #f0f9ff;
                        padding: 15px;
                        border-radius: 8px;
                    }}
                    
                    .action-buttons-{prop_id} {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        grid-gap: 15px;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Determina immagine corretta
                    import os
                    import random
                    
                    # Determina immagine in base alla proprietà con opzione di fallback - usando Unsplash per immagini affidabili
                    image_options = {
                        "villa": ["https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80", 
                                  "https://images.unsplash.com/photo-1613977257363-707ba9348227?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"],
                        "appartamento": ["https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", 
                                        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"],
                        "casa": ["https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1175&q=80",
                               "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1192&q=80"],
                        "default": ["https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"]
                    }
                    
                    # Immagini specifiche per proprietà con nomi particolari
                    specific_images = {
                        "villa del sole": "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
                    }
                    
                    # Controlla se esiste un'immagine specifica per questa proprietà
                    prop_name_lower = prop_name.lower()
                    if prop_name_lower in specific_images:
                        image_url = specific_images[prop_name_lower]
                    else:
                        # Seleziona la categoria corretta o usa default
                        image_category = "default"
                        prop_type_lower = prop.get('type', '').lower()
                        
                        for key in image_options.keys():
                            if key in prop_type_lower or key in prop_name_lower:
                                image_category = key
                                break
                        
                        # Seleziona un'immagine casuale dalla categoria
                        image_url = random.choice(image_options[image_category])
                    
                    # Genera valutazione casuale tra 8.0 e 9.9 per ogni proprietà
                    if 'rating' not in prop:
                        prop['rating'] = round(random.uniform(8.0, 9.9), 1)
                    
                    # Genera recensioni casuali tra 50 e 300
                    if 'reviews' not in prop:
                        prop['reviews'] = random.randint(50, 300)
                    
                    # Crea un container principale unico
                    prop_col = st.container()
                    with prop_col:
                        # UTILIZZIAMO UN LAYOUT SIMILE A BOOKING.COM
                        
                        # Invece di usare HTML per l'immagine, utilizziamo i componenti Streamlit
                        # Prima creiamo un container per mantenere lo stile consistente
                        img_container = st.container()
                        with img_container:
                            # Mostriamo l'immagine direttamente con st.image
                            st.image(image_url, use_container_width=True)
                            
                            # Aggiungiamo il rating e il tipo dopo l'immagine come testo normale
                            rating_col, type_col = st.columns([1, 1])
                            with rating_col:
                                st.markdown(f"**Valutazione:** {prop['rating']}")
                            with type_col:
                                st.markdown(f"**Tipo:** {prop_type}")
                            
                            # Promozione rimossa
                        
                        # Contenuto principale usando componenti Streamlit nativi
                        st.subheader(prop_name)
                        
                        # Informazioni sulla posizione e recensioni
                        location_reviews = st.container()
                        with location_reviews:
                            st.markdown(f"📍 {prop_location} | ⭐ {prop['reviews']} recensioni")
                        
                        # Genera 3-5 servizi principali
                        services = prop.get('services', [])
                        if not services:
                            services = ["Wi-Fi", "Parcheggio", "Aria condizionata", "Piscina", "Vista panoramica", 
                                      "Colazione inclusa", "TV", "Terrazza", "Accesso spiaggia"]
                            # Scegli randomicamente 3-5 servizi
                            services = random.sample(services, random.randint(3, 5))
                        
                        # Mostra i servizi come markdown
                        st.markdown("### Servizi")
                        service_text = ", ".join(services[:4])
                        if len(services) > 4:
                            service_text += f" +{len(services) - 4} altro"
                        st.markdown(service_text)
                        
                        # Separatore
                        st.markdown("---")
                        
                        # Informazioni sul prezzo in stile Booking.com ma con componenti Streamlit
                        # Genera uno sconto casuale per alcune proprietà
                        has_discount = random.random() > 0.7
                        discount_percentage = random.choice([10, 15, 20, 25]) if has_discount else 0
                        original_price = prop_price
                        discounted_price = original_price * (1 - discount_percentage/100) if has_discount else original_price
                        
                        # Messaggi di disponibilità limitata rimossi
                        
                        # Mostra prezzo con eventuale sconto
                        price_col1, price_col2 = st.columns([3, 1])
                        
                        with price_col1:
                            # Mostra sempre il prezzo senza sconti o messaggi promozionali
                            st.markdown(f"**€{original_price:,.2f}** / notte")
                        
                        with price_col2:
                            st.caption("Tasse e imposte incluse")
                        
                        # Bottoni azione
                        check_col, fav_col = st.columns([4, 1])
                        with check_col:
                            st.button("Verifica disponibilità", key=f"check_{prop_id}", type="primary", use_container_width=True)
                        with fav_col:
                            st.button("♡", key=f"fav_{prop_id}")
                        
                        # Inizializziamo lo stato se non esiste
                        if f"clicked_{prop_id}" not in st.session_state:
                            st.session_state[f"clicked_{prop_id}"] = False
                                
                        if st.session_state[f"clicked_{prop_id}"]:
                            st.success(f"Hai mostrato interesse per {prop_name}! Controlla la disponibilità per continuare.")
        
                        # Fine della card principale
                    
                    # Questa sezione non è più necessaria perché è stata integrata nella struttura a griglia sopra
                    
                    # SEZIONE BOOKING CON GRIGLIA PERFETTAMENTE ALLINEATA
                    # ===================================================
                    
                    # Importazioni necessarie
                    import time
                    import os
                    import datetime
                    from datetime import timedelta
                    import random
                    
                    # Creiamo un container dedicato per la sezione booking
                    booking_section = st.container()
                    
                    with booking_section:
                        # Stili CSS per griglia perfetta
                        st.markdown(f"""
                        <style>
                        /* Stili per la sezione prenotazioni */
                        .booking-container-{prop_id} {{
                            display: grid;
                            grid-template-columns: 1fr;
                            grid-gap: 20px;
                            padding: 20px;
                            background: white;
                            border-radius: 12px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                            margin: 30px 0;
                            position: relative;
                        }}
                        
                        .booking-container-{prop_id}::before {{
                            content: '';
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 5px;
                            background: #3b82f6;
                        }}
                        
                        .booking-header-{prop_id} {{
                            text-align: center;
                            padding: 15px;
                            margin-bottom: 20px;
                            background: #f8fafc;
                            border-radius: 8px;
                            border-left: 4px solid #3b82f6;
                        }}
                        
                        .booking-platforms-{prop_id} {{
                            display: grid;
                            grid-template-columns: 1fr 1fr 1fr;
                            grid-gap: 20px;
                        }}
                        
                        .platform-card-{prop_id} {{
                            display: grid;
                            grid-template-rows: auto auto auto auto auto;
                            grid-gap: 10px;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                            transition: all 0.3s ease;
                            align-items: center;
                            justify-items: center;
                        }}
                        
                        .platform-card-{prop_id}:hover {{
                            transform: translateY(-5px);
                            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                        }}
                        
                        .platform-logo-{prop_id} {{
                            width: 180px;
                            height: 60px;
                            object-fit: contain;
                        }}
                        
                        .platform-booking-{prop_id} {{
                            background: #28a745;
                            color: white;
                            padding: 8px 16px;
                            border-radius: 20px;
                            font-weight: bold;
                            text-align: center;
                        }}
                        
                        .platform-availability-{prop_id} {{
                            background: #17a2b8;
                            color: white;
                            padding: 6px 12px;
                            border-radius: 20px;
                            font-size: 0.9rem;
                            text-align: center;
                        }}
                        
                        .platform-reviews-{prop_id} {{
                            font-size: 0.9rem;
                            color: #6c757d;
                            text-align: center;
                        }}
                        
                        .platform-stars-{prop_id} {{
                            color: #ffc107;
                            font-size: 1rem;
                            text-align: center;
                        }}
                        
                        /* Animazioni */
                        @keyframes fadeIn {{
                            from {{ opacity: 0; transform: translateY(10px); }}
                            to {{ opacity: 1; transform: translateY(0); }}
                        }}
                        
                        @keyframes pulse {{
                            0% {{ transform: scale(1); }}
                            50% {{ transform: scale(1.02); }}
                            100% {{ transform: scale(1); }}
                        }}
                        
                        .booking-success-{prop_id} {{
                            display: grid;
                            grid-template-columns: 1fr;
                            grid-gap: 10px;
                            background: #d4edda;
                            color: #155724;
                            padding: 20px;
                            border-radius: 8px;
                            margin-top: 20px;
                            animation: pulse 2s infinite;
                        }}
                        
                        .booking-pending-{prop_id} {{
                            display: grid;
                            grid-template-columns: 1fr;
                            grid-gap: 10px;
                            background: #fff3cd;
                            color: #856404;
                            padding: 20px;
                            border-radius: 8px;
                            margin-top: 20px;
                        }}
                        
                        .booking-date-{prop_id} {{
                            background: rgba(0,0,0,0.05);
                            padding: 8px 15px;
                            border-radius: 4px;
                            font-size: 0.9rem;
                            color: #495057;
                            text-align: center;
                        }}
                        </style>
                        
                        <div class="booking-container-{prop_id}">
                                        """, unsafe_allow_html=True)
                    
                    # Definiamo una funzione per mostrare un ritardo e poi la conferma
                    def show_booking_confirmation(platform, name, container, price, prop_id=None):
                        with container:
                            with st.spinner(f"Verifica disponibilità su {platform} per {name}..."):
                                time.sleep(1.5)  # Primo ritardo
                                
                            st.warning(f"""
                                **Prenotazione in corso...**
                                
                                Stiamo elaborando la tua richiesta per {name} su {platform}.
                                Importo: €{price:.2f} (pagamento sicuro)
                                
                                Check-in: {(datetime.datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')} - Check-out: {(datetime.datetime.now() + timedelta(days=37)).strftime('%d/%m/%Y')}
                            """)
                            
                            time.sleep(1.5)  # Secondo ritardo
                            
                            st.success(f"""
                                **Prenotazione confermata!**
                                
                                La tua prenotazione per {name} su {platform} è stata confermata.
                                Riceverai a breve una email con tutti i dettagli.
                                
                                Codice prenotazione: {platform[:2].upper()}{random.randint(100000, 999999)}
                            """)
                    
                    # Funzione per generare un prezzo casuale realistico per ogni piattaforma
                    def get_platform_price(base_price, platform):
                        variance = random.uniform(-0.1, 0.15)  # Variazione casuale tra -10% e +15%
                        if platform == "Booking.com":
                            # Booking tende ad avere prezzi leggermente più alti
                            return base_price * (1 + variance + 0.05)
                        elif platform == "Airbnb":
                            # Airbnb ha prezzi più variabili
                            return base_price * (1 + variance)
                        else:  # VRBO
                            # VRBO può avere prezzi più competitivi
                            return base_price * (1 + variance - 0.02)
                    
                    # Prezzo base per notte in base alla tipologia di proprietà
                    base_price = 120 if "appartamento" in prop_name.lower() else 180
                    base_price = 250 if "villa" in prop_name.lower() else base_price
                    
                    # Genera recensioni random realistiche
                    booking_reviews = random.randint(34, 126)
                    booking_rating = round(random.uniform(8.2, 9.4), 1)
                    
                    airbnb_reviews = random.randint(18, 87)
                    airbnb_rating = round(random.uniform(4.5, 5.0), 1)
                    
                    vrbo_reviews = random.randint(12, 65)
                    vrbo_rating = round(random.uniform(4.3, 4.9), 1)
                    
                    # Calcola prezzi diversi per ogni piattaforma
                    booking_price = get_platform_price(base_price, "Booking.com")
                    airbnb_price = get_platform_price(base_price, "Airbnb")
                    vrbo_price = get_platform_price(base_price, "VRBO")
                    
                    # Messaggi di disponibilità sui portali rimossi
                    with booking_section:
                        # Intestazione 
                        st.subheader("Prenota sui migliori portali")
                        st.markdown(f"""<div style="height:5px; background:#3b82f6; 
                                     margin-bottom:20px; border-radius:5px;"></div>""", unsafe_allow_html=True)
                        
                        # Placeholder per le conferme di prenotazione
                        booking_confirm = st.empty()
                        airbnb_confirm = st.empty()
                        vrbo_confirm = st.empty()
                        
                        # Creiamo tre colonne per le piattaforme
                        col1, col2, col3 = st.columns(3)
                        
                        # BOOKING
                        with col1:
                            booking_logo_path = "booking.png"
                            if os.path.exists(booking_logo_path):
                                st.image(booking_logo_path, width=180)
                            else:
                                st.markdown("<h3 style='text-align:center; color:#003580;'>Booking.com</h3>", unsafe_allow_html=True)
                            
                            st.markdown(f"""<div style="border:1px solid #ddd; border-top:4px solid #003580; 
                                         border-radius:8px; padding:15px; text-align:center;">
                                         <div style="font-size:20px; font-weight:bold;">€{booking_price:.2f}</div>
                                         <div>{booking_reviews} recensioni</div>
                                         <div style="color:#ffc107;">{'★' * int(booking_rating/2)} {booking_rating}/10</div>
                                         </div>""", unsafe_allow_html=True)
                            
                            booking_button = st.button("Prenota ora", key=f"booking_{prop_id}", use_container_width=True)
                            if booking_button:
                                show_booking_confirmation("Booking.com", prop_name, booking_confirm, booking_price * 7)
                        
                        # AIRBNB
                        with col2:
                            airbnb_logo_path = "airbnb.png"
                            if os.path.exists(airbnb_logo_path):
                                st.image(airbnb_logo_path, width=180)
                            else:
                                st.markdown("<h3 style='text-align:center; color:#FF5A5F;'>Airbnb</h3>", unsafe_allow_html=True)
                            
                            st.markdown(f"""<div style="border:1px solid #ddd; border-top:4px solid #FF5A5F; 
                                         border-radius:8px; padding:15px; text-align:center;">
                                         <div style="font-size:20px; font-weight:bold;">€{airbnb_price:.2f}</div>
                                         <div>{airbnb_reviews} recensioni</div>
                                         <div style="color:#ffc107;">{'★' * int(airbnb_rating)} {airbnb_rating}/5</div>
                                         </div>""", unsafe_allow_html=True)
                            
                            airbnb_button = st.button("Prenota ora", key=f"airbnb_{prop_id}", use_container_width=True)
                            if airbnb_button:
                                show_booking_confirmation("Airbnb", prop_name, airbnb_confirm, airbnb_price * 7)
                        
                        # VRBO
                        with col3:
                            vrbo_logo_path = "VRBO.png"
                            if os.path.exists(vrbo_logo_path):
                                st.image(vrbo_logo_path, width=180)
                            else:
                                st.markdown("<h3 style='text-align:center; color:#3D67FF;'>VRBO</h3>", unsafe_allow_html=True)
                            
                            st.markdown(f"""<div style="border:1px solid #ddd; border-top:4px solid #3D67FF; 
                                         border-radius:8px; padding:15px; text-align:center;">
                                         <div style="font-size:20px; font-weight:bold;">€{vrbo_price:.2f}</div>
                                         <div>{vrbo_reviews} recensioni</div>
                                         <div style="color:#ffc107;">{'★' * int(vrbo_rating)} {vrbo_rating}/5</div>
                                         </div>""", unsafe_allow_html=True)
                            
                            vrbo_button = st.button("Prenota ora", key=f"vrbo_{prop_id}", use_container_width=True)
                            if vrbo_button:
                                show_booking_confirmation("VRBO", prop_name, vrbo_confirm, vrbo_price * 7)
                    
                    # Fine della sezione booking - tutto è chiuso nei tag precedenti
                    
                    
                    # Property details modal (shown when details button is clicked)
                    if st.session_state.get(f"show_details_{prop_id}", False):
                        with st.expander(f"Dettagli di {prop_name}", expanded=True):
                            # Intestazione
                            st.markdown(f"### {prop_name}", unsafe_allow_html=True)
                            st.markdown(f"**Tipo:** {prop_type}", unsafe_allow_html=True)
                            
                            # Informazioni principali
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("#### 📍 Località")
                                st.markdown(f"**{prop_location}**", unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown("#### 💰 Prezzo")
                                st.markdown(f"**€{prop_price:,.2f}**", unsafe_allow_html=True)
                            
                            st.markdown("#### 📞 Contatto")
                            st.markdown(f"**{prop_phone}**", unsafe_allow_html=True)
                            
                            # Servizi
                            st.markdown("#### ✨ Servizi disponibili")
                            
                            if prop_services:
                                service_text = ", ".join([f"✓ {service}" for service in prop_services])
                                st.markdown(service_text)
                            else:
                                st.markdown("*Nessun servizio specificato per questa proprietà.*")
                            
                            # Pulsante chiudi
                            col1, col2, col3 = st.columns([1, 1, 1])
                            with col2:
                                if st.button("✖️ Chiudi dettagli", key=f"close_details_{prop_id}", use_container_width=True):
                                    st.session_state[f"show_details_{prop_id}"] = False
                                    st.rerun()

# Funzione per mostrare la schermata di benvenuto con animazioni e presentazione dell'azienda
def show_welcome_screen():
    """Mostra la schermata di benvenuto con animazioni e presentazione dell'azienda"""
    
    # CSS per lo stile Booking.com per la pagina di benvenuto
    st.markdown("""
    <style>
    .welcome-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    
    .welcome-header {
        text-align: center;
        margin-bottom: 50px;
    }
    
    .welcome-title {
        font-size: 2.8em;
        font-weight: 800;
        color: var(--primary-color);
        margin-bottom: 16px;
        letter-spacing: -0.03em;
    }
    
    .welcome-subtitle {
        font-size: 1.4em;
        color: #6B7280;
        max-width: 800px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }
    
    .hero-section {
        display: flex;
        background: linear-gradient(135deg, var(--primary-color) 0%, #004b9d 100%);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        margin-bottom: 60px;
    }
    
    .hero-content {
        padding: 60px;
        color: white;
        flex: 1;
    }
    
    .hero-title {
        font-size: 2.4em;
        font-weight: 700;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    
    .hero-description {
        font-size: 1.2em;
        margin-bottom: 30px;
        line-height: 1.6;
        opacity: 0.9;
    }
    
    .hero-image {
        flex: 1;
        background-image: url('https://cf.bstatic.com/xdata/images/hotel/max1024x768/271592705.jpg');
        background-size: cover;
        background-position: center;
        min-height: 400px;
    }
    
    .hero-cta {
        display: inline-block;
        background-color: white;
        color: var(--primary-color);
        padding: 12px 28px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1em;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .hero-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .feature-card {
        background-color: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }
    
    .feature-card-header {
        background-color: var(--primary-light);
        padding: 20px;
        display: flex;
        align-items: center;
    }
    
    .feature-card-icon {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--primary-color);
        color: white;
        border-radius: 12px;
        margin-right: 16px;
        font-size: 1.5em;
    }
    
    .feature-card-title {
        font-size: 1.3em;
        font-weight: 600;
        color: var(--primary-color);
        margin: 0;
    }
    
    .feature-card-content {
        padding: 24px;
    }
    
    .feature-card-text {
        font-size: 1em;
        color: #4B5563;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .feature-list {
        padding-left: 20px;
    }
    
    .feature-item {
        margin-bottom: 8px;
        color: #4B5563;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-between;
        margin: 50px 0;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
        flex: 1;
        min-width: 200px;
        margin: 20px;
    }
    
    .stat-value {
        font-size: 3em;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 10px;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 1.1em;
        color: #6B7280;
    }
    
    .testimonial-container {
        margin: 60px 0;
        padding: 50px;
        background-color: var(--primary-light);
        border-radius: 12px;
        position: relative;
    }
    
    .testimonial-quote {
        font-size: 1.3em;
        line-height: 1.8;
        font-style: italic;
        color: #1F2937;
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
        position: relative;
    }
    
    .testimonial-quote:before {
        content: '"';
        font-size: 4em;
        position: absolute;
        left: -30px;
        top: -20px;
        color: var(--primary-color);
        opacity: 0.3;
    }
    
    .testimonial-author {
        text-align: center;
        margin-top: 20px;
    }
    
    .author-name {
        font-weight: 600;
        color: var(--primary-color);
    }
    
    .author-title {
        font-size: 0.9em;
        color: #6B7280;
    }
    
    .cta-section {
        text-align: center;
        margin: 60px 0;
    }
    
    .cta-title {
        font-size: 2em;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 20px;
    }
    
    .cta-description {
        font-size: 1.2em;
        color: #6B7280;
        max-width: 700px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }
    
    .cta-button {
        display: inline-block;
        background-color: var(--secondary-color);
        color: white;
        padding: 15px 40px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2em;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
    }
    
    .cta-button:hover {
        background-color: #005ea6;
        box-shadow: var(--shadow-lg);
        transform: translateY(-3px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Inizializza lo stato della schermata di benvenuto se non esiste
    if 'welcome_screen_step' not in st.session_state:
        st.session_state.welcome_screen_step = 1
    
    # Importa l'animazione di benvenuto
    from animations import add_animated_welcome
    add_animated_welcome()
    
    # Prima pagina di benvenuto con design moderno ispirato a Booking.com
    if st.session_state.welcome_screen_step == 1:
        # Invece di usare una singola chiamata st.markdown, dividiamo in componenti Streamlit
        
        # Usiamo un contenitore principale per ridurre lo spazio verticale
        main_container = st.container()
        
        with main_container:
            # Intestazione con stile compatto
            st.markdown("<h1 style='margin-bottom: 0.5rem;'>Gestisci i tuoi immobili come un professionista</h1>", unsafe_allow_html=True)
            st.markdown("<p style='margin-bottom: 1.5rem; font-size: 1.2rem;'>CiaoHost è la piattaforma completa che trasforma la gestione dei tuoi immobili in un'esperienza semplice, efficiente e redditizia.</p>", unsafe_allow_html=True)
            
            # Sezione Hero con colonne
            col1, col2 = st.columns([3, 2], gap="small")
            with col1:
                st.markdown("<h3>Aumenta i tuoi guadagni del 30% con la nostra piattaforma avanzata</h3>", unsafe_allow_html=True)
                st.markdown("<p>Unisci la potenza dell'intelligenza artificiale con strumenti di gestione all'avanguardia per massimizzare il potenziale dei tuoi immobili.</p>", unsafe_allow_html=True)
            
            with col2:
                # Utilizziamo un'immagine da un URL più affidabile
                st.image("https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", 
                        use_container_width=True)
            
            # Feature Cards - riduciamo lo spazio
            st.markdown("<h2 style='margin-top: 1rem; margin-bottom: 0.5rem;'>Le nostre funzionalità principali</h2>", unsafe_allow_html=True)
        
        # Continuiamo a usare il contenitore principale per le cards
        with main_container:
            feature_cols = st.columns(3, gap="small")
            
            with feature_cols[0]:
                st.markdown("<h3>📊 Prezzi Dinamici</h3>", unsafe_allow_html=True)
                st.markdown("""
                Ottimizza automaticamente i prezzi in base alla domanda, agli eventi locali e alla stagionalità per massimizzare i tuoi guadagni.
                
                - Analisi competitiva dei prezzi
                - Adattamento automatico alle stagioni
                - Suggerimenti basati sui dati di mercato
                """)
                
            with feature_cols[1]:
                st.markdown("<h3>🧹 Gestione Pulizie</h3>", unsafe_allow_html=True)
                st.markdown("""
                Coordina il team di pulizia con un calendario automatizzato, notifiche in tempo reale e rapporti di qualità.
                
                - Pianificazione intelligente
                - Check-list personalizzabili
                - Gestione del personale di servizio
                """)
                
            with feature_cols[2]:
                st.markdown("<h3>📱 Automazione Completa</h3>", unsafe_allow_html=True)
                st.markdown("""
                Risparmia tempo con messaggi automatici di benvenuto, istruzioni per il check-in e promemoria per gli ospiti.
                
                - Messaggi personalizzati
                - Gestione delle recensioni
                - Comunicazione multilingua
                """)
            
            # Stats - riduciamo lo spazio
            st.markdown("<h2 style='margin-top: 1rem; margin-bottom: 0.5rem;'>I nostri numeri</h2>", unsafe_allow_html=True)
            
            # Utilizziamo colonne all'interno del container principale
            stat_cols = st.columns(4, gap="small")
            
            with stat_cols[0]:
                st.markdown("<h3 style='margin-bottom: 0;'>97%</h3>", unsafe_allow_html=True)
                st.markdown("<p style='margin-top: 0;'>Clienti soddisfatti</p>", unsafe_allow_html=True)
                
            with stat_cols[1]:
                st.markdown("<h3 style='margin-bottom: 0;'>30%</h3>", unsafe_allow_html=True)
                st.markdown("<p style='margin-top: 0;'>Aumento medio dei ricavi</p>", unsafe_allow_html=True)
                
            with stat_cols[2]:
                st.markdown("<h3 style='margin-bottom: 0;'>70%</h3>", unsafe_allow_html=True)
                st.markdown("<p style='margin-top: 0;'>Tempo risparmiato</p>", unsafe_allow_html=True)
                
            with stat_cols[3]:
                st.markdown("<h3 style='margin-bottom: 0;'>24/7</h3>", unsafe_allow_html=True)
                st.markdown("<p style='margin-top: 0;'>Supporto disponibile</p>", unsafe_allow_html=True)
            
            # Testimonial con margini ridotti
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            st.info("""
            "*Da quando utilizzo CiaoHost ho aumentato le prenotazioni del 40% e ho risparmiato ore di lavoro ogni settimana. La piattaforma è incredibilmente intuitiva e il supporto è sempre pronto ad aiutarmi.*"
            
            **Marco Bianchi** - Proprietario di 5 appartamenti a Roma
            """)
        
        # Call to Action all'interno dello stesso contenitore
        with main_container:
            st.markdown("<h3 style='margin-top: 1rem; margin-bottom: 0.5rem;'>Pronto a trasformare la tua attività?</h3>", unsafe_allow_html=True)
            st.markdown("<p style='margin-bottom: 1rem;'>Unisciti a migliaia di proprietari che hanno già rivoluzionato la gestione dei loro immobili con CiaoHost.</p>", unsafe_allow_html=True)
            
            # Pulsante di navigazione senza spazio eccessivo
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            
            if st.button("Continua per scoprire di più →", use_container_width=True, key="welcome_next_1"):
                st.session_state.welcome_screen_step = 2
                st.rerun()
    
    # Stile CSS per le animazioni avanzate
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes zoomIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    .welcome-title {
        animation: fadeIn 1.2s ease-out;
    }
    .welcome-subtitle {
        animation: fadeIn 1.5s ease-out;
    }
    .welcome-text {
        animation: fadeIn 1.8s ease-out;
    }
    .welcome-feature {
        animation: slideIn 1s ease-out;
    }
    .welcome-cta {
        animation: scaleIn 1.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Contenuto in base allo step corrente
    if st.session_state.welcome_screen_step == 1:
        # Prima schermata: Solo logo e contenuto principale
        st.markdown("""
        <div style="height: 20px;"></div>
        """, unsafe_allow_html=True)
        
        # Logo con effetti migliorati - CSS corretto
        st.markdown("""
        <style>
        .welcome-container {
            text-align: center;
            margin: 1rem auto 3rem auto;
            padding: 2rem 0;
            position: relative;
            max-width: 800px;
        }
        .logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            margin: 0 auto;
        }
        .logo-glow {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(67, 97, 238, 0.2) 0%, rgba(255, 255, 255, 0) 70%);
            animation: pulse 3s infinite ease-in-out;
            margin: 0 auto;
        }
        .logo-glow::before {
            content: '';
            position: absolute;
            top: -10px;
            left: -10px;
            right: -10px;
            bottom: -10px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(67, 97, 238, 0.1) 0%, rgba(255, 255, 255, 0) 70%);
            animation: pulse 3s infinite ease-in-out 0.5s;
            z-index: -1;
        }
        .logo-glow::after {
            content: '';
            position: absolute;
            top: -20px;
            left: -20px;
            right: -20px;
            bottom: -20px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(67, 97, 238, 0.05) 0%, rgba(255, 255, 255, 0) 70%);
            animation: pulse 3s infinite ease-in-out 1s;
            z-index: -2;
        }
        .title-gradient {
            font-size: 4rem;
            font-weight: 800;
            margin: 1.5rem 0 1rem 0;
            background: linear-gradient(90deg, #4361ee, #3a56d4, #4361ee);
            background-size: 200% auto;
            color: transparent;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient 3s linear infinite;
            text-align: center;
            width: 100%;
        }
        .subtitle-wrapper {
            width: 100%;
            text-align: center;
            margin: 0 auto;
        }
        .subtitle {
            font-size: 1.6rem;
            font-weight: 600;
            color: #5a6e8c;
            margin-bottom: 1.5rem;
            position: relative;
            display: inline-block;
            text-align: center;
        }
        .subtitle-line {
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, #4361ee, transparent);
            animation: lineAnim 2s infinite;
        }
        /* Nascondiamo i bordi delle colonne di Streamlit */
        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        /* Centra il logo all'interno del suo contenitore */
        [data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin: 0 auto !important;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes lineAnim {
            0% { width: 0; left: 50%; }
            50% { width: 100%; left: 0; }
            100% { width: 0; left: 50%; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Contenitore principale centralizzato
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        
        # Logo con effetto glow
        st.markdown('<div class="logo-glow">', unsafe_allow_html=True)
        
        # Utilizziamo la nostra funzione di logo con dimensione aumentata
        show_company_logo(size="large", with_text=False)
        
        st.markdown('</div>', unsafe_allow_html=True)
        

        
        # Titolo e sottotitolo
        st.markdown('<h1 class="title-gradient">CiaoHost AI Manager</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="subtitle-wrapper">
            <p class="subtitle">
                La piattaforma intelligente per la gestione dei tuoi immobili
                <span class="subtitle-line"></span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Includiamo Font Awesome e aggiungiamo stile CSS migliorato per le card
        st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        """, unsafe_allow_html=True)
        
        # Aggiungiamo lo stile CSS in un tag separato per evitare problemi di visualizzazione
        st.markdown("""
        <style>
        [data-testid="column"] {
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            padding: 0 !important;
            margin: 0 10px;
            transition: all 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        [data-testid="column"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(67, 97, 238, 0.15);
        }
        .card-header {
            background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%);
            padding: 1.8rem 1rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            border-radius: 16px 16px 0 0;
        }
        .card-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1NiIgaGVpZ2h0PSIxMDAiPjxwYXRoIGQ9Ik0yOCA2NkwwIDUwTDAgMTZMMjggMEw1NiAxNkw1NiA1MEwyOCA2NkwyOCAxMDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgyNTUsMjU1LDI1NSwwLjEpIiBzdHJva2Utd2lkdGg9IjIiPjwvcGF0aD48cGF0aCBkPSJNMjggMEwyOCAzNEw1NiA1MEw1NiAxNkwyOCAwWiIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjEpIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIgc3Ryb2tlLXdpZHRoPSIyIj48L3BhdGg+PC9zdmc+');
            background-position: center;
            opacity: 0.2;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Aggiungiamo il resto degli stili in un altro tag per evitare problemi
        st.markdown("""
        <style>
        .card-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto;
            display: block;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
            position: relative;
            z-index: 2;
        }
        .card-title {
            color: white;
            font-size: 1.5rem;
            margin-top: 1rem;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 2;
        }
        .card-text {
            font-size: 1.1rem;
            line-height: 1.7;
            color: #495057;
            margin: 1rem 0;
            padding: 0;
        }
        .highlight-blue {
            font-weight: 600;
            color: #4361ee;
        }
        .feature-list {
            list-style-type: none;
            padding-left: 0;
            margin: 0.5rem 0 1rem 0;
        }
        .feature-item {
            margin-bottom: 0.8rem;
            color: #495057;
            position: relative;
            padding-left: 1.5rem;
        }
        .feature-item:before {
            content: '✓';
            color: #4361ee;
            position: absolute;
            left: 0;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Aggiungiamo uno stile per contenere le card
        st.markdown("""
        <style>
        .card-container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            margin: 0 10px;
            transition: all 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .card-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(67, 97, 238, 0.15);
        }
        .card-content {
            padding: 1.5rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Card principale "Software sviluppato in Italia" - più lunga e sopra le altre
        st.markdown("""
        <div style="background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin: 2rem 0; padding: 2rem; transition: all 0.3s ease; border: 2px solid #e6effd;">
            <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
                <div style="flex-shrink: 0;">
                    <div style="animation: float 3s ease-in-out infinite;">
                        <img src="https://flagcdn.com/w80/it.png" 
                             style="width: 50px; height: auto; border-radius: 6px; filter: drop-shadow(0 3px 6px rgba(0,0,0,0.2)); border: 1px solid #fff;" 
                             alt="Bandiera Italia">
                    </div>
                    <p style="font-size: 0.9rem; font-weight: 600; color: #4361ee; margin-top: 0.5rem; text-align: center; line-height: 1.2;">
                        Software<br>sviluppato<br>in Italia
                    </p>
                </div>
                <div style="flex: 1;">
                    <h3 style="font-size: 1.8rem; font-weight: 700; color: #4361ee; margin-bottom: 1rem; border-bottom: 2px solid #e6effd; padding-bottom: 0.5rem;">
                        🇮🇹 Eccellenza Italiana nel Property Management
                    </h3>
                    <p style="font-size: 1.1rem; line-height: 1.7; color: #495057; margin-bottom: 1.2rem;">
                        <strong>CiaoHost</strong> è orgogliosamente <span style="color: #4361ee; font-weight: 600;">100% Made in Italy</span>, 
                        sviluppato da un team di esperti italiani che comprende profondamente le esigenze del mercato immobiliare nazionale. 
                        La nostra piattaforma combina la tradizione italiana dell'ospitalità con l'innovazione tecnologica più avanzata.
                    </p>
                    <p style="font-size: 1.1rem; line-height: 1.7; color: #495057; margin-bottom: 1.2rem;">
                        Nato dall'esperienza diretta nel settore degli affitti brevi in Italia, CiaoHost è stato progettato per rispondere 
                        alle specifiche normative italiane, alle dinamiche del turismo locale e alle peculiarità del mercato immobiliare del Bel Paese. 
                        <span style="color: #4361ee; font-weight: 600;">Ogni funzionalità è pensata per gli host italiani, da italiani.</span>
                    </p>
                    <div style="background: linear-gradient(135deg, #f0f7ff 0%, #e6effd 100%); padding: 1rem; border-radius: 8px; border-left: 4px solid #4361ee;">
                        <p style="font-size: 1rem; color: #495057; margin: 0; font-style: italic;">
                            "Dalla Sicilia al Trentino, da Venezia alla Costiera Amalfitana - CiaoHost parla italiano e conosce l'Italia come nessun altro."
                        </p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Creiamo le card usando componenti Streamlit
        col1, col2, col3 = st.columns(3)
        
        # Card 1: Gestione Semplificata
        with col1:
            st.markdown("""
            <div class="card-container">
                <div class="card-header">
                    <img src="https://img.icons8.com/fluency/240/null/cottage.png" class="card-icon" alt="Gestione">
                    <h3 class="card-title">Gestione Semplificata</h3>
                </div>
                <div class="card-content">
                    <p class="card-text">
                        <span class="highlight-blue">CiaoHost</span> semplifica la gestione dei tuoi affitti brevi con un'interfaccia intuitiva e strumenti potenti.
                    </p>
                    <ul class="feature-list">
                        <li class="feature-item">Dashboard personalizzabile</li>
                        <li class="feature-item">Gestione prenotazioni centralizzata</li>
                        <li class="feature-item">Calendario sincronizzato</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Card 2: Tecnologia Avanzata
        with col2:
            st.markdown("""
            <div class="card-container">
                <div class="card-header">
                    <img src="https://img.icons8.com/fluency/240/null/artificial-intelligence.png" class="card-icon" alt="AI">
                    <h3 class="card-title">Tecnologia Avanzata</h3>
                </div>
                <div class="card-content">
                    <p class="card-text">
                        La nostra piattaforma combina <span class="highlight-blue">intelligenza artificiale</span> e <span class="highlight-blue">automazione</span> per ottimizzare ogni aspetto della tua attività.
                    </p>
                    <ul class="feature-list">
                        <li class="feature-item">Prezzi dinamici basati sui dati</li>
                        <li class="feature-item">Assistente virtuale multilingua</li>
                        <li class="feature-item">Analisi predittiva del mercato</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Card 3: Risultati Concreti
        with col3:
            st.markdown("""
            <div class="card-container">
                <div class="card-header">
                    <img src="https://img.icons8.com/fluency/240/null/economic-improvement.png" class="card-icon" alt="Risultati">
                    <h3 class="card-title">Risultati Concreti</h3>
                </div>
                <div class="card-content">
                    <p class="card-text">
                        I nostri strumenti di gestione avanzati ti aiutano a <span class="highlight-blue">massimizzare i guadagni</span> e ridurre il tempo dedicato alla gestione.
                    </p>
                    <ul class="feature-list">
                        <li class="feature-item">Aumento medio del 30% dei ricavi</li>
                        <li class="feature-item">Riduzione del 70% del tempo di gestione</li>
                        <li class="feature-item">Miglioramento delle recensioni</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Statistiche in evidenza
        st.markdown("""
        <div style="margin-top: 2rem; animation: fadeIn 2s ease-out;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem; text-align: center;">
                <div style="flex: 1; min-width: 150px; background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);">
                    <h3 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">+30%</h3>
                    <p style="font-size: 1rem;">Aumento medio dei guadagni</p>
                </div>
                <div style="flex: 1; min-width: 150px; background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);">
                    <h3 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">5000+</h3>
                    <p style="font-size: 1rem;">Host soddisfatti</p>
                </div>
                <div style="flex: 1; min-width: 150px; background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);">
                    <h3 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">24/7</h3>
                    <p style="font-size: 1rem;">Supporto clienti</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Pulsante per continuare
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Scopri di più", use_container_width=True, key="welcome_next_1_alt"):
                st.session_state.welcome_screen_step = 2
                st.rerun()
    
    elif st.session_state.welcome_screen_step == 2:
        # Seconda schermata: Chi siamo (migliorata)
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, #f0f7ff 0%, #e6effd 100%); border-radius: 15px; box-shadow: 0 10px 30px rgba(67, 97, 238, 0.1); margin-bottom: 2rem;">
            <h1 class="welcome-title" style="font-size: 2.8rem; font-weight: 700; color: #4361ee; margin-bottom: 1rem; text-shadow: 0 2px 10px rgba(67, 97, 238, 0.2);">
                Chi Siamo
            </h1>
            <p class="welcome-subtitle" style="font-size: 1.3rem; color: #5a6e8c; margin-bottom: 1rem; font-weight: 500;">
                La storia dietro CiaoHost
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Immagine del team e storia dell'azienda
        col_img, col_text = st.columns([1, 2])
        
        with col_img:
            st.markdown("""
            <div style="animation: slideInLeft 1.5s ease-out; text-align: center;">
                <img src="https://img.icons8.com/fluency/240/null/conference-call.png" style="width: 90%; max-width: 200px; filter: drop-shadow(0 5px 15px rgba(67, 97, 238, 0.3)); margin-bottom: 1rem;">
                <div style="background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%); color: white; padding: 1rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3); text-align: center; margin-top: 1rem;">
                    <h3 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">Dal 2025</h3>
                    <p style="font-size: 1rem;">Al servizio degli host</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_text:
            st.markdown("""
            <div class="welcome-text" style="padding: 1.5rem; background-color: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); animation: fadeIn 1.5s ease-out;">
                <h3 style="font-size: 1.5rem; font-weight: 600; color: #4361ee; margin-bottom: 1rem; border-bottom: 2px solid #e6effd; padding-bottom: 0.5rem;">La nostra storia</h3>
                <p style="font-size: 1.1rem; line-height: 1.7; color: #495057; margin-bottom: 1.5rem;">
                    <span style="font-weight: 600; color: #4361ee;">CiaoHost</span> nasce nel 2025 dall'idea di un gruppo di esperti nel settore immobiliare e tecnologico
                    con l'obiettivo di rivoluzionare la gestione degli affitti brevi in Italia.
                </p>
                <p style="font-size: 1.1rem; line-height: 1.7; color: #495057; margin-bottom: 1.5rem;">
                    La nostra missione è <span style="font-weight: 600; color: #4361ee;">semplificare la vita degli host</span>, automatizzando i processi ripetitivi
                    e fornendo strumenti intelligenti per ottimizzare i guadagni e migliorare l'esperienza degli ospiti.
                </p>
                <p style="font-size: 1.1rem; line-height: 1.7; color: #495057; margin-bottom: 0.5rem;">
                    Oggi, CiaoHost è utilizzato da migliaia di host in tutta Italia e continua a crescere
                    grazie al passaparola dei nostri clienti soddisfatti.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Titolo della timeline
        st.markdown("<h2 style='text-align: center; color: #4361ee; margin-top: 3rem;'>Il nostro percorso</h2>", unsafe_allow_html=True)
        st.markdown("<div style='height: 3px; background: linear-gradient(90deg, transparent, #4361ee, transparent); margin: 0 auto 2rem auto; width: 200px;'></div>", unsafe_allow_html=True)
        
        # Timeline con componenti Streamlit
        st.markdown("""
        <style>
        .timeline-dot {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            color: white;
            font-weight: 700;
            box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);
            line-height: 50px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Contenitore con sfondo bianco
        st.markdown("<div style='background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        
        # Creiamo la timeline con colonne
        cols = st.columns(4)
        
        # Punto 1: Fondazione
        with cols[0]:
            st.markdown("<div class='timeline-dot'>2025</div>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; margin-top: 1rem;'>Fondazione</h4>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6c757d; font-size: 0.9rem;'>Nasce CiaoHost</p>", unsafe_allow_html=True)
        
        # Punto 2: Espansione
        with cols[1]:
            st.markdown("<div class='timeline-dot'>2026</div>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; margin-top: 1rem;'>Espansione</h4>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6c757d; font-size: 0.9rem;'>Crescita nazionale</p>", unsafe_allow_html=True)
        
        # Punto 3: Innovazione
        with cols[2]:
            st.markdown("<div class='timeline-dot'>2027</div>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; margin-top: 1rem;'>Innovazione</h4>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6c757d; font-size: 0.9rem;'>Nuove tecnologie</p>", unsafe_allow_html=True)
        
        # Punto 4: Leader
        with cols[3]:
            st.markdown("<div class='timeline-dot'>Oggi</div>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; margin-top: 1rem;'>Leader</h4>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6c757d; font-size: 0.9rem;'>Riferimento di mercato</p>", unsafe_allow_html=True)
        
        # Chiudiamo il contenitore
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Pulsanti di navigazione
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Indietro", use_container_width=True, key="welcome_back_2"):
                st.session_state.welcome_screen_step = 1
                st.rerun()
        with col2:
            if st.button("Continua", use_container_width=True, key="welcome_next_2"):
                st.session_state.welcome_screen_step = 4
                st.rerun()
    

    elif st.session_state.welcome_screen_step == 4:
        # Quarta schermata: Perché sceglierci
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 class="welcome-title" style="font-size: 2.5rem; font-weight: 700; color: #4361ee; margin-bottom: 1rem;">
                Perché Scegliere CiaoHost
            </h1>
            <p class="welcome-subtitle" style="font-size: 1.2rem; color: #6c757d; margin-bottom: 2rem;">
                I vantaggi che ci distinguono
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Vantaggi
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="welcome-feature" style="padding: 1.5rem; background-color: #f8f9fa; border-radius: 10px; height: 100%; margin-bottom: 1rem;">
                <h3 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem; color: #212529;">Risparmio di Tempo</h3>
                <p style="font-size: 1rem; color: #6c757d; line-height: 1.6;">
                    Automatizza fino all'80% delle attività di gestione quotidiane, liberando il tuo tempo per ciò che conta davvero.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="welcome-feature" style="padding: 1.5rem; background-color: #f8f9fa; border-radius: 10px; height: 100%; animation-delay: 0.3s;">
                <h3 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem; color: #212529;">Aumento dei Guadagni</h3>
                <p style="font-size: 1rem; color: #6c757d; line-height: 1.6;">
                    I nostri clienti registrano un aumento medio del 25% dei guadagni grazie ai nostri strumenti di ottimizzazione.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="welcome-feature" style="padding: 1.5rem; background-color: #f8f9fa; border-radius: 10px; height: 100%; margin-bottom: 1rem; animation-delay: 0.2s;">
                <h3 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem; color: #212529;">Supporto Dedicato</h3>
                <p style="font-size: 1rem; color: #6c757d; line-height: 1.6;">
                    Un team di esperti sempre a tua disposizione per aiutarti a massimizzare il potenziale dei tuoi immobili.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="welcome-feature" style="padding: 1.5rem; background-color: #f8f9fa; border-radius: 10px; height: 100%; animation-delay: 0.4s;">
                <h3 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem; color: #212529;">Facilità d'Uso</h3>
                <p style="font-size: 1rem; color: #6c757d; line-height: 1.6;">
                    Un'interfaccia intuitiva progettata per essere utilizzata da chiunque, senza necessità di competenze tecniche.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Call to action
        st.markdown("""
        <div class="welcome-cta" style="text-align: center; margin-top: 2rem; padding: 2rem; background-color: #e6effd; border-radius: 10px;">
            <h2 style="font-size: 1.8rem; font-weight: 700; color: #4361ee; margin-bottom: 1rem;">
                Pronto a trasformare la gestione dei tuoi immobili?
            </h2>
            <p style="font-size: 1.1rem; color: #6c757d; margin-bottom: 1.5rem;">
                Unisciti a migliaia di host soddisfatti e scopri come CiaoHost può rivoluzionare il tuo business.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pulsanti di navigazione
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("Indietro", use_container_width=True, key="welcome_back_4"):
                st.session_state.welcome_screen_step = 2
                st.rerun()
        with col2:
            if st.button("Accedi o Registrati", use_container_width=True, key="welcome_finish"):
                # Reset dello step per la prossima visita
                st.session_state.welcome_screen_step = 1
                # Imposta il flag per mostrare la schermata di login
                st.session_state.show_login_screen = True
                st.rerun()
        with col3:
            pass

# Importa il nuovo sistema di login
from new_login_system import show_login as new_show_login

def show_login():
    # Usa solo il nuovo sistema di login e poi termina la funzione
    new_show_login()
    return
    
    # Il codice sotto non verrà mai eseguito
    # Manteniamo il vecchio codice commentato per riferimento
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
        
        /* Stile dei form input - versione professionale */
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
        div[data-baseweb="input"] input {
            font-size: 15px !important;
        }
        
        /* Stile dei bottoni - versione professionale */
        .stButton button {
            background-color: #1a56db !important;
            color: white !important;
            font-weight: 500 !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.6rem 1rem !important;
            font-size: 15px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08) !important;
        }
        .stButton button:hover {
            background-color: #1e429f !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12) !important;
        }
        
        /* Stile per le tabs - versione professionale */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent !important;
            border-bottom: 1px solid #e2e8f0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 15px;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            color: #1a56db !important;
            border-bottom: 2px solid #1a56db !important;
        }
        
        /* Nascondi elementi Streamlit non necessari */
        #MainMenu, .stDeployButton, footer {
            display: none !important;
        }
        
        /* Animazione semplice */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Layout a 2 colonne (più pulito e professionale)
    col_left, col_right = st.columns([1, 1])
    
    # Colonna sinistra: Branding e informazioni
    with col_left:
        # Logo e titolo
        st.markdown("<h1 style='font-size: 2.5rem; font-weight: 700; color: #1a56db; margin-top: 3rem;'>CiaoHost Suite</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.1rem; color: #4a5568; margin-bottom: 2rem; line-height: 1.6;'>Piattaforma avanzata di gestione patrimoniale immobiliare per professionisti e investitori.</p>", unsafe_allow_html=True)
        
        # Separatore
        st.markdown("<hr style='height: 1px; background: #e2e8f0; margin: 2rem 0; border: none;'>", unsafe_allow_html=True)
        
        # Sezione soluzioni enterprise
        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 600; color: #1a202c; margin-bottom: 1rem;'>Soluzioni Enterprise</h3>", unsafe_allow_html=True)
        
        # Feature 1
        feature1_col1, feature1_col2 = st.columns([1, 9])
        with feature1_col1:
            st.markdown("<div style='background-color: #ebf5ff; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;'><svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#1a56db' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='20 6 9 17 4 12'></polyline></svg></div>", unsafe_allow_html=True)
        with feature1_col2:
            st.markdown("<div style='color: #4a5568; padding-top: 3px;'>Dashboard personalizzata con analytics avanzati</div>", unsafe_allow_html=True)
        
        # Feature 2
        feature2_col1, feature2_col2 = st.columns([1, 9])
        with feature2_col1:
            st.markdown("<div style='background-color: #ebf5ff; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;'><svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#1a56db' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='20 6 9 17 4 12'></polyline></svg></div>", unsafe_allow_html=True)
        with feature2_col2:
            st.markdown("<div style='color: #4a5568; padding-top: 3px;'>Gestione multi-portfolio con reporting finanziario</div>", unsafe_allow_html=True)
        
        # Feature 3
        feature3_col1, feature3_col2 = st.columns([1, 9])
        with feature3_col1:
            st.markdown("<div style='background-color: #ebf5ff; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;'><svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#1a56db' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='20 6 9 17 4 12'></polyline></svg></div>", unsafe_allow_html=True)
        with feature3_col2:
            st.markdown("<div style='color: #4a5568; padding-top: 3px;'>Integrazione con sistemi finanziari aziendali</div>", unsafe_allow_html=True)
        
        # Partner box
        st.markdown("<div style='margin-top: 2rem; text-align: center; padding: 1.5rem; background-color: #f7fafc; border-radius: 8px; border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.9rem; color: #4a5568; margin-bottom: 0.5rem;'>Partner fidato di</p>", unsafe_allow_html=True)
        
        partner_col1, partner_col2, partner_col3 = st.columns(3)
        with partner_col1:
            st.markdown("<div style='font-weight: 600; color: #2d3748; opacity: 0.7; text-align: center;'>JP Morgan</div>", unsafe_allow_html=True)
        with partner_col2:
            st.markdown("<div style='font-weight: 600; color: #2d3748; opacity: 0.7; text-align: center;'>Blackstone</div>", unsafe_allow_html=True)
        with partner_col3:
            st.markdown("<div style='font-weight: 600; color: #2d3748; opacity: 0.7; text-align: center;'>Goldman Sachs</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Colonna destra: form di login professionale
    with col_right:
        # Container per il form di login
        st.markdown("""
        <style>
        .enterprise-login-container {
            background-color: white;
            border-radius: 8px;
            padding: 3rem 2.5rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            margin-top: 3rem;
            animation: fadeIn 0.5s ease-out;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="enterprise-login-container">', unsafe_allow_html=True)
        
        # Titolo del form
        st.markdown("<h2 style='font-size: 1.5rem; font-weight: 600; color: #1a202c; margin-bottom: 1.5rem;'>Accedi all'area riservata</h2>", unsafe_allow_html=True)
        
        # Tab per login/registrazione
        tab1, tab2 = st.tabs(["Accedi", "Registrati"])
        
        with tab1:
            # Email/Username
            email = st.text_input("Email", placeholder="nome@esempio.com")
            
            # Password
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            # Remember me
            remember = st.checkbox("Ricordami", value=True)
            
            # Login button
            if st.button("Accedi", use_container_width=True):
                st.session_state.is_authenticated = True
                st.session_state.current_page = 'dashboard'
                st.session_state.show_login_screen = False
                st.rerun()
            
            # Recovery options
            st.markdown("<div style='text-align: center; margin-top: 1.5rem; font-size: 0.9rem;'><a href='#' style='color: #1a56db; text-decoration: none;'>Password dimenticata?</a></div>", unsafe_allow_html=True)
        
        with tab2:
            # Nome
            st.text_input("Nome", placeholder="Il tuo nome")
            
            # Email
            st.text_input("Email", placeholder="nome@esempio.com", key="reg_email")
            
            # Password con meter
            password_reg = st.text_input("Password", type="password", placeholder="••••••••", key="reg_password")
            
            # Password strength meter
            if password_reg:
                strength = update_password_strength(password_reg)
                st.progress(strength / 100.0)
                if strength < 40:
                    st.caption("Password debole: aggiungere numeri e caratteri speciali")
                elif strength < 70:
                    st.caption("Password media: aggiungere caratteri speciali")
                else:
                    st.caption("Password forte")
            
            # Terms
            st.checkbox("Accetto i Termini di Servizio", key="terms")
            
            # Register button
            if st.button("Crea Account", use_container_width=True):
                st.success("Account creato con successo! Puoi accedere ora.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Nota sulla sicurezza
        st.markdown("""
        <div style="margin-top: 1rem; text-align: center;">
            <p style="font-size: 0.8rem; color: #718096; display: flex; align-items: center; justify-content: center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                Connessione protetta con crittografia SSL a 256 bit
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Tab per login/registrazione
        tab1, tab2 = st.tabs(["Accedi", "Registrati"])
        
        with tab1:
            # Email
            email = st.text_input("Email", placeholder="nome@esempio.com")
            
            # Password input con icona e stile migliorato
            st.markdown("""
                    <label style="font-size: 0.95rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem; display: block; margin-top: 1rem;">
                        <span style="display: inline-flex; align-items: center; gap: 6px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#4361ee" viewBox="0 0 16 16">
                                <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2zM5 8h6a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/>
                            </svg>
                            Password
                        </span>
                    </label>
                """, unsafe_allow_html=True)
            password = st.text_input("", type="password", key="login_pw", placeholder="Inserisci la tua password")
            
            # Remember me checkbox con migliore formattazione
            col_remember, col_forgot = st.columns(2)
            with col_remember:
                st.markdown("""
                    <div style="margin-top: 1rem;">
                """, unsafe_allow_html=True)
                st.checkbox("Ricordami", key="remember_me")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col_forgot:
                st.markdown("""
                    <div style="text-align: right; margin-top: 1.2rem;">
                        <a href="#" style="font-size: 0.9rem; font-weight: 500;">Password dimenticata?</a>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            
            # Login button con migliore styling e feedback visivo
            login_button = st.form_submit_button("Accedi", use_container_width=True)
            
            if login_button:
                if not email or not password:
                    st.error("Inserisci email e password.")
                elif email == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
                    # Show loading animation
                    with st.spinner("Accesso in corso..."):
                        time.sleep(0.5)  # Simulate loading
                        st.session_state.is_authenticated = True
                        st.session_state.current_user_email = "admin"
                        st.session_state.current_page = 'home'
                        st.rerun()
                elif email in st.session_state.users and st.session_state.users[email] == password:
                    # Show loading animation
                    with st.spinner("Accesso in corso..."):
                        time.sleep(0.5)  # Simulate loading
                        st.session_state.is_authenticated = True
                        st.session_state.current_user_email = email
                        st.session_state.current_page = 'home'
                        st.rerun()
                else:
                    st.error("Credenziali non valide.")
        
        with tab2:
            st.markdown("<p style='height: 20px;'></p>", unsafe_allow_html=True)
            
            # Welcome message for registration
            st.markdown("""
                <div style="margin-bottom: 1.5rem;">
                    <h3 style="font-size: 1.5rem; font-weight: 600; color: #334155; margin-bottom: 0.5rem;">Crea un nuovo account 🚀</h3>
                    <p style="color: #64748b; font-size: 1rem;">Registrati per iniziare a gestire i tuoi immobili</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Inizializza variabili di sessione per la password se non esistono
            if 'password_strength' not in st.session_state:
                st.session_state.password_strength = {
                    'color': "#64748b",
                    'text': "Non inserita",
                    'width': "0%"
                }
            
            # Script JavaScript per monitorare l'input della password in tempo reale
            st.markdown("""
            <script>
            // Sarà eseguito quando il documento HTML è completamente caricato
            document.addEventListener('DOMContentLoaded', function() {
                // Funzione che trova il campo password tramite placeholder
                function findPasswordField() {
                    let inputs = document.querySelectorAll('input');
                    for (let input of inputs) {
                        if (input.placeholder === 'Crea una password' && input.type === 'password') {
                            return input;
                        }
                    }
                    return null;
                }
                
                // Controlla ogni 300ms se il campo password è disponibile
                let checkInterval = setInterval(function() {
                    const passwordField = findPasswordField();
                    if (passwordField) {
                        clearInterval(checkInterval);
                        
                        // Aggiunge un event listener per l'input in tempo reale
                        passwordField.addEventListener('input', function() {
                            // Invia un evento personalizzato a Streamlit
                            window.parent.postMessage({
                                type: 'streamlit:setComponentValue',
                                value: this.value
                            }, '*');
                        });
                    }
                }, 300);
            });
            </script>
            """, unsafe_allow_html=True)
            
            # Funzione per valutare la forza della password
            def update_password_strength():
                password = st.session_state.reg_pw
                if not password:
                    st.session_state.password_strength = {
                        'color': "#64748b",
                        'text': "Non inserita",
                        'width': "0%"
                    }
                    return
                
                # Calcolo forza password
                strength = len(password)
                has_number = any(char.isdigit() for char in password)
                has_upper = any(char.isupper() for char in password)
                has_lower = any(char.islower() for char in password)
                has_special = any(not char.isalnum() for char in password)
                
                # Valutazione forza password con criteri più specifici
                if strength < 6:
                    st.session_state.password_strength = {
                        'color': "#ef4444",  # Red
                        'text': "Debole",
                        'width': "30%"
                    }
                elif strength < 10 or sum([has_number, has_special, has_upper, has_lower]) < 3:
                    st.session_state.password_strength = {
                        'color': "#f59e0b",  # Yellow
                        'text': "Media",
                        'width': "60%"
                    }
                else:
                    st.session_state.password_strength = {
                        'color': "#10b981",  # Green
                        'text': "Forte",
                        'width': "100%"
                    }
            
            # Email input con icona e stile migliorato
            st.markdown("""
                <label style="font-size: 0.95rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem; display: block;">
                    <span style="display: inline-flex; align-items: center; gap: 6px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#4361ee" viewBox="0 0 16 16">
                            <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2zm13 2.383-4.708 2.825L15 11.105V5.383zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741zM1 11.105l4.708-2.897L1 5.383v5.722z"/>
                        </svg>
                        Indirizzo Email
                    </span>
                </label>
            """, unsafe_allow_html=True)
            new_email = st.text_input("", key="reg_email", placeholder="Inserisci la tua email")
            
            # Password security meter
            st.markdown("""
                <div style="margin-top: 1.2rem; margin-bottom: 0.8rem;">
                    <label style="font-size: 0.95rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem; display: block;">
                        <span style="display: inline-flex; align-items: center; gap: 6px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#4361ee" viewBox="0 0 16 16">
                                <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/>
                            </svg>
                            Password
                        </span>
                    </label>
                </div>
            """, unsafe_allow_html=True)
            
            # Password fields in columns with better styling
            col_pwd1, col_pwd2 = st.columns(2)
            with col_pwd1:
                new_password = st.text_input("", type="password", key="reg_pw", placeholder="Crea una password", on_change=update_password_strength)
            with col_pwd2:
                confirm_password = st.text_input("", type="password", key="confirm_pw", placeholder="Ripeti la password")
            
            # Password strength indicator usando i valori salvati nella session state
            strength_color = st.session_state.password_strength['color']
            strength_text = st.session_state.password_strength['text']
            strength_width = st.session_state.password_strength['width']
            
            st.markdown(f"""
                <div style="margin-top: 0.5rem; margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span style="font-size: 0.8rem; color: #64748b;">Sicurezza Password</span>
                        <span style="font-size: 0.8rem; color: {strength_color}; font-weight: 500;">{strength_text}</span>
                    </div>
                    <div style="height: 4px; background-color: #e2e8f0; border-radius: 2px; overflow: hidden;">
                        <div style="height: 100%; width: {strength_width}; background-color: {strength_color}; border-radius: 2px;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Terms and conditions checkbox con link
            st.markdown("""
                <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
                    <p style="margin: 0; padding: 0;"></p>
                </div>
            """, unsafe_allow_html=True)
            st.checkbox("Accetto i Termini e le Condizioni", key="terms_accepted", help="Devi accettare i termini per continuare")
            st.markdown("""
                <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.3rem;">
                    Cliccando su "Crea Account", accetti la nostra <a href="#">Privacy Policy</a> e i <a href="#">Termini di Servizio</a>.
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            
            # Form per il pulsante di registrazione
            with st.form("register_form"):
                # Register button con animazione hover
                register_button = st.form_submit_button("Crea Account", use_container_width=True)
                
                if register_button:
                    if not new_email or not new_password:
                        st.error("Inserisci email e password validi.")
                    elif not st.session_state.get("terms_accepted", False):
                        st.error("Devi accettare i Termini e le Condizioni per continuare.")
                    elif new_email in st.session_state.users:
                        st.error("Email già registrata!")
                    elif new_email == ADMIN_CREDENTIALS["username"]:
                        st.error("Questo username è riservato.")
                    elif "@" not in new_email or "." not in new_email:
                        st.error("Inserisci un indirizzo email valido.")
                    elif len(new_password) < 6:
                        st.error("La password deve contenere almeno 6 caratteri.")
                    elif new_password != confirm_password:
                        st.error("Le password non corrispondono.")
                    else:
                        # Add new user with loading animation
                        with st.spinner("Creazione account in corso..."):
                            time.sleep(0.5)  # Simulate loading
                            st.session_state.users[new_email] = new_password
                            save_database()
                            st.success("Registrazione completata! Ora puoi accedere.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Linea divisoria con stile migliorato
        st.markdown("""
            <div style="display: flex; align-items: center; margin: 2.5rem 0 2rem 0;">
                <div style="flex-grow: 1; height: 1px; background: linear-gradient(to right, rgba(226, 232, 240, 0), rgba(226, 232, 240, 1));"></div>
                <div style="margin: 0 1.2rem; color: #94a3b8; font-size: 0.9rem; font-weight: 600; letter-spacing: 0.05em;">ACCEDI CON</div>
                <div style="flex-grow: 1; height: 1px; background: linear-gradient(to left, rgba(226, 232, 240, 0), rgba(226, 232, 240, 1));"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Social login options con icone moderne e stile migliorato
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: center; gap: 1.2rem;">
                    <button class="social-btn" style="background-color: #4267B2; color: white; font-size: 15px; width: 45%;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z"/>
                        </svg>
                        Facebook
                    </button>
                    <button class="social-btn" style="background-color: white; color: #333; border: 1px solid #e2e8f0 !important; font-size: 15px; width: 45%;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        Google
                    </button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        


def show_subscription_plans():
    st.markdown("""
        <h1 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 1rem;">
            <span style="color: #4361ee;">💼</span> Piani di Abbonamento
        </h1>
        <p style="font-size: 1.1rem; color: #6c757d; margin-bottom: 2rem;">
            Scegli il piano più adatto alle tue esigenze per la gestione dei tuoi immobili
        </p>
    """, unsafe_allow_html=True)

    # Pricing toggle
    col_toggle_left, col_toggle_center, col_toggle_right = st.columns([2, 1, 2])
    with col_toggle_center:
        billing_period = st.radio(
            "Periodo di fatturazione",
            ["Mensile", "Annuale (sconto 15%)"],
            horizontal=True,
            key="billing_period"
        )
    
    is_annual = billing_period.startswith("Annuale")
    
    # Calculate prices based on billing period
    base_price = 25
    pro_price = 44.99
    
    if is_annual:
        base_price = round(base_price * 0.85, 2)
        pro_price = round(pro_price * 0.85, 2)
    
    # Pricing cards
    st.markdown("<div style='display: flex; gap: 20px; margin-top: 2rem;'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(f"""
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); height: 100%; position: relative; padding: 2rem; border: 1px solid #dee2e6;">
                <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #e6effd; color: #4361ee; padding: 5px 15px; border-radius: 20px; font-weight: 500; font-size: 0.9rem;">
                    Base
                </div>
                <div style="text-align: center; margin-bottom: 1.5rem; margin-top: 0.5rem;">
                    <h2 style="font-size: 2.5rem; font-weight: 700; color: #4361ee; margin-bottom: 0.5rem;">€{base_price}</h2>
                    <p style="color: #6c757d; font-size: 0.9rem;">per immobile / {('mese (fatturato annualmente)' if is_annual else 'mese')}</p>
                    <p style="color: #6c757d; font-size: 0.9rem;">+ 10% commissione</p>
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Concierge AI multilingua 24/7</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Ottimizzazione prezzi con AI</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Dashboard base con statistiche</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Sistema antifrode ospiti</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Archivio fiscale e fatturazione</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Scegli Piano Base", key="buy_base", use_container_width=True):
            with st.spinner("Attivazione del piano in corso..."):
                time.sleep(1)
                st.success("Ottima scelta! Preparazione della tua dashboard...")
                # Prepara i dati di esempio
                data = {
                    'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
                    'Guadagno': [1200, 1350, 1800, 2200, 2100, 2400],
                    'Occupazione': [75, 82, 88, 95, 93, 98],
                    'Prenotazioni': [10, 12, 15, 18, 17, 20]
                }
                st.session_state.data = pd.DataFrame(data)
                
                # Imposta direttamente la variabile di sessione
                st.session_state.subscription_purchased = True
                st.session_state.subscription_type = "base"
                
                # Mostra l'effetto coriandoli per celebrare l'acquisto
                show_confetti()
                
                # Messaggio di successo
                st.success("Abbonamento attivato con successo! Tra 5 secondi verrai reindirizzato alla dashboard.")
                
                # Aggiungi un ritardo di 5 secondi
                time.sleep(5)
                
                # Imposta la pagina corrente
                st.session_state.current_page = 'dashboard'
                
                # Forza il rerun
                st.rerun()

    with col2:
        st.markdown(f"""
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); height: 100%; position: relative; padding: 2rem; border: 2px solid #4361ee; transform: scale(1.05);">
                <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #4361ee; color: white; padding: 5px 15px; border-radius: 20px; font-weight: 500; font-size: 0.9rem;">
                    Pro
                </div>
                <div style="position: absolute; top: -12px; right: -12px; background-color: #ff9800; color: white; padding: 5px 10px; border-radius: 20px; font-weight: 500; font-size: 0.8rem;">
                    Più popolare
                </div>
                <div style="text-align: center; margin-bottom: 1.5rem; margin-top: 0.5rem;">
                    <h2 style="font-size: 2.5rem; font-weight: 700; color: #4361ee; margin-bottom: 0.5rem;">€{pro_price}</h2>
                    <p style="color: #6c757d; font-size: 0.9rem;">per immobile / {('mese (fatturato annualmente)' if is_annual else 'mese')}</p>
                    <p style="color: #6c757d; font-size: 0.9rem;">+ 10% commissione</p>
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span><strong>Tutto il Piano Base</strong></span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Dashboard avanzata personalizzabile</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Analisi predittiva delle prenotazioni</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Personalizzazione avanzata del chatbot AI</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Supporto tecnico prioritario dedicato</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Integrazione API con portali esterni</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Scegli Piano Pro", key="buy_pro", use_container_width=True):
            with st.spinner("Attivazione del piano in corso..."):
                time.sleep(1)
                st.success("Eccellente scelta! Preparazione della tua dashboard PRO...")
                # Prepara i dati di esempio
                data = {
                    'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
                    'Guadagno': [1200, 1350, 1800, 2200, 2100, 2400],
                    'Occupazione': [75, 82, 88, 95, 93, 98],
                    'Prenotazioni': [10, 12, 15, 18, 17, 20]
                }
                st.session_state.data = pd.DataFrame(data)
                
                # Imposta direttamente la variabile di sessione
                st.session_state.subscription_purchased = True
                st.session_state.subscription_type = "pro"
                
                # Mostra l'effetto coriandoli per celebrare l'acquisto
                show_confetti()
                
                # Messaggio di successo
                st.success("Abbonamento PRO attivato con successo! Tra 5 secondi verrai reindirizzato alla dashboard.")
                
                # Aggiungi un ritardo di 5 secondi
                time.sleep(5)
                
                # Imposta la pagina corrente
                st.session_state.current_page = 'dashboard'
                
                # Forza il rerun
                st.rerun()
    
    with col3:
        st.markdown(f"""
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); height: 100%; position: relative; padding: 2rem; border: 1px solid #dee2e6;">
                <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #e6effd; color: #4361ee; padding: 5px 15px; border-radius: 20px; font-weight: 500; font-size: 0.9rem;">
                    Enterprise
                </div>
                <div style="text-align: center; margin-bottom: 1.5rem; margin-top: 0.5rem;">
                    <h2 style="font-size: 2.5rem; font-weight: 700; color: #4361ee; margin-bottom: 0.5rem;">Contattaci</h2>
                    <p style="color: #6c757d; font-size: 0.9rem;">per un'offerta personalizzata</p>
                    <p style="color: #6c757d; font-size: 0.9rem;">+ commissione personalizzata</p>
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span><strong>Tutto il Piano Pro</strong></span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Soluzioni su misura per grandi portafogli</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Account manager dedicato</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Formazione personalizzata del team</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>Sviluppo di funzionalità su misura</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #4361ee; margin-right: 0.5rem; font-size: 1.2rem;">✓</span>
                        <span>SLA garantito con supporto 24/7</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Contattaci", key="contact_enterprise", use_container_width=True):
            st.info("Un nostro consulente ti contatterà al più presto per discutere le tue esigenze specifiche.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("""
        <div style="margin-top: 4rem;">
            <h2 style="font-size: 1.8rem; font-weight: 600; margin-bottom: 1.5rem;">Domande Frequenti</h2>
        </div>
    """, unsafe_allow_html=True)
    
    faq_col1, faq_col2 = st.columns(2)
    
    with faq_col1:
        with st.expander("Posso cambiare piano in qualsiasi momento?"):
            st.markdown("""
                Sì, puoi passare da un piano all'altro in qualsiasi momento. Se passi a un piano superiore, 
                l'aggiornamento sarà immediato. Se passi a un piano inferiore, il cambiamento avverrà alla fine 
                del periodo di fatturazione corrente.
            """)
        
        with st.expander("Come funziona la commissione del 10%?"):
            st.markdown("""
                La commissione del 10% viene applicata solo sulle prenotazioni effettivamente confermate 
                attraverso la piattaforma. Non ci sono commissioni su prenotazioni che gestisci esternamente.
            """)
        
        with st.expander("Posso provare la piattaforma prima di acquistare?"):
            st.markdown("""
                Offriamo una demo gratuita di 14 giorni del Piano Pro senza necessità di carta di credito. 
                Contattaci per attivare la tua prova gratuita.
            """)
    
    with faq_col2:
        with st.expander("Quali metodi di pagamento accettate?"):
            st.markdown("""
                Accettiamo tutte le principali carte di credito (Visa, Mastercard, American Express), 
                PayPal, bonifico bancario e, per i piani Enterprise, anche fatturazione diretta.
            """)
        
        with st.expander("Posso annullare il mio abbonamento?"):
            st.markdown("""
                Sì, puoi annullare il tuo abbonamento in qualsiasi momento. Se annulli, manterrai 
                l'accesso fino alla fine del periodo di fatturazione corrente.
            """)
        
        with st.expander("Offrite sconti per più immobili?"):
            st.markdown("""
                Sì, offriamo sconti progressivi basati sul numero di immobili gestiti. A partire da 5 immobili, 
                riceverai uno sconto del 5%, che aumenta fino al 20% per portafogli di oltre 20 immobili.
            """)
    
    # Footer note
    st.markdown("""
        <div style="margin-top: 3rem; padding: 1rem; background-color: #f8f9fa; border-radius: 8px; text-align: center;">
            <p style="color: #6c757d; margin-bottom: 0;">Tutti i prezzi sono IVA esclusa. Per soluzioni personalizzate per grandi portafogli immobiliari, contatta il nostro team commerciale.</p>
        </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    # Importa la dashboard migliorata
    from dashboard import show_enhanced_dashboard
    
    # Mostra la dashboard migliorata
    show_enhanced_dashboard()
    
    # Aggiungi il footer
    show_footer()

# Placeholder functions for attached_assets functionalities
def show_cleaning_management_page():
    # Aggiungi CSS specifico per questa pagina
    st.markdown("""
    <style>
        /* Force light theme for this page */
        .main .block-container {
            background-color: white !important;
        }
        
        /* Style for buttons in this page */
        .stButton button {
            background-color: #4361ee !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
        }
        
        /* Style for dataframes in this page */
        .dataframe {
            background-color: white !important;
            color: #333333 !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        
        /* Style for tabs in this page */
        .stTabs [data-baseweb="tab"] {
            background-color: white !important;
            color: #333333 !important;
            font-weight: 500 !important;
        }
        
        /* Style for tab content in this page */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: white !important;
            color: #333333 !important;
            padding: 16px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Verifica se l'utente ha un abbonamento attivo
    if not st.session_state.get('subscription_purchased', False):
        st.warning("Per accedere alla gestione pulizie è necessario acquistare un piano di abbonamento.")
        # Mostra un messaggio di attesa e poi reindirizza
        with st.spinner("Reindirizzamento alla pagina dei piani di abbonamento..."):
            time.sleep(2)
            st.session_state.current_page = 'subscriptions'
            st.rerun()
        return
    
    # Versione semplificata della gestione pulizie
    st.title("🧹 Gestione Pulizie")
    
    # Pulsanti di navigazione
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🏠 Home", key="clean_home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        if st.button("🔄 Aggiorna", key="clean_refresh", use_container_width=True):
            st.success("Dati aggiornati!")
    
    st.markdown("---")
    
    # Tabs per le diverse funzionalità
    tab_titles = ["Calendario Pulizie", "Servizi di Pulizia", "Programmazione", "Messaggi Automatici"]
    tabs = st.tabs(tab_titles)
    
    with tabs[0]:  # Calendario Pulizie
        st.subheader("Calendario Pulizie")
        st.info("Qui potrai visualizzare il calendario delle pulizie programmate.")
        
        # Esempio di calendario
        st.markdown("### Pulizie programmate")
        calendar_data = {
            'Data': ['15/05/2023', '18/05/2023', '20/05/2023', '25/05/2023', '30/05/2023'],
            'Proprietà': ['Villa Marina', 'Appartamento Centro', 'Casa Giardino', 'Loft Moderno', 'Villa Marina'],
            'Servizio': ['Pulizia Standard', 'Pulizia Profonda', 'Pulizia Standard', 'Pulizia Standard', 'Pulizia Profonda'],
            'Stato': ['Completata', 'Programmata', 'Programmata', 'Programmata', 'Programmata']
        }
        calendar_df = pd.DataFrame(calendar_data)
        st.dataframe(calendar_df, use_container_width=True)
    
    with tabs[1]:  # Servizi di Pulizia
        from attached_assets.cleaning_management import show_cleaning_services
        show_cleaning_services()
    
    with tabs[2]:  # Programmazione
        st.subheader("Programmazione Pulizie")
        st.info("Qui potrai programmare nuove pulizie.")
        
        # Form di esempio
        with st.form("schedule_form"):
            st.selectbox("Proprietà", ["Villa Marina", "Appartamento Centro", "Casa Giardino", "Loft Moderno"])
            st.selectbox("Servizio", ["Pulizia Standard", "Pulizia Profonda"])
            st.date_input("Data")
            st.time_input("Ora")
            st.text_area("Note")
            
            if st.form_submit_button("Programma Pulizia"):
                st.success("Pulizia programmata con successo!")
    
    with tabs[3]:  # Messaggi Automatici
        from attached_assets.cleaning_management import show_automated_messages
        show_automated_messages()
    
    # Aggiungi il footer
    show_footer()


def show_dynamic_pricing_page():
    # Aggiungi CSS specifico per questa pagina
    st.markdown("""
    <style>
        /* Force light theme for this page */
        .main .block-container {
            background-color: white !important;
        }
        
        /* Style for buttons in this page */
        .stButton button {
            background-color: #4361ee !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
        }
        
        /* Style for dataframes in this page */
        .dataframe {
            background-color: white !important;
            color: #333333 !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        
        /* Style for tabs in this page */
        .stTabs [data-baseweb="tab"] {
            background-color: white !important;
            color: #333333 !important;
            font-weight: 500 !important;
        }
        
        /* Style for tab content in this page */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: white !important;
            color: #333333 !important;
            padding: 16px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Verifica se l'utente ha un abbonamento attivo
    if not st.session_state.get('subscription_purchased', False):
        st.warning("Per accedere ai prezzi dinamici è necessario acquistare un piano di abbonamento.")
        # Mostra un messaggio di attesa e poi reindirizza
        with st.spinner("Reindirizzamento alla pagina dei piani di abbonamento..."):
            time.sleep(2)
            st.session_state.current_page = 'subscriptions'
            st.rerun()
        return
    
    # Versione semplificata dei prezzi dinamici
    st.title("💰 Prezzi Dinamici")
    
    # Pulsanti di navigazione
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🏠 Home", key="price_home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        if st.button("🔄 Aggiorna", key="price_refresh", use_container_width=True):
            st.success("Dati aggiornati!")
    
    st.markdown("---")
    
    # Tabs per le diverse funzionalità
    tab_titles = ["Panoramica Prezzi", "Gestione Stagioni", "Ottimizzazione AI", "Monitoraggio Mercato"]
    tabs = st.tabs(tab_titles)
    
    with tabs[0]:  # Panoramica Prezzi
        st.subheader("Panoramica Prezzi")
        st.info("Qui potrai visualizzare e gestire i prezzi delle tue proprietà.")
        
        # Esempio di tabella prezzi
        price_data = {
            'Proprietà': ['Villa Marina', 'Appartamento Centro', 'Casa Giardino', 'Loft Moderno'],
            'Prezzo Base': [120, 80, 95, 110],
            'Prezzo Weekend': [150, 100, 120, 140],
            'Prezzo Alta Stagione': [180, 120, 140, 160],
            'Sconto Settimanale': ['10%', '15%', '10%', '5%']
        }
        price_df = pd.DataFrame(price_data)
        st.dataframe(price_df, use_container_width=True)
        
        # Grafico esempio
        st.subheader("Andamento Prezzi")
        chart_data = pd.DataFrame({
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'],
            'Villa Marina': [120, 120, 130, 140, 150, 160, 180, 180, 160, 140, 130, 150],
            'Appartamento Centro': [80, 80, 85, 90, 100, 110, 120, 120, 110, 90, 85, 100]
        }).set_index('Mese')
        st.line_chart(chart_data)
    
    with tabs[1]:  # Gestione Stagioni
        st.subheader("Gestione Stagioni")
        st.info("Qui potrai definire le stagioni e i relativi prezzi.")
        
        # Esempio di stagioni
        seasons_data = {
            'Stagione': ['Bassa', 'Media', 'Alta', 'Altissima'],
            'Periodo': ['Nov-Mar', 'Apr-Mag, Ott', 'Giu, Set', 'Lug-Ago'],
            'Moltiplicatore': ['1.0x', '1.2x', '1.5x', '2.0x']
        }
        seasons_df = pd.DataFrame(seasons_data)
        st.dataframe(seasons_df, use_container_width=True)
        
        # Form di esempio
        with st.form("season_form"):
            st.selectbox("Stagione", ["Bassa", "Media", "Alta", "Altissima"])
            st.date_input("Data Inizio")
            st.date_input("Data Fine")
            st.number_input("Moltiplicatore Prezzo", min_value=1.0, max_value=3.0, value=1.5, step=0.1)
            
            if st.form_submit_button("Salva Stagione"):
                st.success("Stagione salvata con successo!")
    
    with tabs[2]:  # Ottimizzazione AI
        st.subheader("Ottimizzazione AI")
        st.info("Qui potrai utilizzare l'intelligenza artificiale per ottimizzare i prezzi.")
        
        st.markdown("### Suggerimenti AI")
        st.markdown("Basandoci sui dati di mercato e sulle tue performance storiche, suggeriamo:")
        
        suggestions = [
            "Aumenta i prezzi del 15% nei weekend di Giugno",
            "Riduci i prezzi infrasettimanali di Novembre del 10%",
            "Offri uno sconto del 20% per soggiorni di almeno 7 notti in Bassa Stagione"
        ]
        
        for i, suggestion in enumerate(suggestions):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.info(suggestion)
            with col2:
                if st.button("Applica", key=f"apply_{i}"):
                    st.success("Suggerimento applicato!")
        
        st.markdown("### Analisi Competitiva")
        st.markdown("Le tue proprietà rispetto alla concorrenza:")
        
        comp_data = {
            'Proprietà': ['Villa Marina', 'Appartamento Centro'],
            'Tuo Prezzo': ['€120', '€80'],
            'Prezzo Medio Concorrenza': ['€135', '€75'],
            'Suggerimento': ['Aumenta', 'Mantieni']
        }
        comp_df = pd.DataFrame(comp_data)
        st.dataframe(comp_df, use_container_width=True)
    
    with tabs[3]:  # Monitoraggio Mercato
        st.subheader("Monitoraggio Mercato")
        st.info("Qui potrai monitorare i trend di mercato nella tua zona.")
        
        st.markdown("### Trend di Prezzo per Zona")
        trend_data = pd.DataFrame({
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
            'Centro': [100, 105, 110, 115, 120, 125],
            'Periferia': [70, 72, 75, 78, 80, 82],
            'Mare': [150, 155, 160, 170, 180, 200]
        }).set_index('Mese')
        st.line_chart(trend_data)
        
        st.markdown("### Eventi Locali")
        events_data = {
            'Data': ['15/06/2023', '20/07/2023', '10/08/2023'],
            'Evento': ['Festival Musicale', 'Mostra d\'Arte', 'Sagra Locale'],
            'Impatto Previsto': ['Alto', 'Medio', 'Basso'],
            'Suggerimento': ['Aumenta prezzi del 25%', 'Aumenta prezzi del 15%', 'Nessuna azione']
        }
        events_df = pd.DataFrame(events_data)
        st.dataframe(events_df, use_container_width=True)

def show_fiscal_management_page():
    # Aggiungi CSS specifico per questa pagina
    st.markdown("""
    <style>
        /* Force light theme for this page */
        .main .block-container {
            background-color: white !important;
        }
        
        /* Style for buttons in this page */
        .stButton button {
            background-color: #4361ee !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
        }
        
        /* Style for dataframes in this page */
        .dataframe {
            background-color: white !important;
            color: #333333 !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        
        /* Style for tabs in this page */
        .stTabs [data-baseweb="tab"] {
            background-color: white !important;
            color: #333333 !important;
            font-weight: 500 !important;
        }
        
        /* Style for tab content in this page */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: white !important;
            color: #333333 !important;
            padding: 16px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Verifica se l'utente ha un abbonamento attivo
    if not st.session_state.get('subscription_purchased', False):
        st.warning("Per accedere alla gestione utenti è necessario acquistare un piano di abbonamento.")
        # Mostra un messaggio di attesa e poi reindirizza
        with st.spinner("Reindirizzamento alla pagina dei piani di abbonamento..."):
            time.sleep(2)
            st.session_state.current_page = 'subscriptions'
            st.rerun()
        return
    
    st.header("👥 Gestione Utenti")
    
    # Mostra un'animazione di caricamento
    from loading_animations import show_loading_animation
    show_loading_animation("Caricamento gestione utenti...", duration=1)
    
    # Create tabs for different user management functions
    tabs = st.tabs(["Check-in/Check-out", "Gestione Utenti", "Prenotazioni", "Impostazioni"])
    
    with tabs[0]:
        # Importa e mostra la gestione check-in/check-out
        from user_checkin_management import show_checkin_management
        show_checkin_management()
    
    with tabs[1]:
        show_user_management()
    
    with tabs[2]:
        show_invoicing()
    
    with tabs[3]:
        show_fiscal_settings()

def show_user_management():
    """Display and manage users from the database"""
    st.subheader("Gestione Utenti")
    
    # Get users from session state
    users = st.session_state.users
    
    if not users:
        st.info("Non ci sono utenti registrati nel sistema.")
        return
    
    # Create a dataframe for display
    user_data = []
    for i, (email, _) in enumerate(users.items(), 1):
        # Extract username from email
        username = email.split('@')[0] if '@' in email else email
        
        # Generate a fiscal ID (simulated)
        fiscal_id = f"USR{i:04d}"
        
        user_data.append({
            "ID": fiscal_id,
            "Email": email,
            "Username": username,
            "Data Registrazione": "21/05/2025",  # Simulated date
            "Stato": "Attivo"
        })
    
    # Create a dataframe
    user_df = pd.DataFrame(user_data)
    
    # Add search functionality
    search_term = st.text_input("Cerca utente:", placeholder="Inserisci email o username")
    
    if search_term:
        filtered_df = user_df[
            user_df["Email"].str.contains(search_term, case=False) | 
            user_df["Username"].str.contains(search_term, case=False)
        ]
        if filtered_df.empty:
            st.warning(f"Nessun utente trovato per '{search_term}'")
            st.dataframe(user_df, use_container_width=True)
        else:
            st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(user_df, use_container_width=True)
    
    # User details section
    st.subheader("Dettagli Utente")
    
    # Select a user to view details
    selected_user = st.selectbox(
        "Seleziona un utente",
        options=user_df["Email"].tolist(),
        format_func=lambda x: f"{x} ({next((u['Username'] for u in user_data if u['Email'] == x), '')})"
    )
    
    if selected_user:
        selected_user_data = next((u for u in user_data if u["Email"] == selected_user), None)
        
        if selected_user_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**ID Fiscale:** {selected_user_data['ID']}")
                st.markdown(f"**Email:** {selected_user_data['Email']}")
                st.markdown(f"**Username:** {selected_user_data['Username']}")
            
            with col2:
                st.markdown(f"**Data Registrazione:** {selected_user_data['Data Registrazione']}")
                st.markdown(f"**Stato:** {selected_user_data['Stato']}")
                st.markdown(f"**Tipo Account:** {'Standard' if selected_user_data['Email'] != 'admin' else 'Amministratore'}")
            
            # Fiscal actions
            st.subheader("Azioni Fiscali")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Genera Fattura", key=f"gen_invoice_{selected_user_data['ID']}"):
                    st.success(f"Fattura generata per {selected_user_data['Username']}")
            
            with col2:
                if st.button("Esporta Dati Fiscali", key=f"export_{selected_user_data['ID']}"):
                    st.success(f"Dati fiscali esportati per {selected_user_data['Username']}")
            
            with col3:
                if st.button("Invia Promemoria", key=f"remind_{selected_user_data['ID']}"):
                    st.success(f"Promemoria inviato a {selected_user_data['Email']}")

def show_invoicing():
    """Display invoicing functionality"""
    st.subheader("Fatturazione")
    st.info("Questa sezione permetterebbe di gestire la fatturazione per gli utenti.")
    
    # Simulated invoicing data
    if 'invoices' not in st.session_state:
        st.session_state.invoices = [
            {
                "id": "INV001",
                "user_email": next(iter(st.session_state.users.keys()), "esempio@email.com"),
                "amount": 100.0,
                "date": "15/05/2025",
                "status": "Pagata"
            }
        ]
    
    # Display invoices
    invoice_data = []
    for invoice in st.session_state.invoices:
        invoice_data.append({
            "ID": invoice["id"],
            "Utente": invoice["user_email"],
            "Importo": f"€{invoice['amount']:.2f}",
            "Data": invoice["date"],
            "Stato": invoice["status"]
        })
    
    if invoice_data:
        st.dataframe(pd.DataFrame(invoice_data), use_container_width=True)
    else:
        st.info("Nessuna fattura presente nel sistema.")

def show_fiscal_reporting():
    """Display fiscal reporting functionality"""
    st.subheader("Reportistica Fiscale")
    st.info("Questa sezione permetterebbe di generare report fiscali per gli utenti.")
    
    # Simulated reporting options
    report_type = st.selectbox(
        "Tipo di Report",
        ["Fatturazione Mensile", "Riepilogo Annuale", "Dichiarazione IVA", "Report Personalizzato"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Data Inizio")
    
    with col2:
        end_date = st.date_input("Data Fine")
    
    if st.button("Genera Report"):
        # Simula generazione report
        with st.spinner(f"Generazione report {report_type} in corso per il periodo {start_date} - {end_date}..."):
            import time
            time.sleep(1.5)  # Simula elaborazione
            st.success(f"Report {report_type} generato con successo!")
        # TODO: Implement actual report generation functionality
        
        # Simulated chart (placeholder)
        chart_data = pd.DataFrame({
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag'],
            'Fatturato': [1200, 1350, 1800, 2200, 2100]
        })
        
        st.bar_chart(chart_data.set_index('Mese'))

def show_fiscal_settings():
    """Display fiscal settings functionality"""
    st.subheader("Impostazioni Fiscali")
    st.info("Questa sezione permetterebbe di configurare le impostazioni fiscali.")
    
    # Simulated settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Partita IVA", value="IT12345678901")
        st.text_input("Ragione Sociale", value="CiaoHost Srl")
        st.text_input("Indirizzo", value="Via Roma 123, Milano")
    
    with col2:
        st.selectbox("Regime Fiscale", ["Ordinario", "Forfettario", "Semplificato"])
        st.number_input("Aliquota IVA (%)", value=22)
        st.checkbox("Emetti Fattura Elettronica", value=True)
    
    if st.button("Salva Impostazioni"):
        # Simula salvataggio impostazioni
        with st.spinner("Salvataggio impostazioni in corso..."):
            import time
            time.sleep(1)  # Simula un breve ritardo per il salvataggio
            st.success("Impostazioni fiscali salvate con successo!")
        # TODO: Implement actual fiscal settings saving functionality

def show_property_management_page():
    # Aggiungi CSS specifico per questa pagina
    st.markdown("""
    <style>
        /* Force light theme for this page */
        .main .block-container {
            background-color: white !important;
        }
        
        /* Style for buttons in this page */
        .stButton button {
            background-color: #4361ee !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
        }
        
        /* Style for dataframes in this page */
        .dataframe {
            background-color: white !important;
            color: #333333 !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        
        /* Style for tabs in this page */
        .stTabs [data-baseweb="tab"] {
            background-color: white !important;
            color: #333333 !important;
            font-weight: 500 !important;
        }
        
        /* Style for tab content in this page */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: white !important;
            color: #333333 !important;
            padding: 16px !important;
        }
        
        /* Style for inputs in this page */
        .stNumberInput, .stTextInput, .stTextArea, .stSelectbox, .stMultiselect {
            background-color: white !important;
            color: #333333 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Verifica se l'utente ha un abbonamento attivo
    if not st.session_state.get('subscription_purchased', False):
        st.warning("Per accedere alla gestione proprietà è necessario acquistare un piano di abbonamento.")
        # Mostra un messaggio di attesa e poi reindirizza
        with st.spinner("Reindirizzamento alla pagina dei piani di abbonamento..."):
            time.sleep(2)
            st.session_state.current_page = 'subscriptions'
            st.rerun()
        return
    
    # Usa la nuova implementazione della gestione proprietà
    show_property_management()

def show_report_builder_page():
    # Aggiungi CSS specifico per questa pagina
    st.markdown("""
    <style>
        /* Force light theme for this page */
        .main .block-container {
            background-color: white !important;
        }
        
        /* Style for buttons in this page */
        .stButton button {
            background-color: #4361ee !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
        }
        
        /* Style for dataframes in this page */
        .dataframe {
            background-color: white !important;
            color: #333333 !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        
        /* Style for tabs in this page */
        .stTabs [data-baseweb="tab"] {
            background-color: white !important;
            color: #333333 !important;
            font-weight: 500 !important;
        }
        
        /* Style for tab content in this page */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: white !important;
            color: #333333 !important;
            padding: 16px !important;
        }
        
        /* Style for inputs in this page */
        .stNumberInput, .stTextInput, .stTextArea, .stSelectbox, .stMultiselect {
            background-color: white !important;
            color: #333333 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Verifica se l'utente ha un abbonamento attivo
    if not st.session_state.get('subscription_purchased', False):
        st.warning("Per accedere alla creazione report è necessario acquistare un piano di abbonamento.")
        # Mostra un messaggio di attesa e poi reindirizza
        with st.spinner("Reindirizzamento alla pagina dei piani di abbonamento..."):
            time.sleep(2)
            st.session_state.current_page = 'subscriptions'
            st.rerun()
        return
    
    # Importa e chiama la funzione dal modulo report_builder
    from attached_assets.report_builder import show_report_builder
    show_report_builder()

def show_settings_page():
    # Aggiungi CSS specifico per questa pagina
    st.markdown("""
    <style>
        /* Force light theme for this page */
        .main .block-container {
            background-color: white !important;
        }
        
        /* Style for buttons in this page */
        .stButton button {
            background-color: #4361ee !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
        }
        
        /* Style for dataframes in this page */
        .dataframe {
            background-color: white !important;
            color: #333333 !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        
        /* Style for tabs in this page */
        .stTabs [data-baseweb="tab"] {
            background-color: white !important;
            color: #333333 !important;
            font-weight: 500 !important;
        }
        
        /* Style for tab content in this page */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: white !important;
            color: #333333 !important;
            padding: 16px !important;
        }
        
        /* Style for inputs in this page */
        .stNumberInput, .stTextInput, .stTextArea, .stSelectbox, .stMultiselect {
            background-color: white !important;
            color: #333333 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Verifica se l'utente ha un abbonamento attivo
    if not st.session_state.get('subscription_purchased', False):
        st.warning("Per accedere alle impostazioni è necessario acquistare un piano di abbonamento.")
        # Mostra un messaggio di attesa e poi reindirizza
        with st.spinner("Reindirizzamento alla pagina dei piani di abbonamento..."):
            time.sleep(2)
            st.session_state.current_page = 'subscriptions'
            st.rerun()
        return
    
    settings.show_settings()

def show_ai_management_page():
    """Pagina dell'Assistente AI per la gestione immobiliare"""
    
    # CSS per il design professionale del chatbot gestionale
    st.markdown("""
    <style>
    /* Container principale del chatbot gestionale con design luxury */
    .ai-management-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        border-radius: 24px;
        padding: 0;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 25px 50px rgba(30, 58, 138, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    /* Header del chatbot gestionale */
    .ai-management-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        text-align: center;
        position: relative;
        z-index: 2;
    }
    
    .ai-management-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    .ai-management-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    .ai-management-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        margin-top: 1rem;
        font-size: 0.9rem;
        color: white;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Stile per i messaggi chat gestionali */
    .stChatMessage[data-testid*="user"] {
        background: linear-gradient(135deg, #1e40af 0%, #3730a3 100%) !important;
        border-radius: 18px 18px 4px 18px !important;
        margin-left: 20% !important;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3) !important;
    }
    
    .stChatMessage[data-testid*="bot"] {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
        border-radius: 18px 18px 18px 4px !important;
        margin-right: 20% !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }
    
    /* Input chat gestionale migliorato */
    .stChatInput {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95)) !important;
        border-radius: 20px !important;
        border: 2px solid rgba(59, 130, 246, 0.4) !important;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.15), 0 4px 15px rgba(0,0,0,0.1) !important;
        backdrop-filter: blur(20px) !important;
        margin: 20px 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput:hover {
        border-color: rgba(59, 130, 246, 0.6) !important;
        box-shadow: 0 15px 40px rgba(59, 130, 246, 0.2), 0 6px 20px rgba(0,0,0,0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    .stChatInput input {
        background: transparent !important;
        border: none !important;
        font-size: 16px !important;
        color: #1e293b !important;
        padding: 15px 20px !important;
        font-weight: 500 !important;
    }
    
    .stChatInput input::placeholder {
        color: #64748b !important;
        font-style: italic !important;
        font-weight: 400 !important;
    }
    
    /* Pulsante di invio migliorato */
    .stChatInput button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 10px 15px !important;
        margin: 5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stChatInput button:hover {
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .ai-management-container {
            margin: -1rem -0.5rem 1rem -0.5rem;
        }
        
        .ai-management-title {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Verifica se l'utente ha un abbonamento attivo
    if not st.session_state.get('subscription_purchased', False):
        st.warning("Per accedere all'Assistente AI Gestionale è necessario acquistare un piano di abbonamento.")
        with st.spinner("Reindirizzamento alla pagina dei piani di abbonamento..."):
            time.sleep(2)
            st.session_state.current_page = 'subscriptions'
            st.rerun()
        return
    
    # Header principale
    st.markdown("""
    <div class="ai-management-container">
        <div class="ai-management-header">
            <h1 class="ai-management-title">🏢 CiaoHost AI Gestionale</h1>
            <p class="ai-management-subtitle">Assistente AI specializzato per la gestione immobiliare professionale</p>
            <div class="ai-management-badge">🎯 Esperto in Real Estate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Indicatori di stato specializzati
    st.markdown("### 🟢 Status Sistema")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📈 Analisi Mercato")
    with col2:
        st.success("💰 Calcoli ROI")
    with col3:
        st.warning("📋 Contratti & Report")
    
    # Inizializza messaggi gestionali separati
    if 'management_messages' not in st.session_state:
        st.session_state.management_messages = []
    
    # Separatore visivo
    st.markdown("---")
    st.markdown("### 💼 Chat con l'AI Gestionale")
    
    # Area chat con componenti Streamlit nativi
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.management_messages:
            role = message["role"]
            content = message["content"]
            avatar_map = {"user": "👤", "bot": "🏢", "admin": "⚙️"}
            
            with st.chat_message(name=role, avatar=avatar_map.get(role)):
                st.markdown(content)
    
    # Area di input migliorata per AI Gestionale
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.05));
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
        backdrop-filter: blur(10px);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
        ">
            <div style="
                font-size: 24px;
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">🏢</div>
            <div style="
                font-size: 16px;
                font-weight: 600;
                color: #1e293b;
            ">Scrivi la tua richiesta gestionale</div>
        </div>
        <div style="
            font-size: 14px;
            color: #64748b;
            font-style: italic;
        ">💡 Chiedi analisi di mercato, calcoli ROI, contratti, normative e molto altro...</div>
    </div>
    """, unsafe_allow_html=True)
    
    user_input = st.chat_input("✨ Scrivi qui la tua domanda per l'AI Gestionale...", key="management_chat_input")
    if user_input:
        st.session_state.management_messages.append({"role": "user", "content": user_input})
        
        # Controlla se è un comando di prenotazione o se c'è una prenotazione in corso
        booking_response = handle_booking(user_input)
        if booking_response:
            st.session_state.management_messages.append({"role": "bot", "content": booking_response})
        else:
            # Se non è una prenotazione, controlla se è un comando admin
            admin_response = handle_admin_access(user_input)
            if admin_response:
                st.session_state.management_messages.append({"role": "admin", "content": admin_response})
            else:
                # Usa il modello AI con contesto gestionale
                if not (st.session_state.admin_state and st.session_state.admin_state.get('mode') == 'auth'):
                    if model:
                        try:
                            property_summary = "Nessuna proprietà nel database."
                            if st.session_state.properties:
                                prop_count = len(st.session_state.properties)
                                property_summary = f"{prop_count} proprietà nel database:\n"
                                for prop_id, prop in st.session_state.properties.items():
                                    prop_name = prop.get('name', 'N/A')
                                    prop_type = prop.get('type', 'N/A')
                                    prop_location = prop.get('location', 'N/A')
                                    property_summary += f"- ID {prop_id}: {prop_name} ({prop_type}) a {prop_location}\n"
                            
                            conversation_history = []
                            for msg in st.session_state.management_messages[-10:]:
                                gemini_role = "user" if msg["role"] == "user" else "model"
                                conversation_history.append({"role": gemini_role, "parts": [{"text": msg["content"]}]})
                        
                            if conversation_history and conversation_history[-1]["role"] == "user":
                                current_prompt_text = conversation_history.pop()["parts"][0]["text"]
                            else:
                                current_prompt_text = user_input

                            # Usa il contesto gestionale invece di quello immobiliare
                            final_prompt = f"{CONTESTO_GESTIONALE}\n\n{property_summary}\n\n{current_prompt_text}"
                            response = model.generate_content([{"role": "user", "parts": [{"text": final_prompt}]}])
                            bot_reply = response.text
                        except Exception as e:
                            bot_reply = f"🏢 Scusa, ho riscontrato un errore: {str(e)}"
                    else:
                        bot_reply = "🏢 Il modello AI gestionale non è disponibile al momento."
                    
                    st.session_state.management_messages.append({"role": "bot", "content": bot_reply})
        
        st.rerun()

# Funzione per il tema chiaro/scuro
def setup_theme():
    # Imposta sempre il tema chiaro
    st.session_state.theme = 'light'
    
    # CSS per il tema premium ispirato a Booking.com
    light_theme = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --background-color: #f5f7fa;
        --text-color: #1a2b48;
        --card-bg-color: #ffffff;
        --border-color: #e8ecf0;
        --primary-color: #003580;
        --primary-light: #e9f0fa;
        --secondary-color: #0071c2;
        --accent-color: #5392f9;
        --success-color: #008009;
        --info-color: #4cc9f0;
        --warning-color: #feba02;
        --danger-color: #e21a22;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
        --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        line-height: 1.6 !important;
        font-size: 15px !important;
    }
    
    .stApp {
        background-color: var(--background-color) !important;
    }
    
    /* Styling di base */
    .container {
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding: 0 1rem !important;
    }
    
    /* Miglioramenti per i controlli di input */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stTimeInput input, .stTextArea textarea {
        background-color: white !important;
        border-color: var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-color) !important;
        padding: 0.75rem 1rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus, .stTimeInput input:focus, .stTextArea textarea:focus {
        border-color: var(--secondary-color) !important;
        box-shadow: 0 0 0 2px rgba(0, 113, 194, 0.2) !important;
    }
    
    /* Miglioramenti per i pulsanti */
    .stButton button {
        background-color: var(--secondary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton button:hover {
        background-color: #005ea6 !important;
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Miglioramenti per i selettori */
    .stSelectbox, .stMultiselect {
        background-color: white !important;
        color: var(--text-color) !important;
    }
    
    .stSelectbox > div > div, .stMultiselect > div > div {
        background-color: white !important;
        border-color: var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stSelectbox > div > div:hover, .stMultiselect > div > div:hover {
        border-color: var(--secondary-color) !important;
    }
    
    /* Miglioramenti per sliders */
    .stSlider > div > div > div {
        background-color: var(--secondary-color) !important;
    }
    
    /* Miglioramenti per i testi */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }
    
    h1 {
        font-size: 2.2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        margin-bottom: 1.2rem !important;
    }
    
    h3 {
        font-size: 1.4rem !important;
        margin-bottom: 1rem !important;
    }
    
    p, span, div, label {
        color: var(--text-color) !important;
    }
    
    /* Card styling */
    .card {
        background-color: white !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-sm) !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .card:hover {
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-3px) !important;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block !important;
        padding: 0.25rem 0.75rem !important;
        border-radius: 50px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    
    .badge-primary {
        background-color: var(--primary-light) !important;
        color: var(--primary-color) !important;
    }
    
    .badge-success {
        background-color: rgba(0, 128, 9, 0.1) !important;
        color: var(--success-color) !important;
    }
    
    .badge-warning {
        background-color: rgba(254, 186, 2, 0.1) !important;
        color: var(--warning-color) !important;
    }
    
    /* Property card enhancements */
    .property-card {
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.3s ease !important;
    }
    
    .property-card:hover {
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-3px) !important;
    }
    
    .property-image {
        border-radius: var(--radius-md) var(--radius-md) 0 0 !important;
        overflow: hidden !important;
    }
    
    .property-details {
        padding: 1.25rem !important;
    }
    
    .property-price {
        font-weight: 700 !important;
        color: var(--primary-color) !important;
        font-size: 1.25rem !important;
    }
    
    .property-features {
        display: flex !important;
        gap: 0.75rem !important;
        margin-top: 0.75rem !important;
    }
    
    .property-feature {
        font-size: 0.9rem !important;
        color: #6b7280 !important;
    }
    
    /* Eccezioni per elementi con colori specifici */
    .primary-text {
        color: var(--primary-color) !important;
    }
    
    .secondary-text {
        color: var(--secondary-color) !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    /* Search bar enhancements */
    .search-bar {
        background-color: white !important;
        padding: 1.5rem !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--shadow-md) !important;
        margin-bottom: 2rem !important;
    }
    
    /* Rating badge */
    .rating-badge {
        background-color: var(--primary-color) !important;
        color: white !important;
        padding: 0.4rem 0.6rem !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    /* Deal badge */
    .deal-badge {
        background-color: var(--success-color) !important;
        color: white !important;
        padding: 0.35em 0.7em !important;
        border-radius: 50px !important;
        font-weight: 500 !important;
        font-size: 0.85em !important;
        display: inline-block !important;
    }
    
    .secondary-text {
        color: var(--secondary-color) !important;
    }
    
    /* Stile per l'header */
    .main-header {
        background-color: white !important;
        border-bottom: 1px solid #dee2e6 !important;
    }
    """
    
    # Aggiungiamo stili per i link
    st.markdown("""
    <style>
    /* Stile per i link */
    a {
        color: var(--primary-color) !important;
    }
    
    a:hover {
        color: #2a4bdb !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Stili per i tabs
    st.markdown("""
    <style>
    /* Stile per i tab */
    button[role="tab"] {
        background-color: #f8f9fa !important;
        color: #212529 !important;
    }
    
    button[role="tab"][aria-selected="true"] {
        background-color: white !important;
        color: var(--primary-color) !important;
        border-bottom: 2px solid var(--primary-color) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    dark_theme = """
    :root {
        --background-color: #1a1a1a;
        --text-color: #ffffff;
        --card-bg-color: #2d2d2d;
        --border-color: #444444;
        --primary-color: #6c8eff;
        --secondary-color: #d0d0d0;
        --success-color: #4caf50;
        --info-color: #64b5f6;
        --warning-color: #ffb74d;
        --danger-color: #f44336;
    }
    
    body {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    .stApp {
        background-color: var(--background-color) !important;
    }
    
    /* Miglioramenti per i controlli di input */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stTimeInput input, .stTextArea textarea {
        background-color: #333333 !important;
        border-color: var(--border-color) !important;
        color: white !important;
    }
    
    /* Miglioramenti per i pulsanti */
    .stButton button {
        background-color: #3a3a3a !important;
        color: white !important;
        border: 1px solid #555555 !important;
    }
    
    .stButton button:hover {
        background-color: #4a4a4a !important;
        border-color: var(--primary-color) !important;
    }
    
    /* Miglioramenti per i selettori */
    .stSelectbox, .stMultiselect {
        background-color: #333333 !important;
        color: white !important;
    }
    
    /* Miglioramenti per i testi */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    p, span, div, label {
        color: #e0e0e0 !important;
    }
    
    /* Eccezioni per elementi con colori specifici */
    .primary-text {
        color: var(--primary-color) !important;
    }
    
    .secondary-text {
        color: var(--secondary-color) !important;
    }
    
    /* Stile specifico per la sidebar */
    .stSidebar, [data-testid="stSidebar"], [data-testid="stSidebarNav"], .css-1d391kg, .css-1lcbmhc {
        background-color: #ffffff !important;
        border-right: 1px solid #dee2e6 !important;
    }
    
    /* Forza tutti gli elementi della sidebar ad avere sfondo bianco e testo scuro */
    .stSidebar *, [data-testid="stSidebar"] *, [data-testid="stSidebarNav"] * {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Stile per l'header */
    .main-header {
        background-color: #ffffff !important;
        border-bottom: 1px solid #dee2e6 !important;
    }
    
    /* Stile per le card e i container */
    div[data-testid="stVerticalBlock"] > div {
        background-color: var(--card-bg-color) !important;
    }
    
    /* Stile per i link */
    a {
        color: var(--primary-color) !important;
    }
    
    a:hover {
        color: #8ca8ff !important;
    }
    
    /* Stile per i dataframe */
    .stDataFrame {
        background-color: #333333 !important;
    }
    
    /* Stile per i tab */
    button[role="tab"] {
        background-color: #333333 !important;
        color: #e0e0e0 !important;
    }
    
    button[role="tab"][aria-selected="true"] {
        background-color: #4a4a4a !important;
        color: white !important;
        border-bottom: 2px solid var(--primary-color) !important;
    }
    """
    
    # Applica il tema corrente
    if st.session_state.theme == 'light':
        st.markdown(f"<style>{light_theme}</style>", unsafe_allow_html=True)
    else:
        st.markdown(f"<style>{dark_theme}</style>", unsafe_allow_html=True)

def main():
    # Configurazione della pagina
    st.set_page_config(
        page_title="CiaoHost AI Manager",
        page_icon="🏡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Assicuriamoci che il database sia caricato all'avvio
    load_database()
    
    # Assicuriamoci che lo stato di autenticazione sia impostato correttamente
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False
    
    # Aggiungiamo JavaScript per scorrere all'inizio della pagina ad ogni cambio di schermata
    # e nascondiamo qualsiasi CSS visibile nella pagina
    st.markdown("""
    <script>
        // Funzione per scorrere all'inizio della pagina
        function scrollToTop() {
            window.scrollTo(0, 0);
        }
        
        // Esegui la funzione quando la pagina è caricata
        window.addEventListener('load', scrollToTop);
        
        // Osserva i cambiamenti nel DOM per rilevare i cambi di pagina
        const observer = new MutationObserver(scrollToTop);
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)
    
    # Aggiungiamo uno stile per nascondere qualsiasi CSS visibile
    st.markdown("""
    <style>
    /* Nascondiamo qualsiasi testo che assomiglia a CSS */
    .stMarkdown p:contains(".card-icon {") {
        display: none !important;
    }
    .stMarkdown p:contains(".card-title {") {
        display: none !important;
    }
    .stMarkdown p:contains(".card-text {") {
        display: none !important;
    }
    .stMarkdown p:contains(".highlight-blue {") {
        display: none !important;
    }
    .stMarkdown p:contains(".feature-list {") {
        display: none !important;
    }
    .stMarkdown p:contains(".feature-item {") {
        display: none !important;
    }
    .stMarkdown p:contains(".feature-item:before {") {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Applica tutte le animazioni
    from animations import add_all_animations
    add_all_animations()
    
    # Forza il tema chiaro con CSS aggiuntivo e migliora la GUI
    st.markdown("""
    <style>
        /* Base theme - Modern and Clean */
        html, body, [class*="css"], [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"],
        [data-testid="stSidebarNav"], [data-testid="stSidebarUserContent"], .stApp, .stTabs, .stTabContent {
            background-color: #f8fafc !important;
            color: #334155 !important;
            font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }
        
        /* Modern text styling with improved readability */
        p, span, div, label, a, li, ul, ol, td {
            color: #475569 !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }
        
        /* Heading hierarchy with modern styling */
        h1 {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            margin-bottom: 1.5rem !important;
            color: #1e293b !important;
            letter-spacing: -0.5px !important;
            line-height: 1.2 !important;
        }
        
        h2 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            margin-bottom: 1.2rem !important;
            color: #1e293b !important;
            line-height: 1.3 !important;
        }
        
        h3 {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
            color: #1e293b !important;
            line-height: 1.4 !important;
        }
        
        /* Enhanced sidebar with modern gradient */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%) !important;
            border-right: 1px solid rgba(0,0,0,0.05) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
            padding: 1.5rem 1rem !important;
        }
        
        /* Modern sidebar buttons with hover effects */
        [data-testid="stSidebar"] button {
            background-color: white !important;
            color: #3b82f6 !important;
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03) !important;
            transition: all 0.3s ease !important;
            margin-bottom: 10px !important;
            font-weight: 500 !important;
            padding: 12px 16px !important;
            width: 100% !important;
            text-align: left !important;
        }
        
        [data-testid="stSidebar"] button:hover {
            background-color: #eff6ff !important;
            border-color: #3b82f6 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(59, 130, 246, 0.1) !important;
        }
        
        /* Active sidebar button */
        [data-testid="stSidebar"] button:active, [data-testid="stSidebar"] button:focus {
            background-color: #dbeafe !important;
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
        }
        
        /* Modern table styling with subtle shadows */
        table, [data-testid="stTable"], [data-testid="stDataFrame"], div[data-testid="stDataFrameContainer"] {
            background-color: white !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.04) !important;
            border: none !important;
            margin: 1.5rem 0 !important;
        }
        
        /* Enhanced dataframe styling */
        .dataframe {
            width: 100% !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            font-family: 'Poppins', 'Segoe UI', sans-serif !important;
        }
        
        /* Modern header styling with gradient */
        .dataframe th {
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 14px 18px !important;
            text-align: left !important;
            border: none !important;
            font-size: 14px !important;
            letter-spacing: 0.5px !important;
        }
        
        /* Table row styling with alternating colors */
        .dataframe tr:nth-child(even) {
            background-color: #f8fafc !important;
        }
        
        .dataframe tr:hover {
            background-color: #eff6ff !important;
            transition: background-color 0.2s ease !important;
        }
        
        /* Table cell styling */
        .dataframe td {
            padding: 12px 16px !important;
            border-top: 1px solid #e2e8f0 !important;
            font-size: 14px !important;
        }
        
        /* Modern input fields */
        input[type="text"], input[type="number"], input[type="password"], input[type="email"], input[type="date"], textarea, select, .stTextInput > div > div > input, .stNumberInput > div > div > input {
            background-color: white !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 1rem !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        }
        
        input[type="text"]:focus, input[type="number"]:focus, input[type="password"]:focus, input[type="email"]:focus, input[type="date"]:focus, textarea:focus, select:focus, .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
            outline: none !important;
        }
        
        /* Modern buttons */
        .stButton > button {
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
            letter-spacing: 0.3px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(59, 130, 246, 0.3) !important;
            filter: brightness(1.05) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* Card styling for property listings */
        .card-container {
            background-color: white !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.04) !important;
            padding: 20px !important;
            transition: all 0.3s ease !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            border: 1px solid #f1f5f9 !important;
        }
        
        .card-container:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 12px 24px rgba(0,0,0,0.06) !important;
            border-color: #e2e8f0 !important;
        }
        
        /* Modern select boxes */
        .stSelectbox > div > div {
            background-color: white !important;
            border-radius: 8px !important;
        }
        
        /* Slider styling */
        .stSlider > div > div > div {
            background-color: #e2e8f0 !important;
        }
        
        .stSlider > div > div > div > div {
            background-color: #3b82f6 !important;
        }
        
        /* Checkbox styling */
        .stCheckbox > div > div > label > div {
            background-color: white !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 4px !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: white !important;
            border-radius: 8px !important;
            border: 1px solid #f1f5f9 !important;
            padding: 10px 15px !important;
            font-weight: 500 !important;
        }
        
        .streamlit-expanderContent {
            background-color: white !important;
            border-radius: 0 0 8px 8px !important;
            border: 1px solid #f1f5f9 !important;
            border-top: none !important;
            padding: 15px !important;
        }
        
        .dataframe tr:hover td {
            background-color: #f0f4ff !important;
        }
        
        /* Modern tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            background-color: white !important;
            border-radius: 10px !important;
            padding: 5px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03) !important;
            display: flex !important;
            justify-content: center !important;
            margin-bottom: 20px !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: white !important;
            color: #4361ee !important;
            border-radius: 8px !important;
            margin: 0 5px !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            border: 1px solid rgba(67, 97, 238, 0.1) !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #f0f4ff !important;
            transform: translateY(-2px) !important;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%) !important;
            color: white !important;
            box-shadow: 0 4px 10px rgba(67, 97, 238, 0.2) !important;
            border: none !important;
        }
        
        .stTabs [data-baseweb="tab-highlight"] {
            display: none !important;
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            padding: 20px 0 !important;
        }
        
        /* Modern card styling */
        .stCard, [data-testid="stExpander"] {
            background-color: white !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
            padding: 20px !important;
            border: none !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        }
        
        .stCard:hover, [data-testid="stExpander"]:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1) !important;
        }
        
        /* Modern input styling */
        input, textarea, [data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"], 
        .stNumberInput, .stTextInput, .stTextArea, .stSelectbox, .stMultiselect {
            background-color: white !important;
            color: #333333 !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
            transition: all 0.3s ease !important;
        }
        
        input:focus, textarea:focus, [data-baseweb="input"]:focus, [data-baseweb="textarea"]:focus, [data-baseweb="select"]:focus {
            border-color: #4361ee !important;
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2) !important;
            outline: none !important;
        }
        
        /* Modern alert styling */
        .stAlert {
            background-color: white !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            padding: 15px 20px !important;
            margin: 15px 0 !important;
            border-left: 5px solid #4361ee !important;
        }
        
        /* Success alert */
        .stAlert[data-baseweb="notification"][kind="success"] {
            border-left-color: #10B981 !important;
        }
        
        /* Warning alert */
        .stAlert[data-baseweb="notification"][kind="warning"] {
            border-left-color: #F59E0B !important;
        }
        
        /* Error alert */
        .stAlert[data-baseweb="notification"][kind="error"] {
            border-left-color: #EF4444 !important;
        }
        
        /* Modern metric styling */
        [data-testid="stMetric"] {
            background-color: white !important;
            padding: 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            transition: transform 0.3s ease !important;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px) !important;
        }
        
        [data-testid="stMetric"] label {
            color: #4361ee !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
        }
        
        [data-testid="stMetric"] div[data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            color: #2d3748 !important;
        }
        
        /* Modern plot styling */
        .stPlot, [data-testid="stPlotContainer"], .js-plotly-plot, .plotly, .plot-container {
            background-color: white !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            padding: 10px !important;
        }
        
        /* Modern widget styling */
        .stSlider, .stSelectbox, .stMultiselect, .stDateInput, .stTimeInput, .stNumberInput, .stTextInput, .stTextArea {
            background-color: white !important;
            color: #333333 !important;
            margin-bottom: 20px !important;
        }
        
        /* Modern slider styling */
        .stSlider [data-baseweb="slider"] {
            height: 6px !important;
            background-color: #e2e8f0 !important;
        }
        
        .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
            background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%) !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3) !important;
        }
        
        /* Modern expander styling */
        .streamlit-expanderHeader, .streamlit-expanderContent {
            background-color: white !important;
            color: #333333 !important;
            border-radius: 10px !important;
        }
        
        .streamlit-expanderHeader {
            border: 1px solid #e2e8f0 !important;
            padding: 15px 20px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #f0f4ff !important;
            border-color: #4361ee !important;
        }
        
        /* Modern radio and checkbox styling */
        .stRadio, .stCheckbox {
            background-color: white !important;
            color: #333333 !important;
            padding: 10px !important;
            border-radius: 10px !important;
        }
        
        .stRadio label, .stCheckbox label {
            font-weight: 500 !important;
        }
        
        /* Modern download button styling */
        .stDownloadButton button {
            background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 10px rgba(67, 97, 238, 0.2) !important;
        }
        
        .stDownloadButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(67, 97, 238, 0.3) !important;
        }
        
        /* Modern file uploader styling */
        .stFileUploader {
            background-color: white !important;
            color: #333333 !important;
            border: 2px dashed #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 20px !important;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader:hover {
            border-color: #4361ee !important;
            background-color: #f0f4ff !important;
        }
        
        /* Modern progress bar styling */
        .stProgress > div {
            background-color: #e2e8f0 !important;
            height: 8px !important;
            border-radius: 4px !important;
        }
        
        .stProgress > div > div {
            background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%) !important;
            border-radius: 4px !important;
        }
        
        /* Modern main navigation bar styling */
        .main-header {
            background: white !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
            border-radius: 12px !important;
            margin-bottom: 20px !important;
            padding: 15px 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }
        
        /* Main navigation buttons */
        .nav-buttons .stButton button {
            background-color: white !important;
            color: #4361ee !important;
            border: 1px solid rgba(67, 97, 238, 0.2) !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
            margin: 0 5px !important;
        }
        
        .nav-buttons .stButton button:hover {
            background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%) !important;
            color: white !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 10px rgba(67, 97, 238, 0.2) !important;
            border-color: transparent !important;
        }
        
        /* Active navigation button */
        .nav-buttons .stButton button.active {
            background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%) !important;
            color: white !important;
            border-color: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Imposta il tema
    setup_theme()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    
    if 'data' not in st.session_state:
        data = {
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
            'Guadagno': [1200, 1350, 1800, 2200, 2100, 2400],
            'Occupazione': [75, 82, 88, 95, 93, 98],
            'Prenotazioni': [10, 12, 15, 18, 17, 20]
        }
        st.session_state.data = pd.DataFrame(data)
    
    # Carica il database
    # Inizializza le variabili di sessione se non esistono
    
    load_database()
    
    st.markdown("""
    <style>
        /* Force Light Theme */
        html, body, [class*="css"] {
            color: #333 !important;
            background-color: #ffffff !important;
        }
        
        /* Base Styles */
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333 !important;
            background-color: #f8f9fa !important;
        }
        
        /* Force sidebar to be light */
        .css-1d391kg, .css-1lcbmhc, .css-12oz5g7, .css-zt5igj, .css-1oe6wy4, .css-1aehpvj, .css-18e3th9 {
            background-color: #ffffff !important;
            color: #333333 !important;
        }
        
        /* Force all text to be visible */
        p, h1, h2, h3, h4, h5, h6, span, div, label, .stMarkdown, .stText {
            color: #333333 !important;
        }
        
        /* Modern Color Scheme */
        :root {
            --primary-color: #4361ee;
            --primary-hover: #3a56d4;
            --secondary-color: #3f37c9;
            --accent-color: #4cc9f0;
            --success-color: #4CAF50;
            --warning-color: #ff9800;
            --danger-color: #f44336;
            --light-bg: #f8f9fa;
            --dark-bg: #212529;
            --border-color: #dee2e6;
        }
        
        /* Improved Chat Container */
        .stChatInputContainer {
            position: fixed;
            bottom: 0rem;
            left: 0;
            right: 0;
            padding: 0.75rem 1.5rem;
            background-color: white;
            border-top: 1px solid var(--border-color);
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
            z-index: 999;
            width: 100%;
            box-sizing: border-box;
        }
        
        /* Chat Message Styling */
        .stChatMessage {
            background-color: white !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
            padding: 12px !important;
            margin-bottom: 12px !important;
        }
        
        /* Main Container Padding */
        .main .block-container { 
            padding-bottom: 6rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Enhanced Header */
        .main-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        /* Navigation Buttons Grid */
        .nav-buttons {
            display: grid !important;
            grid-template-columns: repeat(6, minmax(90px, 1fr)) !important;
            grid-gap: 8px !important;
            width: 100% !important;
            margin-left: auto !important;
        }
        
        /* Navigation Button Container */
        .nav-buttons > div {
            display: contents !important;
        }
        
        /* Navigation Button Column */
        .nav-buttons > div > div {
            margin: 0 !important;
            padding: 0 !important;
            height: auto !important;
        }
        
        /* Button Container */
        .nav-buttons .stButton {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Button Styling */
        .nav-buttons .stButton button {
            width: 100% !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            padding: 0 12px !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background-color: #4361ee !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        }
        
        /* Button Hover Effect */
        .nav-buttons .stButton button:hover {
            background-color: #3a56d4 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Logout Button */
        .nav-buttons .stButton button.logout-btn,
        button[key*="logout"] {
            background-color: var(--danger-color) !important;
        }
        
        /* Logout Button Hover */
        .nav-buttons .stButton button.logout-btn:hover,
        button[key*="logout"]:hover {
            background-color: #d32f2f !important;
        }
        
        /* Sidebar Styling */
        .css-1d391kg, .css-163ttbj, .css-1wrcr25 {
            background-color: white !important;
            border-right: 1px solid var(--border-color) !important;
        }
        
        /* Sidebar Button Styling */
        .sidebar .stButton button, [data-testid="stSidebar"] .stButton button {
            background-color: #f8f9fa !important;
            color: #333333 !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 10px !important;
            text-align: left !important;
            padding: 14px 18px !important;
            margin-bottom: 8px !important;
            transition: all 0.2s ease !important;
            display: flex !important;
            align-items: center !important;
            font-weight: 500 !important;
            font-size: 1.05rem !important;
            min-height: 54px !important;
        }
        
        /* Sidebar Button Hover */
        .sidebar .stButton button:hover, [data-testid="stSidebar"] .stButton button:hover {
            background-color: #e9ecef !important;
            border-color: #4361ee !important;
            color: #4361ee !important;
        }
        
        /* Card Container Styling */
        .card-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid var(--border-color);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .card-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        /* Metric Card Styling */
        .metric-card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            padding: 15px;
            text-align: center;
            border: 1px solid var(--border-color);
        }
        
        /* Data Table Styling */
        .stDataFrame {
            border-radius: 10px !important;
            overflow: hidden !important;
            border: 1px solid var(--border-color) !important;
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background-color: white !important;
            border-radius: 8px !important;
            border: 1px solid var(--border-color) !important;
            padding: 10px 15px !important;
            margin-bottom: 5px !important;
        }
        
        /* Expander Content */
        .streamlit-expanderContent {
            background-color: white !important;
            border-radius: 0 0 8px 8px !important;
            border: 1px solid var(--border-color) !important;
            border-top: none !important;
            padding: 15px !important;
        }
        
        /* Input Field Styling */
        .stTextInput input, .stNumberInput input, .stSelectbox, .stMultiselect {
            border-radius: 8px !important;
            border: 1px solid var(--border-color) !important;
            padding: 10px 15px !important;
        }
        
        /* Input Field Focus */
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2) !important;
        }
        
        /* Header Styling */
        h1, h2, h3, h4, h5, h6 {
            color: #212529 !important;
            font-weight: 600 !important;
        }
        
        /* Ensure the header maintains its layout with sidebar open */
        .main-header {
            width: 100% !important;
            max-width: 100% !important;
            padding: 0.75rem 1.5rem !important;
            box-sizing: border-box !important;
            display: flex !important;
            flex-wrap: wrap !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    header_cols = st.columns([2, 3, 3])
    with header_cols[0]:
        # Logo più semplice nell'header (nascosto nella pagina di login)
        if st.session_state.get('current_page') != 'login':
            show_company_logo(size="small", with_text=True)
    
    with header_cols[1]:
        # Spazio vuoto
        st.markdown('<div class="title-container"></div>', unsafe_allow_html=True)

    with header_cols[2]:
        # Rimossi i pulsanti di navigazione in alto a destra
        st.markdown('<div class="nav-buttons-placeholder"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar Navigation
    if st.session_state.get('is_authenticated', False):
        with st.sidebar:
            # CSS per la sidebar moderna
            st.markdown("""
            <style>
                /* Modern sidebar styling */
                [data-testid="stSidebar"] {
                    background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
                    border-right: 1px solid rgba(0,0,0,0.05) !important;
                    box-shadow: 2px 0px 10px rgba(0,0,0,0.03) !important;
                    width: 320px !important;
                    max-width: 320px !important;
                }
                
                /* Ensure sidebar elements get the full width */
                section[data-testid="stSidebar"] > div {
                    width: 320px !important;
                    max-width: 320px !important;
                }
                
                /* Sidebar content container */
                [data-testid="stSidebar"] > div:first-child {
                    padding: 2rem 1.75rem !important;
                }
                
                /* Migliora lo spazio nei componenti della sidebar */
                [data-testid="stSidebar"] .stButton {
                    margin-bottom: 0.85rem !important;
                }
                
                /* Aggiungi più spazio per gli elementi testuali */
                [data-testid="stSidebar"] p, [data-testid="stSidebar"] div {
                    font-size: 1.05rem !important;
                }
                
                /* Sidebar header */
                .sidebar-header {
                    text-align: center;
                    margin-bottom: 2rem;
                    padding-bottom: 1.5rem;
                    border-bottom: 1px solid rgba(0,0,0,0.05);
                }
                
                /* Logo container */
                .logo-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin-bottom: 1rem;
                }
                
                /* App title */
                .app-title {
                    color: #4361ee !important;
                    font-size: 1.8rem !important;
                    font-weight: 700 !important;
                    margin-top: 0.5rem !important;
                    letter-spacing: -0.5px !important;
                    background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%) !important;
                    -webkit-background-clip: text !important;
                    -webkit-text-fill-color: transparent !important;
                }
                
                /* Navigation section */
                .nav-section {
                    margin-bottom: 1.5rem;
                }
                
                /* Section title */
                .section-title {
                    color: #2d3748 !important;
                    font-size: 1.2rem !important;
                    font-weight: 600 !important;
                    margin-bottom: 1rem !important;
                    padding-left: 0.5rem !important;
                    border-left: 3px solid #4361ee !important;
                }
                
                /* Navigation buttons */
                [data-testid="stSidebar"] button {
                    background-color: white !important;
                    color: #4361ee !important;
                    border: 1px solid rgba(67, 97, 238, 0.2) !important;
                    border-radius: 8px !important;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
                    transition: all 0.3s ease !important;
                    margin-bottom: 8px !important;
                    font-weight: 500 !important;
                    padding: 10px 15px !important;
                    text-align: left !important;
                    display: flex !important;
                    align-items: center !important;
                }
                
                [data-testid="stSidebar"] button:hover {
                    background-color: #f0f4ff !important;
                    border-color: #4361ee !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 4px 8px rgba(67, 97, 238, 0.1) !important;
                }
                
                /* Divider */
                .sidebar-divider {
                    height: 1px;
                    background: linear-gradient(90deg, rgba(0,0,0,0.03) 0%, rgba(0,0,0,0.06) 50%, rgba(0,0,0,0.03) 100%);
                    margin: 1.5rem 0;
                    border: none;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Header della sidebar
            st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            
            # Logo
            show_company_logo(size="small", with_text=False)
            st.markdown('<h1 class="app-title">CiaoHost</h1>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sottotitolo
            st.markdown('<p style="text-align: center; color: #718096; margin-top: -0.5rem;">Gestione Proprietà Intelligente</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sezione Funzionalità Base
            st.markdown('<div class="nav-section">', unsafe_allow_html=True)
            st.markdown('<h3 class="section-title">Funzionalità Base</h3>', unsafe_allow_html=True)
            
            # Determina quale pagina è attiva
            is_home_active = st.session_state.current_page == 'home'
            is_ai_active = st.session_state.current_page == 'ai'
            is_search_active = st.session_state.current_page == 'search_properties'
            is_subscriptions_active = st.session_state.current_page == 'subscriptions'
            
            # Pulsanti con indicatore di attivo
            if st.button("🏠 Home Principale", key="sidebar_home", 
                        help="Torna alla pagina principale", use_container_width=True):
                st.session_state.current_page = 'home'
                st.rerun()
                
            if st.button("🤖 Assistente AI", key="sidebar_ai", 
                        help="Accedi all'assistente AI", use_container_width=True):
                st.session_state.current_page = 'ai'
                st.rerun()
                
            if st.button("🔍 Ricerca Immobili", key="sidebar_search", 
                        help="Cerca tra le proprietà disponibili", use_container_width=True):
                st.session_state.current_page = 'search_properties'
                st.rerun()
                
            if st.button("💼 Piani Abbonamento", key="sidebar_subscriptions", 
                        help="Visualizza i piani di abbonamento disponibili", use_container_width=True):
                st.session_state.current_page = 'subscriptions'
                st.rerun()
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sezione visibile solo con abbonamento attivo
            if st.session_state.get('subscription_purchased', False):
                # Aggiungi un divisore
                st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
                
                # Sezione Funzionalità Premium
                st.markdown('<div class="nav-section">', unsafe_allow_html=True)
                st.markdown('<h3 class="section-title">Funzionalità Premium</h3>', unsafe_allow_html=True)
                
                # Determina se dashboard è attiva
                is_dashboard_active = st.session_state.current_page == 'dashboard'
                
                # Dashboard (spostata qui perché richiede abbonamento)
                if st.button("📊 Dashboard Dati", key="sidebar_dashboard", 
                            help="Visualizza la dashboard con i dati delle tue proprietà", use_container_width=True):
                    # Assicuriamoci che l'abbonamento sia attivo
                    if 'subscription_purchased' not in st.session_state:
                        st.session_state.subscription_purchased = True
                    
                    st.session_state.current_page = 'dashboard'
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Aggiungi un divisore
                st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
                
                # Sezione Strumenti Gestionali
                st.markdown('<div class="nav-section">', unsafe_allow_html=True)
                st.markdown('<h3 class="section-title">Strumenti Gestionali</h3>', unsafe_allow_html=True)
                
                # Determina quali strumenti sono attivi
                is_cleaning_active = st.session_state.current_page == 'cleaning_management'
                is_pricing_active = st.session_state.current_page == 'dynamic_pricing'
                is_fiscal_active = st.session_state.current_page == 'fiscal_management'
                is_property_active = st.session_state.current_page == 'property_management'
                is_report_active = st.session_state.current_page == 'report_builder'
                is_settings_active = st.session_state.current_page == 'settings'
                is_ai_management_active = st.session_state.current_page == 'ai_management'
                
                # Pulsanti con indicatore di attivo
                if st.button("🤖 Assistente AI Gestionale", key="sidebar_ai_management", 
                            help="Assistente AI specializzato per la gestione immobiliare", use_container_width=True):
                    st.session_state.current_page = 'ai_management'
                    st.rerun()
                    
                if st.button("🧹 Gestione Pulizie", key="sidebar_cleaning", 
                            help="Gestisci le pulizie delle tue proprietà", use_container_width=True):
                    st.session_state.current_page = 'cleaning_management'
                    st.rerun()
                    
                if st.button("⚖️ Prezzi Dinamici", key="sidebar_dynamic_pricing", 
                            help="Imposta prezzi dinamici per le tue proprietà", use_container_width=True):
                    st.session_state.current_page = 'dynamic_pricing'
                    st.rerun()
                    
                if st.button("👥 Gestione Utenti", key="sidebar_fiscal_management", 
                            help="Gestisci utenti, check-in e check-out delle prenotazioni", use_container_width=True):
                    st.session_state.current_page = 'fiscal_management'
                    st.rerun()
                    
                if st.button("🏘️ Gestione Proprietà", key="sidebar_property_management", 
                            help="Gestisci le tue proprietà", use_container_width=True):
                    st.session_state.current_page = 'property_management'
                    st.rerun()
                    
                if st.button("📄 Creazione Report", key="sidebar_report_builder", 
                            help="Crea report personalizzati", use_container_width=True):
                    st.session_state.current_page = 'report_builder'
                    st.rerun()
                    
                if st.button("⚙️ Impostazioni", key="sidebar_settings", 
                            help="Configura le impostazioni dell'applicazione", use_container_width=True):
                    st.session_state.current_page = 'settings'
                    st.rerun()
                    
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Messaggio per utenti senza abbonamento
                st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f6f9ff 0%, #f0f4ff 100%); 
                            padding: 15px; 
                            border-radius: 10px; 
                            border-left: 4px solid #4361ee;
                            margin: 10px 0;">
                    <p style="margin: 0; color: #333333; font-weight: 500;">
                        👑 <span style="font-weight: 600;">Sblocca funzionalità premium</span><br>
                        Acquista un piano di abbonamento per accedere a tutti gli strumenti gestionali avanzati.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # Aggiungi un divisore
            st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
            
            # Sezione Account
            st.markdown('<div class="nav-section">', unsafe_allow_html=True)
            
            # Box utente con sfondo verde
            user_email = st.session_state.get('current_user_email', 'Utente')
            user_name = user_email.split('@')[0].capitalize()
            
            # Seleziona un'immagine di profilo casuale professionale
            profile_images = [
                "https://randomuser.me/api/portraits/men/32.jpg",
                "https://randomuser.me/api/portraits/women/44.jpg",
                "https://randomuser.me/api/portraits/men/22.jpg",
                "https://randomuser.me/api/portraits/women/68.jpg",
                "https://randomuser.me/api/portraits/men/75.jpg"
            ]
            
            # Usa l'email come seed per selezionare un'immagine in modo coerente per lo stesso utente
            import hashlib
            seed = int(hashlib.md5(user_email.encode()).hexdigest(), 16) % len(profile_images)
            profile_img = profile_images[seed]
            
            # Creiamo un box utente con layout a colonne
            cols = st.columns([1, 4])
            
            # Colonna immagine con bordo circolare
            with cols[0]:
                st.markdown(f"""
                <div style="
                    width: 60px; 
                    height: 60px; 
                    border-radius: 50%; 
                    overflow: hidden; 
                    border: 3px solid #4361ee;
                    box-shadow: 0 0 10px rgba(67, 97, 238, 0.3);
                    margin-right: 12px;
                ">
                    <img src="{profile_img}" 
                         style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                """, unsafe_allow_html=True)
            
            # Colonna informazioni utente
            with cols[1]:
                st.markdown(f"""
                <div style="padding-left: 15px; margin-top: 6px;">
                    <div style="font-weight: bold; font-size: 16px;">{user_name}</div>
                    <div style="color: #0d9488; display: flex; align-items: center; margin-top: 4px;">
                        <span style="color: #10b981; font-size: 16px; margin-right: 5px;">●</span> 
                        Utente attivo
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Pulsante di logout
            if st.button("🚪 Logout", key="sidebar_logout", 
                        help="Esci dall'applicazione", use_container_width=True):
                st.session_state.is_authenticated = False
                st.session_state.current_page = 'login'
                st.session_state.messages = []
                st.session_state.admin_state = {'mode': None, 'step': None}
                st.session_state.subscription_purchased = False
                st.session_state.current_user_email = None
                st.rerun()
                
            st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.get('is_authenticated', False):
        show_login()
    else:
        # Page rendering logic based on st.session_state.current_page
        if st.session_state.current_page == 'home':
            # Hero section moderna con effetto gradiente e animazione
            st.markdown("""
                <style>
                    @keyframes gradientAnimation {
                        0% {background-position: 0% 50%;}
                        50% {background-position: 100% 50%;}
                        100% {background-position: 0% 50%;}
                    }
                    
                    .hero-section {
                        background: linear-gradient(-45deg, #4361ee, #3a56d4, #4895ef, #4cc9f0);
                        background-size: 400% 400%;
                        animation: gradientAnimation 15s ease infinite;
                        padding: 4rem 2rem;
                        border-radius: 16px;
                        text-align: center;
                        margin-bottom: 2rem;
                        box-shadow: 0 10px 30px rgba(67, 97, 238, 0.15);
                    }
                    
                    .hero-title {
                        font-size: 3rem;
                        font-weight: 800;
                        margin-bottom: 1.5rem;
                        color: white;
                        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    
                    .hero-subtitle {
                        font-size: 1.3rem;
                        color: rgba(255,255,255,0.9);
                        margin-bottom: 2.5rem;
                        max-width: 700px;
                        margin-left: auto;
                        margin-right: auto;
                        line-height: 1.6;
                    }
                    
                    .hero-badge {
                        display: inline-block;
                        background-color: rgba(255,255,255,0.2);
                        color: white;
                        padding: 0.5rem 1rem;
                        border-radius: 50px;
                        margin: 0 0.5rem 1rem 0.5rem;
                        font-weight: 500;
                        backdrop-filter: blur(5px);
                    }
                </style>
                
                <div class="hero-section">
                    <h1 class="hero-title">CiaoHost Manager</h1>
                    <p class="hero-subtitle">
                        Gestisci le tue proprietà in modo intelligente con la piattaforma all-in-one per host professionali
                    </p>
                    <div>
                        <span class="hero-badge">🏠 Gestione Proprietà</span>
                        <span class="hero-badge">📊 Analisi Dati</span>
                        <span class="hero-badge">🤖 Assistenza AI</span>
                        <span class="hero-badge">💰 Prezzi Dinamici</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Search form con stile moderno
            st.markdown("""
                <style>
                    /* Modern search form styling */
                    .search-container {
                        background-color: white;
                        border-radius: 12px;
                        padding: 20px;
                        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
                        margin-bottom: 2rem;
                        border: 1px solid rgba(0,0,0,0.05);
                    }
                    
                    .search-title {
                        font-size: 1.2rem;
                        font-weight: 600;
                        margin-bottom: 1.5rem;
                        color: #2d3748;
                        text-align: center;
                    }
                    
                    .search-button {
                        background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 12px 24px;
                        font-weight: 600;
                        width: 100%;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        box-shadow: 0 4px 10px rgba(67, 97, 238, 0.2);
                    }
                    
                    .search-button:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 6px 15px rgba(67, 97, 238, 0.3);
                    }
                </style>
                
                <div class="search-container">
                    <h3 class="search-title">Cerca tra le tue proprietà</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Form di ricerca con colonne
            search_col1, search_col2, search_col3 = st.columns([3, 2, 1])
            
            with search_col1:
                destination = st.text_input("Destinazione", placeholder="Inserisci città o nome proprietà", key="search_destination")
            
            with search_col2:
                dates = st.date_input("Periodo", value=[pd.to_datetime("today"), pd.to_datetime("today") + pd.Timedelta(days=7)], key="search_dates")
            
            with search_col3:
                guests = st.number_input("Ospiti", min_value=1, max_value=10, value=2, key="search_guests")
            
            # Pulsante di ricerca stilizzato
            if st.button("🔍 Cerca Proprietà", key="search_button", use_container_width=True):
                st.session_state.current_page = 'search_properties'
                st.rerun()
            
            # Featured properties section
            st.markdown("""
                <h2 style="font-size: 1.8rem; font-weight: 600; margin: 2rem 0 1.5rem 0; color: #212529;">
                    Alloggi in evidenza
                </h2>
            """, unsafe_allow_html=True)
            
            # Carica proprietà reali dal database
            db_properties = list(st.session_state.get('properties', {}).values())
            
            # Se non ci sono proprietà nel database, usa esempi di fallback
            if not db_properties:
                db_properties = [
                    {
                        "name": "Villa Paradiso Mare",
                        "location": "Costa Smeralda, Sardegna",
                        "price": 320,
                        "rating": 4.9,
                        "image": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"
                    },
                    {
                        "name": "Luxury Penthouse",
                        "location": "Centro Storico, Roma",
                        "price": 275,
                        "rating": 4.8,
                        "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"
                    },
                    {
                        "name": "Chalet Dolomiti",
                        "location": "Cortina d'Ampezzo, Veneto",
                        "price": 390,
                        "rating": 4.9,
                        "image": "https://images.unsplash.com/photo-1542718610-a1d656d1884c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"
                    },
                    {
                        "name": "Design Loft",
                        "location": "Navigli, Milano",
                        "price": 230,
                        "rating": 4.7,
                        "image": "https://images.unsplash.com/photo-1613545325278-f24b0cae1224?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"
                    },
                    {
                        "name": "Villa Toscana",
                        "location": "Val d'Orcia, Toscana",
                        "price": 295,
                        "rating": 4.8,
                        "image": "https://images.unsplash.com/photo-1599809275671-b5942cabc7a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"
                    },
                    {
                        "name": "Attico Panoramico",
                        "location": "Posillipo, Napoli",
                        "price": 280,
                        "rating": 4.9,
                        "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"
                    }
                ]
            
            # Limita a massimo 6 proprietà per il carousel
            featured_properties = db_properties[:6]
            
            # Aggiungi CSS per il carousel moderno
            st.markdown("""
                <style>
                /* Modern carousel styling */
                .carousel-container {
                    overflow-x: auto;
                    display: flex;
                    padding: 1.5rem 0;
                    scroll-behavior: smooth;
                    -webkit-overflow-scrolling: touch;
                    gap: 20px;
                }
                
                
                .carousel-container::-webkit-scrollbar {
                    height: 8px;
                }
                .carousel-container::-webkit-scrollbar-track {
                    background: #f0f4ff;
                    border-radius: 10px;
                }
                
                .carousel-container::-webkit-scrollbar-thumb {
                    background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%);
                    border-radius: 16px;
                }
                
                .carousel-item {
                    flex: 0 0 auto;
                    width: 340px;
                    background-color: white;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
                    cursor: pointer;
                    transition: all 0.4s ease;
                    border: 1px solid rgba(0,0,0,0.05);
                }
                .carousel-item:hover {
                    transform: translateY(-10px);
                    box-shadow: 0 15px 35px rgba(67, 97, 238, 0.15);
                }
                
                .property-image {
                    height: 220px;
                    width: 100%;
                    object-fit: cover;
                    transition: transform 0.5s ease;
                }
                
                .carousel-item:hover .property-image {
                    transform: scale(1.05);
                }
                
                .property-info {
                    padding: 20px;
                }
                
                .property-name {
                    font-size: 1.2rem;
                    font-weight: 700;
                    color: #2d3748;
                    margin-bottom: 8px;
                }
                
                .property-location {
                    display: flex;
                    align-items: center;
                    font-size: 0.9rem;
                    color: #718096;
                    margin-bottom: 15px;
                }
                
                .property-location svg {
                    margin-right: 5px;
                    color: #4361ee;
                }
                
                .property-meta {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-top: 15px;
                }
                
                .property-price {
                    font-size: 1.3rem;
                    font-weight: 700;
                    color: #4361ee;
                }
                
                .property-price span {
                    font-size: 0.9rem;
                    font-weight: 400;
                    color: #718096;
                }
                
                .property-rating {
                    display: flex;
                    align-items: center;
                    background-color: #f0f4ff;
                    padding: 5px 10px;
                    border-radius: 50px;
                    font-weight: 600;
                    color: #4361ee;
                }
                
                .property-rating svg {
                    color: #f59e0b;
                    margin-right: 5px;
                }
                
                .property-badge {
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background: linear-gradient(90deg, #4361ee 0%, #3a56d4 100%);
                    color: white;
                    padding: 5px 12px;
                    border-radius: 50px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    box-shadow: 0 4px 10px rgba(67, 97, 238, 0.3);
                }
                
                .carousel-section-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 1.5rem;
                }
                
                .section-title {
                    font-size: 1.8rem;
                    font-weight: 700;
                    color: #2d3748;
                    position: relative;
                    padding-left: 15px;
                }
                
                .section-title:before {
                    content: "";
                    position: absolute;
                    left: 0;
                    top: 0;
                    height: 100%;
                    width: 5px;
                    background: linear-gradient(180deg, #4361ee 0%, #3a56d4 100%);
                    border-radius: 10px;
                }
                
                .view-all-link {
                    color: #4361ee;
                    font-weight: 600;
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                }
                
                .view-all-link svg {
                    margin-left: 5px;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Intestazione sezione proprietà in evidenza
            st.markdown("""
                <div class="carousel-section-header">
                    <h2 class="section-title">Proprietà in Evidenza</h2>
                </div>
                
                <div class="carousel-container" id="featured-carousel">
            """, unsafe_allow_html=True)
            
            # Creiamo le card delle proprietà usando SOLO componenti Streamlit nativi
            st.subheader("Proprietà in Evidenza")
            
            # Creiamo una riga di 3 colonne per le proprietà
            prop_cols = st.columns(3)
            
            # Distribuiamo le proprietà nelle colonne
            for i, prop in enumerate(featured_properties[:3]):
                with prop_cols[i % 3]:
                    # Assicurati che i campi necessari esistano
                    prop_name = prop.get('name', 'Proprietà')
                    prop_location = prop.get('location', 'Italia')
                    prop_price = prop.get('price', 0)
                    prop_rating = prop.get('rating', 4.0)
                    prop_image = prop.get('image', "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80")
                    
                    # Aggiungi badge "Superhost" casualmente ad alcune proprietà
                    is_superhost = prop_rating >= 4.8
                    
                    # Usa componenti Streamlit nativi
                    st.image(prop_image, use_container_width=True)
                    if is_superhost:
                        st.success("Superhost")
                    
                    st.write(f"### {prop_name}")
                    st.write(f"📍 {prop_location}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**€{prop_price}** / notte")
                    with col2:
                        st.write(f"⭐ {prop_rating}")
                    
                    # Aggiungi un pulsante per vedere i dettagli
                    if st.button("Vedi dettagli", key=f"prop_btn_{i}", use_container_width=True):
                        st.session_state.current_page = 'search_properties'
                        st.rerun()
            
            # Chiudiamo il div del carosello
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Pulsante per visualizzare tutte le proprietà
            if st.button("Visualizza tutte le proprietà", key="view_all_button", help="Visualizza tutte le proprietà", use_container_width=True):
                st.session_state.current_page = 'search_properties'
                st.rerun()
            
            # Popular destinations section con stile moderno
            st.markdown("""
                <div class="carousel-section-header">
                    <h2 class="section-title">Destinazioni Popolari</h2>
                    <a href="#" class="view-all-link" onclick="document.getElementById('view_all_button').click()">
                        Esplora tutte
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M5 12h14"></path>
                            <path d="M12 5l7 7-7 7"></path>
                        </svg>
                    </a>
                </div>
                
                <style>
                    .destinations-grid {
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 20px;
                        margin-bottom: 2rem;
                    }
                    
                    .destination-card {
                        position: relative;
                        border-radius: 16px;
                        overflow: hidden;
                        height: 220px;
                        cursor: pointer;
                        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
                        transition: all 0.4s ease;
                    }
                    
                    .destination-card:hover {
                        transform: translateY(-10px);
                        box-shadow: 0 15px 35px rgba(67, 97, 238, 0.15);
                    }
                    
                    .destination-image {
                        width: 100%;
                        height: 100%;
                        object-fit: cover;
                        transition: transform 0.5s ease;
                    }
                    
                    .destination-card:hover .destination-image {
                        transform: scale(1.05);
                    }
                    
                    .destination-overlay {
                        position: absolute;
                        bottom: 0;
                        left: 0;
                        right: 0;
                        padding: 1.5rem;
                        background: linear-gradient(transparent, rgba(0,0,0,0.7));
                    }
                    
                    .destination-name {
                        font-size: 1.3rem;
                        font-weight: 700;
                        margin: 0;
                        color: white;
                        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    }
                    
                    .destination-properties {
                        font-size: 0.9rem;
                        color: rgba(255,255,255,0.9);
                        margin-top: 5px;
                    }
                </style>
                
                <div class="destinations-grid">
            """, unsafe_allow_html=True)
            
            # Sample destinations con immagini migliori
            destinations = [
                {"name": "Roma", "properties": "245 proprietà", "image": "https://images.unsplash.com/photo-1555992828-ca4dbe41d294?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"},
                {"name": "Firenze", "properties": "189 proprietà", "image": "https://images.unsplash.com/photo-1534445867742-43195f401b6c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"},
                {"name": "Venezia", "properties": "210 proprietà", "image": "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"},
                {"name": "Milano", "properties": "276 proprietà", "image": "https://images.unsplash.com/photo-1574155376612-bfa4ed8aabfd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"}
            ]
            
            # Funzione per gestire il click su una destinazione
            def handle_destination_click(destination):
                # Salviamo la destinazione in una variabile di sessione diversa
                st.session_state.destination_selected = destination
                st.session_state.current_page = 'search_properties'
                st.rerun()
            
            # Creiamo le card delle destinazioni usando SOLO componenti Streamlit nativi
            st.subheader("Destinazioni Popolari")
            
            # Aggiungiamo CSS per lo zoom delle immagini al passaggio del mouse
            st.markdown("""
            <style>
                .zoom-effect {
                    overflow: hidden;
                    border-radius: 10px;
                    margin-bottom: 10px;
                }
                .zoom-effect img {
                    transition: transform 0.5s ease;
                    width: 100%;
                    height: 200px;
                    object-fit: cover;
                }
                .zoom-effect:hover img {
                    transform: scale(1.1);
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Aggiorniamo le immagini delle destinazioni per avere tutte lo stesso formato
            destinations_images = {
                "Roma": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80",
                "Firenze": "https://images.unsplash.com/photo-1534445867742-43195f401b6c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80",
                "Venezia": "https://images.unsplash.com/photo-1514890547357-a9ee288728e0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80",
                "Milano": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80"
            }
            
            # Creiamo una riga di 4 colonne per le destinazioni
            dest_cols = st.columns(4)
            
            # Distribuiamo le destinazioni nelle colonne
            for i, dest in enumerate(destinations):
                with dest_cols[i % 4]:
                    # Usa l'immagine aggiornata se disponibile
                    image_url = destinations_images.get(dest['name'], dest['image'])
                    
                    # Usa componenti Streamlit nativi con effetto zoom
                    st.markdown(f"""
                    <div class="zoom-effect">
                        <img src="{image_url}" alt="{dest['name']}">
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write(f"### {dest['name']}")
                    st.write(f"{dest['properties']}")
                    
                    # Aggiungi un pulsante per vedere le proprietà in questa destinazione
                    if st.button(f"Esplora {dest['name']}", key=f"dest_btn_{dest['name']}", use_container_width=True):
                        handle_destination_click(dest['name'])
            
            # Why choose us section con stile moderno
            st.subheader("Perché scegliere CiaoHost")
            
            # Creiamo una riga di 3 colonne per le caratteristiche
            feature_cols = st.columns(3)
            
            # Definizione delle caratteristiche
            features = [
                {
                    "icon": "⭐",
                    "title": "Alloggi Selezionati",
                    "description": "Solo le migliori strutture, verificate e certificate dal nostro team di esperti per garantirti un soggiorno perfetto."
                },
                {
                    "icon": "💰",
                    "title": "Prezzi Dinamici",
                    "description": "Algoritmi avanzati che ottimizzano i prezzi in tempo reale in base alla domanda, stagionalità ed eventi locali."
                },
                {
                    "icon": "🛎️",
                    "title": "Assistenza 24/7",
                    "description": "Supporto clienti disponibile 24 ore su 24, 7 giorni su 7, in italiano e in inglese per risolvere qualsiasi problema."
                }
            ]
            
            # Distribuiamo le caratteristiche nelle colonne
            for i, feature in enumerate(features):
                with feature_cols[i]:
                    st.write(f"## {feature['icon']}")
                    st.write(f"### {feature['title']}")
                    st.write(feature['description'])
            
            # Sezione recensioni con foto profilo
            st.subheader("Cosa dicono i nostri clienti")
            
            # Definiamo le recensioni con foto profilo
            reviews = [
                {
                    "name": "Marco Rossi",
                    "photo": "https://randomuser.me/api/portraits/men/32.jpg",
                    "rating": 5,
                    "text": "Grazie a CiaoHost ho aumentato le prenotazioni del 40% in soli due mesi. Il sistema di prezzi dinamici è fantastico!",
                    "location": "Roma"
                },
                {
                    "name": "Laura Bianchi",
                    "photo": "https://randomuser.me/api/portraits/women/44.jpg",
                    "rating": 5,
                    "text": "Finalmente posso gestire tutte le mie proprietà da un'unica piattaforma. Servizio clienti eccellente e sempre disponibile.",
                    "location": "Milano"
                },
                {
                    "name": "Alessandro Verdi",
                    "photo": "https://randomuser.me/api/portraits/men/67.jpg",
                    "rating": 4,
                    "text": "La gestione delle pulizie automatizzata mi ha fatto risparmiare tempo e denaro. Consigliato a tutti gli host!",
                    "location": "Firenze"
                }
            ]
            
            # Creiamo una riga di 3 colonne per le recensioni
            review_cols = st.columns(3)
            
            # Aggiungiamo stile CSS per le recensioni
            st.markdown("""
            <style>
                .review-card {
                    background-color: white;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    margin-bottom: 20px;
                }
                
                .review-header {
                    display: flex;
                    align-items: center;
                    margin-bottom: 15px;
                }
                
                .review-photo {
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin-right: 15px;
                }
                
                .review-name {
                    font-weight: 600;
                    margin: 0;
                    font-size: 16px;
                }
                
                .review-location {
                    color: #6c757d;
                    font-size: 14px;
                    margin: 0;
                }
                
                .review-stars {
                    color: #f59e0b;
                    margin-bottom: 10px;
                }
                
                .review-text {
                    font-size: 15px;
                    line-height: 1.6;
                    color: #4a5568;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Distribuiamo le recensioni nelle colonne
            for i, review in enumerate(reviews):
                with review_cols[i]:
                    st.markdown(f"""
                    <div class="review-card">
                        <div class="review-header">
                            <img src="{review['photo']}" class="review-photo" alt="{review['name']}">
                            <div>
                                <p class="review-name">{review['name']}</p>
                                <p class="review-location">{review['location']}</p>
                            </div>
                        </div>
                        <div class="review-stars">{"★" * review['rating'] + "☆" * (5 - review['rating'])}</div>
                        <p class="review-text">"{review['text']}"</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Host section con stile moderno
            st.subheader("Sei un proprietario di immobili?")
            
            # Creiamo due colonne per il contenuto e l'immagine
            host_col1, host_col2 = st.columns(2)
            
            with host_col1:
                # Usa un container con sfondo colorato
                with st.container():
                    st.write("### Unisciti a CiaoHost")
                    st.write("Trasforma la gestione delle tue proprietà con strumenti professionali e intelligenza artificiale.")
                    
                    st.write("✓ Prezzi ottimizzati")
                    st.write("✓ Gestione semplificata")
                    st.write("✓ Maggiore visibilità")
                
                if st.button("Inizia ora", key="host_cta_btn", use_container_width=True):
                    st.session_state.current_page = 'subscriptions'
                    st.rerun()
            
            with host_col2:
                st.image("https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1350&q=80", 
                         caption="Diventa un host con CiaoHost", 
                         use_container_width=True)
            
            # Bottoni per i piani di abbonamento
            host_btn_col1, host_btn_col2 = st.columns(2)
            
            with host_btn_col1:
                if st.button("🚀 Scopri i nostri piani", key="host_discover_plans", use_container_width=True):
                    st.session_state.current_page = 'subscriptions'
                    st.rerun()
            
            with host_btn_col2:
                if st.button("🏠 Registra la tua struttura", key="host_register_property", use_container_width=True):
                    st.session_state.current_page = 'subscriptions'
                    st.rerun()
            
            # Testimonials section
            st.markdown("""
                <h2 style="font-size: 1.8rem; font-weight: 600; margin: 2.5rem 0 1.5rem 0; text-align: center; color: #212529;">
                    Cosa dicono i nostri clienti
                </h2>
            """, unsafe_allow_html=True)
            
            # Testimonials grid
            test_col1, test_col2, test_col3 = st.columns(3)
            
            with test_col1:
                st.markdown("""
                    <div style="background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                        <div style="font-size: 1.2rem; color: #ffc107; margin-bottom: 1rem;">★★★★★</div>
                        <p style="font-size: 0.9rem; color: #212529; margin-bottom: 1rem; font-style: italic;">
                            "Esperienza fantastica! L'appartamento era esattamente come nelle foto, pulito e in una posizione perfetta. Il check-in è stato semplice e l'host sempre disponibile."
                        </p>
                        <div style="display: flex; align-items: center;">
                            <img src="https://randomuser.me/api/portraits/men/22.jpg" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 0.5rem;">
                            <div>
                                <p style="margin: 0; font-weight: 600;">Davide Marino</p>
                                <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">Torino, Italia</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with test_col2:
                st.markdown("""
                    <div style="background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                        <div style="font-size: 1.2rem; color: #ffc107; margin-bottom: 1rem;">★★★★★</div>
                        <p style="font-size: 0.9rem; color: #212529; margin-bottom: 1rem; font-style: italic;">
                            "Prenotazione semplice e veloce. La villa era stupenda, con una vista mozzafiato sul mare. Torneremo sicuramente per le prossime vacanze!"
                        </p>
                        <div style="display: flex; align-items: center;">
                            <img src="https://randomuser.me/api/portraits/women/28.jpg" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 0.5rem;">
                            <div>
                                <p style="margin: 0; font-weight: 600;">Francesca Ricci</p>
                                <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">Venezia, Italia</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with test_col3:
                st.markdown("""
                    <div style="background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                        <div style="font-size: 1.2rem; color: #ffc107; margin-bottom: 1rem;">★★★★★</div>
                        <p style="font-size: 0.9rem; color: #212529; margin-bottom: 1rem; font-style: italic;">
                            "Servizio impeccabile! L'assistenza clienti è stata pronta a risolvere un piccolo problema con il riscaldamento. Consiglio vivamente CiaoHost."
                        </p>
                        <div style="display: flex; align-items: center;">
                            <img src="https://randomuser.me/api/portraits/men/45.jpg" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 0.5rem;">
                            <div>
                                <p style="margin: 0; font-weight: 600;">Roberto Esposito</p>
                                <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">Bologna, Italia</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Newsletter section
            st.markdown("""
                <div style="background-color: #e6effd; padding: 2rem; border-radius: 10px; margin: 2.5rem 0; text-align: center;">
                    <h2 style="font-size: 1.8rem; font-weight: 600; margin-bottom: 1rem; color: #0056b3;">
                        Resta aggiornato sulle nostre offerte
                    </h2>
                    <p style="font-size: 1.1rem; color: #212529; margin-bottom: 1.5rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                        Iscriviti alla nostra newsletter per ricevere offerte esclusive e suggerimenti per i tuoi prossimi viaggi
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Newsletter form
            newsletter_col1, newsletter_col2 = st.columns([3, 1])
            
            with newsletter_col1:
                st.text_input("La tua email", placeholder="Inserisci la tua email", key="newsletter_email")
            
            with newsletter_col2:
                if st.button("Iscriviti", key="newsletter_submit", use_container_width=True):
                    # Stub function for newsletter subscription
                    st.success("Grazie per esserti iscritto alla nostra newsletter!")
                    # TODO: Implement actual newsletter subscription functionality
            
            # User-specific section (only if logged in)
            if st.session_state.get('is_authenticated', False):
                user_name = st.session_state.get('current_user_email', 'Utente').split('@')[0]
                
                # Host dashboard link (SOLO se abbonato)
                if st.session_state.get('subscription_purchased', False):
                    st.markdown("""
                        <div style="background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin: 2.5rem 0;">
                            <h3 style="font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; color: #0056b3;">
                                Area Host
                            </h3>
                            <p style="font-size: 1rem; color: #212529; margin-bottom: 1rem;">
                                Accedi alla tua dashboard per gestire i tuoi immobili, visualizzare le prenotazioni e molto altro.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Host dashboard buttons
                    host_col1, host_col2, host_col3, host_col4 = st.columns(4)
                    
                    with host_col1:
                        if st.button("📊 Dashboard", key="host_dashboard", use_container_width=True):
                            st.session_state.current_page = 'dashboard'
                            st.rerun()
                    
                    with host_col2:
                        if st.button("🏘️ Gestione Proprietà", key="host_properties", use_container_width=True):
                            st.session_state.current_page = 'property_management'
                            st.rerun()
                    
                    with host_col3:
                        if st.button("⚖️ Prezzi Dinamici", key="host_pricing", use_container_width=True):
                            st.session_state.current_page = 'dynamic_pricing'
                            st.rerun()
                    
                    with host_col4:
                        if st.button("🧹 Gestione Pulizie", key="host_cleaning", use_container_width=True):
                            st.session_state.current_page = 'cleaning_management'
                            st.rerun()
                else:
                    # Sezione per utenti autenticati ma non abbonati
                    st.markdown(f"""
                        <div style="background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin: 2.5rem 0;">
                            <h3 style="font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; color: #0056b3;">
                                Ciao {user_name}, vuoi diventare un host?
                            </h3>
                            <p style="font-size: 1rem; color: #212529; margin-bottom: 1rem;">
                                Sblocca tutte le funzionalità premium per gestire i tuoi immobili in modo professionale.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🚀 Scopri i Piani di Abbonamento", key="home_cta_plans", use_container_width=True):
                        st.session_state.current_page = 'subscriptions'
                        st.rerun()

        elif st.session_state.current_page == 'search_properties':
            show_property_search()
        elif st.session_state.current_page == 'subscriptions':
            show_subscription_plans()
        elif st.session_state.current_page == 'dashboard':
            # Assicuriamoci che l'abbonamento sia attivo
            if 'subscription_purchased' not in st.session_state:
                st.session_state.subscription_purchased = True
            show_dashboard()
        elif st.session_state.current_page == 'ai':
            # CSS per il design professionale del chatbot
            st.markdown("""
            <style>
            /* Forzatura tema chiaro - Override tema scuro */
            .stApp {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza tutti i testi a essere scuri su sfondo chiaro */
            .stApp * {
                color: #1e293b !important;
            }
            
            /* Forza sidebar a tema chiaro */
            [data-testid="stSidebar"] {
                background-color: #f8fafc !important;
                color: #1e293b !important;
            }
            
            [data-testid="stSidebar"] * {
                color: #1e293b !important;
            }
            
            /* Forza header e contenuti principali */
            .stApp > header {
                background-color: white !important;
            }
            
            .main .block-container {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza tutti i componenti Streamlit a tema chiaro */
            .stMarkdown, .stText, .stCaption {
                color: #1e293b !important;
            }
            
            .stButton > button {
                background-color: white !important;
                color: #1e293b !important;
                border: 1px solid #e2e8f0 !important;
            }
            
            .stSelectbox, .stTextInput, .stTextArea {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza chat messages a tema chiaro */
            .stChatMessage {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza tutti gli elementi di testo */
            h1, h2, h3, h4, h5, h6, p, span, div, label {
                color: #1e293b !important;
            }
            
            /* Forza elementi specifici di Streamlit */
            .stApp [data-testid="stHeader"] {
                background-color: white !important;
            }
            
            .stApp [data-testid="stToolbar"] {
                background-color: white !important;
            }
            
            .stApp [data-testid="stDecoration"] {
                background-color: white !important;
            }
            
            /* Forza contenuto principale */
            .main {
                background-color: white !important;
            }
            
            .block-container {
                background-color: white !important;
            }
            
            /* Forza tutti i widget */
            .stWidget {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza metriche e indicatori */
            .metric-container {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza colonne */
            .stColumn {
                background-color: transparent !important;
            }
            
            /* Override per elementi che potrebbero rimanere scuri */
            .css-1d391kg, .css-1y4p8pa, .css-12oz5g7 {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza root e body */
            html, body {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza tutti gli elementi con background scuro */
            [style*="background-color: rgb(14, 17, 23)"],
            [style*="background-color: #0e1117"],
            [style*="background-color: rgb(38, 39, 48)"],
            [style*="background-color: #262730"] {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza tutti gli elementi con colore di testo chiaro */
            [style*="color: rgb(250, 250, 250)"],
            [style*="color: #fafafa"],
            [style*="color: white"],
            [style*="color: rgb(255, 255, 255)"] {
                color: #1e293b !important;
            }
            
            /* Forza elementi con classi comuni di tema scuro */
            .dark, .dark-theme, .theme-dark {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza tutti i data-testid comuni */
            [data-testid*="stApp"],
            [data-testid*="stMain"],
            [data-testid*="stSidebar"],
            [data-testid*="stHeader"] {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Forza override universale per tutti gli elementi */
            * {
                background-color: inherit !important;
                color: #1e293b !important;
            }
            
            /* Eccezioni per elementi che devono mantenere i loro colori */
            .chatbot-container,
            .chatbot-header,
            .ai-badge,
            .stChatMessage[data-testid*="user"],
            .stChatMessage[data-testid*="bot"],
            .stChatInput button {
                background: inherit !important;
                color: inherit !important;
            }
            
            /* Container principale del chatbot con design luxury */
            .chatbot-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 24px;
                padding: 0;
                margin: -1rem -1rem 2rem -1rem;
                box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
                position: relative;
                overflow: hidden;
            }
            
            /* Header del chatbot */
            .chatbot-header {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                padding: 2rem;
                text-align: center;
                position: relative;
                z-index: 2;
            }
            
            .chatbot-title {
                font-size: 2.5rem;
                font-weight: 800;
                color: white;
                margin: 0;
                text-shadow: 0 4px 8px rgba(0,0,0,0.3);
                letter-spacing: -0.5px;
            }
            
            .chatbot-subtitle {
                font-size: 1.1rem;
                color: rgba(255, 255, 255, 0.9);
                margin: 0.5rem 0 0 0;
                font-weight: 400;
            }
            
            .ai-badge {
                display: inline-flex;
                align-items: center;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 50px;
                padding: 0.5rem 1rem;
                margin-top: 1rem;
                font-size: 0.9rem;
                color: white;
                font-weight: 600;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            /* Area chat migliorata */
            .chat-area {
                background: rgba(255, 255, 255, 0.95);
                margin: 2rem;
                border-radius: 20px;
                min-height: 500px;
                box-shadow: inset 0 4px 12px rgba(0,0,0,0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.3);
                position: relative;
                z-index: 2;
                padding: 1rem;
            }
            
            /* Stile per i messaggi chat */
            .stChatMessage {
                background: transparent !important;
                border: none !important;
                margin: 1rem 0 !important;
            }
            
            .stChatMessage[data-testid*="user"] {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
                border-radius: 18px 18px 4px 18px !important;
                margin-left: 20% !important;
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
            }
            
            .stChatMessage[data-testid*="user"] .stMarkdown {
                color: white !important;
                font-weight: 500 !important;
            }
            
            .stChatMessage[data-testid*="bot"] {
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
                border-radius: 18px 18px 18px 4px !important;
                margin-right: 20% !important;
                border: 1px solid rgba(148, 163, 184, 0.2) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
            }
            
            .stChatMessage[data-testid*="bot"] .stMarkdown {
                color: #334155 !important;
                font-weight: 500 !important;
            }
            
            .stChatMessage[data-testid*="admin"] {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
                border-radius: 18px !important;
                box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3) !important;
            }
            
            .stChatMessage[data-testid*="admin"] .stMarkdown {
                color: white !important;
                font-weight: 600 !important;
            }
            
            /* Input chat professionale migliorato */
            .stChatInput {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95)) !important;
                border-radius: 20px !important;
                border: 2px solid rgba(102, 126, 234, 0.4) !important;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15), 0 4px 15px rgba(0,0,0,0.1) !important;
                backdrop-filter: blur(20px) !important;
                margin: 20px 2rem 2rem 2rem !important;
                transition: all 0.3s ease !important;
            }
            
            .stChatInput:hover {
                border-color: rgba(102, 126, 234, 0.6) !important;
                box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2), 0 6px 20px rgba(0,0,0,0.15) !important;
                transform: translateY(-2px) !important;
            }
            
            .stChatInput input {
                background: transparent !important;
                border: none !important;
                font-size: 16px !important;
                font-weight: 500 !important;
                color: #1e293b !important;
                padding: 15px 20px !important;
            }
            
            .stChatInput input::placeholder {
                color: #64748b !important;
                font-style: italic !important;
                font-weight: 400 !important;
            }
            
            /* Pulsante di invio migliorato per AI normale */
            .stChatInput button {
                background: linear-gradient(135deg, #667eea, #764ba2) !important;
                border: none !important;
                border-radius: 15px !important;
                padding: 10px 15px !important;
                margin: 5px !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
            }
            
            .stChatInput button:hover {
                background: linear-gradient(135deg, #5a67d8, #6b46c1) !important;
                transform: scale(1.05) !important;
                box-shadow: 0 6px 18px rgba(102, 126, 234, 0.4) !important;
            }
            
            /* Indicatori di stato */
            .status-indicators {
                display: flex;
                justify-content: center;
                gap: 1rem;
                padding: 1rem 2rem;
                background: rgba(255, 255, 255, 0.1);
                margin: 0 2rem;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .status-item {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: rgba(255, 255, 255, 0.9);
                font-size: 0.9rem;
                font-weight: 500;
            }
            
            .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #10b981;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            /* Suggerimenti rapidi */
            .quick-suggestions {
                display: flex;
                gap: 0.5rem;
                padding: 1rem 2rem;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .suggestion-chip {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
                padding: 0.5rem 1rem;
                color: white;
                font-size: 0.85rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }
            
            .suggestion-chip:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }
            
            /* Animazioni fluide */
            .chatbot-container {
                animation: slideInUp 0.8s ease-out;
            }
            
            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .chatbot-container {
                    margin: -1rem -0.5rem 1rem -0.5rem;
                }
                
                .chatbot-title {
                    font-size: 2rem;
                }
                
                .chat-area {
                    margin: 1rem;
                    min-height: 400px;
                }
                
                .stChatMessage[data-testid*="user"] {
                    margin-left: 10% !important;
                }
                
                .stChatMessage[data-testid*="bot"] {
                    margin-right: 10% !important;
                }
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Header principale
            st.markdown("""
            <div class="chatbot-container">
                <div class="chatbot-header">
                    <h1 class="chatbot-title">🤖 CiaoHost AI Assistant</h1>
                    <p class="chatbot-subtitle">Il tuo consulente immobiliare intelligente, sempre al tuo servizio</p>
                    <div class="ai-badge">🧠 Powered by CiaoHost Advanced AI</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Indicatori di stato con componenti Streamlit
            st.markdown("### 🟢 Status Sistema")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.success("🤖 AI Online")
            with col2:
                st.info("⚡ Risposta Istantanea")
            with col3:
                st.warning("🕐 Supporto 24/7")
            

            
            # Separatore visivo
            st.markdown("---")
            st.markdown("### 💬 Chat con l'AI Assistant")
            
            # Area chat con componenti Streamlit nativi
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.get('messages', []):
                    role = message["role"]
                    content = message["content"]
                    avatar_map = {"user": "👤", "bot": "🤖", "admin": "⚙️"}
                    
                    with st.chat_message(name=role, avatar=avatar_map.get(role)):
                        st.markdown(content)
            
            # Area di input migliorata per AI Assistant
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
                border-radius: 20px;
                padding: 20px;
                margin: 20px 0;
                border: 1px solid rgba(102, 126, 234, 0.2);
                backdrop-filter: blur(10px);
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    margin-bottom: 10px;
                ">
                    <div style="
                        font-size: 24px;
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                    ">🤖</div>
                    <div style="
                        font-size: 16px;
                        font-weight: 600;
                        color: #1e293b;
                    ">Scrivi il tuo messaggio</div>
                </div>
                <div style="
                    font-size: 14px;
                    color: #64748b;
                    font-style: italic;
                ">💬 Sono qui per aiutarti con prenotazioni, informazioni e supporto 24/7...</div>
            </div>
            """, unsafe_allow_html=True)
            
            user_input = st.chat_input("✨ Scrivi qui il tuo messaggio per l'AI Assistant...", key="chat_input")
            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Controlla se è un comando di prenotazione o se c'è una prenotazione in corso
                booking_response = handle_booking(user_input)
                if booking_response:
                    st.session_state.messages.append({"role": "bot", "content": booking_response})
                else:
                    # Se non è una prenotazione, controlla se è un comando admin
                    admin_response = handle_admin_access(user_input)
                    if admin_response:
                        st.session_state.messages.append({"role": "admin", "content": admin_response})
                    else:
                        # Se non è né prenotazione né admin, usa il modello AI
                        if not (st.session_state.admin_state and st.session_state.admin_state.get('mode') == 'auth'):
                            if model:
                                try:
                                    property_summary = "Nessuna proprietà nel database."
                                    if st.session_state.properties:
                                        prop_count = len(st.session_state.properties)
                                        property_summary = f"{prop_count} proprietà nel database:\n"
                                        for prop_id, prop in st.session_state.properties.items():
                                            prop_name = prop.get('name', 'N/A')
                                            prop_type = prop.get('type', 'N/A')
                                            prop_location = prop.get('location', 'N/A')
                                            property_summary += f"- ID {prop_id}: {prop_name} ({prop_type}) a {prop_location}\n"
                                    
                                    conversation_history = []
                                    for msg in st.session_state.messages[-10:]:
                                        gemini_role = "user" if msg["role"] == "user" else "model"
                                        conversation_history.append({"role": gemini_role, "parts": [{"text": msg["content"]}]})
                                
                                    if conversation_history and conversation_history[-1]["role"] == "user":
                                        current_prompt_text = conversation_history.pop()["parts"][0]["text"]
                                    else:
                                        current_prompt_text = user_input

                                    final_prompt = f"{CONTESTO_IMMOBILIARE}\n\n{property_summary}\n\n{current_prompt_text}"
                                    response = model.generate_content([{"role": "user", "parts": [{"text": final_prompt}]}])
                                    bot_reply = response.text
                                except Exception as e:
                                    bot_reply = f"🤖 Scusa, ho riscontrato un errore: {str(e)}"
                            else:
                                bot_reply = "🤖 Il modello AI non è disponibile al momento."
                            
                            st.session_state.messages.append({"role": "bot", "content": bot_reply})
                
                st.rerun()
        elif st.session_state.current_page == 'cleaning_management':
            show_cleaning_management_page()
        elif st.session_state.current_page == 'dynamic_pricing':
            show_dynamic_pricing_page()
        elif st.session_state.current_page == 'fiscal_management':
            show_fiscal_management_page()
        elif st.session_state.current_page == 'property_management':
            show_property_management_page()
        elif st.session_state.current_page == 'report_builder':
            show_report_builder_page()
        elif st.session_state.current_page == 'settings':
            show_settings_page()
        elif st.session_state.current_page == 'ai_management':
            show_ai_management_page()
        else:
            # Fallback for any unknown page state
            valid_pages = [
                'home', 'search_properties', 'subscriptions', 'dashboard', 'ai', 'login',
                'cleaning_management', 'dashboard_creator', 'data_insights',
                'dynamic_pricing', 'fiscal_management', 'property_management',
                'report_builder', 'settings', 'ai_management'
            ]
            if st.session_state.current_page not in valid_pages:
                 st.error(f"Pagina '{st.session_state.current_page}' non trovata o non implementata.")
                 # Optionally, redirect to home:
                 # st.session_state.current_page = 'home'
                 # st.rerun()

if __name__ == "__main__":
    main()
    
