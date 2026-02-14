import streamlit as st

# ==============================================================================
# 1. VISUAL FX ENGINE (Castle Chip CSS)
# ==============================================================================
def inject_castle_css(castle_color_hex):
    """
    Erzeugt einen kompakten, hoch-detaillierten Daten-Chip.
    """
    st.markdown(f"""
        <style>
        /* --- DER CHIP (Expander Header) --- */
        div[data-testid="stExpander"] details summary {{
            /* Hintergrund: Dunkel mit feinem Gitter */
            background-color: rgba(20, 20, 25, 0.9) !important;
            background-image: 
                linear-gradient({castle_color_hex} 1px, transparent 1px),
                linear-gradient(90deg, {castle_color_hex} 1px, transparent 1px);
            background-size: 15px 15px;
            background-blend-mode: overlay;
            
            /* Rahmen: Leuchtend in Schloss-Farbe */
            border: 1px solid {castle_color_hex};
            border-left: 4px solid {castle_color_hex};
            border-radius: 4px;
            
            /* Text */
            color: #fff !important;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
            
            /* Kompakt */
            padding: 8px 12px !important;
            min-height: 40px;
            margin-bottom: 5px;
            transition: all 0.3s ease;
        }}
        
        /* Hover Effekt */
        div[data-testid="stExpander"] details summary:hover {{
            box-shadow: 0 0 15px {castle_color_hex};
            border-color: #fff;
        }}

        /* --- DEEP CONTENT (HUD) --- */
        .castle-hud-container {{
            border: 1px solid {castle_color_hex};
            background: rgba(0,0,0,0.5);
            padding: 10px;
            border-top: none;
            margin-top: -5px;
        }}
        
        .hud-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 4px;
            margin-top: 10px;
        }}
        
        .hud-block {{
            background: #222;
            border: 1px solid #444;
            color: #888;
            font-size: 0.6rem;
            text-align: center;
            padding: 5px 2px;
            font-family: 'Rajdhani', sans-serif;
        }}
        
        .hud-block.active {{
            background: {castle_color_hex};
            color: #000;
            font-weight: bold;
            border-color: #fff;
            box-shadow: 0 0 8px {castle_color_hex};
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. LOGIC (52-Tage Architektur)
# ==============================================================================
def calculate_castle_data(current_kin):
    kin_idx = current_kin - 1
    
    # Welches Schloss? (0-4)
    castle_idx = kin_idx // 52
    
    castles = [
        {"name": "Rotes Schloss", "sub": "Start", "color": "#FF3E3E", "dir": "Osten", "action": "Geburt"},
        {"name": "Weißes Schloss", "sub": "Läuterung", "color": "#E0E0E0", "dir": "Norden", "action": "Tod"},
        {"name": "Blaues Schloss", "sub": "Magie", "color": "#2A8CFF", "dir": "Westen", "action": "Wandel"},
        {"name": "Gelbes Schloss", "sub": "Reifen", "color": "#FFD700", "dir": "Süden", "action": "Intelligenz"},
        {"name": "Grünes Schloss", "sub": "Matrix", "color": "#00FF66", "dir": "Mitte", "action": "Sync"}
    ]
    
    c_data = castles[castle_idx]
    
    # Position
    day_in_castle = (kin_idx % 52) + 1
    current_wave_idx = (day_in_castle - 1) // 13
    
    # Wellen im Schloss generieren
    waves = []
    castle_start_kin = (castle_idx * 52) + 1
    wave_colors = ["Rot", "Weiß", "Blau", "Gelb"]
    
    for i in range(4):
        w_start = castle_start_kin + (i * 13)
        waves.append({
            "color": wave_colors[i],
            "start": w_start,
            "end": w_start + 12
        })

    return {
        "name": c_data["name"],
        "sub": c_data["sub"],
        "color": c_data["color"],
        "dir": c_data["dir"],
        "action": c_data["action"],
        "day": day_in_castle,
        "active_wave_idx": current_wave_idx,
        "waves": waves
    }

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    meta = pulse['metadata']
    if meta['is_leap_day']: return

    # Berechnen
    castle = calculate_castle_data(meta['kin'])
    
    # CSS laden
    inject_castle_css(castle['color'])
    
    # --- DER KOMPAKTE CHIP (Expander Label) ---
    label = f"🏰 {castle['name']} ({castle['day']}/52)"
    
    with st.expander(label):
        # --- HIDDEN HUD (Wird ausgeklappt) ---
        st.markdown(f"""
            <div class="castle-hud-container">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:1.1rem; color:{castle['color']}; font-weight:bold;">{castle['sub'].upper()}</div>
                        <div style="font-size:0.8rem; color:#aaa;">{castle['dir']} • {castle['action']}</div>
                    </div>
                    <div style="font-size:2rem; opacity:0.2;">🏰</div>
                </div>
                
                <div class="hud-grid">
        """, unsafe_allow_html=True)
        
        # Grid HTML loop
        grid_html = ""
        for i, w in enumerate(castle['waves']):
            is_active = (i == castle['active_wave_idx'])
            css_class = "hud-block active" if is_active else "hud-block"
            marker = "⚡" if is_active else ""
            grid_html += f"""
                <div class="{css_class}">
                    {marker} {w['color']}<br>
                    {w['start']}-{w['end']}
                </div>
            """
            
        st.markdown(grid_html + "</div></div>", unsafe_allow_html=True)
