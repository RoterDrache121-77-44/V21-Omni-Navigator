import streamlit as st

# ==============================================================================
# 1. VISUAL FX ENGINE (Dual Time-Chip CSS)
# ==============================================================================
def inject_time_css(wave_color, castle_color, progress_pct):
    st.markdown(f"""
        <style>
        /* --- SHARED CHIP BASE --- */
        .time-chip {{
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
            position: relative;
            overflow: hidden;
        }}

        /* --- LEFT: WAVE CHIP (Animated Flux) --- */
        @keyframes subtle-flux {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stExpander"] details summary {{
            border-left: 4px solid {wave_color} !important;
            background: linear-gradient(90deg, rgba(15,15,20,0.95) 0%, rgba(40,40,50,0.95) 100%); 
            color: #fff !important;
            font-family: 'Orbitron', sans-serif; /* Tech Font für Welle */
            border-radius: 4px;
        }}
        
        /* Progress Bar im Wave Chip (Unten) */
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stExpander"] details summary::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            height: 3px;
            background: {wave_color};
            width: {progress_pct}%;
            box-shadow: 0 0 10px {wave_color};
            transition: width 1s ease;
        }}

        /* --- RIGHT: CASTLE CHIP (Solid Fortress) --- */
        div[data-testid="column"]:nth-of-type(2) div[data-testid="stExpander"] details summary {{
            border-right: 4px solid {castle_color} !important;
            background-color: rgba(15, 15, 20, 0.95) !important;
            /* Feines Gitter-Muster für Schloss-Look */
            background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 10px 10px;
            
            color: #e0e0e0 !important;
            font-family: 'Orbitron', sans-serif;
            border-radius: 4px;
            text-align: right !important;
            flex-direction: row-reverse;
        }}

        /* --- CONTENT STYLING --- */
        .deep-panel {{
            background: rgba(255,255,255,0.03);
            padding: 12px;
            margin-top: 5px;
            font-size: 0.85rem;
            border-radius: 4px;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        
        .section-title {{
            font-size: 0.75rem;
            text-transform: uppercase;
            color: #888;
            margin-bottom: 4px;
            display: block;
            letter-spacing: 1px;
        }}
        
        .highlight-val {{
            font-size: 1rem;
            font-weight: bold;
            color: #fff;
            margin-bottom: 10px;
            display: block;
        }}

        .timeline-row {{
            display: flex;
            justify-content: space-between;
            padding: 4px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. DATA LOGIC (Deep Dive Calculation)
# ==============================================================================
def get_wave_data(kin):
    kin_idx = kin - 1
    
    # 1. Basis-Werte
    wave_start_idx = (kin_idx // 13) * 13
    wave_start_kin = wave_start_idx + 1
    current_tone = (kin_idx % 13) + 1
    progress = (current_tone / 13) * 100
    
    # 2. Farbe & Name (Start-Siegel)
    start_seal_id = wave_start_idx % 20
    seal_names = ["Drache", "Wind", "Nacht", "Samen", "Schlange", "Weltenüberbrücker", "Hand", "Stern", "Mond", "Hund", "Affe", "Mensch", "Himmelswanderer", "Magier", "Adler", "Krieger", "Erde", "Spiegel", "Sturm", "Sonne"]
    
    colors = ["Rot", "Weiß", "Blau", "Gelb"]
    wave_color_name = colors[start_seal_id % 4]
    wave_color_hex = {"Rot":"#FF3E3E", "Weiß":"#E0E0E0", "Blau":"#2A8CFF", "Gelb":"#FFD700"}[wave_color_name]
    
    # 3. Mission des Tones (Coaching Aspekt)
    tone_missions = {
        1: "Zweck: Was ist das Ziel? Ziehe es an.",
        2: "Herausforderung: Was steht im Weg? Stabilisiere dich.",
        3: "Dienst: Wie komme ich ins Tun? Aktiviere den Fluss.",
        4: "Form: Wie sieht der Plan aus? Definiere die Maße.",
        5: "Strahlkraft: Woher nehme ich die Ressource? Ermächtige dich.",
        6: "Gleichgewicht: Wie organisiere ich mich? Finde die Balance.",
        7: "Einstimmung: Wie verbinde ich mich? Kanalisiere die Info.",
        8: "Integrität: Lebe ich, was ich glaube? Harmonisiere dich.",
        9: "Absicht: Der letzte Impuls. Realisiere die Bewegung.",
        10: "Manifestation: Das Ergebnis wird sichtbar. Perfektioniere es.",
        11: "Befreiung: Was muss gehen? Lasse los (Dissonanz).",
        12: "Zusammenkunft: Das Fazit. Verstehe das Ganze.",
        13: "Präsenz: Der Übergang. Feiere den magischen Flug."
    }
    
    return {
        "name": f"{seal_names[start_seal_id]}",
        "fullname": f"Welle des {seal_names[start_seal_id]}n",
        "tone": current_tone,
        "progress": progress,
        "start": wave_start_kin,
        "end": wave_start_kin + 12,
        "color": wave_color_hex,
        "mission": tone_missions.get(current_tone, "Sein."),
        "purpose_kin": f"Kin {wave_start_kin}",
        "goal_kin": f"Kin {wave_start_kin + 12}"
    }

def get_castle_data(kin):
    kin_idx = kin - 1
    castle_idx = kin_idx // 52
    
    castles = [
        {"name": "Rotes Schloss", "sub": "Wende", "act": "Geburt / Initiierung", "dir": "Osten", "color": "#FF3E3E"},
        {"name": "Weißes Schloss", "sub": "Kreuzen", "act": "Tod / Läuterung", "dir": "Norden", "color": "#E0E0E0"},
        {"name": "Blaues Schloss", "sub": "Brennen", "act": "Magie / Wandel", "dir": "Westen", "color": "#2A8CFF"},
        {"name": "Gelbes Schloss", "sub": "Geben", "act": "Reife / Intelligenz", "dir": "Süden", "color": "#FFD700"},
        {"name": "Grünes Schloss", "sub": "Zauber", "act": "Matrix / Sync", "dir": "Zentrum", "color": "#00FF66"}
    ]
    c = castles[castle_idx]
    
    day_in_castle = (kin_idx % 52) + 1
    
    # Die 4 Wellen im Schloss berechnen
    waves_in_castle = []
    castle_start_kin = (castle_idx * 52) + 1
    w_colors = ["Rot", "Weiß", "Blau", "Gelb"]
    
    current_wave_idx = (day_in_castle - 1) // 13
    
    for i in range(4):
        w_start = castle_start_kin + (i * 13)
        waves_in_castle.append({
            "label": f"{w_colors[i]}e Welle",
            "range": f"{w_start}-{w_start+12}",
            "active": (i == current_wave_idx)
        })
        
    return {**c, "day": day_in_castle, "sub_waves": waves_in_castle}

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    meta = pulse['metadata']
    if meta['is_leap_day']: return
    
    # Daten
    wave = get_wave_data(meta['kin'])
    castle = get_castle_data(meta['kin'])
    
    # Style
    inject_time_css(wave['color'], castle['color'], wave['progress'])
    
    # Layout
    c1, c2 = st.columns(2)
    
    # --- LINKS: DIE WELLE (Micro) ---
    with c1:
        label = f"🌊 {wave['name']} ({wave['tone']}/13)"
        with st.expander(label):
            st.markdown(f"""
                <div class="deep-panel" style="border-left: 2px solid {wave['color']}">
                    <span class="section-title">Heutige Mission (Ton {wave['tone']})</span>
                    <div class="highlight-val" style="color:{wave['color']}">{wave['mission']}</div>
                    
                    <div class="timeline-row">
                        <span style="color:#888">Start (Zweck)</span>
                        <strong>{wave['purpose_kin']}</strong>
                    </div>
                    <div class="timeline-row">
                        <span style="color:#888">Ziel (Flug)</span>
                        <strong>{wave['goal_kin']}</strong>
                    </div>
                    
                    <div style="margin-top:10px; font-size:0.75rem; color:#aaa; font-style:italic;">
                        "{wave['fullname']}" definiert den Kontext der aktuellen 13 Tage.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # --- RECHTS: DAS SCHLOSS (Macro) ---
    with c2:
        label = f"🏰 {castle['name']} ({castle['day']}/52)"
        with st.expander(label):
            st.markdown(f"""
                <div class="deep-panel" style="border-right: 2px solid {castle['color']}; text-align:right;">
                    <span class="section-title">Kontext: {castle['sub'].upper()}</span>
                    <div class="highlight-val" style="color:{castle['color']}">{castle['act']}</div>
                    
                    <div class="timeline-row" style="justify-content: flex-end; gap:10px;">
                        <strong>{castle['dir']}</strong>
                        <span style="color:#888">Himmelsrichtung</span>
                    </div>
                    
                    <hr style="border-color:rgba(255,255,255,0.1); margin:8px 0;">
                    <span class="section-title" style="text-align:right;">Zeitlinie (4 Wellen)</span>
            """, unsafe_allow_html=True)
            
            # Wellen-Liste (Rechtsbündig)
            for w in castle['sub_waves']:
                marker = "⚡" if w['active'] else ""
                style = f"color:#fff; font-weight:bold;" if w['active'] else "color:#666;"
                st.markdown(f"""
                    <div style="display:flex; justify-content:flex-end; font-size:0.8rem; {style} padding:2px 0;">
                        <span>{w['label']} ({w['range']}) {marker}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
