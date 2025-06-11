import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta
import numpy as np
from utils.json_database import get_all_properties

def show_ultra_modern_dashboard():
    """Dashboard ultra-moderna con design avanzato e animazioni"""
    

    
    # Metriche principali con cards ultra-moderne
    create_ultra_modern_metrics()
    
    # Grafici avanzati
    col1, col2 = st.columns(2)
    
    with col1:
        create_revenue_chart()
    
    with col2:
        create_occupancy_chart()
    
    # Seconda riga di grafici
    col3, col4 = st.columns(2)
    
    with col3:
        create_booking_trends_chart()
    
    with col4:
        create_performance_radar()
    
    # Tabella moderna delle prenotazioni recenti
    create_modern_bookings_table()
    
    # Footer con insights AI
    create_ai_insights_section()

def create_ultra_modern_metrics():
    """Crea metriche con design ultra-moderno"""
    
    # Genera dati di esempio
    revenue = random.randint(15000, 35000)
    bookings = random.randint(45, 120)
    occupancy = random.randint(75, 95)
    rating = round(random.uniform(4.2, 4.9), 1)
    
    # Calcola variazioni percentuali
    revenue_change = random.randint(-15, 25)
    bookings_change = random.randint(-10, 30)
    occupancy_change = random.randint(-5, 15)
    rating_change = round(random.uniform(-0.3, 0.5), 1)
    
    st.markdown("""
    <div class="metrics-container">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            "💰", "Ricavi Totali", f"€{revenue:,}", 
            revenue_change, "vs mese scorso", "#10b981"
        )
    
    with col2:
        create_metric_card(
            "📅", "Prenotazioni", str(bookings), 
            bookings_change, "vs mese scorso", "#3b82f6"
        )
    
    with col3:
        create_metric_card(
            "🏠", "Tasso Occupazione", f"{occupancy}%", 
            occupancy_change, "vs mese scorso", "#8b5cf6"
        )
    
    with col4:
        create_metric_card(
            "⭐", "Rating Medio", str(rating), 
            rating_change, "vs mese scorso", "#f59e0b"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

def create_metric_card(icon, title, value, change, change_label, color):
    """Crea una singola card metrica ultra-moderna"""
    
    change_color = "#10b981" if change >= 0 else "#ef4444"
    change_icon = "↗️" if change >= 0 else "↘️"
    
    st.markdown(f"""
    <div class="ultra-metric-card" style="--accent-color: {color}">
        <div class="metric-header">
            <div class="metric-icon">{icon}</div>
            <div class="metric-trend {('positive' if change >= 0 else 'negative')}">
                <span class="trend-icon">{change_icon}</span>
                <span class="trend-value">{abs(change)}%</span>
            </div>
        </div>
        <div class="metric-content">
            <div class="metric-value">{value}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-change" style="color: {change_color}">
                {change:+.1f}% {change_label}
            </div>
        </div>
        <div class="metric-progress">
            <div class="progress-bar" style="width: {min(abs(change) * 3, 100)}%"></div>
        </div>
    </div>
    
    <style>
    .metrics-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 24px;
        margin-bottom: 32px;
    }}
    
    .ultra-metric-card {{
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
        border-radius: 20px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(20px);
    }}
    
    .ultra-metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-color), transparent);
    }}
    
    .ultra-metric-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }}
    
    .metric-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }}
    
    .metric-icon {{
        font-size: 32px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }}
    
    .metric-trend {{
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }}
    
    .metric-trend.positive {{
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
    }}
    
    .metric-trend.negative {{
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }}
    
    .metric-value {{
        font-size: 32px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 4px;
        font-family: 'Inter', sans-serif;
    }}
    
    .metric-title {{
        font-size: 14px;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 8px;
    }}
    
    .metric-change {{
        font-size: 12px;
        font-weight: 500;
    }}
    
    .metric-progress {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: rgba(0,0,0,0.05);
    }}
    
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, var(--accent-color), rgba(var(--accent-color), 0.6));
        transition: width 1s ease-out;
    }}
    </style>
    """, unsafe_allow_html=True)

def create_revenue_chart():
    """Crea grafico ricavi ultra-moderno"""
    
    st.markdown("""
    <div class="chart-container">
        <h3 class="chart-title">📈 Andamento Ricavi</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Genera dati di esempio
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    revenue_data = [random.randint(8000, 25000) for _ in range(len(dates))]
    
    fig = go.Figure()
    
    # Area chart con gradiente
    fig.add_trace(go.Scatter(
        x=dates,
        y=revenue_data,
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.2)',
        line=dict(color='#667eea', width=3),
        name='Ricavi',
        hovertemplate='<b>%{y:€,.0f}</b><br>%{x}<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        font_color="#64748b",
        showlegend=False,
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            showline=False,
            zeroline=False
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_occupancy_chart():
    """Crea grafico tasso di occupazione"""
    
    st.markdown("""
    <div class="chart-container">
        <h3 class="chart-title">🏠 Tasso di Occupazione</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Genera dati di esempio
    months = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 
              'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']
    occupancy_data = [random.randint(60, 95) for _ in range(12)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=months,
        y=occupancy_data,
        marker=dict(
            color=occupancy_data,
            colorscale='Viridis',
            showscale=False
        ),
        hovertemplate='<b>%{y}%</b><br>%{x}<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        font_color="#64748b",
        showlegend=False,
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            showline=False,
            zeroline=False,
            range=[0, 100]
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_booking_trends_chart():
    """Crea grafico tendenze prenotazioni"""
    
    st.markdown("""
    <div class="chart-container">
        <h3 class="chart-title">📅 Tendenze Prenotazioni</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Genera dati di esempio
    days = list(range(1, 31))
    bookings = [random.randint(2, 15) for _ in range(30)]
    cancellations = [random.randint(0, 3) for _ in range(30)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=bookings,
        mode='lines+markers',
        name='Prenotazioni',
        line=dict(color='#10b981', width=3),
        marker=dict(size=6, color='#10b981')
    ))
    
    fig.add_trace(go.Scatter(
        x=days,
        y=cancellations,
        mode='lines+markers',
        name='Cancellazioni',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=6, color='#ef4444')
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        font_color="#64748b",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=300,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            title="Giorno del mese"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            showline=False,
            zeroline=False
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_performance_radar():
    """Crea grafico radar delle performance"""
    
    st.markdown("""
    <div class="chart-container">
        <h3 class="chart-title">⭐ Performance Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    categories = ['Pulizia', 'Comunicazione', 'Posizione', 'Valore', 'Check-in', 'Accuratezza']
    values = [random.uniform(4.0, 5.0) for _ in range(6)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.2)',
        line=dict(color='#667eea', width=2),
        marker=dict(size=8, color='#667eea'),
        name='Performance'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                showticklabels=False,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(0,0,0,0.1)'
            )
        ),
        showlegend=False,
        font_family="Inter",
        font_color="#64748b",
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_modern_bookings_table():
    """Crea tabella moderna delle prenotazioni recenti"""
    
    st.markdown("""
    <div class="modern-table-container">
        <h3 class="table-title">📋 Prenotazioni Recenti</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Genera dati di esempio
    bookings_data = []
    for i in range(8):
        booking = {
            'ID': f'BK{1000 + i}',
            'Ospite': f'Cliente {i+1}',
            'Check-in': (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%d/%m/%Y'),
            'Check-out': (datetime.now() + timedelta(days=random.randint(31, 60))).strftime('%d/%m/%Y'),
            'Immobile': f'Appartamento {chr(65 + i)}',
            'Valore': f'€{random.randint(200, 800)}',
            'Status': random.choice(['Confermata', 'In attesa', 'Check-in oggi'])
        }
        bookings_data.append(booking)
    
    df = pd.DataFrame(bookings_data)
    
    # Applica stili alla tabella
    def style_status(val):
        if val == 'Confermata':
            return 'background-color: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 12px; font-weight: 500;'
        elif val == 'In attesa':
            return 'background-color: #fef3c7; color: #92400e; padding: 4px 8px; border-radius: 12px; font-weight: 500;'
        else:
            return 'background-color: #dbeafe; color: #1e40af; padding: 4px 8px; border-radius: 12px; font-weight: 500;'
    
    styled_df = df.style.applymap(style_status, subset=['Status'])
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=300
    )

def create_ai_insights_section():
    """Crea sezione insights AI"""
    
    st.markdown("""
    <div class="ai-insights-container">
        <div class="ai-header">
            <div class="ai-icon">🤖</div>
            <div class="ai-title">
                <h3>Insights AI</h3>
                <p>Analisi intelligente delle tue performance</p>
            </div>
        </div>
        <div class="insights-grid">
            <div class="insight-card">
                <div class="insight-icon">📈</div>
                <div class="insight-content">
                    <h4>Trend Positivo</h4>
                    <p>Le prenotazioni sono aumentate del 23% rispetto al mese scorso. Ottimo lavoro!</p>
                </div>
            </div>
            <div class="insight-card">
                <div class="insight-icon">💡</div>
                <div class="insight-content">
                    <h4>Suggerimento</h4>
                    <p>Considera di aumentare i prezzi nei weekend: la domanda è alta e l'occupazione al 95%.</p>
                </div>
            </div>
            <div class="insight-card">
                <div class="insight-icon">⚠️</div>
                <div class="insight-content">
                    <h4>Attenzione</h4>
                    <p>3 immobili hanno rating sotto 4.5. Verifica le recensioni per migliorare il servizio.</p>
                </div>
            </div>
        </div>
    </div>
    
    <style>
    .chart-container, .modern-table-container {
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .chart-title, .table-title {
        font-size: 18px;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 16px 0;
        font-family: 'Inter', sans-serif;
    }
    
    .ai-insights-container {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        border-radius: 24px;
        padding: 32px;
        margin-top: 32px;
        color: white;
    }
    
    .ai-header {
        display: flex;
        align-items: center;
        margin-bottom: 24px;
    }
    
    .ai-icon {
        font-size: 48px;
        margin-right: 16px;
    }
    
    .ai-title h3 {
        margin: 0;
        font-size: 24px;
        font-weight: 700;
    }
    
    .ai-title p {
        margin: 4px 0 0 0;
        opacity: 0.8;
        font-size: 14px;
    }
    
    .insights-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
    }
    
    .insight-card {
        background: rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-4px);
    }
    
    .insight-icon {
        font-size: 32px;
        margin-bottom: 12px;
    }
    
    .insight-content h4 {
        margin: 0 0 8px 0;
        font-size: 16px;
        font-weight: 600;
    }
    
    .insight-content p {
        margin: 0;
        font-size: 14px;
        opacity: 0.9;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# Aggiungi stili globali per le animazioni
st.markdown("""
<style>
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chart-container, .modern-table-container, .ultra-metric-card {
    animation: fadeInUp 0.6s ease-out;
}

.ultra-metric-card:nth-child(1) { animation-delay: 0.1s; }
.ultra-metric-card:nth-child(2) { animation-delay: 0.2s; }
.ultra-metric-card:nth-child(3) { animation-delay: 0.3s; }
.ultra-metric-card:nth-child(4) { animation-delay: 0.4s; }
</style>
""", unsafe_allow_html=True)