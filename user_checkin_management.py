import streamlit as st
import pandas as pd
import json
import uuid
from datetime import datetime
import time
from loading_animations import show_loading_animation, show_success_animation

def load_bookings():
    """Carica le prenotazioni dal database"""
    try:
        with open("c:/Users/DEADSHOT/Desktop/ciaohostreale/ciaohostluss/DatabaseCiaoHostPrenotazioni.json", "r") as f:
            data = json.load(f)
            return data.get("bookings", {})
    except Exception as e:
        st.error(f"Errore nel caricamento delle prenotazioni: {e}")
        return {}

def load_users():
    """Carica gli utenti dal database"""
    try:
        with open("c:/Users/DEADSHOT/Desktop/ciaohostreale/ciaohostluss/DatabaseCiaoHostProprieta.json", "r") as f:
            data = json.load(f)
            return data.get("users", {})
    except Exception as e:
        st.error(f"Errore nel caricamento degli utenti: {e}")
        return {}

def save_bookings(bookings):
    """Salva le prenotazioni nel database"""
    try:
        with open("c:/Users/DEADSHOT/Desktop/ciaohostreale/ciaohostluss/DatabaseCiaoHostPrenotazioni.json", "r") as f:
            data = json.load(f)
        
        data["bookings"] = bookings
        
        with open("c:/Users/DEADSHOT/Desktop/ciaohostreale/ciaohostluss/DatabaseCiaoHostPrenotazioni.json", "w") as f:
            json.dump(data, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Errore nel salvataggio delle prenotazioni: {e}")
        return False

def convert_date(date_str):
    """Converte una data dal formato italiano a un oggetto datetime"""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except:
        return datetime.now()  # Fallback

def show_checkin_management():
    """Mostra la gestione dei check-in e check-out"""
    
    # Carica i dati
    bookings = load_bookings()
    users = load_users()
    
    # Crea una lista di utenti per associarli alle prenotazioni
    user_list = list(users.keys())
    
    # Prepara i dati per la visualizzazione
    checkin_data = []
    checkout_data = []
    
    for booking_id, booking in bookings.items():
        # Assegna casualmente un utente se non è presente
        user_email = booking.get("user_email", user_list[hash(booking_id) % len(user_list)] if user_list else "N/A")
        
        # Estrai username dall'email
        username = user_email.split('@')[0] if '@' in user_email else user_email
        
        # Converti le date
        check_in_date = convert_date(booking.get("check_in_date", "01/01/2023"))
        check_out_date = convert_date(booking.get("check_out_date", "01/01/2023"))
        
        # Crea il record per il check-in
        checkin_record = {
            "ID Prenotazione": booking_id[:8],
            "Proprietà": booking.get("property_name", "N/A"),
            "Utente": username,
            "Email": user_email,
            "Data": booking.get("check_in_date", "N/A"),
            "Ora": booking.get("check_in_time", "N/A"),
            "Ospiti": booking.get("guests", 0),
            "Stato": booking.get("status", "N/A"),
            "Richieste Speciali": booking.get("special_requests", "N/A"),
            "Booking ID": booking_id
        }
        
        # Crea il record per il check-out
        checkout_record = {
            "ID Prenotazione": booking_id[:8],
            "Proprietà": booking.get("property_name", "N/A"),
            "Utente": username,
            "Email": user_email,
            "Data": booking.get("check_out_date", "N/A"),
            "Ora": "12:00",  # Orario di check-out predefinito
            "Ospiti": booking.get("guests", 0),
            "Stato": booking.get("status", "N/A"),
            "Booking ID": booking_id
        }
        
        checkin_data.append(checkin_record)
        checkout_data.append(checkout_record)
    
    # Ordina i dati per data
    checkin_data.sort(key=lambda x: convert_date(x["Data"]))
    checkout_data.sort(key=lambda x: convert_date(x["Data"]))
    
    # Crea i DataFrame
    checkin_df = pd.DataFrame(checkin_data)
    checkout_df = pd.DataFrame(checkout_data)
    
    # Mostra le schede
    tabs = st.tabs(["Check-in", "Check-out", "Aggiungi Prenotazione"])
    
    with tabs[0]:
        st.subheader("Gestione Check-in")
        
        # Filtri
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_property = st.text_input("Filtra per proprietà:", key="filter_checkin_property")
        with col2:
            filter_user = st.text_input("Filtra per utente:", key="filter_checkin_user")
        with col3:
            filter_status = st.selectbox("Stato:", ["Tutti", "Confermata", "In attesa", "Completata", "Cancellata"], key="filter_checkin_status_dropdown")
        
        # Applica i filtri
        filtered_checkin = checkin_df.copy()
        if filter_property:
            filtered_checkin = filtered_checkin[filtered_checkin["Proprietà"].str.contains(filter_property, case=False)]
        if filter_user:
            filtered_checkin = filtered_checkin[
                filtered_checkin["Utente"].str.contains(filter_user, case=False) | 
                filtered_checkin["Email"].str.contains(filter_user, case=False)
            ]
        if filter_status != "Tutti":
            filtered_checkin = filtered_checkin[filtered_checkin["Stato"] == filter_status]
        
        # Mostra la tabella
        if filtered_checkin.empty:
            st.info("Nessun check-in corrisponde ai filtri selezionati.")
        else:
            # Rimuovi la colonna Booking ID dalla visualizzazione
            display_df = filtered_checkin.drop(columns=["Booking ID"])
            st.dataframe(display_df, use_container_width=True)
            
            # Seleziona una prenotazione per completare il check-in
            st.subheader("Completa Check-in")
            selected_checkin = st.selectbox(
                "Seleziona una prenotazione:",
                options=filtered_checkin["Booking ID"].tolist(),
                format_func=lambda x: f"{next((b['ID Prenotazione'] for b in checkin_data if b['Booking ID'] == x), '')} - {next((b['Proprietà'] for b in checkin_data if b['Booking ID'] == x), '')} - {next((b['Utente'] for b in checkin_data if b['Booking ID'] == x), '')}",
                key="select_checkin_booking"
            )
            
            if selected_checkin:
                selected_booking = next((b for b in checkin_data if b["Booking ID"] == selected_checkin), None)
                
                if selected_booking:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Proprietà:** {selected_booking['Proprietà']}")
                        st.markdown(f"**Utente:** {selected_booking['Utente']}")
                        st.markdown(f"**Email:** {selected_booking['Email']}")
                    
                    with col2:
                        st.markdown(f"**Data:** {selected_booking['Data']}")
                        st.markdown(f"**Ora:** {selected_booking['Ora']}")
                        st.markdown(f"**Ospiti:** {selected_booking['Ospiti']}")
                    
                    st.markdown(f"**Richieste Speciali:** {selected_booking['Richieste Speciali']}")
                    
                    # Azioni per il check-in
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✅ Completa Check-in", key=f"complete_checkin_{selected_checkin}"):
                            # Mostra animazione di caricamento
                            show_loading_animation("Completamento check-in in corso...", duration=1)
                            
                            # Aggiorna lo stato della prenotazione
                            booking_id = selected_booking["Booking ID"]
                            if booking_id in bookings:
                                bookings[booking_id]["status"] = "Completata"
                                if save_bookings(bookings):
                                    show_success_animation(f"Check-in completato per {selected_booking['Utente']}!")
                                    time.sleep(1)
                                    st.rerun()
                    
                    with col2:
                        if st.button("❌ Cancella Prenotazione", key=f"cancel_checkin_{selected_checkin}"):
                            # Mostra animazione di caricamento
                            show_loading_animation("Cancellazione prenotazione in corso...", duration=1)
                            
                            # Aggiorna lo stato della prenotazione
                            booking_id = selected_booking["Booking ID"]
                            if booking_id in bookings:
                                bookings[booking_id]["status"] = "Cancellata"
                                if save_bookings(bookings):
                                    show_success_animation("Prenotazione cancellata con successo!")
                                    time.sleep(1)
                                    st.rerun()
                    
                    with col3:
                        if st.button("📝 Modifica Dettagli", key=f"edit_checkin_{selected_checkin}"):
                            st.session_state.edit_booking_id = selected_checkin
                            st.rerun()
    
    with tabs[1]:
        st.subheader("Gestione Check-out")
        
        # Filtri
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_property = st.text_input("Filtra per proprietà:", key="filter_checkout_property")
        with col2:
            filter_user = st.text_input("Filtra per utente:", key="filter_checkout_user")
        with col3:
            filter_status = st.selectbox("Stato:", ["Tutti", "Confermata", "In attesa", "Completata", "Cancellata"], key="filter_checkout_status_dropdown")
        
        # Applica i filtri
        filtered_checkout = checkout_df.copy()
        if filter_property:
            filtered_checkout = filtered_checkout[filtered_checkout["Proprietà"].str.contains(filter_property, case=False)]
        if filter_user:
            filtered_checkout = filtered_checkout[
                filtered_checkout["Utente"].str.contains(filter_user, case=False) | 
                filtered_checkout["Email"].str.contains(filter_user, case=False)
            ]
        if filter_status != "Tutti":
            filtered_checkout = filtered_checkout[filtered_checkout["Stato"] == filter_status]
        
        # Mostra la tabella
        if filtered_checkout.empty:
            st.info("Nessun check-out corrisponde ai filtri selezionati.")
        else:
            # Rimuovi la colonna Booking ID dalla visualizzazione
            display_df = filtered_checkout.drop(columns=["Booking ID"])
            st.dataframe(display_df, use_container_width=True)
            
            # Seleziona una prenotazione per completare il check-out
            st.subheader("Completa Check-out")
            selected_checkout = st.selectbox(
                "Seleziona una prenotazione:",
                options=filtered_checkout["Booking ID"].tolist(),
                format_func=lambda x: f"{next((b['ID Prenotazione'] for b in checkout_data if b['Booking ID'] == x), '')} - {next((b['Proprietà'] for b in checkout_data if b['Booking ID'] == x), '')} - {next((b['Utente'] for b in checkout_data if b['Booking ID'] == x), '')}",
                key="select_checkout_booking"
            )
            
            if selected_checkout:
                selected_booking = next((b for b in checkout_data if b["Booking ID"] == selected_checkout), None)
                
                if selected_booking:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Proprietà:** {selected_booking['Proprietà']}")
                        st.markdown(f"**Utente:** {selected_booking['Utente']}")
                        st.markdown(f"**Email:** {selected_booking['Email']}")
                    
                    with col2:
                        st.markdown(f"**Data:** {selected_booking['Data']}")
                        st.markdown(f"**Ora:** {selected_booking['Ora']}")
                        st.markdown(f"**Ospiti:** {selected_booking['Ospiti']}")
                    
                    # Azioni per il check-out
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("✅ Completa Check-out", key=f"complete_checkout_{selected_checkout}"):
                            # Mostra animazione di caricamento
                            show_loading_animation("Completamento check-out in corso...", duration=1)
                            
                            # Aggiorna lo stato della prenotazione
                            booking_id = selected_booking["Booking ID"]
                            if booking_id in bookings:
                                bookings[booking_id]["status"] = "Completata"
                                if save_bookings(bookings):
                                    show_success_animation(f"Check-out completato per {selected_booking['Utente']}!")
                                    time.sleep(1)
                                    st.rerun()
                    
                    with col2:
                        if st.button("📋 Genera Rapporto", key=f"report_checkout_{selected_checkout}"):
                            # Mostra animazione di caricamento
                            show_loading_animation("Generazione rapporto in corso...", duration=1)
                            
                            # Simula generazione rapporto
                            show_success_animation("Report generato con successo!")
                            
                            # TODO: Implement actual report generation functionality
                            
                            # Mostra un rapporto di esempio (placeholder)
                            st.markdown("""
                            ### Rapporto di Check-out (ESEMPIO)
                            
                            **Stato della proprietà:** Ottimo
                            
                            **Pulizia necessaria:** Standard
                            
                            **Danni riportati:** Nessuno
                            
                            **Note aggiuntive:** Ospite eccellente, ha lasciato la proprietà in ottime condizioni.
                            """)
    
    with tabs[2]:
        st.subheader("Aggiungi Nuova Prenotazione")
        
        # Form per aggiungere una nuova prenotazione
        with st.form("add_booking_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                property_name = st.text_input("Nome Proprietà:", placeholder="Inserisci il nome della proprietà", key="new_booking_property_name")
                property_id = st.text_input("ID Proprietà:", placeholder="Inserisci l'ID della proprietà", key="new_booking_property_id")
                user_email = st.selectbox("Email Utente:", options=user_list, key="new_booking_user_email")
                guests = st.number_input("Numero Ospiti:", min_value=1, max_value=10, value=2, key="new_booking_guests")
            
            with col2:
                check_in_date = st.date_input("Data Check-in:", key="new_booking_checkin_date")
                check_out_date = st.date_input("Data Check-out:", key="new_booking_checkout_date")
                check_in_time = st.time_input("Ora Check-in:", key="new_booking_checkin_time")
                status = st.selectbox("Stato:", options=["Confermata", "In attesa", "Completata", "Cancellata"], key="new_booking_status")
            
            special_requests = st.text_area("Richieste Speciali:", placeholder="Inserisci eventuali richieste speciali", key="new_booking_special_requests")
            
            submit_button = st.form_submit_button("Aggiungi Prenotazione")
            
            if submit_button:
                # Verifica che tutti i campi obbligatori siano compilati
                if not property_name or not property_id or not user_email:
                    st.error("Compila tutti i campi obbligatori.")
                else:
                    # Mostra animazione di caricamento
                    show_loading_animation("Aggiunta prenotazione in corso...", duration=1)
                    
                    # Crea una nuova prenotazione
                    booking_id = str(uuid.uuid4())
                    new_booking = {
                        "property_id": property_id,
                        "property_name": property_name,
                        "user_email": user_email,
                        "check_in_date": check_in_date.strftime("%d/%m/%Y"),
                        "check_out_date": check_out_date.strftime("%d/%m/%Y"),
                        "guests": guests,
                        "check_in_time": check_in_time.strftime("%H:%M"),
                        "special_requests": special_requests,
                        "status": status,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    # Aggiungi la prenotazione al database
                    bookings[booking_id] = new_booking
                    if save_bookings(bookings):
                        show_success_animation("Prenotazione aggiunta con successo!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Si è verificato un errore durante l'aggiunta della prenotazione.")