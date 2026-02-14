import streamlit as st

# ==============================================================================
# 1. VISUAL FX ENGINE (Slim Chip CSS)
# ==============================================================================
def inject_castle_css(castle_color_hex):
    st.markdown(f"""
        <style>
        /* Der Chip-Button (Expander Summary) */
        div[data-testid="stExpander"] details summary {{
            background-color: rgba(15, 15, 20, 0.95) !important;
            border-left: 4px solid {castle_color_hex} !important;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 4px;
            
            color: #e0e0e0 !important;
            font-family: 'Rajdhani', sans-serif;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9rem;
            
            padding: 8px 10px !important;
            min-height: 38px;
            margin-bottom: 0px;
            transition: all 0.2s ease;
        }}
        
        div[data-testid="stExpander"] details summary:hover {{
            border-color: {castle_color_hex};
            color: #fff !important;
        }}

        /* Der Info-Container (ausgeklappt) */
        .castle-info-panel {{
            background: rgba(255,255,255,0.03);
            border-left: 2px solid {castle_color_hex};
            padding: 10px 12px;
            margin-top: 5px;
            border-radius: 0 4px 4px 0;
            font-size: 0.9rem;
        }}
        
        .c-label {{
            color: #777;
            font-size: 0.7rem;
            font-weight: bold;
            display: block;
            margin-bottom: 2px;
            text-transform: uppercase;
        }}
        
        .c-text {{
            color: #ddd;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        
        .wave-list-item {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            padding: 2px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        
        .wave-active {{
            color: {castle_color_hex};
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. LOGIC (52-Tage Kontext)
# ==============================================================================
def calculate_castle_data(current_kin):
    kin_idx = current_kin - 1
    castle_idx = kin_idx // 52
    
    # Datenbank der 5 Schlösser (Mit Fließtext-Beschreibungen)
    castles = [
        {
            "name": "Rotes Schloss", "suffix": "des Drehens", "color": "#FF3E3E", 
            "dir": "Osten", "action": "Initiieren & Gebären",
            "desc": "Hier beginnt der Zyklus. Das Wissen wird initiiert. Es ist die Zeit des Starts und der frischen Energie."
        },
        {
            "name": "Weißes Schloss", "suffix": "des Kreuzens", "color": "#E0E0E0", 
            "dir": "Norden", "action": "Läutern & Verfeinern",
            "desc": "Die Energie wird geprüft und geklärt. Was Bestand hat, bleibt. Der Krieger kreuzt den Pfad."
        },
        {
            "name": "Blaues Schloss", "suffix": "des Brennens", "color": "#2A8CFF", 
            "dir": "Westen", "action": "Transformieren & Magie",
            "desc": "Der alchemistische Kern. Durch Intensität wandelt sich die Form. Hier liegt der Fokus auf Transformation."
        },
        {
            "name": "Gelbes Schloss", "suffix": "des Gebens", "color": "#FFD700", 
            "dir": "Süden", "action": "Reifen & Ernten",
            "desc": "Die Sonne bringt das Wissen zur Reife. Die Früchte der vorherigen Prozesse werden sichtbar."
        },
        {
            "name": "Grünes Schloss", "suffix": "der Verzauberung", "color": "#00FF66", 
            "dir": "Zentrum", "action": "Synchronisieren",
            "desc": "Der Ausgang der Matrix. Wir fliegen mit dem gewonnenen Wissen in die nächste Dimension."
        }
    ]
    
    c = castles[castle_idx]
    
    # Position
    day = (kin_idx % 52) + 1
    active_wave = (day - 1) // 13
    
    # Wellen-Liste generieren
    start_kin = (castle_idx * 52) + 1
    waves = []
    colors = ["Rot", "Weiß", "Blau", "Gelb"]
    
    for i in range(4):
        w_start = start_kin + (i * 13)
        waves.append({
            "label": f"{colors[i]}e Welle",
            "range": f"Kin {w_start}-{w_start+12}",
            "is_active": (i == active_wave)
        })

    return {
        "title": f"{c['name']}",
        "full_name": f"{c['name']} {c['suffix']}",
        "color": c['color'],
        "dir": c['dir'],
        "act": c['action'],
        "desc": c['desc'],
        "day": day,
        "waves": waves
    }

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    meta = pulse['metadata']
    if meta['is_leap_day']: return
    
    # Berechnen
    data = calculate_castle_data(meta['kin'])
    
    # CSS laden
    inject_castle_css(data['color'])
    
    # LAYOUT TRICK: Wir nutzen 2 Spalten und füllen nur die linke!
    # Dadurch ist das Modul visuell "halbiert" und schafft Platz für später.
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Der Expander-Button (Kompakt)
        label = f"🏰 {data['title']} ({data['day']}/52)"
        
        with st.expander(label):
            # Der "kleine aber feine" Inhalt
            st.markdown(f"""
                <div class="castle-info-panel">
                    <span class="c-label">Richtung & Aktion</span>
                    <div class="c-text">
                        <strong>{data['dir']} • {data['act']}</strong>
                    </div>
                    
                    <span class="c-label">Bedeutung</span>
                    <div class="c-text" style="font-style:italic; opacity:0.9;">
                        "{data['desc']}"
                    </div>
                    
                    <span class="c-label">Struktur (52 Tage)</span>
                    <div style="margin-top:2px;">
            """, unsafe_allow_html=True)
            
            # Die Liste der 4 Wellen
            for w in data['waves']:
                active_class = "wave-active" if w['is_active'] else "style='color:#666'"
                marker = "➤" if w['is_active'] else "•"
                
                st.markdown(f"""
                    <div class="wave-list-item">
                        <span {active_class}>{marker} {w['label']}</span>
                        <span style="opacity:0.6">{w['range']}</span>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div></div>", unsafe_allow_html=True)
