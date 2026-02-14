import streamlit as st

# ==============================================================================
# 1. VISUAL FX ENGINE (Castle HUD)
# ==============================================================================
def inject_castle_css(castle_color_hex, active_wave_idx):
    """
    Zeichnet eine Festungs-Architektur.
    active_wave_idx: 0 bis 3 (Welche der 4 Wellen ist aktiv?)
    """
    st.markdown(f"""
        <style>
        /* --- CASTLE CONTAINER --- */
        .castle-fortress {{
            border: 2px solid {castle_color_hex};
            background: rgba(0,0,0,0.4);
            border-radius: 4px;
            padding: 10px;
            margin-bottom: 5px;
            position: relative;
            /* Ein feines Gitter im Hintergrund */
            background-image: linear-gradient({castle_color_hex} 1px, transparent 1px),
            linear-gradient(90deg, {castle_color_hex} 1px, transparent 1px);
            background-size: 20px 20px;
            background-blend-mode: overlay;
            opacity: 0.9;
        }}

        /* Header Label */
        .castle-header {{
            background: {castle_color_hex};
            color: #000;
            font-family: 'Orbitron', sans-serif;
            font-weight: bold;
            text-transform: uppercase;
            padding: 2px 8px;
            display: inline-block;
            font-size: 0.8rem;
            margin-bottom: 10px;
        }}

        /* --- DIE 4 TÜRME (Wellen) --- */
        .castle-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 5px;
        }}

        .wave-block {{
            border: 1px solid rgba(255,255,255,0.2);
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            color: #aaa;
            background: rgba(0,0,0,0.8);
            font-family: 'Rajdhani', sans-serif;
            text-align: center;
            flex-direction: column;
        }}

        /* Der aktive Block leuchtet */
        .wave-block-active {{
            border: 1px solid {castle_color_hex};
            background: rgba({castle_color_hex}, 0.2); /* Hex muss hier RGB sein, wir tricksen */
            background: {castle_color_hex};
            color: #000;
            font-weight: bold;
            box-shadow: 0 0 10px {castle_color_hex};
            transform: scale(1.05);
            z-index: 2;
        }}

        .mini-label {{ font-size: 0.6rem; opacity: 0.7; }}
        
        /* Deep Content Styling */
        .castle-deep {{
            border-left: 2px solid {castle_color_hex};
            padding-left: 10px;
            margin-top: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. LOGIC (Die 52-Tage Architektur)
# ==============================================================================
def calculate_castle_data(current_kin):
    kin_idx = current_kin - 1
    
    # 1. Welches Schloss? (0-4)
    castle_idx = kin_idx // 52
    
    # 2. Daten der 5 Schlösser
    castles = [
        {"name": "Rotes Schloss des Drehens", "color": "#FF3E3E", "dir": "Osten", "action": "Geburt"},
        {"name": "Weißes Schloss des Kreuzens", "color": "#E0E0E0", "dir": "Norden", "action": "Tod/Läuterung"},
        {"name": "Blaues Schloss des Brennens", "color": "#2A8CFF", "dir": "Westen", "action": "Transformation/Magie"},
        {"name": "Gelbes Schloss des Gebens", "color": "#FFD700", "dir": "Süden", "action": "Reifen/Intelligenz"},
        {"name": "Grünes Schloss der Verzauberung", "color": "#00FF66", "dir": "Zentrum", "action": "Matrix/Synchronisation"}
    ]
    
    c_data = castles[castle_idx]
    
    # 3. Position im Schloss (1-52)
    day_in_castle = (kin_idx % 52) + 1
    
    # 4. Welche Welle im Schloss? (0-3)
    # Jedes Schloss hat 4 Wellen: Rot, Weiß, Blau, Gelb
    current_wave_idx = (day_in_castle - 1) // 13
    
    # Start Kin des Schlosses
    castle_start_kin = (castle_idx * 52) + 1
    
    # Die 4 Wellen dieses Schlosses berechnen
    waves = []
    seal_names = [
        "Drache", "Wind", "Nacht", "Samen", "Schlange", "Weltenüberbrücker", "Hand",
        "Stern", "Mond", "Hund", "Affe", "Mensch", "Himmelswanderer", "Magier",
        "Adler", "Krieger", "Erde", "Spiegel", "Sturm", "Sonne"
    ]
    
    for i in range(4):
        # Start Kin der Welle
        w_start = castle_start_kin + (i * 13)
        # Siegel Index (0-19)
        s_idx = (w_start - 1) % 20 
        w_name = seal_names[s_idx]
        
        # Farbe der Welle (Rot, Weiß, Blau, Gelb)
        wave_colors = ["Rot", "Weiß", "Blau", "Gelb"]
        
        waves.append({
            "name": w_name,
            "color": wave_colors[i],
            "start": w_start,
            "end": w_start + 12
        })

    return {
        "idx": castle_idx,
        "name": c_data["name"],
        "color": c_data["color"],
        "direction": c_data["dir"],
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
    inject_castle_css(castle['color'], castle['active_wave_idx'])
    
    # --- VISUAL HUD ---
    st.markdown(f"""
        <div class="castle-fortress">
            <div class="castle-header">{castle['name']}</div>
            <div style="font-size:0.8rem; color:#ddd; margin-bottom:5px;">
                Tag {castle['day']} / 52 • {castle['direction']} • {castle['action']}
            </div>
            
            <div class="castle-grid">
    """, unsafe_allow_html=True)
    
    # Grid generieren
    cols = st.columns(4) # Wir nutzen Streamlit Columns für Layout, aber HTML für Style
    # Halt, wir müssen HTML generieren für die 'wave-block' Klassen.
    
    grid_html = ""
    for i, w in enumerate(castle['waves']):
        is_active = (i == castle['active_wave_idx'])
        css_class = "wave-block wave-block-active" if is_active else "wave-block"
        
        grid_html += f"""
            <div class="{css_class}">
                <span class="mini-label">{w['color']}</span>
                <span>{w['name'][:3]}.</span> </div>
        """
    
    st.markdown(grid_html + "</div></div>", unsafe_allow_html=True)

    # --- DER GRIFF (Expander) ---
    with st.expander("🏰 Schloss-Architektur ansehen"):
        st.markdown(f"""
            <div class="castle-deep">
                <strong style="color:{castle['color']}">{castle['direction']}e Himmelsrichtung</strong>
                <p>Dieses Schloss dient dazu, die Energie zu <strong>{castle['action']}</strong>.</p>
                <hr style="border-color:rgba(255,255,255,0.1)">
                <div style="font-size:0.9rem;">
        """, unsafe_allow_html=True)
        
        # Tabelle der 4 Wellen
        for i, w in enumerate(castle['waves']):
            marker = "➤" if i == castle['active_wave_idx'] else "•"
            style = f"color:{castle['color']}; font-weight:bold;" if i == castle['active_wave_idx'] else "color:#888;"
            
            st.markdown(f"""
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; {style}">
                    <span>{marker} {w['color']}e Welle ({w['name']})</span>
                    <span>Kin {w['start']}-{w['end']}</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div></div>", unsafe_allow_html=True)
