import streamlit as st

# ==============================================================================
# 1. VISUAL FX ENGINE (Dual Chip CSS)
# ==============================================================================
def inject_bio_css(fam_color, clan_color):
    st.markdown(f"""
        <style>
        /* Shared Chip Style */
        .bio-chip {{
            background-color: rgba(15, 15, 20, 0.95);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 4px;
            color: #e0e0e0;
            font-family: 'Rajdhani', sans-serif;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.85rem;
            padding: 8px 10px;
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        /* Linker Chip (Familie) */
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stExpander"] details summary {{
            border-left: 4px solid {fam_color} !important;
            background-color: rgba(15, 15, 20, 0.95) !important;
            color: #e0e0e0 !important;
            font-family: 'Rajdhani', sans-serif;
            border-radius: 4px;
        }}

        /* Rechter Chip (Clan) */
        div[data-testid="column"]:nth-of-type(2) div[data-testid="stExpander"] details summary {{
            border-right: 4px solid {clan_color} !important; /* Rechts der Balken */
            background-color: rgba(15, 15, 20, 0.95) !important;
            color: #e0e0e0 !important;
            font-family: 'Rajdhani', sans-serif;
            border-radius: 4px;
            text-align: right !important; /* Text rechtsbündig */
            flex-direction: row-reverse; /* Pfeil auf die andere Seite */
        }}

        /* Data List Styling */
        .data-row {{
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding: 6px 0;
            font-size: 0.85rem;
        }}
        .data-key {{ color: #888; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1px; }}
        .data-val {{ color: #eee; font-weight: bold; text-align: right; }}
        
        .section-head {{
            margin-top: 10px;
            margin-bottom: 5px;
            font-size: 0.8rem;
            color: {fam_color}; /* Standard Fallback */
            border-bottom: 1px dashed rgba(255,255,255,0.1);
            padding-bottom: 2px;
            text-transform: uppercase;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. DATA LOGIC (Alles extrahieren)
# ==============================================================================
def get_family_details(seal):
    # Mapping der Chakren & Finger (Falls nicht in DB, hier Fallback)
    # Die DB hat meistens schon 'chakra' und 'holon'.
    
    # 5 Familien Farben
    fam_colors = {
        "Polar": "#A020F0", "Kardinal": "#FF3E3E", "Zentral": "#E0E0E0", 
        "Signal": "#FFD700", "Tor": "#00FF66"
    }
    color = fam_colors.get(seal.get('family'), "#fff")
    
    return {
        "name": seal.get('family', 'Unbekannt'),
        "color": color,
        "chakra": seal.get('chakra', '---'),
        "holon": seal.get('holon', '---'), # Finger/Zeh
        "action": seal.get('action', '---'), # z.B. Nährt
        "essence": seal.get('essence', '---'),
        "power": seal.get('power', '---'),
        "sense": seal.get('sense', '---') # Sinnesorgan
    }

def get_clan_details(seal):
    # Clan Zuordnung (Feuer, Blut, Wahrheit, Himmel)
    # Farben für Clans (Feuer=Gelb/Rot Mix -> Orange, Blut=Rot, Wahrheit=Weiß, Himmel=Blau)
    clan_colors = {
        "Feuer": "#FF8C00", "Blut": "#FF3E3E", "Wahrheit": "#E0E0E0", "Himmel": "#2A8CFF"
    }
    c_name = seal.get('clan', 'Unbekannt')
    color = clan_colors.get(c_name, "#888")
    
    return {
        "name": c_name,
        "color": color,
        "planet": seal.get('planet', '---'),
        "flow": seal.get('flow', '---'), # Galaktisch-Karmisch / Solar-Prophetisch
        "code_num": seal.get('id', 0)
    }

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    meta = pulse['metadata']
    if meta['is_leap_day']: return
    
    # Daten aus dem Seal holen
    seal = pulse['tzolkin']['identity']['seal']
    
    fam = get_family_details(seal)
    clan = get_clan_details(seal)
    
    # CSS laden
    inject_bio_css(fam['color'], clan['color'])
    
    # ZWEI SPALTEN
    c1, c2 = st.columns(2)
    
    # --- LINKS: FAMILIE (Körper & Chakren) ---
    with c1:
        with st.expander(f"🌍 {fam['name']}"):
            # Sektion Header Style
            st.markdown(f"<div style='color:{fam['color']}; font-weight:bold; margin-bottom:5px;'>BIO-HOLON</div>", unsafe_allow_html=True)
            
            # Daten Liste (Loop ist sauberer)
            data_points = [
                ("Chakra", fam['chakra']),
                ("Körperteil", fam['holon']),
                ("Sinn", fam['sense']),
                ("Essenz", fam['essence']),
                ("Aktion", fam['action']),
                ("Kraft", fam['power'])
            ]
            
            for k, v in data_points:
                st.markdown(f"""
                <div class="data-row">
                    <span class="data-key">{k}</span>
                    <span class="data-val">{v}</span>
                </div>
                """, unsafe_allow_html=True)

    # --- RECHTS: CLAN (Planeten & Kosmos) ---
    with c2:
        with st.expander(f"🔥 {clan['name']}"):
            # Sektion Header Style
            st.markdown(f"<div style='color:{clan['color']}; font-weight:bold; margin-bottom:5px; text-align:right;'>PLANETAR</div>", unsafe_allow_html=True)
            
            # Daten Liste
            planet_data = [
                ("Planet", clan['planet']),
                ("Atem/Fluss", clan['flow']),
                ("Clan Typ", f"{clan['name']} Clan"),
                ("Code Zahl", f".{clan['code_num']}."),
                ("Chromatik", "Polar -> Portal") # Generisch, da komplex zu berechnen ohne extra DB
            ]
            
            for k, v in planet_data:
                st.markdown(f"""
                <div class="data-row">
                    <span class="data-key">{k}</span>
                    <span class="data-val" style="color:{clan['color']}">{v}</span>
                </div>
                """, unsafe_allow_html=True)
