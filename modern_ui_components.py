import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def create_modern_card(title, content, icon="📊", color="#3b82f6", actions=None):
    """
    Crea una card moderna con design glassmorphism
    
    Args:
        title: Titolo della card
        content: Contenuto della card
        icon: Icona da mostrare
        color: Colore principale
        actions: Lista di azioni/pulsanti
    """
    
    actions_html = ""
    if actions:
        actions_html = '<div class="card-actions">'
        for action in actions:
            actions_html += f'<button class="card-action-btn">{action}</button>'
        actions_html += '</div>'
    
    st.markdown(f"""
    <div class="modern-card" style="--card-color: {color}">
        <div class="card-header">
            <div class="card-icon">{icon}</div>
            <h3 class="card-title">{title}</h3>
        </div>
        <div class="card-content">
            {content}
        </div>
        {actions_html}
    </div>
    
    <style>
    .modern-card {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .modern-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--card-color), transparent);
    }}
    
    .modern-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }}
    
    .card-header {{
        display: flex;
        align-items: center;
        margin-bottom: 16px;
    }}
    
    .card-icon {{
        font-size: 24px;
        margin-right: 12px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }}
    
    .card-title {{
        font-size: 18px;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        flex: 1;
    }}
    
    .card-content {{
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 16px;
    }}
    
    .card-actions {{
        display: flex;
        gap: 8px;
        justify-content: flex-end;
    }}
    
    .card-action-btn {{
        background: var(--card-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .card-action-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    </style>
    """, unsafe_allow_html=True)

def create_stats_grid(stats):
    """
    Crea una griglia di statistiche moderne
    
    Args:
        stats: Lista di dizionari con 'title', 'value', 'icon', 'change', 'color'
    """
    
    cols = st.columns(len(stats))
    
    for i, stat in enumerate(stats):
        with cols[i]:
            change_color = "#10b981" if stat.get('change', 0) >= 0 else "#ef4444"
            change_icon = "↗️" if stat.get('change', 0) >= 0 else "↘️"
            
            st.markdown(f"""
            <div class="stat-card" style="--stat-color: {stat.get('color', '#3b82f6')}">
                <div class="stat-header">
                    <div class="stat-icon">{stat.get('icon', '📊')}</div>
                    <div class="stat-change" style="color: {change_color}">
                        {change_icon} {abs(stat.get('change', 0))}%
                    </div>
                </div>
                <div class="stat-value">{stat.get('value', '0')}</div>
                <div class="stat-title">{stat.get('title', 'Statistica')}</div>
            </div>
            
            <style>
            .stat-card {{
                background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9));
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 16px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 8px 25px rgba(0,0,0,0.08);
                backdrop-filter: blur(20px);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            
            .stat-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: var(--stat-color);
            }}
            
            .stat-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.12);
            }}
            
            .stat-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }}
            
            .stat-icon {{
                font-size: 24px;
            }}
            
            .stat-change {{
                font-size: 12px;
                font-weight: 600;
                padding: 2px 6px;
                border-radius: 8px;
                background: rgba(255,255,255,0.8);
            }}
            
            .stat-value {{
                font-size: 28px;
                font-weight: 800;
                color: #1e293b;
                margin-bottom: 4px;
            }}
            
            .stat-title {{
                font-size: 14px;
                color: #64748b;
                font-weight: 500;
            }}
            </style>
            """, unsafe_allow_html=True)

def create_modern_button(text, icon="", style="primary", size="medium", full_width=False):
    """
    Crea un pulsante moderno personalizzato
    
    Args:
        text: Testo del pulsante
        icon: Icona del pulsante
        style: "primary", "secondary", "success", "warning", "danger"
        size: "small", "medium", "large"
        full_width: Se True, il pulsante occupa tutta la larghezza
    """
    
    button_styles = {
        "primary": {"bg": "linear-gradient(135deg, #3b82f6, #1e40af)", "color": "white"},
        "secondary": {"bg": "linear-gradient(135deg, #64748b, #475569)", "color": "white"},
        "success": {"bg": "linear-gradient(135deg, #10b981, #059669)", "color": "white"},
        "warning": {"bg": "linear-gradient(135deg, #f59e0b, #d97706)", "color": "white"},
        "danger": {"bg": "linear-gradient(135deg, #ef4444, #dc2626)", "color": "white"}
    }
    
    button_sizes = {
        "small": {"padding": "8px 16px", "font_size": "14px"},
        "medium": {"padding": "12px 24px", "font_size": "16px"},
        "large": {"padding": "16px 32px", "font_size": "18px"}
    }
    
    style_config = button_styles.get(style, button_styles["primary"])
    size_config = button_sizes.get(size, button_sizes["medium"])
    width_style = "width: 100%;" if full_width else ""
    
    button_id = f"modern_btn_{hash(text + icon + style)}"
    
    st.markdown(f"""
    <button class="modern-button" id="{button_id}" style="
        background: {style_config['bg']};
        color: {style_config['color']};
        padding: {size_config['padding']};
        font-size: {size_config['font_size']};
        {width_style}
    ">
        {icon} {text}
    </button>
    
    <style>
    .modern-button {{
        border: none;
        border-radius: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        margin: 4px;
    }}
    
    .modern-button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }}
    
    .modern-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    
    .modern-button:hover::before {{
        left: 100%;
    }}
    
    .modern-button:active {{
        transform: translateY(0);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

def create_modern_input(label, placeholder="", input_type="text", icon=""):
    """
    Crea un input moderno con design avanzato
    
    Args:
        label: Etichetta dell'input
        placeholder: Placeholder text
        input_type: Tipo di input
        icon: Icona da mostrare
    """
    
    input_id = f"modern_input_{hash(label)}"
    
    st.markdown(f"""
    <div class="modern-input-container">
        <label class="modern-input-label" for="{input_id}">
            {icon} {label}
        </label>
        <input 
            type="{input_type}" 
            id="{input_id}"
            class="modern-input" 
            placeholder="{placeholder}"
        />
    </div>
    
    <style>
    .modern-input-container {{
        margin: 16px 0;
    }}
    
    .modern-input-label {{
        display: block;
        font-size: 14px;
        font-weight: 600;
        color: #374151;
        margin-bottom: 8px;
    }}
    
    .modern-input {{
        width: 100%;
        padding: 12px 16px;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        font-size: 16px;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    .modern-input:focus {{
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        background: white;
    }}
    
    .modern-input::placeholder {{
        color: #9ca3af;
    }}
    </style>
    """, unsafe_allow_html=True)

def create_modern_chart(data, chart_type="line", title="", height=400):
    """
    Crea un grafico moderno con Plotly
    
    Args:
        data: Dati per il grafico
        chart_type: Tipo di grafico ("line", "bar", "pie", "area")
        title: Titolo del grafico
        height: Altezza del grafico
    """
    
    # Configurazione moderna per tutti i grafici
    modern_layout = {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'family': 'Inter, sans-serif', 'color': '#374151'},
        'title': {
            'text': title,
            'font': {'size': 20, 'color': '#1f2937'},
            'x': 0.5,
            'xanchor': 'center'
        },
        'margin': {'l': 40, 'r': 40, 't': 60, 'b': 40},
        'height': height,
        'showlegend': True,
        'legend': {
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': 1.02,
            'xanchor': 'right',
            'x': 1
        }
    }
    
    if chart_type == "line":
        fig = px.line(data, x=data.columns[0], y=data.columns[1:])
        fig.update_traces(line=dict(width=3))
        
    elif chart_type == "bar":
        fig = px.bar(data, x=data.columns[0], y=data.columns[1:])
        fig.update_traces(marker=dict(cornerradius=4))
        
    elif chart_type == "area":
        fig = px.area(data, x=data.columns[0], y=data.columns[1:])
        
    elif chart_type == "pie":
        fig = px.pie(data, values=data.columns[1], names=data.columns[0])
        
    # Applica il layout moderno
    fig.update_layout(**modern_layout)
    
    # Stili per gli assi
    fig.update_xaxes(
        showgrid=False,
        showline=False,
        zeroline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.05)',
        showline=False,
        zeroline=False
    )
    
    # Container moderno per il grafico
    st.markdown("""
    <div class="modern-chart-container">
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    </div>
    
    <style>
    .modern-chart-container {
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def create_modern_table(data, title="", searchable=True):
    """
    Crea una tabella moderna con funzionalità avanzate
    
    Args:
        data: DataFrame con i dati
        title: Titolo della tabella
        searchable: Se abilitare la ricerca
    """
    
    st.markdown(f"""
    <div class="modern-table-container">
        <div class="table-header">
            <h3 class="table-title">{title}</h3>
            {'''<div class="table-search">
                <input type="text" placeholder="Cerca..." class="search-input">
                <span class="search-icon">🔍</span>
            </div>''' if searchable else ''}
        </div>
    </div>
    
    <style>
    .modern-table-container {{
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    .table-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }}
    
    .table-title {{
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
    }}
    
    .table-search {{
        position: relative;
    }}
    
    .search-input {{
        padding: 8px 40px 8px 16px;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        font-size: 14px;
        background: white;
        transition: all 0.3s ease;
    }}
    
    .search-input:focus {{
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }}
    
    .search-icon {{
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        color: #9ca3af;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Mostra la tabella con stili personalizzati
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

def create_modern_alert(message, alert_type="info", dismissible=True):
    """
    Crea un alert moderno
    
    Args:
        message: Messaggio dell'alert
        alert_type: "info", "success", "warning", "error"
        dismissible: Se l'alert può essere chiuso
    """
    
    alert_configs = {
        "info": {"bg": "#dbeafe", "border": "#3b82f6", "icon": "ℹ️", "color": "#1e40af"},
        "success": {"bg": "#dcfce7", "border": "#10b981", "icon": "✅", "color": "#065f46"},
        "warning": {"bg": "#fef3c7", "border": "#f59e0b", "icon": "⚠️", "color": "#92400e"},
        "error": {"bg": "#fee2e2", "border": "#ef4444", "icon": "❌", "color": "#991b1b"}
    }
    
    config = alert_configs.get(alert_type, alert_configs["info"])
    close_btn = '<button class="alert-close">×</button>' if dismissible else ''
    
    st.markdown(f"""
    <div class="modern-alert" style="
        background: {config['bg']};
        border-left: 4px solid {config['border']};
        color: {config['color']};
    ">
        <div class="alert-content">
            <span class="alert-icon">{config['icon']}</span>
            <span class="alert-message">{message}</span>
        </div>
        {close_btn}
    </div>
    
    <style>
    .modern-alert {{
        padding: 16px 20px;
        border-radius: 12px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        backdrop-filter: blur(10px);
        animation: slideInAlert 0.3s ease-out;
    }}
    
    .alert-content {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    
    .alert-icon {{
        font-size: 18px;
    }}
    
    .alert-message {{
        font-weight: 500;
        line-height: 1.4;
    }}
    
    .alert-close {{
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.2s ease;
        color: inherit;
    }}
    
    .alert-close:hover {{
        opacity: 1;
    }}
    
    @keyframes slideInAlert {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    </style>
    """, unsafe_allow_html=True)