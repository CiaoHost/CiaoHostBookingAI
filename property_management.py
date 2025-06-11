import streamlit as st
import pandas as pd
import os
import json
import uuid
import time
from datetime import datetime
from utils.json_database import (
    get_all_properties, get_property, add_property, update_property, delete_property
)

def show_property_management():
    st.markdown("<h1 class='main-header'>Gestione Immobili</h1>", unsafe_allow_html=True)
    
    # Create tabs for different property management sections
    tabs = st.tabs(["Elenco Immobili", "Aggiungi Immobile", "Modifica Immobile"])
    
    with tabs[0]:
        show_property_list()
    
    with tabs[1]:
        add_new_property()
    
    with tabs[2]:
        edit_property()

def show_property_list():
    st.subheader("I Tuoi Immobili")
    
    # Get all properties
    properties = get_all_properties()
    
    if not properties:
        st.info("Non hai ancora registrato immobili. Vai alla scheda 'Aggiungi Immobile' per iniziare.")
        return
    
    # Create a DataFrame for better display
    property_list = []
    for prop in properties:
        # Count bookings for this property (if we had a bookings system)
        bookings_count = 0  # Placeholder for future booking functionality
        
        property_list.append({
            "ID": prop.get("id"),
            "Nome": prop.get("name"),
            "Città": prop.get("city"),
            "Indirizzo": prop.get("address"),
            "Tipo": prop.get("type"),
            "Camere": prop.get("bedrooms"),
            "Bagni": prop.get("bathrooms"),
            "Ospiti Max": prop.get("max_guests"),
            "Prezzo Base": f"€{prop.get('base_price'):.2f}",
            "Prezzo Attuale": f"€{prop.get('base_price'):.2f}",  # Using base_price as current_price
            "Prenotazioni": bookings_count,
            "Stato": prop.get("status", "Attivo")
        })
    
    df = pd.DataFrame(property_list)
    st.dataframe(df, use_container_width=True)
    
    # Property details expander
    st.subheader("Dettagli Immobile")
    selected_id = st.selectbox("Seleziona un immobile per vedere i dettagli", 
                              [p.get("name") for p in properties],
                              format_func=lambda x: x)
    
    if selected_id:
        selected_property = next((p for p in properties if p.get("name") == selected_id), None)
        
        if selected_property:
            with st.expander("Visualizza dettagli completi", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Nome:** {selected_property.get('name')}")
                    st.markdown(f"**Tipo:** {selected_property.get('type')}")
                    st.markdown(f"**Indirizzo:** {selected_property.get('address')}")
                    st.markdown(f"**Città:** {selected_property.get('city')}")
                    st.markdown(f"**Camere:** {selected_property.get('bedrooms')}")
                    st.markdown(f"**Bagni:** {selected_property.get('bathrooms')}")
                    st.markdown(f"**Capacità:** {selected_property.get('max_guests')} ospiti")
                
                with col2:
                    st.markdown(f"**Prezzo Base:** €{selected_property.get('base_price'):.2f}")
                    st.markdown(f"**Prezzo Attuale:** €{selected_property.get('base_price'):.2f}")
                    st.markdown(f"**Pulizie:** €{selected_property.get('cleaning_fee'):.2f}")
                    st.markdown(f"**Check-in:** {selected_property.get('check_in_instructions', 'N/A')}")
                    st.markdown(f"**WiFi:** {selected_property.get('wifi_details', 'N/A')}")
                    st.markdown(f"**Stato:** {selected_property.get('status', 'Attivo')}")
                
                st.markdown("### Descrizione")
                st.write(selected_property.get('description', 'Nessuna descrizione disponibile.'))
                
                st.markdown("### Servizi")
                amenities = selected_property.get('amenities', [])
                if amenities:
                    # Display amenities in a grid
                    amenity_cols = st.columns(3)
                    for i, amenity in enumerate(amenities):
                        amenity_cols[i % 3].markdown(f"✓ {amenity}")
                else:
                    st.info("Nessun servizio registrato.")
                
                # Property actions
                st.markdown("### Azioni")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Disattiva/Attiva", key="toggle_active"):
                        # Toggle active status
                        current_status = selected_property.get("status", "Attivo")
                        new_status = "Inattivo" if current_status == "Attivo" else "Attivo"
                        
                        # Update property with new status
                        updated_property = selected_property.copy()
                        updated_property["status"] = new_status
                        success = update_property(selected_property.get("id"), updated_property)
                        
                        if success:
                            st.success(f"Stato dell'immobile aggiornato a: {new_status}")
                            st.rerun()
                        else:
                            st.error("Si è verificato un errore durante l'aggiornamento dello stato.")
                
                with col2:
                    if st.button("Elimina", key="delete_selected"):
                        # Confirm deletion
                        st.warning("Sei sicuro di voler eliminare questo immobile?")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("Sì, elimina", key="confirm_delete"):
                                # Delete property
                                success = delete_property(selected_property.get("id"))
                                
                                if success:
                                    st.success("Immobile eliminato con successo!")
                                    st.rerun()
                                else:
                                    st.error("Si è verificato un errore durante l'eliminazione dell'immobile.")
                        
                        with col2:
                            if st.button("No, annulla", key="cancel_delete"):
                                st.rerun()

def add_new_property():
    st.subheader("Aggiungi Nuovo Immobile")
    
    with st.form("add_property_form"):
        # Basic info
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nome Immobile*", placeholder="Es: Appartamento Centro Storico")
            property_type = st.selectbox("Tipo*", 
                                        ["Appartamento", "Casa", "Villa", "B&B", "Camera Privata", "Altro"])
            city = st.text_input("Città*", placeholder="Es: Napoli")
            address = st.text_input("Indirizzo*", placeholder="Es: Via Roma, 123")
        
        with col2:
            bedrooms = st.number_input("Camere da letto*", min_value=0, value=1)
            bathrooms = st.number_input("Bagni*", min_value=0.0, value=1.0, step=0.5)
            max_guests = st.number_input("Ospiti Massimi*", min_value=1, value=2)
            base_price = st.number_input("Prezzo Base per Notte (€)*", min_value=0.0, value=50.0)
            cleaning_fee = st.number_input("Costo Pulizie (€)", min_value=0.0, value=30.0)
        
        # Property details
        st.subheader("Dettagli Immobile")
        
        # Upload property photos
        st.subheader("Foto Immobile")
        uploaded_files = st.file_uploader("Carica Foto dell'Immobile", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
        
        if uploaded_files:
            st.success(f"Caricate {len(uploaded_files)} foto")
            
            # Display thumbnails of uploaded photos
            cols = st.columns(min(4, len(uploaded_files)))
            for i, uploaded_file in enumerate(uploaded_files):
                with cols[i % 4]:
                    st.image(uploaded_file, caption=f"Foto {i+1}", width=150)
        
        check_in_instructions = st.text_area("Istruzioni Check-in", placeholder="Es: Ritirare le chiavi presso...")
        wifi_details = st.text_input("Dettagli WiFi", placeholder="Es: Nome rete: xxx, Password: yyy")
        
        # Checkout instructions
        checkout_instructions = st.text_area("Istruzioni Check-out", placeholder="Es: Lasciare le chiavi sul tavolo...")
        
        # Amenities
        st.subheader("Servizi")
        amenities_options = ["WiFi", "Aria Condizionata", "Riscaldamento", "Cucina", "Lavatrice", 
                             "Asciugatrice", "TV", "Parcheggio", "Ascensore", "Piscina", 
                             "Palestra", "Colazione", "Vista Mare", "Terrazza", "Balcone"]
        
        # Display amenities in multiple columns
        amenities_cols = st.columns(3)
        selected_amenities = []
        
        for i, amenity in enumerate(amenities_options):
            if amenities_cols[i % 3].checkbox(amenity, key=f"amenity_{i}"):
                selected_amenities.append(amenity)
        
        # Description
        st.subheader("Descrizione")
        description = st.text_area("Descrizione", 
                                placeholder="Descrivi il tuo immobile...", 
                                height=100)
        
        # Phone number
        phone = st.text_input("Numero di telefono", placeholder="Es: +39 123 456 7890")
        
        # Submit button
        submit_button = st.form_submit_button("Aggiungi Immobile")
    
    # Outside the form
    if submit_button:
        # Validate required fields
        if not (name and property_type and city and address):
            st.error("Compila tutti i campi obbligatori (contrassegnati con *).")
            return
        
        # Generate property ID
        property_id = str(uuid.uuid4())
        
        # Process and save uploaded photos
        photos = []
        if uploaded_files:
            # Create directory for property photos
            photo_dir = os.path.join("data", "property_photos", property_id)
            os.makedirs(photo_dir, exist_ok=True)
            
            for i, file in enumerate(uploaded_files):
                file_ext = os.path.splitext(file.name)[1].lower()
                photo_path = os.path.join(photo_dir, f"photo_{i+1}{file_ext}")
                
                with open(photo_path, "wb") as f:
                    f.write(file.getbuffer())
                
                photos.append(photo_path)
                
        # Prepare property data
        property_data = {
            "id": property_id,
            "name": name,
            "type": property_type,
            "city": city,
            "address": address,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "max_guests": max_guests,
            "base_price": base_price,
            "cleaning_fee": cleaning_fee,
            "check_in_instructions": check_in_instructions,
            "wifi_details": wifi_details,
            "checkout_instructions": checkout_instructions,
            "amenities": selected_amenities,
            "photos": photos,
            "status": "Attivo",
            "phone": phone,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Add property to database
        success = add_property(property_data)
        
        if success:
            # Mostra un'animazione di successo
            from loading_animations import show_success_animation
            show_success_animation(f"Immobile '{name}' aggiunto con successo!")
            time.sleep(2)  # Mostra l'animazione per 2 secondi
            st.rerun()
        else:
            # Mostra un'animazione di errore
            from loading_animations import show_error_animation
            show_error_animation("Si è verificato un errore durante l'aggiunta della proprietà.")

def edit_property():
    st.subheader("Modifica Immobile")
    
    # Check if we're editing a specific property
    property_to_edit_id = st.session_state.get("property_to_edit")
    
    # Get all properties
    properties = get_all_properties()
    
    # Property selection
    if not property_to_edit_id:
        if not properties:
            st.info("Non hai ancora registrato immobili. Vai alla scheda 'Aggiungi Immobile' per iniziare.")
            return
        
        property_to_edit_id = st.selectbox("Seleziona l'immobile da modificare",
                                         [p.get("id") for p in properties],
                                         format_func=lambda x: next((p.get("name") for p in properties if p.get("id") == x), x))
    
    # Get the selected property
    selected_property = next((p for p in properties if p.get("id") == property_to_edit_id), None)
    
    if not selected_property:
        st.error("Immobile non trovato.")
        return
    
    with st.form("edit_property_form"):
        # Basic info
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nome Immobile*", value=selected_property.get("name", ""))
            property_type = st.selectbox("Tipo*", 
                                        ["Appartamento", "Casa", "Villa", "B&B", "Camera Privata", "Altro"],
                                        index=["Appartamento", "Casa", "Villa", "B&B", "Camera Privata", "Altro"].index(selected_property.get("type", "Appartamento")) if selected_property.get("type") in ["Appartamento", "Casa", "Villa", "B&B", "Camera Privata", "Altro"] else 0)
            city = st.text_input("Città*", value=selected_property.get("city", ""))
            address = st.text_input("Indirizzo*", value=selected_property.get("address", ""))
        
        with col2:
            # Assicuriamoci che i valori siano del tipo corretto
            try:
                bedrooms_value = int(selected_property.get("bedrooms", 1))
            except (TypeError, ValueError):
                bedrooms_value = 1
                
            try:
                bathrooms_value = float(selected_property.get("bathrooms", 1.0))
            except (TypeError, ValueError):
                bathrooms_value = 1.0
                
            try:
                max_guests_value = int(selected_property.get("max_guests", 2))
            except (TypeError, ValueError):
                max_guests_value = 2
                
            try:
                base_price_value = float(selected_property.get("base_price", 50.0))
            except (TypeError, ValueError):
                base_price_value = 50.0
                
            try:
                cleaning_fee_value = float(selected_property.get("cleaning_fee", 30.0))
            except (TypeError, ValueError):
                cleaning_fee_value = 30.0
            
            bedrooms = st.number_input("Camere da letto*", min_value=0, value=bedrooms_value)
            bathrooms = st.number_input("Bagni*", min_value=0.0, value=bathrooms_value, step=0.5)
            max_guests = st.number_input("Ospiti Massimi*", min_value=1, value=max_guests_value)
            base_price = st.number_input("Prezzo Base per Notte (€)*", min_value=0.0, value=base_price_value)
            cleaning_fee = st.number_input("Costo Pulizie (€)", min_value=0.0, value=cleaning_fee_value)
        
        # Property details
        st.subheader("Dettagli Immobile")
        
        # Show existing photos
        st.subheader("Foto dell'Immobile")
        existing_photos = selected_property.get("photos", [])
        
        if existing_photos:
            st.write("Foto esistenti:")
            photo_cols = st.columns(min(4, len(existing_photos)))
            for i, photo_path in enumerate(existing_photos):
                if os.path.exists(photo_path):
                    with photo_cols[i % 4]:
                        st.image(photo_path, caption=f"Foto {i+1}", width=150)
        
        # Upload new photos
        uploaded_files = st.file_uploader("Carica Nuove Foto", 
                                         accept_multiple_files=True, 
                                         type=["jpg", "jpeg", "png"],
                                         key="edit_property_photos")
        
        if uploaded_files:
            st.success(f"Caricate {len(uploaded_files)} nuove foto")
            new_photo_cols = st.columns(min(4, len(uploaded_files)))
            for i, uploaded_file in enumerate(uploaded_files):
                with new_photo_cols[i % 4]:
                    st.image(uploaded_file, caption=f"Nuova Foto {i+1}", width=150)
                    
        # Other details
        check_in_instructions = st.text_area("Istruzioni Check-in", value=selected_property.get("check_in_instructions", ""))
        wifi_details = st.text_input("Dettagli WiFi", value=selected_property.get("wifi_details", ""))
        checkout_instructions = st.text_area("Istruzioni Check-out", value=selected_property.get("checkout_instructions", ""))
        
        # Amenities
        st.subheader("Servizi")
        amenities_options = ["WiFi", "Aria Condizionata", "Riscaldamento", "Cucina", "Lavatrice", 
                            "Asciugatrice", "TV", "Parcheggio", "Ascensore", "Piscina", 
                            "Palestra", "Colazione", "Vista Mare", "Terrazza", "Balcone"]
        
        current_amenities = selected_property.get("amenities", [])
        
        # Display amenities in multiple columns
        amenities_cols = st.columns(3)
        selected_amenities = []
        
        for i, amenity in enumerate(amenities_options):
            if amenities_cols[i % 3].checkbox(amenity, 
                                            value=amenity in current_amenities,
                                            key=f"edit_amenity_{i}"):
                selected_amenities.append(amenity)
        
        # Description
        st.subheader("Descrizione")
        description = st.text_area("Descrizione", 
                                value=selected_property.get("description", ""),
                                height=150)
        
        # Phone number
        phone = st.text_input("Numero di telefono", value=selected_property.get("phone", ""))
        
        # Status
        status = st.selectbox("Stato", ["Attivo", "Inattivo"], 
                            index=0 if selected_property.get("status", "Attivo") == "Attivo" else 1)
        
        # Submit button
        submit_button = st.form_submit_button("Aggiorna Immobile")
    
    # Outside the form
    if submit_button:
        # Validate required fields
        if not (name and property_type and city and address):
            st.error("Compila tutti i campi obbligatori (contrassegnati con *).")
            return
        
        # Process and save new uploaded photos
        photos = selected_property.get("photos", [])
        if uploaded_files:
            # Create directory for property photos if it doesn't exist
            photo_dir = os.path.join("data", "property_photos", property_to_edit_id)
            os.makedirs(photo_dir, exist_ok=True)
            
            for i, file in enumerate(uploaded_files):
                file_ext = os.path.splitext(file.name)[1].lower()
                photo_path = os.path.join(photo_dir, f"photo_{len(photos) + i + 1}{file_ext}")
                
                with open(photo_path, "wb") as f:
                    f.write(file.getbuffer())
                
                photos.append(photo_path)
        
        # Update property data
        updated_property = {
            **selected_property,  # Keep existing data
            "name": name,
            "type": property_type,
            "city": city,
            "address": address,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "max_guests": max_guests,
            "base_price": base_price,
            "cleaning_fee": cleaning_fee,
            "check_in_instructions": check_in_instructions,
            "wifi_details": wifi_details,
            "checkout_instructions": checkout_instructions,
            "amenities": selected_amenities,
            "photos": photos,
            "status": status,
            "phone": phone,
            "description": description,
            "updated_at": datetime.now().isoformat()
        }
        
        # Update property in database
        success = update_property(property_to_edit_id, updated_property)
        
        if success:
            st.success(f"Immobile '{name}' aggiornato con successo!")
            
            # Clear the editing selection
            if "property_to_edit" in st.session_state:
                del st.session_state.property_to_edit
            
            st.rerun()
        else:
            st.error("Si è verificato un errore durante l'aggiornamento dell'immobile.")
    
    # Cancel button outside the form
    if st.button("Annulla Modifiche"):
        if "property_to_edit" in st.session_state:
            del st.session_state.property_to_edit
        st.rerun()

def show_property_statistics():
    """Display statistics about properties"""
    st.subheader("Statistiche Proprietà")
    
    # Get all properties
    properties = get_all_properties()
    
    if not properties:
        st.info("Non ci sono proprietà registrate. Aggiungi proprietà per visualizzare le statistiche.")
        return
    
    # Calculate statistics
    total_properties = len(properties)
    total_bedrooms = sum(prop.get("bedrooms", 0) for prop in properties)
    total_bathrooms = sum(prop.get("bathrooms", 0) for prop in properties)
    total_capacity = sum(prop.get("max_guests", 0) for prop in properties)
    avg_price = sum(prop.get("base_price", 0) for prop in properties) / total_properties if total_properties > 0 else 0
    
    # Property types
    property_types = {}
    for prop in properties:
        prop_type = prop.get("type", "Non specificato")
        property_types[prop_type] = property_types.get(prop_type, 0) + 1
    
    # Cities
    cities = {}
    for prop in properties:
        city = prop.get("city", "Non specificata")
        cities[city] = cities.get(city, 0) + 1
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Totale Proprietà", total_properties)
        st.metric("Capacità Totale", f"{total_capacity} ospiti")
    
    with col2:
        st.metric("Camere Totali", total_bedrooms)
        st.metric("Bagni Totali", total_bathrooms)
    
    with col3:
        st.metric("Prezzo Medio", f"€{avg_price:.2f}")
    
    # Display property types chart
    if property_types:
        st.subheader("Tipi di Proprietà")
        property_types_df = pd.DataFrame({
            "Tipo": list(property_types.keys()),
            "Numero": list(property_types.values())
        })
        st.bar_chart(property_types_df.set_index("Tipo"))
    
    # Display cities chart
    if cities:
        st.subheader("Proprietà per Città")
        cities_df = pd.DataFrame({
            "Città": list(cities.keys()),
            "Numero": list(cities.values())
        })
        st.bar_chart(cities_df.set_index("Città"))
    
    # Property list by price
    st.subheader("Proprietà per Prezzo")
    price_data = [{
        "Nome": prop.get("name"),
        "Tipo": prop.get("type", ""),
        "Città": prop.get("city", ""),
        "Prezzo Base": prop.get("base_price", 0)
    } for prop in properties]
    
    price_df = pd.DataFrame(price_data)
    price_df = price_df.sort_values("Prezzo Base", ascending=False)
    st.dataframe(price_df, use_container_width=True)