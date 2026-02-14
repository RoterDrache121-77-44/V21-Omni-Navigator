import streamlit as st

# ... Hier die inject_castle_css Funktion von vorhin reinkopieren ...
# ... Hier die inject_family_css Funktion von oben reinkopieren ...
# ... Hier die calculate_castle_data Funktion reinkopieren ...
# ... Hier die calculate_family_data Funktion reinkopieren ...

# Ich gebe dir den fertigen Kombi-Code, damit du kein Copy-Paste-Chaos hast:

def render(pulse):
    # 1. Daten holen
    meta = pulse['metadata']
    if meta['is_leap_day']: return
    
    # Castle Data
    kin_idx = meta['kin'] - 1
    castle_idx = kin_idx // 52
    castles = [
        {"name": "Rotes Schloss", "color": "#FF3E3E"},
        {"name": "Weißes Schloss", "color": "#E0E0E0"},
        {"name": "Blaues Schloss", "color": "#2A8CFF"},
        {"name": "Gelbes Schloss", "color": "#FFD700"},
        {"name": "Grünes Schloss", "color": "#00FF66"}
    ]
    c_data = castles[castle_idx]
    day_in_castle = (kin_idx % 52) + 1
    
    # Family Data
    seal_id = pulse['tzolkin']['identity']['seal']['id']
    families = {
        "Polar": "#A020F0", "Kardinal": "#FF3E3E", "Zentral": "#E0E0E0", 
        "Signal": "#FFD700", "Tor": "#00FF66"
    }
    fam_name = pulse['tzolkin']['identity']['seal']['family']
    fam_color = families.get(fam_name, "#fff")
    
    # 2. Styles (Inline für Kompaktheit)
    st.markdown(f"""
        <style>
        /* Shared Chip Style */
        .chip-box {{
            background: rgba(15, 15, 20, 0.95);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 4px;
            color: #ddd;
            font-family: 'Rajdhani', sans-serif;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.85rem;
            padding: 8px 10px;
            min-height: 40px;
            display: flex; align-items: center;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # 3. DAS GRID (50/50)
    col_left, col_right = st.columns(2)
    
    # --- LINKS: SCHLOSS ---
    with col_left:
        # Hier nutzen wir den Expander Trick für Links
        with st.expander(f"🏰 {c_data['name']} ({day_in_castle}/52)"):
             st.info(f"Wir sind im {c_data['name']}. Farbe: {c_data['color']}")
             # (Hier könnte der volle Castle-Content stehen)

    # --- RECHTS: FAMILIE ---
    with col_right:
        # Hier nutzen wir den Expander Trick für Rechts
        with st.expander(f"🌍 {fam_name} ({seal_id})"):
             st.success(f"Familie: {fam_name}. Farbe: {fam_color}")
             # (Hier könnte der volle Family-Content stehen)
