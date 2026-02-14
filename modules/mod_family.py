import streamlit as st

# ==============================================================================
# 1. VISUAL FX (Family Chip)
# ==============================================================================
def inject_family_css(fam_color):
    st.markdown(f"""
        <style>
        /* Der Chip-Button (Rechts) */
        .fam-chip {{
            background-color: rgba(15, 15, 20, 0.95) !important;
            border-left: 4px solid {fam_color} !important;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 4px;
            color: #e0e0e0;
            font-family: 'Rajdhani', sans-serif;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9rem;
            padding: 8px 10px;
            min-height: 38px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .fam-chip:hover {{
            border-color: {fam_color};
            color: #fff;
            box-shadow: 0 0 10px {fam_color};
        }}
        
        /* Inhalt */
        .fam-content {{
            background: rgba(255,255,255,0.03);
            border-right: 2px solid {fam_color};
            padding: 10px;
            margin-top: 5px;
            border-radius: 4px 0 0 4px; /* Spiegelverkehrt zum Schloss */
            text-align: right; /* Rechtsbündig für den rechten Chip */
        }}
        
        .f-label {{ color: #777; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 2px; }}
        .f-val {{ color: #eee; font-weight: bold; margin-bottom: 8px; }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. LOGIC (Die 5 Erdfamilien)
# ==============================================================================
def calculate_family_data(seal_id):
    # Mapping der 20 Siegel auf 5 Familien
    # ID 1=Drache (Kardinal) ...
    
    families = {
        "Polar":   {"ids": [3, 8, 13, 18], "color": "#A020F0", "chakra": "Kronen", "action": "Tönt die Chromatik", "finger": "Daumen"},
        "Kardinal": {"ids": [1, 6, 11, 16], "color": "#FF3E3E", "chakra": "Kehlkopf", "action": "Etabliert die Genesis", "finger": "Zeigefinger"},
        "Zentral":  {"ids": [2, 7, 12, 17], "color": "#E0E0E0", "chakra": "Herz", "action": "Gräbt die Tunnel", "finger": "Mittelfinger"},
        "Signal":   {"ids": [4, 9, 14, 19], "color": "#FFD700", "chakra": "Solarplexus", "action": "Enträtselt das Mysterium", "finger": "Ringfinger"},
        "Tor":      {"ids": [5, 10, 15, 20], "color": "#00FF66", "chakra": "Wurzel", "action": "Öffnet die Portale", "finger": "Kleiner Finger"}
    }
    
    # Finde die Familie für das Siegel
    my_fam = None
    my_fam_name = ""
    
    for fname, data in families.items():
        if seal_id in data['ids']:
            my_fam = data
            my_fam_name = fname
            break
            
    if not my_fam: return None

    return {
        "name": my_fam_name,
        "color": my_fam['color'],
        "chakra": my_fam['chakra'],
        "action": my_fam['action'],
        "finger": my_fam['finger']
    }

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    meta = pulse['metadata']
    if meta['is_leap_day']: return
    
    seal_id = pulse['tzolkin']['identity']['seal']['id']
    fam = calculate_family_data(seal_id)
    
    inject_family_css(fam['color'])
    
    # TRICK: Wir nutzen hier die RECHTE Spalte
    c1, c2 = st.columns(2)
    
    with c2: # <--- Rechts!
        label = f"🌍 Familie: {fam['name']}"
        with st.expander(label):
            st.markdown(f"""
                <div class="fam-content">
                    <span class="f-label">Holon (Körper)</span>
                    <div class="f-val">{fam['finger']} ({fam['chakra']})</div>
                    
                    <span class="f-label">Mission (Code)</span>
                    <div class="f-val" style="color:{fam['color']}">{fam['action']}</div>
                    
                    <span class="f-label">Funktion</span>
                    <div style="font-size:0.8rem; color:#aaa;">
                        Die {fam['name']}e Familie hält die Frequenz der Erde.
                    </div>
                </div>
            """, unsafe_allow_html=True)
