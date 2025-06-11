import streamlit as st
import time
import random

def show_ultra_modern_loading(message="Caricamento in corso...", duration=3, style="modern"):
    """
    Mostra un'animazione di caricamento ultra-moderna
    
    Args:
        message: Messaggio da mostrare
        duration: Durata in secondi
        style: "modern", "particles", "wave", "pulse", "gradient"
    """
    
    loading_styles = {
        "modern": create_modern_loader,
        "particles": create_particles_loader,
        "wave": create_wave_loader,
        "pulse": create_pulse_loader,
        "gradient": create_gradient_loader
    }
    
    loader_func = loading_styles.get(style, create_modern_loader)
    
    # Container per il loading
    loading_container = st.empty()
    
    with loading_container.container():
        loader_func(message)
    
    # Simula il caricamento
    progress_bar = st.progress(0)
    for i in range(duration * 10):
        progress_bar.progress((i + 1) / (duration * 10))
        time.sleep(0.1)
    
    # Rimuovi il loading
    loading_container.empty()
    progress_bar.empty()

def create_modern_loader(message):
    """Loader moderno con design glassmorphism"""
    
    st.markdown(f"""
    <div class="ultra-loading-container">
        <div class="loading-content">
            <div class="modern-spinner">
                <div class="spinner-ring"></div>
                <div class="spinner-ring"></div>
                <div class="spinner-ring"></div>
            </div>
            <div class="loading-text">{message}</div>
            <div class="loading-dots">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        </div>
    </div>
    
    <style>
    .ultra-loading-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.3s ease-out;
    }}
    
    .loading-content {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 48px;
        text-align: center;
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
    }}
    
    .modern-spinner {{
        position: relative;
        width: 80px;
        height: 80px;
        margin: 0 auto 24px auto;
    }}
    
    .spinner-ring {{
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid transparent;
        border-radius: 50%;
        animation: spin 2s linear infinite;
    }}
    
    .spinner-ring:nth-child(1) {{
        border-top-color: #3b82f6;
        animation-delay: 0s;
    }}
    
    .spinner-ring:nth-child(2) {{
        border-right-color: #8b5cf6;
        animation-delay: 0.3s;
        width: 70%;
        height: 70%;
        top: 15%;
        left: 15%;
    }}
    
    .spinner-ring:nth-child(3) {{
        border-bottom-color: #10b981;
        animation-delay: 0.6s;
        width: 40%;
        height: 40%;
        top: 30%;
        left: 30%;
    }}
    
    .loading-text {{
        color: white;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 16px;
        font-family: 'Inter', sans-serif;
    }}
    
    .loading-dots {{
        display: flex;
        justify-content: center;
        gap: 8px;
    }}
    
    .dot {{
        width: 8px;
        height: 8px;
        background: #3b82f6;
        border-radius: 50%;
        animation: dotPulse 1.5s ease-in-out infinite;
    }}
    
    .dot:nth-child(2) {{
        animation-delay: 0.2s;
        background: #8b5cf6;
    }}
    
    .dot:nth-child(3) {{
        animation-delay: 0.4s;
        background: #10b981;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    @keyframes dotPulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.7; }}
        50% {{ transform: scale(1.3); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_particles_loader(message):
    """Loader con effetto particelle"""
    
    st.markdown(f"""
    <div class="particles-loading-container">
        <div class="particles-content">
            <div class="particles-animation">
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
            </div>
            <div class="particles-text">{message}</div>
        </div>
    </div>
    
    <style>
    .particles-loading-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }}
    
    .particles-content {{
        text-align: center;
        position: relative;
    }}
    
    .particles-animation {{
        position: relative;
        width: 120px;
        height: 120px;
        margin: 0 auto 32px auto;
    }}
    
    .particle {{
        position: absolute;
        width: 12px;
        height: 12px;
        background: white;
        border-radius: 50%;
        animation: particleFloat 3s ease-in-out infinite;
    }}
    
    .particle:nth-child(1) {{ top: 0; left: 50%; animation-delay: 0s; }}
    .particle:nth-child(2) {{ top: 15%; right: 15%; animation-delay: 0.4s; }}
    .particle:nth-child(3) {{ top: 50%; right: 0; animation-delay: 0.8s; }}
    .particle:nth-child(4) {{ bottom: 15%; right: 15%; animation-delay: 1.2s; }}
    .particle:nth-child(5) {{ bottom: 0; left: 50%; animation-delay: 1.6s; }}
    .particle:nth-child(6) {{ bottom: 15%; left: 15%; animation-delay: 2s; }}
    .particle:nth-child(7) {{ top: 50%; left: 0; animation-delay: 2.4s; }}
    .particle:nth-child(8) {{ top: 15%; left: 15%; animation-delay: 2.8s; }}
    
    .particles-text {{
        color: white;
        font-size: 20px;
        font-weight: 600;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    
    @keyframes particleFloat {{
        0%, 100% {{ 
            transform: translateY(0) scale(1);
            opacity: 0.7;
        }}
        50% {{ 
            transform: translateY(-20px) scale(1.2);
            opacity: 1;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_wave_loader(message):
    """Loader con effetto onda"""
    
    st.markdown(f"""
    <div class="wave-loading-container">
        <div class="wave-content">
            <div class="wave-animation">
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
            </div>
            <div class="wave-text">{message}</div>
        </div>
    </div>
    
    <style>
    .wave-loading-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }}
    
    .wave-content {{
        text-align: center;
    }}
    
    .wave-animation {{
        width: 100px;
        height: 100px;
        margin: 0 auto 32px auto;
        position: relative;
    }}
    
    .wave {{
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid #3b82f6;
        border-radius: 50%;
        opacity: 0;
        animation: waveExpand 2s ease-out infinite;
    }}
    
    .wave:nth-child(2) {{
        animation-delay: 0.7s;
        border-color: #8b5cf6;
    }}
    
    .wave:nth-child(3) {{
        animation-delay: 1.4s;
        border-color: #10b981;
    }}
    
    .wave-text {{
        color: white;
        font-size: 18px;
        font-weight: 600;
    }}
    
    @keyframes waveExpand {{
        0% {{
            transform: scale(0);
            opacity: 1;
        }}
        100% {{
            transform: scale(1.5);
            opacity: 0;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_pulse_loader(message):
    """Loader con effetto pulse"""
    
    st.markdown(f"""
    <div class="pulse-loading-container">
        <div class="pulse-content">
            <div class="pulse-animation">
                <div class="pulse-circle"></div>
            </div>
            <div class="pulse-text">{message}</div>
        </div>
    </div>
    
    <style>
    .pulse-loading-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }}
    
    .pulse-content {{
        text-align: center;
    }}
    
    .pulse-animation {{
        width: 80px;
        height: 80px;
        margin: 0 auto 32px auto;
        position: relative;
    }}
    
    .pulse-circle {{
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 50%;
        animation: pulseScale 2s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
    }}
    
    .pulse-text {{
        color: white;
        font-size: 18px;
        font-weight: 600;
        animation: textGlow 2s ease-in-out infinite;
    }}
    
    @keyframes pulseScale {{
        0%, 100% {{
            transform: scale(1);
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
        }}
        50% {{
            transform: scale(1.2);
            box-shadow: 0 0 50px rgba(59, 130, 246, 0.8);
        }}
    }}
    
    @keyframes textGlow {{
        0%, 100% {{ text-shadow: 0 0 10px rgba(255, 255, 255, 0.5); }}
        50% {{ text-shadow: 0 0 20px rgba(255, 255, 255, 0.8); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_gradient_loader(message):
    """Loader con effetto gradiente animato"""
    
    st.markdown(f"""
    <div class="gradient-loading-container">
        <div class="gradient-content">
            <div class="gradient-spinner"></div>
            <div class="gradient-text">{message}</div>
        </div>
    </div>
    
    <style>
    .gradient-loading-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 4s ease infinite;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }}
    
    .gradient-content {{
        text-align: center;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .gradient-spinner {{
        width: 60px;
        height: 60px;
        margin: 0 auto 24px auto;
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }}
    
    .gradient-text {{
        color: white;
        font-size: 18px;
        font-weight: 600;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def show_skeleton_loader(lines=3):
    """Mostra uno skeleton loader per il contenuto"""
    
    skeleton_html = ""
    for i in range(lines):
        width = random.randint(60, 100)
        skeleton_html += f'<div class="skeleton-line" style="width: {width}%;"></div>'
    
    st.markdown(f"""
    <div class="skeleton-container">
        {skeleton_html}
    </div>
    
    <style>
    .skeleton-container {{
        padding: 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        margin: 16px 0;
    }}
    
    .skeleton-line {{
        height: 16px;
        background: linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 8px;
        margin-bottom: 12px;
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def show_progress_loader(progress, message="Caricamento..."):
    """Mostra un loader con barra di progresso moderna"""
    
    st.markdown(f"""
    <div class="progress-loader-container">
        <div class="progress-content">
            <div class="progress-icon">⚡</div>
            <div class="progress-text">{message}</div>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: {progress}%"></div>
            </div>
            <div class="progress-percentage">{progress}%</div>
        </div>
    </div>
    
    <style>
    .progress-loader-container {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 32px;
        margin: 24px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    .progress-content {{
        text-align: center;
    }}
    
    .progress-icon {{
        font-size: 48px;
        margin-bottom: 16px;
        animation: bounce 2s infinite;
    }}
    
    .progress-text {{
        font-size: 18px;
        font-weight: 600;
        color: #334155;
        margin-bottom: 20px;
    }}
    
    .progress-bar-container {{
        width: 100%;
        height: 8px;
        background: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 12px;
    }}
    
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        border-radius: 4px;
        transition: width 0.3s ease;
        position: relative;
    }}
    
    .progress-bar::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }}
    
    .progress-percentage {{
        font-size: 14px;
        color: #64748b;
        font-weight: 600;
    }}
    
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    </style>
    """, unsafe_allow_html=True)