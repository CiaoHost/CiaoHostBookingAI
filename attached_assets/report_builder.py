import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime, timedelta
import os
import plotly.express as px
import plotly.graph_objects as go
from utils.database import get_all_properties, get_property, get_all_bookings, get_all_invoices, get_booking
from utils.pdf_export import create_property_report_pdf, create_financial_report_pdf
from utils.report_generator import generate_report_template, add_section_to_report, render_report_in_streamlit, generate_pdf_report, download_report, generate_ai_report

def show_report_builder():
    main()

def main():
    st.markdown("<h1 class='main-header'>Gestione Fiscale</h1>", unsafe_allow_html=True)
    
    # Aggiungi CSS per forzare il tema chiaro
    st.markdown("""
    <style>
    /* Force light theme everywhere */
    html, body, [class*="css"], [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"],
    [data-testid="stSidebarNav"], [data-testid="stSidebarUserContent"], .stApp, .stTabs, .stTabContent {
        background-color: white !important;
        color: #333333 !important;
    }
    
    /* Main header styling */
    .main-header {
        color: #4361ee !important;
        font-size: 2.2rem !important;
        margin-bottom: 1rem !important;
        font-weight: bold !important;
    }
    
    /* Force all text to be dark */
    p, h1, h2, h3, h4, h5, h6, span, div, label, button, a, li, ul, ol, th, td {
        color: #333333 !important;
    }
    
    /* Force all tables to have light background */
    table, th, td, tr, [data-testid="stTable"], [data-testid="stDataFrame"], div[data-testid="stDataFrameContainer"] {
        background-color: white !important;
        color: #333333 !important;
        border-color: #dee2e6 !important;
    }
    
    /* Style for tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #333333 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4361ee !important;
        color: white !important;
    }
    .card {
        background-color: white !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 5px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    /* Style for buttons */
    .stButton>button {
        background-color: #4361ee !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
    }
    .stButton>button:hover {
        background-color: #3a56d4 !important;
    }
    
    /* Style for selectbox and input */
    .stSelectbox>div>div, .stDateInput>div>div {
        border-radius: 4px !important;
        background-color: white !important;
        color: #333333 !important;
    }
    
    /* Style for tables */
    .dataframe {
        border-collapse: collapse !important;
        width: 100% !important;
    }
    .dataframe th {
        background-color: #f8f9fa !important;
        color: #333333 !important;
        padding: 8px !important;
        text-align: left !important;
        font-weight: bold !important;
        border: 1px solid #dee2e6 !important;
    }
    .dataframe td {
        padding: 8px !important;
        border: 1px solid #dee2e6 !important;
        background-color: white !important;
        color: #333333 !important;
    }
    .dataframe tr:nth-child(even) {
        background-color: #f8f9fa !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Forza sempre la modalità chiara
    st.markdown('<div class="light-mode">', unsafe_allow_html=True)
    
    # Carica i dati direttamente dal file JSON
    try:
        # Percorso del file JSON
        json_file_path = "c:/Users/DEADSHOT/Desktop/ciaohostreale/ciaohostluss/DatabaseCiaoHostProprieta.json"
        
        # Leggi il file JSON
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Estrai le proprietà
        properties_dict = data.get('properties', {})
        
        # Converti le proprietà in una lista di dizionari
        properties_list = []
        for prop_id, prop_data in properties_dict.items():
            prop_data['id'] = prop_id  # Aggiungi l'ID come campo
            properties_list.append(prop_data)
        
        # Crea il dataframe delle proprietà
        df_properties = pd.DataFrame(properties_list)
        
        # Se non ci sono proprietà, mostra un messaggio di avviso
        if df_properties.empty:
            st.warning("Non ci sono immobili nel database. Aggiungi almeno un immobile per utilizzare la Gestione Fiscale.")
            return
        
        # Creiamo dati di esempio per le fatture basati sulle proprietà esistenti
        invoices_list = []
        
        # Crea alcune fatture di esempio per ogni proprietà
        for idx, prop in enumerate(properties_list):
            prop_id = prop['id']
            prop_name = prop.get('name', f"Proprietà {idx+1}")
            
            # Crea 3 fatture per ogni proprietà (una per trimestre)
            for quarter in range(1, 4):
                month = quarter * 3
                invoices_list.append({
                    'id': f"inv_{idx}_{quarter}",
                    'property_id': prop_id,
                    'property_name': prop_name,
                    'guest_name': f"Cliente {idx*3+quarter}",
                    'invoice_date': f"2024-{month:02d}-15",
                    'amount': round(prop.get('price', 100) * 7 * (1 + 0.1 * quarter), 2),  # Prezzo base + variazione per trimestre
                    'tax_amount': round(prop.get('price', 100) * 7 * 0.22, 2),  # 22% IVA
                    'total_amount': round(prop.get('price', 100) * 7 * (1 + 0.1 * quarter) * 1.22, 2),  # Totale con IVA
                    'status': 'Pagata' if quarter < 3 else 'Da pagare',
                    'payment_method': 'Bonifico' if quarter % 2 == 0 else 'Carta di credito',
                    'invoice_number': f"2024/{quarter}/{idx+1}",
                    'stay_period': f"2024-{month:02d}-01 - 2024-{month:02d}-08"
                })
        
        # Crea il dataframe delle fatture
        df_invoices = pd.DataFrame(invoices_list)
        
        # Informa l'utente che stiamo utilizzando dati di esempio per le fatture
        st.info("Utilizzo dati di esempio per le fatture. Le proprietà sono caricate dal database reale.")
            
    except Exception as e:
        st.error(f"Errore nel caricamento dei dati: {str(e)}")
        
        # Crea dati di esempio per dimostrare la funzionalità
        st.info("Utilizzo dati di esempio per dimostrare la funzionalità della Gestione Fiscale.")
        
        # Crea dataframe di esempio per le proprietà
        df_properties = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Villa Mare', 'Appartamento Centro', 'Casa Montagna'],
            'location': ['Rimini', 'Milano', 'Cortina'],
            'bedrooms': [4, 2, 3],
            'bathrooms': [3, 1, 2],
            'max_guests': [8, 4, 6],
            'price': [250, 120, 180]
        })
        
        # Crea una lista di proprietà di esempio
        properties_list = []
        for i in range(len(df_properties)):
            prop = {
                'id': df_properties.iloc[i]['id'],
                'name': df_properties.iloc[i]['name'],
                'location': df_properties.iloc[i]['location'],
                'bedrooms': df_properties.iloc[i]['bedrooms'],
                'bathrooms': df_properties.iloc[i]['bathrooms'],
                'max_guests': df_properties.iloc[i]['max_guests'],
                'price': df_properties.iloc[i]['price']
            }
            properties_list.append(prop)
        
        # Crea dataframe di esempio per le fatture
        df_invoices = pd.DataFrame({
            'id': [101, 102, 103, 104, 105, 106],
            'property_id': [1, 2, 3, 1, 2, 3],
            'property_name': ['Villa Mare', 'Appartamento Centro', 'Casa Montagna', 'Villa Mare', 'Appartamento Centro', 'Casa Montagna'],
            'guest_name': ['Mario Rossi', 'Giulia Bianchi', 'Paolo Verdi', 'Laura Neri', 'Marco Gialli', 'Anna Blu'],
            'invoice_date': ['2024-01-15', '2024-02-10', '2024-03-05', '2024-04-20', '2024-05-12', '2024-06-08'],
            'amount': [1500, 600, 1260, 2250, 600, 1260],
            'tax_amount': [330, 132, 277.2, 495, 132, 277.2],
            'total_amount': [1830, 732, 1537.2, 2745, 732, 1537.2],
            'status': ['Pagata', 'Pagata', 'Pagata', 'Pagata', 'Da pagare', 'Da pagare'],
            'payment_method': ['Bonifico', 'Carta di credito', 'Bonifico', 'Carta di credito', 'Bonifico', 'Carta di credito'],
            'invoice_number': ['2024/1/1', '2024/1/2', '2024/1/3', '2024/2/1', '2024/2/2', '2024/2/3'],
            'stay_period': ['2024-01-01 - 2024-01-08', '2024-02-05 - 2024-02-10', '2024-03-01 - 2024-03-08', 
                           '2024-04-15 - 2024-04-22', '2024-05-10 - 2024-05-15', '2024-06-01 - 2024-06-08']
        })
    
    # Create tabs
    tabs = st.tabs(["Archivio Fiscale", "Gestione Ospiti", "Generazione Fatture", "Esportazione", "Impostazioni Fiscali"])
    
    with tabs[0]:
        show_fiscal_archive(df_invoices, df_properties, properties_list)
        
    with tabs[1]:
        show_guests(df_invoices, properties_list)
        
    with tabs[2]:
        generate_invoices(df_properties, properties_list)
        
    with tabs[3]:
        export_fiscal_data(df_invoices, df_properties)
        
    with tabs[4]:
        fiscal_settings()
    
    # Chiudi il div della modalità
    st.markdown('</div>', unsafe_allow_html=True)

def show_fiscal_archive(df_invoices, df_properties, properties_list):
    """Mostra l'archivio fiscale con filtri e statistiche"""
    st.subheader("Archivio Fiscale")
    st.markdown("Visualizza e analizza i dati fiscali relativi ai tuoi immobili.")
    
    # Crea due colonne per i filtri
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtro per anno
        current_year = datetime.now().year
        year_options = list(range(current_year-2, current_year+1))
        selected_year = st.selectbox("Anno", options=year_options, index=len(year_options)-1, key="archive_year")
        
        # Filtro per immobile
        property_options = {p.get('id', str(i)): p.get('name', f"Proprietà {i+1}") 
                          for i, p in enumerate(properties_list)}
        property_options["all"] = "Tutti gli Immobili"
        
        selected_property = st.selectbox(
            "Immobile",
            options=["all"] + [k for k in property_options.keys() if k != "all"],
            format_func=lambda x: property_options.get(x, x),
            key="archive_property"
        )
    
    with col2:
        # Filtro per trimestre
        quarter_options = {
            "all": "Tutto l'anno",
            "1": "1° Trimestre (Gen-Mar)",
            "2": "2° Trimestre (Apr-Giu)",
            "3": "3° Trimestre (Lug-Set)",
            "4": "4° Trimestre (Ott-Dic)"
        }
        selected_quarter = st.selectbox(
            "Periodo",
            options=list(quarter_options.keys()),
            format_func=lambda x: quarter_options[x],
            key="archive_quarter"
        )
        
        # Filtro per stato pagamento
        status_options = ["Tutti", "Pagata", "Da pagare"]
        selected_status = st.selectbox("Stato Pagamento", options=status_options, key="archive_status")
    
    # Applica i filtri
    filtered_df = df_invoices.copy()
    
    # Filtra per anno
    filtered_df = filtered_df[filtered_df['invoice_date'].str.startswith(str(selected_year))]
    
    # Filtra per immobile
    if selected_property != "all":
        filtered_df = filtered_df[filtered_df['property_id'] == selected_property]
    
    # Filtra per trimestre
    if selected_quarter != "all":
        q = int(selected_quarter)
        start_month = (q - 1) * 3 + 1
        end_month = q * 3
        month_filter = [f"{selected_year}-{m:02d}" for m in range(start_month, end_month + 1)]
        filtered_df = filtered_df[filtered_df['invoice_date'].str[:7].isin(month_filter)]
    
    # Filtra per stato pagamento
    if selected_status != "Tutti":
        filtered_df = filtered_df[filtered_df['status'] == selected_status]
    
    # Mostra statistiche
    st.subheader("Riepilogo")
    
    # Crea tre colonne per le statistiche
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_invoices = len(filtered_df)
        st.markdown(f"""
        <div class="card">
            <h3>Fatture</h3>
            <p style="font-size: 2rem; font-weight: bold; color: #1E88E5;">{total_invoices}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_amount = filtered_df['total_amount'].sum()
        st.markdown(f"""
        <div class="card">
            <h3>Totale Fatturato</h3>
            <p style="font-size: 2rem; font-weight: bold; color: #1E88E5;">€ {total_amount:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_tax = filtered_df['tax_amount'].sum()
        st.markdown(f"""
        <div class="card">
            <h3>Totale IVA</h3>
            <p style="font-size: 2rem; font-weight: bold; color: #1E88E5;">€ {total_tax:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mostra grafico di distribuzione per immobile
    if not filtered_df.empty:
        st.subheader("Distribuzione Fatturato per Immobile")
        
        # Raggruppa per immobile
        property_summary = filtered_df.groupby('property_name')['total_amount'].sum().reset_index()
        
        # Crea il grafico
        fig = px.pie(
            property_summary, 
            values='total_amount', 
            names='property_name',
            title='Distribuzione Fatturato per Immobile',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostra grafico di andamento mensile
        st.subheader("Andamento Mensile")
        
        # Estrai mese e anno dalla data della fattura
        filtered_df['month'] = pd.to_datetime(filtered_df['invoice_date']).dt.strftime('%Y-%m')
        
        # Raggruppa per mese
        monthly_summary = filtered_df.groupby('month')['total_amount'].sum().reset_index()
        
        # Ordina per mese
        monthly_summary = monthly_summary.sort_values('month')
        
        # Crea il grafico
        fig = px.line(
            monthly_summary, 
            x='month', 
            y='total_amount',
            title='Andamento Mensile del Fatturato',
            labels={'month': 'Mese', 'total_amount': 'Fatturato (€)'},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Mostra la tabella delle fatture
    st.subheader("Elenco Fatture")
    
    if filtered_df.empty:
        st.info("Nessuna fattura trovata con i filtri selezionati.")
    else:
        # Seleziona e rinomina le colonne da visualizzare
        display_df = filtered_df[['invoice_number', 'property_name', 'guest_name', 'invoice_date', 'total_amount', 'status']]
        display_df.columns = ['Numero Fattura', 'Immobile', 'Cliente', 'Data', 'Importo (€)', 'Stato']
        
        # Formatta l'importo
        display_df['Importo (€)'] = display_df['Importo (€)'].apply(lambda x: f"{x:,.2f}")
        
        # Mostra la tabella
        st.dataframe(display_df, use_container_width=True)
        
        # Pulsante per esportare i dati
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Esporta Dati in CSV",
            data=csv,
            file_name=f"archivio_fiscale_{selected_year}.csv",
            mime="text/csv",
            key="archive_download"
        )

def show_guests(df_invoices, properties_list):
    """Mostra e gestisce gli ospiti che hanno soggiornato negli immobili"""
    st.subheader("Gestione Ospiti")
    st.markdown("Visualizza e gestisci gli ospiti che hanno soggiornato nei tuoi immobili.")
    
    # Crea tre colonne per i filtri
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filtro per immobile
        property_options = {p.get('id', str(i)): p.get('name', f"Proprietà {i+1}") 
                          for i, p in enumerate(properties_list)}
        property_options["all"] = "Tutti gli Immobili"
        
        selected_property = st.selectbox(
            "Immobile",
            options=["all"] + [k for k in property_options.keys() if k != "all"],
            format_func=lambda x: property_options.get(x, x),
            key="guest_property"
        )
    
    with col2:
        # Filtro per periodo
        period_options = ["Settimana", "Mese", "Anno", "Tutto"]
        selected_period = st.selectbox("Periodo", options=period_options, key="guest_period")
    
    with col3:
        # Filtro per stato pagamento
        status_options = ["Tutti", "Pagata", "Da pagare"]
        selected_status = st.selectbox("Stato Pagamento", options=status_options, key="guest_status")
    
    # Applica i filtri
    filtered_df = df_invoices.copy()
    
    # Filtra per immobile
    if selected_property != "all":
        filtered_df = filtered_df[filtered_df['property_id'] == selected_property]
    
    # Filtra per stato pagamento
    if selected_status != "Tutti":
        filtered_df = filtered_df[filtered_df['status'] == selected_status]
    
    # Filtra per periodo
    today = datetime.now().date()
    if selected_period == "Settimana":
        # Filtra per l'ultima settimana
        one_week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        filtered_df = filtered_df[filtered_df['invoice_date'] >= one_week_ago]
    elif selected_period == "Mese":
        # Filtra per l'ultimo mese
        one_month_ago = today.replace(day=1).strftime("%Y-%m-%d")
        filtered_df = filtered_df[filtered_df['invoice_date'] >= one_month_ago]
    elif selected_period == "Anno":
        # Filtra per l'anno corrente
        current_year = today.strftime("%Y")
        filtered_df = filtered_df[filtered_df['invoice_date'].str.startswith(current_year)]
    
    # Aggiungi colonna per il numero di notti
    filtered_df['nights'] = filtered_df['stay_period'].apply(lambda x: 
        (datetime.strptime(x.split(' - ')[1], "%Y-%m-%d") - 
         datetime.strptime(x.split(' - ')[0], "%Y-%m-%d")).days
    )
    
    # Mostra la tabella degli ospiti
    if filtered_df.empty:
        st.info("Nessun ospite trovato con i filtri selezionati.")
    else:
        # Ordina per data (più recenti prima)
        filtered_df = filtered_df.sort_values('invoice_date', ascending=False)
        
        # Crea una tabella con le informazioni richieste
        guest_table = filtered_df[['guest_name', 'property_name', 'stay_period', 'nights', 'total_amount', 'status', 'invoice_number', 'id']]
        guest_table.columns = ['Ospite', 'Immobile', 'Periodo Soggiorno', 'Notti', 'Importo Pagato (€)', 'Stato Pagamento', 'Numero Fattura', 'ID']
        
        # Formatta l'importo
        guest_table['Importo Pagato (€)'] = guest_table['Importo Pagato (€)'].apply(lambda x: f"€ {x:,.2f}")
        
        # Nascondi la colonna ID
        guest_table_display = guest_table.drop(columns=['ID'])
        
        # Mostra la tabella
        st.dataframe(guest_table_display, use_container_width=True)
        
        # Aggiungi pulsante per esportare i dati
        csv = guest_table_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Esporta Elenco Ospiti in CSV",
            data=csv,
            file_name=f"elenco_ospiti_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
        )
        
        # Sezione per visualizzare i dettagli dell'ospite selezionato
        st.subheader("Dettagli Ospite")
        
        # Seleziona un ospite dalla tabella
        guest_options = {row['id']: f"{row['guest_name']} - {row['stay_period']}" for _, row in filtered_df.iterrows()}
        selected_guest_id = st.selectbox(
            "Seleziona un ospite per visualizzare i dettagli",
            options=list(guest_options.keys()),
            format_func=lambda x: guest_options[x],
            key="selected_guest"
        )
        
        # Mostra i dettagli dell'ospite selezionato
        selected_guest = filtered_df[filtered_df['id'] == selected_guest_id].iloc[0]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            status_color = "#4CAF50" if selected_guest['status'] == "Pagata" else "#FF9800"
            
            st.markdown(f"""
            <div class="card">
                <h3>Ospite: {selected_guest['guest_name']}</h3>
                <p><strong>Immobile:</strong> {selected_guest['property_name']}</p>
                <p><strong>Periodo Soggiorno:</strong> {selected_guest['stay_period']}</p>
                <p><strong>Numero Notti:</strong> {selected_guest['nights']}</p>
                <p><strong>Data Fattura:</strong> {selected_guest['invoice_date']}</p>
                <p><strong>Importo Base:</strong> € {selected_guest['amount']:,.2f}</p>
                <p><strong>IVA:</strong> € {selected_guest['tax_amount']:,.2f}</p>
                <p><strong>Totale Pagato:</strong> € {selected_guest['total_amount']:,.2f}</p>
                <p><strong>Metodo Pagamento:</strong> {selected_guest['payment_method']}</p>
                <p><strong>Stato Pagamento:</strong> <span style="color: {status_color}; font-weight: bold;">{selected_guest['status']}</span></p>
                <p><strong>Numero Fattura:</strong> {selected_guest['invoice_number']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
            
            # Pulsanti per le azioni
            if st.button("Visualizza Fattura", key=f"view_invoice_{selected_guest_id}"):
                st.info(f"Visualizzazione della fattura {selected_guest['invoice_number']} (funzionalità dimostrativa)")
            
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
            
            if st.button("Contatta Ospite", key=f"contact_{selected_guest_id}"):
                st.success(f"Invio messaggio all'ospite {selected_guest['guest_name']} (funzionalità dimostrativa)")
            
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
            
            if selected_guest['status'] == "Da pagare":
                if st.button("Registra Pagamento", key=f"pay_{selected_guest_id}"):
                    st.success(f"Pagamento registrato per l'ospite {selected_guest['guest_name']} (funzionalità dimostrativa)")
            
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
            
            if st.button("Stampa Ricevuta", key=f"receipt_{selected_guest_id}"):
                st.info(f"Stampa ricevuta per l'ospite {selected_guest['guest_name']} (funzionalità dimostrativa)")
        
        # Aggiungi una sezione per le note sull'ospite
        st.subheader("Note sull'Ospite")
        guest_notes = st.text_area(
            "Aggiungi note sull'ospite",
            value="",
            height=100,
            key=f"notes_{selected_guest_id}"
        )
        
        if st.button("Salva Note"):
            st.success("Note salvate con successo (funzionalità dimostrativa)")
            
        # Statistiche sull'ospite
        if st.checkbox("Mostra Statistiche Ospite", value=False):
            st.subheader("Statistiche Ospite")
            
            # Simuliamo alcune statistiche
            st.markdown(f"""
            <div class="card">
                <p><strong>Numero Soggiorni Totali:</strong> {1 + int(selected_guest_id) % 3}</p>
                <p><strong>Totale Speso:</strong> € {selected_guest['total_amount'] * (1 + int(selected_guest_id) % 3):,.2f}</p>
                <p><strong>Durata Media Soggiorno:</strong> {selected_guest['nights'] + int(selected_guest_id) % 2} notti</p>
                <p><strong>Ultimo Soggiorno:</strong> {selected_guest['stay_period']}</p>
            </div>
            """, unsafe_allow_html=True)

def generate_invoices(df_properties, properties_list):
    """Genera nuove fatture"""
    st.subheader("Generazione Fatture")
    st.markdown("Crea nuove fatture per i tuoi immobili e clienti.")
    
    # Form per la creazione di una nuova fattura
    with st.form("new_invoice_form"):
        st.subheader("Nuova Fattura")
        
        # Seleziona immobile
        property_options = {p.get('id', str(i)): p.get('name', f"Proprietà {i+1}") 
                          for i, p in enumerate(properties_list)}
        
        selected_property_id = st.selectbox(
            "Immobile",
            options=list(property_options.keys()),
            format_func=lambda x: property_options.get(x, x),
            key="form_property_select"
        )
        
        # Recupera i dettagli dell'immobile selezionato
        selected_property = next((p for p in properties_list if p.get('id') == selected_property_id), None)
        property_price = selected_property.get('price', 100) if selected_property else 100
        
        # Dati cliente
        col1, col2 = st.columns(2)
        
        with col1:
            guest_name = st.text_input("Nome Cliente", value="", key="form_guest_name")
            guest_email = st.text_input("Email Cliente", value="", key="form_guest_email")
        
        with col2:
            guest_phone = st.text_input("Telefono Cliente", value="", key="form_guest_phone")
            guest_address = st.text_input("Indirizzo Cliente", value="", key="form_guest_address")
        
        # Dati soggiorno
        col1, col2 = st.columns(2)
        
        with col1:
            check_in = st.date_input("Data Check-in", value=datetime.now().date(), key="form_check_in")
        
        with col2:
            check_out = st.date_input("Data Check-out", value=datetime.now().date() + timedelta(days=7), key="form_check_out")
        
        # Calcola la durata del soggiorno
        stay_duration = (check_out - check_in).days
        
        # Dati fattura
        col1, col2, col3 = st.columns(3)
        
        with col1:
            invoice_date = st.date_input("Data Fattura", value=datetime.now().date(), key="form_invoice_date")
            invoice_number = st.text_input("Numero Fattura", value=f"{datetime.now().year}/{datetime.now().month}/{len(properties_list)+1}", key="form_invoice_number")
        
        with col2:
            base_amount = st.number_input("Importo Base (€)", value=float(property_price * stay_duration), step=10.0, key="form_base_amount")
            tax_rate = st.number_input("Aliquota IVA (%)", value=22.0, min_value=0.0, max_value=100.0, step=1.0, key="form_tax_rate")
        
        with col3:
            payment_method = st.selectbox(
                "Metodo Pagamento", 
                options=["Bonifico", "Carta di credito", "Contanti", "PayPal"],
                key="form_payment_method"
            )
            payment_status = st.selectbox(
                "Stato Pagamento", 
                options=["Da pagare", "Pagata"],
                key="form_payment_status"
            )
        
        # Calcola importi
        tax_amount = base_amount * (tax_rate / 100)
        total_amount = base_amount + tax_amount
        
        # Mostra riepilogo
        st.subheader("Riepilogo Importi")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Importo Base", f"€ {base_amount:.2f}")
        
        with col2:
            st.metric("IVA", f"€ {tax_amount:.2f}")
        
        with col3:
            st.metric("Totale", f"€ {total_amount:.2f}")
        
        # Pulsante per generare la fattura
        submitted = st.form_submit_button("Genera Fattura")
        
        if submitted:
            st.success(f"Fattura {invoice_number} generata con successo per {guest_name} (funzionalità dimostrativa)")
            
            # Qui si potrebbe salvare la fattura nel database
            st.balloons()
    
    # Sezione per la generazione automatica di fatture
    st.subheader("Generazione Automatica")
    st.markdown("Genera automaticamente fatture per prenotazioni esistenti.")
    
    with st.form(key="auto_generate_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            auto_property = st.selectbox(
                "Immobile",
                options=["all"] + list(property_options.keys()),
                format_func=lambda x: "Tutti gli Immobili" if x == "all" else property_options.get(x, x),
                key="auto_property_select"
            )
        
        with col2:
            period_options = {
                "current_month": "Mese Corrente",
                "last_month": "Mese Precedente",
                "current_quarter": "Trimestre Corrente",
                "custom": "Periodo Personalizzato"
            }
            auto_period = st.selectbox(
                "Periodo", 
                options=list(period_options.keys()), 
                format_func=lambda x: period_options[x],
                key="auto_period_select"
            )
        
        if auto_period == "custom":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Data Inizio", value=datetime.now().replace(day=1).date(), key="auto_start_date")
            with col2:
                end_date = st.date_input("Data Fine", value=datetime.now().date(), key="auto_end_date")
        
        # Pulsante di invio del form
        submitted = st.form_submit_button("Genera Fatture Automaticamente")
        
        if submitted:
            st.success("Fatture generate automaticamente (funzionalità dimostrativa)")
            st.info("Sono state generate 3 nuove fatture per le prenotazioni nel periodo selezionato.")

def export_fiscal_data(df_invoices, df_properties):
    """Esporta dati fiscali in vari formati"""
    st.subheader("Esportazione Dati Fiscali")
    st.markdown("Esporta i dati fiscali in vari formati per la contabilità e la dichiarazione dei redditi.")
    
    # Filtri per l'esportazione
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtro per anno
        current_year = datetime.now().year
        year_options = list(range(current_year-2, current_year+1))
        export_year = st.selectbox("Anno", options=year_options, index=len(year_options)-1, key="export_year")
    
    with col2:
        # Filtro per periodo
        period_options = {
            "full_year": "Anno Completo",
            "q1": "1° Trimestre (Gen-Mar)",
            "q2": "2° Trimestre (Apr-Giu)",
            "q3": "3° Trimestre (Lug-Set)",
            "q4": "4° Trimestre (Ott-Dic)",
            "custom": "Periodo Personalizzato"
        }
        export_period = st.selectbox("Periodo", options=list(period_options.keys()), 
                                   format_func=lambda x: period_options[x], key="export_period")
    
    if export_period == "custom":
        col1, col2 = st.columns(2)
        with col1:
            export_start_date = st.date_input("Data Inizio", value=datetime(export_year, 1, 1).date(), key="export_start")
        with col2:
            export_end_date = st.date_input("Data Fine", value=datetime(export_year, 12, 31).date(), key="export_end")
    
    # Filtra i dati in base ai criteri selezionati
    filtered_df = df_invoices.copy()
    
    # Filtra per anno
    filtered_df = filtered_df[filtered_df['invoice_date'].str.startswith(str(export_year))]
    
    # Filtra per periodo
    if export_period == "q1":
        month_filter = [f"{export_year}-{m:02d}" for m in range(1, 4)]
        filtered_df = filtered_df[filtered_df['invoice_date'].str[:7].isin(month_filter)]
    elif export_period == "q2":
        month_filter = [f"{export_year}-{m:02d}" for m in range(4, 7)]
        filtered_df = filtered_df[filtered_df['invoice_date'].str[:7].isin(month_filter)]
    elif export_period == "q3":
        month_filter = [f"{export_year}-{m:02d}" for m in range(7, 10)]
        filtered_df = filtered_df[filtered_df['invoice_date'].str[:7].isin(month_filter)]
    elif export_period == "q4":
        month_filter = [f"{export_year}-{m:02d}" for m in range(10, 13)]
        filtered_df = filtered_df[filtered_df['invoice_date'].str[:7].isin(month_filter)]
    elif export_period == "custom":
        start_str = export_start_date.strftime("%Y-%m-%d")
        end_str = export_end_date.strftime("%Y-%m-%d")
        filtered_df = filtered_df[(filtered_df['invoice_date'] >= start_str) & (filtered_df['invoice_date'] <= end_str)]
    
    # Mostra anteprima dei dati
    st.subheader("Anteprima Dati")
    
    if filtered_df.empty:
        st.info("Nessun dato disponibile per il periodo selezionato.")
    else:
        # Seleziona e rinomina le colonne da visualizzare
        display_df = filtered_df[['invoice_number', 'property_name', 'guest_name', 'invoice_date', 'amount', 'tax_amount', 'total_amount', 'status']]
        display_df.columns = ['Numero Fattura', 'Immobile', 'Cliente', 'Data', 'Imponibile (€)', 'IVA (€)', 'Totale (€)', 'Stato']
        
        # Formatta gli importi
        for col in ['Imponibile (€)', 'IVA (€)', 'Totale (€)']:
            display_df[col] = display_df[col].apply(lambda x: f"{x:,.2f}")
        
        # Mostra la tabella
        st.dataframe(display_df, use_container_width=True)
        
        # Riepilogo
        st.subheader("Riepilogo")
        
        total_taxable = filtered_df['amount'].sum()
        total_tax = filtered_df['tax_amount'].sum()
        total_amount = filtered_df['total_amount'].sum()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Totale Imponibile", f"€ {total_taxable:,.2f}")
        
        with col2:
            st.metric("Totale IVA", f"€ {total_tax:,.2f}")
        
        with col3:
            st.metric("Totale Fatturato", f"€ {total_amount:,.2f}")
        
        # Opzioni di esportazione
        st.subheader("Opzioni di Esportazione")
        
        export_format = st.radio(
            "Formato di Esportazione",
            options=["CSV", "Excel", "PDF", "XML (Fattura Elettronica)"],
            horizontal=True,
            key="export_format"
        )
        
        # Pulsante per esportare
        if export_format == "CSV":
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Esporta in CSV",
                data=csv,
                file_name=f"dati_fiscali_{export_year}.csv",
                mime="text/csv",
                key="download_csv"
            )
        elif export_format == "Excel":
            # Crea un buffer per il file Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                display_df.to_excel(writer, sheet_name='Fatture', index=False)
                
                # Accedi al workbook e al worksheet
                workbook = writer.book
                worksheet = writer.sheets['Fatture']
                
                # Aggiungi formattazione
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',
                    'border': 1
                })
                
                # Applica la formattazione all'intestazione
                for col_num, value in enumerate(display_df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    
                # Imposta la larghezza delle colonne
                worksheet.set_column('A:A', 15)  # Numero Fattura
                worksheet.set_column('B:B', 20)  # Immobile
                worksheet.set_column('C:C', 20)  # Cliente
                worksheet.set_column('D:D', 12)  # Data
                worksheet.set_column('E:G', 15)  # Importi
                worksheet.set_column('H:H', 10)  # Stato
            
            # Prepara il file per il download
            output.seek(0)
            
            st.download_button(
                label="Esporta in Excel",
                data=output,
                file_name=f"dati_fiscali_{export_year}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_excel"
            )
        elif export_format == "PDF":
            st.info("Esportazione in PDF (funzionalità dimostrativa)")
            st.warning("Per generare PDF è necessario installare librerie aggiuntive come WeasyPrint o ReportLab.")
        else:  # XML
            st.info("Esportazione in formato Fattura Elettronica XML (funzionalità dimostrativa)")
            st.warning("Per generare file XML conformi allo standard di Fatturazione Elettronica è necessario implementare le specifiche tecniche dell'Agenzia delle Entrate.")

def fiscal_settings():
    """Impostazioni fiscali"""
    st.subheader("Impostazioni Fiscali")
    st.markdown("Configura le impostazioni fiscali per la tua attività.")
    
    # Dati azienda
    st.subheader("Dati Azienda")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Ragione Sociale", value="CiaoHost Srl", key="company_name")
        company_address = st.text_input("Indirizzo", value="Via Roma 123", key="company_address")
        company_city = st.text_input("Città", value="Milano", key="company_city")
    
    with col2:
        company_vat = st.text_input("Partita IVA", value="IT12345678901", key="company_vat")
        company_tax_code = st.text_input("Codice Fiscale", value="ABCDEF12G34H567I", key="company_tax_code")
        company_rea = st.text_input("REA", value="MI-1234567", key="company_rea")
    
    # Impostazioni IVA
    st.subheader("Impostazioni IVA")
    
    vat_regime = st.selectbox(
        "Regime Fiscale",
        options=["Ordinario", "Forfettario", "Regime di Vantaggio"],
        key="vat_regime"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_vat_rate = st.number_input("Aliquota IVA Predefinita (%)", value=22.0, min_value=0.0, max_value=100.0, step=1.0, key="default_vat_rate")
    
    with col2:
        vat_payment_frequency = st.selectbox(
            "Frequenza Liquidazione IVA",
            options=["Mensile", "Trimestrale", "Annuale"],
            key="vat_payment_frequency"
        )
    
    # Impostazioni fatturazione
    st.subheader("Impostazioni Fatturazione")
    
    col1, col2 = st.columns(2)
    
    with col1:
        invoice_prefix = st.text_input("Prefisso Numero Fattura", value="CIAOHOST-", key="invoice_prefix")
        next_invoice_number = st.number_input("Prossimo Numero Fattura", value=1, min_value=1, step=1, key="next_invoice_number")
    
    with col2:
        invoice_notes = st.text_area("Note Predefinite in Fattura", value="Grazie per aver scelto CiaoHost!", key="invoice_notes")
        auto_send_invoice = st.checkbox("Invia automaticamente le fatture via email", value=True, key="auto_send_invoice")
    
    # Impostazioni contabili
    st.subheader("Impostazioni Contabili")
    
    accounting_method = st.selectbox(
        "Metodo Contabile",
        options=["Competenza", "Cassa"],
        key="accounting_method"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        fiscal_year_start = st.date_input("Inizio Anno Fiscale", value=datetime(datetime.now().year, 1, 1).date(), key="fiscal_year_start")
    
    with col2:
        fiscal_year_end = st.date_input("Fine Anno Fiscale", value=datetime(datetime.now().year, 12, 31).date(), key="fiscal_year_end")
    
    # Pulsante per salvare le impostazioni
    if st.button("Salva Impostazioni", key="save_settings"):
        st.success("Impostazioni fiscali salvate con successo (funzionalità dimostrativa)")

def build_custom_report(df, properties=None):
    """Build a custom report with user-defined sections"""
    st.subheader("Crea Report Personalizzato")
    st.markdown("Costruisci un report personalizzato selezionando i dati, gli intervalli e le visualizzazioni che desideri includere.")
    
    # Initialize report structure if not exists
    if 'current_report' not in st.session_state:
        st.session_state.current_report = generate_report_template(
            title="Report Personalizzato",
            description="Report personalizzato creato con CiaoHost Report Builder",
            sections=[],
            author="",
            date=datetime.now().strftime("%d/%m/%Y")
        )
    
    # Report basic info
    with st.expander("Informazioni Report", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            report_title = st.text_input("Titolo Report", value=st.session_state.current_report.get("title", ""), key="report_title")
            report_author = st.text_input("Autore", value=st.session_state.current_report.get("author", ""), key="report_author")
        
        with col2:
            report_description = st.text_area("Descrizione", value=st.session_state.current_report.get("description", ""), key="report_description")
            report_date = st.date_input("Data Report", value=datetime.now(), key="report_date")
        
        # Update report details
        if st.button("Aggiorna Dettagli Report", key="update_report_details"):
            st.session_state.current_report["title"] = report_title
            st.session_state.current_report["author"] = report_author
            st.session_state.current_report["description"] = report_description
            st.session_state.current_report["date"] = report_date.strftime("%d/%m/%Y")
            st.success("Dettagli report aggiornati!")
    
    # Date filter for data
    with st.expander("Filtra Dati", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "Data Inizio",
                value=(datetime.now() - timedelta(days=180)).date(),
                key="filter_start_date"
            )
        
        with col2:
            end_date = st.date_input(
                "Data Fine",
                value=datetime.now().date(),
                key="filter_end_date"
            )
        
        # Property filter
        property_options = {}
        if properties:
            # Se abbiamo una lista di proprietà, creiamo le opzioni
            property_options = {p.get('id', str(i)): p.get('name', f"Proprietà {i+1}") 
                              for i, p in enumerate(properties)}
        else:
            # Altrimenti, estraiamo le proprietà uniche dal dataframe
            unique_properties = df['property_id'].unique()
            property_options = {prop_id: f"Proprietà {i+1}" 
                              for i, prop_id in enumerate(unique_properties)}
        
        # Aggiungi l'opzione "Tutti gli Immobili"
        property_options["all"] = "Tutti gli Immobili"
        
        selected_property = st.selectbox(
            "Immobile",
            options=["all"] + [k for k in property_options.keys() if k != "all"],
            format_func=lambda x: property_options.get(x, x),
            key="filter_property"
        )
        
        # Apply filters to dataframe
        filtered_df = df.copy()
        
        # Date filters
        if 'checkin_date' in filtered_df.columns:
            try:
                filtered_df['checkin_date'] = pd.to_datetime(filtered_df['checkin_date'])
                filtered_df = filtered_df[filtered_df['checkin_date'].dt.date >= start_date]
            except:
                st.warning("Errore nella conversione delle date di check-in. Il filtro per data di check-in non è stato applicato.")
        
        if 'checkout_date' in filtered_df.columns:
            try:
                filtered_df['checkout_date'] = pd.to_datetime(filtered_df['checkout_date'])
                filtered_df = filtered_df[filtered_df['checkout_date'].dt.date <= end_date]
            except:
                st.warning("Errore nella conversione delle date di check-out. Il filtro per data di check-out non è stato applicato.")
        
        # Property filter
        if selected_property != "all" and 'property_id' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['property_id'] == selected_property]
        
        # Show filtered data preview
        if not filtered_df.empty:
            st.write(f"Dati filtrati: {len(filtered_df)} record")
            st.dataframe(filtered_df.head(5))
        else:
            st.warning("Nessun dato corrisponde ai filtri selezionati.")
    
    # Add new section
    with st.expander("Aggiungi Sezione", expanded=True):
        st.subheader("Aggiungi una nuova sezione al report")
        
        section_title = st.text_input("Titolo Sezione", key="new_section_title")
        section_content = st.text_area("Contenuto", key="new_section_content", height=150)
        
        # Visualization options
        add_visualization = st.checkbox("Aggiungi Visualizzazione", key="add_viz_checkbox")
        
        if add_visualization:
            viz_type = st.selectbox(
                "Tipo di Visualizzazione",
                options=["bar", "line", "pie", "scatter", "histogram", "heatmap"],
                key="viz_type"
            )
            
            # Configure visualization based on type
            if viz_type == "bar":
                x_col = st.selectbox("Asse X", options=filtered_df.columns.tolist(), key="bar_x")
                y_col = st.selectbox("Asse Y", options=filtered_df.columns.tolist(), key="bar_y")
                
                viz_config = {
                    "x_column": x_col,
                    "y_column": y_col,
                    "title": f"{y_col} per {x_col}"
                }
            
            elif viz_type == "line":
                x_col = st.selectbox("Asse X (data)", options=filtered_df.columns.tolist(), key="line_x")
                y_cols = st.multiselect("Assi Y (metriche)", options=filtered_df.columns.tolist(), key="line_y")
                
                viz_config = {
                    "x_column": x_col,
                    "y_columns": y_cols,
                    "title": f"Trend di {', '.join(y_cols)} nel tempo"
                }
            
            elif viz_type == "pie":
                value_col = st.selectbox("Colonna dei Valori", options=filtered_df.columns.tolist(), key="pie_values")
                
                viz_config = {
                    "column": value_col,
                    "title": f"Distribuzione di {value_col}"
                }
            
            elif viz_type in ["scatter", "histogram", "heatmap"]:
                st.info(f"La configurazione per grafici di tipo {viz_type} sarà disponibile in una versione futura.")
            
            viz_caption = st.text_input("Didascalia Visualizzazione", key="viz_caption")
        
        # Add section button
        if st.button("Aggiungi Sezione al Report", key="add_section_button"):
            if section_title and section_content:
                visualizations = []
                
                if add_visualization:
                    visualizations.append({
                        "type": viz_type,
                        "config": viz_config,
                        "caption": viz_caption
                    })
                
                # Add section to report
                st.session_state.current_report = add_section_to_report(
                    st.session_state.current_report,
                    section_title,
                    section_content,
                    visualizations
                )
                
                st.success(f"Sezione '{section_title}' aggiunta al report!")
                
                # Clear inputs
                st.session_state.new_section_title = ""
                st.session_state.new_section_content = ""
            else:
                st.error("Il titolo e il contenuto della sezione sono obbligatori.")
    
    # Preview report
    if len(st.session_state.current_report.get("sections", [])) > 0:
        with st.expander("Anteprima Report", expanded=True):
            st.subheader("Anteprima del Report")
            
            render_report_in_streamlit(st.session_state.current_report, filtered_df)
            
            # Download options
            st.subheader("Download Report")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Download PDF", key="download_pdf_button"):
                    pdf_buffer = generate_pdf_report(st.session_state.current_report, filtered_df)
                    
                    if pdf_buffer:
                        st.download_button(
                            label="Scarica PDF",
                            data=pdf_buffer,
                            file_name=f"{st.session_state.current_report['title'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            key="download_pdf_file"
                        )
                    else:
                        st.error("Impossibile generare il PDF. Prova con un altro formato.")
            
            with col2:
                if st.button("Download Excel", key="download_excel_button"):
                    download_report(st.session_state.current_report, filtered_df, file_format="excel")
            
            with col3:
                if st.button("Download HTML", key="download_html_button"):
                    download_report(st.session_state.current_report, filtered_df, file_format="html")
            
            # Save report
            if st.button("Salva Report", key="save_report_button"):
                if 'saved_reports' not in st.session_state:
                    st.session_state.saved_reports = []
                
                # Add timestamp to report
                report_to_save = st.session_state.current_report.copy()
                report_to_save["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                st.session_state.saved_reports.append(report_to_save)
                st.success("Report salvato con successo!")

def create_ai_report(df):
    """Create an AI-generated report"""
    st.subheader("Genera Report con AI")
    st.markdown("Lascia che l'intelligenza artificiale analizzi i tuoi dati e generi un report completo.")
    
    # Verifica se la funzionalità AI è disponibile
    from utils.ai_insights import gemini_available
    
    if not gemini_available:
        st.warning("Si è verificato un errore nell'inizializzazione del client Gemini.")
        st.info("La funzionalità di report AI è configurata per utilizzare l'API di Gemini, ma si è verificato un errore durante l'inizializzazione.")
        
        # Mostra informazioni sull'errore
        with st.expander("Informazioni sull'errore"):
            st.markdown("""
            L'applicazione è configurata per utilizzare l'API di Google Gemini per la generazione di report AI.
            
            Se stai riscontrando problemi, potrebbe essere dovuto a:
            
            1. Problemi di connessione alla rete
            2. Limiti di quota dell'API
            3. Problemi temporanei con il servizio Gemini
            
            Prova a riavviare l'applicazione o contatta l'amministratore di sistema se il problema persiste.
            """)
        return
    
    # Report type selection
    report_type = st.selectbox(
        "Tipo di Report",
        options=["overview", "detailed", "executive"],
        format_func=lambda x: {
            "overview": "Panoramica Generale",
            "detailed": "Report Dettagliato",
            "executive": "Report Esecutivo"
        }.get(x, x),
        key="ai_report_type"
    )
    
    # Report title
    report_title = st.text_input("Titolo Report", value="Report AI - Analisi Dati", key="ai_report_title")
    
    # Generate report button
    if st.button("Genera Report AI", key="generate_ai_report"):
        with st.spinner("L'AI sta analizzando i tuoi dati e generando il report..."):
            try:
                # Generate AI report
                ai_report = generate_ai_report(df, report_type, report_title)
                
                # Verifica se il report è stato generato correttamente
                if isinstance(ai_report, str) and ("Funzionalità AI non disponibile" in ai_report or "Errore nella generazione" in ai_report):
                    st.error(ai_report)
                    return
                
                # Store in session state
                st.session_state.current_report = ai_report
                
                # Show success message
                st.success("Report generato con successo!")
                
                # Preview the report
                render_report_in_streamlit(ai_report, df)
                
                # Download options
                st.subheader("Download Report")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Download PDF", key="ai_pdf"):
                        pdf_buffer = generate_pdf_report(ai_report, df)
                        
                        if pdf_buffer:
                            st.download_button(
                                label="Scarica PDF",
                                data=pdf_buffer,
                                file_name=f"{ai_report['title'].replace(' ', '_')}.pdf",
                                mime="application/pdf"
                            )
                        else:
                            st.error("Impossibile generare il PDF. Prova con un altro formato.")
                
                with col2:
                    if st.button("Download Excel", key="ai_excel"):
                        # Simula download Excel
                        st.success("Report Excel generato con successo! Il download inizierà automaticamente tra qualche secondo.")
                        # Mostra un pulsante temporaneo di download
                        st.download_button(
                            label="Scarica Excel",
                            data=b"Report simulato",  # Dati segnaposto
                            file_name=f"report_ai_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        # TODO: Implement actual Excel report downloading functionality
                
                with col3:
                    if st.button("Download HTML", key="ai_html"):
                        # Simula download HTML
                        st.success("Report HTML generato con successo! Il download inizierà automaticamente tra qualche secondo.")
                        # Genera un contenuto HTML di esempio
                        html_content = f"""
                        <html>
                        <head><title>Report AI - {datetime.now().strftime('%d/%m/%Y')}</title></head>
                        <body>
                            <h1>Report Generato da CiaoHost AI</h1>
                            <p>Data: {datetime.now().strftime('%d/%m/%Y')}</p>
                            <p>Questo è un report dimostrativo generato dal sistema.</p>
                        </body>
                        </html>
                        """
                        # Mostra un pulsante temporaneo di download
                        st.download_button(
                            label="Scarica HTML",
                            data=html_content,
                            file_name=f"report_ai_{datetime.now().strftime('%Y%m%d')}.html",
                            mime="text/html"
                        )
                        # TODO: Implement actual HTML report downloading functionality
                
                # Save report
                if st.button("Salva Report", key="ai_save"):
                    if 'saved_reports' not in st.session_state:
                        st.session_state.saved_reports = []
                    
                    # Add timestamp to report
                    report_to_save = ai_report.copy()
                    report_to_save["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    st.session_state.saved_reports.append(report_to_save)
                    st.success("Report salvato con successo!")
            
            except Exception as e:
                st.error(f"Errore nella generazione del report: {str(e)}")

def view_saved_reports(df):
    """View and manage saved reports"""
    st.subheader("Report Salvati")
    
    if 'saved_reports' not in st.session_state or not st.session_state.saved_reports:
        st.info("Non hai ancora salvato alcun report. Crea un report personalizzato o AI e salvalo per vederlo qui.")
        return
    
    # Display saved reports
    for i, report in enumerate(st.session_state.saved_reports):
        with st.expander(f"{report['title']} - {report.get('saved_at', 'Data non disponibile')}"):
            st.write(f"**Descrizione:** {report['description']}")
            st.write(f"**Autore:** {report['author']}")
            st.write(f"**Data:** {report['date']}")
            st.write(f"**Sezioni:** {len(report['sections'])}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("Visualizza", key=f"view_{i}"):
                    render_report_in_streamlit(report, df)
            
            with col2:
                if st.button("Modifica", key=f"edit_{i}"):
                    st.session_state.current_report = report.copy()
                    st.success("Report caricato nell'editor. Vai alla tab 'Report Personalizzato' per modificarlo.")
            
            with col3:
                if st.button("Download PDF", key=f"pdf_{i}"):
                    pdf_buffer = generate_pdf_report(report, df)
                    
                    if pdf_buffer:
                        st.download_button(
                            label="Scarica PDF",
                            data=pdf_buffer,
                            file_name=f"{report['title'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            key=f"download_pdf_{i}"
                        )
            
            with col4:
                if st.button("Elimina", key=f"delete_{i}"):
                    st.session_state.saved_reports.pop(i)
                    st.success("Report eliminato con successo!")
                    st.rerun()