import streamlit as st

def render(pulse):
    # Daten aus dem Puls extrahieren
    tzolkin = pulse['tzolkin']
    meta = pulse['metadata']
    moon = pulse['moon']
    
    # Die Farbe des Tages für das UI bestimmen
    ui_color = tzolkin['identity']['seal']['color'] # Rot, Weiß, Blau oder Gelb
    color_hex = {
        "Rot": "#FF3E3E", 
        "Weiß": "#E0E0E0", 
        "Blau": "#2A8CFF", 
        "Gelb": "#FFD700"
    }.get(ui_color, "#00FF66") # Grün als Fallback (Hunab Ku)

    # Das HTML/CSS Paket für den Header
    st.markdown(f"""
        <div class="glass-container" style="border-top: 3px solid {color_hex}; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; color: #888; margin-bottom: 0;">
                {meta['date_str']} • {moon['moon']['name']}
            </p>
            <h1 style="margin: 5px 0; font-size: 2.2rem; color: {color_hex};">
                {tzolkin['identity']['name']}
            </h1>
            <p style="font-style: italic; color: #aaa; font-size: 0.9rem;">
                "{tzolkin.get('message', 'Harmonisierung der Zeit...')}"
            </p>
            <div style="position: absolute; top: 10px; right: 20px; font-size: 3rem; font-weight: 800; opacity: 0.1;">
                {meta['kin']}
            </div>
        </div>
    """, unsafe_allow_html=True)

