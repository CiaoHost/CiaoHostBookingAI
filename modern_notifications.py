import streamlit as st
import time
from datetime import datetime

def show_modern_notification(message, type="info", duration=3, position="top-right"):
    """
    Mostra una notifica moderna con animazioni
    
    Args:
        message: Testo della notifica
        type: "success", "error", "warning", "info"
        duration: Durata in secondi
        position: "top-right", "top-left", "bottom-right", "bottom-left"
    """
    
    # Colori e icone per tipo
    notification_styles = {
        "success": {
            "color": "#10b981",
            "bg": "linear-gradient(135deg, #dcfce7, #bbf7d0)",
            "icon": "✅",
            "border": "#10b981"
        },
        "error": {
            "color": "#ef4444", 
            "bg": "linear-gradient(135deg, #fee2e2, #fecaca)",
            "icon": "❌",
            "border": "#ef4444"
        },
        "warning": {
            "color": "#f59e0b",
            "bg": "linear-gradient(135deg, #fef3c7, #fde68a)", 
            "icon": "⚠️",
            "border": "#f59e0b"
        },
        "info": {
            "color": "#3b82f6",
            "bg": "linear-gradient(135deg, #dbeafe, #bfdbfe)",
            "icon": "ℹ️", 
            "border": "#3b82f6"
        }
    }
    
    style = notification_styles.get(type, notification_styles["info"])
    
    # Posizioni
    positions = {
        "top-right": "top: 20px; right: 20px;",
        "top-left": "top: 20px; left: 20px;",
        "bottom-right": "bottom: 20px; right: 20px;",
        "bottom-left": "bottom: 20px; left: 20px;"
    }
    
    position_style = positions.get(position, positions["top-right"])
    
    # ID unico per la notifica
    notification_id = f"notification_{int(time.time() * 1000)}"
    
    st.markdown(f"""
    <div id="{notification_id}" class="modern-notification" style="{position_style}">
        <div class="notification-content">
            <div class="notification-icon">{style['icon']}</div>
            <div class="notification-message">{message}</div>
            <div class="notification-close" onclick="closeNotification('{notification_id}')">×</div>
        </div>
        <div class="notification-progress"></div>
    </div>
    
    <style>
    .modern-notification {{
        position: fixed;
        z-index: 10000;
        min-width: 300px;
        max-width: 400px;
        background: {style['bg']};
        border: 1px solid {style['border']};
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(20px);
        animation: slideInNotification 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
    }}
    
    .notification-content {{
        display: flex;
        align-items: center;
        padding: 16px 20px;
        gap: 12px;
    }}
    
    .notification-icon {{
        font-size: 20px;
        flex-shrink: 0;
    }}
    
    .notification-message {{
        flex: 1;
        color: {style['color']};
        font-weight: 500;
        font-size: 14px;
        line-height: 1.4;
    }}
    
    .notification-close {{
        font-size: 18px;
        color: {style['color']};
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.2s;
        flex-shrink: 0;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .notification-close:hover {{
        opacity: 1;
    }}
    
    .notification-progress {{
        height: 3px;
        background: {style['color']};
        animation: progressBar {duration}s linear;
        transform-origin: left;
    }}
    
    @keyframes slideInNotification {{
        from {{
            opacity: 0;
            transform: translateX(100%);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes slideOutNotification {{
        from {{
            opacity: 1;
            transform: translateX(0);
        }}
        to {{
            opacity: 0;
            transform: translateX(100%);
        }}
    }}
    
    @keyframes progressBar {{
        from {{
            transform: scaleX(1);
        }}
        to {{
            transform: scaleX(0);
        }}
    }}
    </style>
    
    <script>
    function closeNotification(id) {{
        const notification = document.getElementById(id);
        if (notification) {{
            notification.style.animation = 'slideOutNotification 0.3s ease-in';
            setTimeout(() => {{
                notification.remove();
            }}, 300);
        }}
    }}
    
    // Auto-remove notification after duration
    setTimeout(() => {{
        closeNotification('{notification_id}');
    }}, {duration * 1000});
    </script>
    """, unsafe_allow_html=True)

def show_toast_notification(message, type="info"):
    """Mostra una notifica toast semplice"""
    
    if type == "success":
        st.success(f"✅ {message}")
    elif type == "error":
        st.error(f"❌ {message}")
    elif type == "warning":
        st.warning(f"⚠️ {message}")
    else:
        st.info(f"ℹ️ {message}")

def show_floating_action_button():
    """Mostra un pulsante di azione flottante moderno"""
    
    st.markdown("""
    <div class="floating-action-button" onclick="showQuickActions()">
        <div class="fab-icon">+</div>
    </div>
    
    <div id="quick-actions" class="quick-actions-menu" style="display: none;">
        <div class="quick-action" onclick="addProperty()">
            <div class="action-icon">🏠</div>
            <div class="action-text">Aggiungi Immobile</div>
        </div>
        <div class="quick-action" onclick="addBooking()">
            <div class="action-icon">📅</div>
            <div class="action-text">Nuova Prenotazione</div>
        </div>
        <div class="quick-action" onclick="sendMessage()">
            <div class="action-icon">💬</div>
            <div class="action-text">Invia Messaggio</div>
        </div>
    </div>
    
    <style>
    .floating-action-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1000;
    }
    
    .floating-action-button:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .fab-icon {
        color: white;
        font-size: 24px;
        font-weight: 300;
        transition: transform 0.3s ease;
    }
    
    .floating-action-button:hover .fab-icon {
        transform: rotate(45deg);
    }
    
    .quick-actions-menu {
        position: fixed;
        bottom: 100px;
        right: 30px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 12px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        z-index: 999;
        animation: fadeInUp 0.3s ease-out;
    }
    
    .quick-action {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        border-radius: 12px;
        cursor: pointer;
        transition: background 0.2s ease;
        gap: 12px;
        min-width: 180px;
    }
    
    .quick-action:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    .action-icon {
        font-size: 20px;
    }
    
    .action-text {
        font-size: 14px;
        font-weight: 500;
        color: #334155;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    
    <script>
    function showQuickActions() {
        const menu = document.getElementById('quick-actions');
        if (menu.style.display === 'none') {
            menu.style.display = 'block';
        } else {
            menu.style.display = 'none';
        }
    }
    
    function addProperty() {
        alert('Funzione: Aggiungi Immobile');
        document.getElementById('quick-actions').style.display = 'none';
    }
    
    function addBooking() {
        alert('Funzione: Nuova Prenotazione');
        document.getElementById('quick-actions').style.display = 'none';
    }
    
    function sendMessage() {
        alert('Funzione: Invia Messaggio');
        document.getElementById('quick-actions').style.display = 'none';
    }
    
    // Chiudi menu quando si clicca fuori
    document.addEventListener('click', function(event) {
        const fab = document.querySelector('.floating-action-button');
        const menu = document.getElementById('quick-actions');
        
        if (!fab.contains(event.target) && !menu.contains(event.target)) {
            menu.style.display = 'none';
        }
    });
    </script>
    """, unsafe_allow_html=True)

def show_progress_indicator(progress, text="Caricamento..."):
    """Mostra un indicatore di progresso moderno"""
    
    st.markdown(f"""
    <div class="modern-progress-container">
        <div class="progress-text">{text}</div>
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: {progress}%"></div>
        </div>
        <div class="progress-percentage">{progress}%</div>
    </div>
    
    <style>
    .modern-progress-container {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    .progress-text {{
        font-size: 16px;
        font-weight: 600;
        color: #334155;
        margin-bottom: 12px;
        text-align: center;
    }}
    
    .progress-bar-container {{
        width: 100%;
        height: 8px;
        background: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 8px;
    }}
    
    .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 4px;
        transition: width 0.3s ease;
        position: relative;
    }}
    
    .progress-bar-fill::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }}
    
    .progress-percentage {{
        font-size: 14px;
        color: #64748b;
        text-align: center;
        font-weight: 500;
    }}
    
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def show_loading_skeleton():
    """Mostra uno skeleton loader moderno"""
    
    st.markdown("""
    <div class="skeleton-container">
        <div class="skeleton-header">
            <div class="skeleton-avatar"></div>
            <div class="skeleton-text-container">
                <div class="skeleton-text skeleton-title"></div>
                <div class="skeleton-text skeleton-subtitle"></div>
            </div>
        </div>
        <div class="skeleton-content">
            <div class="skeleton-text skeleton-line"></div>
            <div class="skeleton-text skeleton-line"></div>
            <div class="skeleton-text skeleton-line short"></div>
        </div>
    </div>
    
    <style>
    .skeleton-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }
    
    .skeleton-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .skeleton-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        margin-right: 16px;
    }
    
    .skeleton-text-container {
        flex: 1;
    }
    
    .skeleton-text {
        background: linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 4px;
        margin-bottom: 8px;
    }
    
    .skeleton-title {
        height: 20px;
        width: 60%;
    }
    
    .skeleton-subtitle {
        height: 16px;
        width: 40%;
    }
    
    .skeleton-line {
        height: 16px;
        width: 100%;
        margin-bottom: 12px;
    }
    
    .skeleton-line.short {
        width: 70%;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    </style>
    """, unsafe_allow_html=True)