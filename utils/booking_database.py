import json
import os
from datetime import datetime

BOOKINGS_DB_FILE = "DatabaseCiaoHostPrenotazioni.json"

def load_bookings_database():
    """Carica il database delle prenotazioni da file JSON"""
    if os.path.exists(BOOKINGS_DB_FILE):
        try:
            with open(BOOKINGS_DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Errore durante il caricamento del database delle prenotazioni: {e}")
            return {"bookings": {}}
    else:
        # Se il file non esiste, crea un database vuoto
        save_bookings_database({"bookings": {}})
        return {"bookings": {}}

def save_bookings_database(data):
    """Salva il database delle prenotazioni su file JSON"""
    try:
        with open(BOOKINGS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Errore durante il salvataggio del database delle prenotazioni: {e}")

def add_booking(booking_data):
    """Aggiunge una nuova prenotazione al database"""
    try:
        # Carica il database attuale
        data = load_bookings_database()
        
        # Genera un ID univoco per la prenotazione
        import uuid
        booking_id = str(uuid.uuid4())
        
        # Aggiungi timestamp
        booking_data['created_at'] = datetime.now().isoformat()
        
        # Aggiungi la prenotazione al database
        data['bookings'][booking_id] = booking_data
        
        # Salva il database aggiornato
        save_bookings_database(data)
        
        return booking_id
    except Exception as e:
        print(f"Errore durante l'aggiunta della prenotazione: {e}")
        return None

def get_all_bookings():
    """Restituisce tutte le prenotazioni nel database"""
    data = load_bookings_database()
    return data.get('bookings', {})