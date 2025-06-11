import streamlit as st
import uuid
from datetime import datetime
import re

def detect_booking_intent(message):
    """
    Rileva se l'utente ha espresso l'intenzione di prenotare un alloggio.
    
    Args:
        message (str): Il messaggio dell'utente
        
    Returns:
        bool: True se l'utente vuole prenotare, False altrimenti
    """
    # Frasi che indicano l'intenzione di prenotare
    booking_phrases = [
        "vorrei prenotare", "voglio prenotare", "posso prenotare",
        "voglio affittare", "vorrei affittare", "posso affittare",
        "cerco un alloggio", "cerco una casa", "cerco un appartamento",
        "vorrei soggiornare", "voglio soggiornare", "posso soggiornare",
        "disponibilità", "prenotazione", "affittare", "alloggiare"
    ]
    
    message_lower = message.lower()
    
    # Controlla se una delle frasi è presente nel messaggio
    for phrase in booking_phrases:
        if phrase in message_lower:
            return True
            
    return False

def handle_booking(message_text):
    """Gestisce il processo di prenotazione attraverso la chat"""
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
    
    # Controlla se l'utente ha espresso l'intenzione di prenotare in linguaggio naturale
    elif detect_booking_intent(message_text) and not booking_state.get('active', False):
        # Elenca le proprietà disponibili
        available_properties = {pid: prop for pid, prop in st.session_state.properties.items() 
                               if prop.get("status", "").lower() == "disponibile" or 
                                  prop.get("status", "").lower() == "attivo"}
        
        if not available_properties:
            return "Mi dispiace, al momento non ci sono immobili disponibili per la prenotazione."
        
        property_list = "\n".join([f"- {prop.get('name', 'N/A')} ({prop.get('type', 'N/A')}) a {prop.get('location', 'N/A')}" 
                                  for prop in available_properties.values()])
        
        return f"""
✨ **Sono felice di aiutarti con la prenotazione!**

Ecco gli immobili disponibili:

{property_list}

Per prenotare, usa il comando `/prenota` seguito dal nome dell'immobile.
Esempio: `/prenota Villa Bella`
"""
    
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