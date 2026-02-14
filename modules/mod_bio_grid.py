import streamlit as st

# ==============================================================================
# 1. VISUAL FX ENGINE
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
        }}

        /* --- LINKER CHIP: WELLE (mit Progress Bar) --- */
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stExpander"] details summary {{
            border-left: 4px solid {wave_color} !important;
            background: linear-gradient(90deg, rgba(15,15,20,0.95) 0%, rgba(40,40,50,0.95) 100%); 
            color: #fff !important;
            font-family: 'Orbitron', sans-serif;
            border-radius: 4px;
            position: relative;
            overflow: hidden;
        }}
        
        /* Progress Bar Animation (Unten am Chip) */
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

        /* --- RECHTER CHIP: SCHLOSS (Gitter) --- */
        div[data-testid="column"]:nth-of-type(2) div[data-testid="stExpander"] details summary {{
            border-right: 4px solid {castle_color} !important;
            background-color: rgba(15, 15, 20, 0.95) !important;
            background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 10px 10px;
            color: #e0e0e0 !important;
            font-family: 'Orbitron', sans-serif;
            border-radius: 4px;
            text-align: right !important;
            flex-direction: row-reverse; /* Pfeil nach links */
        }}

        /* --- INHALT STYLING --- */
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
# 2. DATA LOGIC
# ==============================================================================
def get_wave_data(kin):
    kin_idx = kin - 1
    
    # Basis
    wave_start_idx = (kin_idx // 13) * 13
    wave_start_kin = wave_start_idx + 1
    current_tone = (kin_idx % 13) + 1
    progress = (current_tone / 13) * 100
    
    # Farbe & Name
    start_seal_id = wave_start_idx % 20
    seal_names = ["Drache", "Wind", "Nacht", "Samen", "Schlange", "Weltenüberbrücker", "Hand", "Stern", "Mond", "Hund", "Affe", "Mensch", "Himmelswanderer", "Magier", "Adler", "Krieger", "Erde", "Spiegel", "Sturm", "Sonne"]
    
    # Mapping
    colors = ["Rot", "Weiß", "Blau", "Gelb"]
    wave_color_name = colors[start_seal_id % 4]
    wave_color_hex = {"Rot":"#FF3E3E", "Weiß":"#E0E0E0", "Blau":"#2A8CFF", "Gelb":"#FFD700"}[wave_color_name]
    
    wave_name = seal_names[start_seal_id]
    
    # Missionen (Kurz & Knackig)
    tone_missions = {
        1: "Zweck: Was ist das Ziel?",
        2: "Herausforderung: Was steht im Weg?",
        3: "Dienst: Wie komme ich ins Tun?",
        4: "Form: Wie sieht der Plan aus?",
        5: "Strahlkraft: Wo sind meine Ressourcen?",
        6: "Gleichgewicht: Wie organisiere ich mich?",
        7: "Einstimmung: Wie verbinde ich mich?",
        8: "Integrität: Lebe ich, was ich glaube?",
        9: "Absicht: Der letzte Impuls.",
        10: "Manifestation: Das Ergebnis wird sichtbar.",
        11: "Befreiung: Was muss ich loslassen?",
        12: "Zusammenkunft: Verstehe das Ganze.",
        13: "Präsenz: Feiere den Übergang."
    }
    
    return {
        "name": wave_name,
        "tone": current_tone,
        "progress": progress,
        "color": wave_color_hex,
        "mission": tone_missions.get(current_tone, "Sein."),
        "start": f"Kin {wave_start_kin}",
        "end": f"Kin {wave_start_kin + 12}"
    }

def get_castle_data(kin):
    kin_idx = kin - 1
    castle_idx = kin_idx // 52
    
    castles = [
        {"name": "Rotes Schloss", "sub": "Wende", "act": "Geburt", "dir": "Osten", "color": "#FF3E3E"},
        {"name": "Weißes Schloss", "sub": "Kreuzen", "act": "Läuterung", "dir": "Norden", "color": "#E0E0E0"},
        {"name": "Blaues Schloss", "sub": "Brennen", "act": "Magie", "dir": "Westen", "color": "#2A8CFF"},
        {"name": "Gelbes Schloss", "sub": "Geben", "act": "Reife", "dir": "Süden", "color": "#FFD700"},
        {"name": "Grünes Schloss", "sub": "Zauber", "act": "Matrix", "dir": "Zentrum", "color": "#00FF66"}
    ]
    c = castles[castle_idx]
    day = (kin_idx % 52) + 1
    
    # 4 Wellen berechnen
    waves = []
    castle_start = (castle_idx * 52) + 1
    colors = ["Rot", "Weiß", "Blau", "Gelb"]
    curr_wave_idx = (day - 1) // 13
    
    for i in range(4):
        ws = castle_start + (i*13)
        waves.append({
            "label": f"{colors[i]}e Welle",
            "range": f"{ws}-{ws+12}",
            "active": (i == curr_wave_idx)
        })
        
    return {**c, "day": day, "waves": waves}

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    meta = pulse['metadata']
    if meta['is_leap_day']: return
    
    w = get_wave_data(meta['kin'])
    c = get_castle_data(meta['kin'])
    
    inject_time_css(w['color'], c['color'], w['progress'])
    
    cols = st.columns(2)
    
    # --- WELLE (LINKS) ---
    with cols[0]:
        with st.expander(f"🌊 {w['name']} ({w['tone']}/13)"):
            # WICHTIG: unsafe_allow_html=True
            st.markdown(f"""
                <div class="deep-panel" style="border-left: 2px solid {w['color']}">
                    <span class="section-title">Heutige Mission (Ton {w['tone']})</span>
                    <div class="highlight-val" style="color:{w['color']}">{w['mission']}</div>
                    
                    <div class="timeline-row">
                        <span style="color:#888">Start (Zweck)</span>
                        <strong>{w['start']}</strong>
                    </div>
                    <div class="timeline-row">
                        <span style="color:#888">Ziel (Flug)</span>
                        <strong>{w['end']}</strong>
                    </div>
                    
                    <div style="margin-top:10px; font-size:0.75rem; color:#aaa; font-style:italic;">
                        "Welle: {w['name']}" definiert den Kontext.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # --- SCHLOSS (RECHTS) ---
    with cols[1]:
        with st.expander(f"🏰 {c['name']} ({c['day']}/52)"):
            # WICHTIG: unsafe_allow_html=True
            st.markdown(f"""
                <div class="deep-panel" style="border-right: 2px solid {c['color']}; text-align:right;">
                    <span class="section-title">Kontext: {c['sub'].upper()}</span>
                    <div class="highlight-val" style="color:{c['color']}">{c['act']}</div>
                    
                    <div class="timeline-row" style="justify-content: flex-end; gap:10px;">
                        <strong>{c['dir']}</strong>
                        <span style="color:#888">Richtung</span>
                    </div>
                    
                    <hr style="border-color:rgba(255,255,255,0.1); margin:8px 0;">
                    <span class="section-title" style="text-align:right;">Zeitlinie</span>
            """, unsafe_allow_html=True)
            
            # Wellen Loop
            for item in c['waves']:
                marker = "⚡" if item['active'] else ""
                style = "color:#fff; font-weight:bold;" if item['active'] else "color:#666;"
                st.markdown(f"""
                    <div style="display:flex; justify-content:flex-end; font-size:0.8rem; {style} padding:2px 0;">
                        <span>{item['label']} ({item['range']}) {marker}</span>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
