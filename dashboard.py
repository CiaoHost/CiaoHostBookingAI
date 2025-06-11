import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from utils.json_database import get_all_properties

def show_enhanced_dashboard():
    """Mostra una dashboard migliorata con statistiche e grafici interattivi"""
    
    # Importa e mostra la dashboard ultra-moderna
    from dashboard_ultra_modern import show_ultra_modern_dashboard
    show_ultra_modern_dashboard()
    return
    
    # CSS personalizzato per la dashboard
    st.markdown("""
    <style>
    .dashboard-header {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }
    .dashboard-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }
    .dashboard-subtitle {
        font-size: 16px;
        opacity: 0.9;
        margin-top: 5px;
    }
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    .dashboard-card-title {
        font-size: 16px;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 15px;
    }
    .dashboard-card-value {
        font-size: 28px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 5px;
    }
    .dashboard-card-trend {
        font-size: 14px;
        display: flex;
        align-items: center;
    }
    .trend-up {
        color: #10b981;
    }
    .trend-down {
        color: #ef4444;
    }
    .dashboard-section {
        margin-bottom: 30px;
    }
    .dashboard-section-title {
        font-size: 20px;
        font-weight: 600;
        color: #334155;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    .dashboard-section-title svg {
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header della dashboard
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">📊 Dashboard CiaoHost</h1>
        <p class="dashboard-subtitle">Panoramica delle performance dei tuoi immobili</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pulsanti di navigazione
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
    with col1:
        if st.button("🏠 Home", key="dash_home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        if st.button("📥 Esporta", key="dash_export", use_container_width=True):
            st.info("Funzionalità di esportazione in arrivo!")
    with col3:
        if st.button("🔄 Aggiorna", key="dash_refresh", use_container_width=True):
            st.success("Dati aggiornati!")
    
    # Ottieni le proprietà dal database
    properties = get_all_properties()
    
    # Genera dati realistici basati sulle proprietà
    # Ultimi 6 mesi
    today = datetime.now()
    months = []
    for i in range(5, -1, -1):
        month = today - timedelta(days=30*i)
        months.append(month.strftime('%b'))
    
    # Genera dati per ogni proprietà
    property_data = {}
    total_revenue = 0
    total_bookings = 0
    avg_occupancy = 0
    
    for prop in properties:
        base_price = prop.get('base_price', 50)
        property_data[prop['name']] = {
            'revenue': [],
            'occupancy': [],
            'bookings': []
        }
        
        for i in range(6):
            # Genera dati casuali ma realistici
            monthly_bookings = random.randint(5, 15)
            occupancy_rate = random.randint(60, 95)
            revenue = monthly_bookings * base_price * (1 + random.uniform(0.1, 0.5))
            
            property_data[prop['name']]['revenue'].append(revenue)
            property_data[prop['name']]['occupancy'].append(occupancy_rate)
            property_data[prop['name']]['bookings'].append(monthly_bookings)
            
            total_revenue += revenue
            total_bookings += monthly_bookings
            avg_occupancy += occupancy_rate
    
    # Calcola medie e totali
    num_properties = len(properties) or 1
    num_months = 6
    avg_revenue = total_revenue / (num_properties * num_months)
    avg_occupancy = avg_occupancy / (num_properties * num_months)
    conversion_rate = random.uniform(65, 85)
    
    # Crea DataFrame per i grafici
    data = {
        'Mese': months,
        'Guadagno': [0] * 6,
        'Occupazione': [0] * 6,
        'Prenotazioni': [0] * 6
    }
    
    for prop_name, prop_data in property_data.items():
        for i in range(6):
            data['Guadagno'][i] += prop_data['revenue'][i]
            data['Occupazione'][i] += prop_data['occupancy'][i] / num_properties
            data['Prenotazioni'][i] += prop_data['bookings'][i]
    
    df = pd.DataFrame(data)
    
    # Calcola trend rispetto al mese precedente
    revenue_trend = ((data['Guadagno'][-1] - data['Guadagno'][-2]) / data['Guadagno'][-2] * 100) if data['Guadagno'][-2] > 0 else 0
    occupancy_trend = ((data['Occupazione'][-1] - data['Occupazione'][-2]) / data['Occupazione'][-2] * 100) if data['Occupazione'][-2] > 0 else 0
    bookings_trend = ((data['Prenotazioni'][-1] - data['Prenotazioni'][-2]) / data['Prenotazioni'][-2] * 100) if data['Prenotazioni'][-2] > 0 else 0
    conversion_trend = random.uniform(-5, 10)
    
    # Metriche principali con card personalizzate
    st.markdown('<div class="dashboard-section-title">📈 Metriche principali</div>', unsafe_allow_html=True)
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        trend_class = "trend-up" if revenue_trend >= 0 else "trend-down"
        trend_icon = "↗" if revenue_trend >= 0 else "↘"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="dashboard-card-title">Guadagno Medio</div>
            <div class="dashboard-card-value">€{avg_revenue:.2f}</div>
            <div class="dashboard-card-trend {trend_class}">
                {trend_icon} {abs(revenue_trend):.1f}% rispetto al mese scorso
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[1]:
        trend_class = "trend-up" if occupancy_trend >= 0 else "trend-down"
        trend_icon = "↗" if occupancy_trend >= 0 else "↘"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="dashboard-card-title">Occupazione Media</div>
            <div class="dashboard-card-value">{avg_occupancy:.1f}%</div>
            <div class="dashboard-card-trend {trend_class}">
                {trend_icon} {abs(occupancy_trend):.1f}% rispetto al mese scorso
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[2]:
        trend_class = "trend-up" if bookings_trend >= 0 else "trend-down"
        trend_icon = "↗" if bookings_trend >= 0 else "↘"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="dashboard-card-title">Prenotazioni Totali</div>
            <div class="dashboard-card-value">{total_bookings}</div>
            <div class="dashboard-card-trend {trend_class}">
                {trend_icon} {abs(bookings_trend):.1f}% rispetto al mese scorso
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[3]:
        trend_class = "trend-up" if conversion_trend >= 0 else "trend-down"
        trend_icon = "↗" if conversion_trend >= 0 else "↘"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="dashboard-card-title">Tasso di Conversione</div>
            <div class="dashboard-card-value">{conversion_rate:.1f}%</div>
            <div class="dashboard-card-trend {trend_class}">
                {trend_icon} {abs(conversion_trend):.1f}% rispetto al mese scorso
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grafici
    st.markdown('<div class="dashboard-section-title">📊 Andamento Mensile</div>', unsafe_allow_html=True)
    chart_tabs = st.tabs(["📈 Guadagni", "🏠 Occupazione", "📅 Prenotazioni"])
    
    with chart_tabs[0]:
        st.line_chart(df.set_index('Mese')['Guadagno'], use_container_width=True)
    with chart_tabs[1]:
        st.line_chart(df.set_index('Mese')['Occupazione'], use_container_width=True)
    with chart_tabs[2]:
        st.bar_chart(df.set_index('Mese')['Prenotazioni'], use_container_width=True)
    
    # Proprietà più performanti
    st.markdown('<div class="dashboard-section-title">🏆 Proprietà più performanti</div>', unsafe_allow_html=True)
    
    # Calcola le performance totali per ogni proprietà
    property_performance = []
    for prop_name, prop_data in property_data.items():
        total_prop_revenue = sum(prop_data['revenue'])
        avg_prop_occupancy = sum(prop_data['occupancy']) / 6
        total_prop_bookings = sum(prop_data['bookings'])
        
        # Calcola un punteggio di performance
        performance_score = (total_prop_revenue / 1000) + (avg_prop_occupancy / 10) + total_prop_bookings
        
        property_performance.append({
            'name': prop_name,
            'revenue': total_prop_revenue,
            'occupancy': avg_prop_occupancy,
            'bookings': total_prop_bookings,
            'score': performance_score
        })
    
    # Ordina per punteggio di performance
    property_performance.sort(key=lambda x: x['score'], reverse=True)
    
    # Mostra le prime 3 proprietà (o meno se ce ne sono meno)
    top_properties = property_performance[:min(3, len(property_performance))]
    
    if top_properties:
        prop_cols = st.columns(min(3, len(top_properties)))
        for i, prop in enumerate(top_properties):
            with prop_cols[i]:
                st.markdown(f"""
                <div class="dashboard-card">
                    <div class="dashboard-card-title">{prop['name']}</div>
                    <div style="margin-bottom: 15px;">
                        <div style="font-size: 14px; color: #64748b; margin-bottom: 5px;">Guadagno Totale</div>
                        <div style="font-size: 18px; font-weight: 600; color: #1e293b;">€{prop['revenue']:.2f}</div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <div style="font-size: 14px; color: #64748b; margin-bottom: 5px;">Occupazione Media</div>
                        <div style="font-size: 18px; font-weight: 600; color: #1e293b;">{prop['occupancy']:.1f}%</div>
                    </div>
                    <div>
                        <div style="font-size: 14px; color: #64748b; margin-bottom: 5px;">Prenotazioni</div>
                        <div style="font-size: 18px; font-weight: 600; color: #1e293b;">{prop['bookings']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Aggiungi proprietà per vedere le statistiche di performance.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabella dati
    st.markdown('<div class="dashboard-section-title">📋 Dati Dettagliati</div>', unsafe_allow_html=True)
    st.dataframe(
        df,
        column_config={
            "Mese": st.column_config.TextColumn("Mese"),
            "Guadagno": st.column_config.NumberColumn("Guadagno (€)", format="€%.2f"),
            "Occupazione": st.column_config.ProgressColumn("Occupazione (%)", format="%d%%", min_value=0, max_value=100),
            "Prenotazioni": st.column_config.NumberColumn("Prenotazioni", format="%d")
        },
        use_container_width=True,
        hide_index=True
    )