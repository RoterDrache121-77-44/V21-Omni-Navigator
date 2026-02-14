import streamlit as st

# ==============================================================================
# 1. VISUAL FX ENGINE (Dynamic Wave CSS)
# ==============================================================================
def inject_wave_css(wave_color_hex, progress_pct):
    """
    Erzeugt einen ultra-flachen, klickbaren Expander mit wilder Animation.
    """
    st.markdown(f"""
        <style>
        /* --- WILD FLUX ANIMATION --- */
        @keyframes flux-flow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* --- DER EXPANDER ALS BUTTON (Der Hack) --- */
        /* Wir zielen genau auf den Header des Expanders */
        div[data-testid="stExpander"] details summary {{
            /* Hintergrund: Wilder Gradient basierend auf Wellen-Farbe */
            background: linear-gradient(90deg, 
                {wave_color_hex} 0%, 
                #000 50%, 
                {wave_color_hex} 100%);
            background-size: 200% 200%;
            animation: flux-flow 3s ease infinite;
            
            /* Flacher Look */
            border: 1px solid {wave_color_hex};
            border-radius: 4px; /* Eckiger/Flacher */
            color: #fff !important;
            
            /* Typografie */
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            font-size: 1rem;
            
            /* Kompakt */
            padding: 10px 15px !important;
            min-height: 45px;
            margin-bottom: 5px;
            
            /* Progress Bar Hack: Ein Schatten nach innen als Balken */
            box-shadow: inset {progress_pct * 5}px -3px 0px 0px rgba(255,255,255,0.8);
            transition: box-shadow 1s ease;
        }}
        
        /* Hover Effekt */
        div[data-testid="stExpander"] details summary:hover {{
            box-shadow: inset {progress_pct * 5}px -3px 0px 0px #fff, 0 0 15px {wave_color_hex};
            color: #fff;
        }}

        /* Pfeil verstecken (Optional, macht es sauberer) */
        div[data-testid="stExpander"] details summary svg {{
            opacity: 0.5;
            color: #fff;
        }}
        
        /* Inhalt Style */
        .wave-content {{
            background: rgba(0,0,0,0.3);
            border-left: 2px solid {wave_color_hex};
            padding: 15px;
            margin-top: 5px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. LOGIC (Berechnung der Welle & Farbe)
# ==============================================================================
def calculate_wave_data(current_kin):
    # 0-basiert rechnen
    kin_idx = current_kin - 1
    
    # Start der Welle (immer Ton 1)
    wave_start_idx = (kin_idx // 13) * 13
    wave_start_kin = wave_start_idx + 1
    
    # Position (1-13)
    current_tone = (kin_idx % 13) + 1
    progress = (current_tone / 13) * 100
    
    # Farbe der Welle bestimmen (Basierend auf Start-Siegel)
    # Start Siegel ID (0-19)
    # 0=Rot, 1=Weiß, 2=Blau, 3=Gelb ... Modulo 4
    start_seal_id = wave_start_idx % 20
    color_code = start_seal_id % 4
    
    # Mapping
    color_map = {
        0: ("Rot", "#FF0040"),    # Neon Rot
        1: ("Weiß", "#E0E0E0"),   # Helles Grau/Weiß
        2: ("Blau", "#0080FF"),   # Electric Blue
        3: ("Gelb", "#FFD700")    # Gold Gelb
    }
    
    color_name, color_hex = color_map.get(color_code, ("Weiß", "#fff"))
    
    # Name der Welle (Siegel Name holen)
    seal_names = [
        "Drache", "Wind", "Nacht", "Samen", "Schlange", "Weltenüberbrücker", "Hand",
        "Stern", "Mond", "Hund", "Affe", "Mensch", "Himmelswanderer", "Magier",
        "Adler", "Krieger", "Erde", "Spiegel", "Sturm", "Sonne"
    ]
    wave_name = seal_names[start_seal_id]
    
    return {
        "name": f"Welle des {wave_name}",
        "color_name": color_name,
        "color_hex": color_hex,
        "tone": current_tone,
        "progress": progress,
        "start": wave_start_kin,
        "end": wave_start_kin + 12
    }

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    meta = pulse['metadata']
    if meta['is_leap_day']:
        st.info("Hunab Ku: Keine lineare Zeitwelle.")
        return

    # 1. Berechnen
    wave = calculate_wave_data(meta['kin'])
    
    # 2. CSS Injizieren (Das ist der Trick für das Aussehen)
    inject_wave_css(wave['color_hex'], wave['progress'])
    
    # 3. Der Button (Expander)
    # Der Label-Text ist das, was auf dem Button steht
    label_text = f"🌊 {wave['name']} ({wave['tone']}/13)"
    
    with st.expander(label_text, expanded=False):
        # --- INHALT (Wird erst beim Klick sichtbar) ---
        st.markdown(f"""
            <div class="wave-content">
                <h3 style="margin-top:0;">Analyse: {wave['name']}</h3>
                <p style="color:#aaa;">Die Welle wird gefärbt durch die Energie: <strong>{wave['color_name']}</strong>.</p>
                
                <div style="display:flex; justify-content:space-between; margin-top:20px;">
                    <div style="text-align:center;">
                        <div style="font-size:0.8rem; color:#888;">START</div>
                        <div style="font-size:1.2rem; font-weight:bold;">KIN {wave['start']}</div>
                        <div style="font-size:0.7rem;">(Zweck)</div>
                    </div>
                    <div style="font-size:2rem;">➔</div>
                    <div style="text-align:center;">
                        <div style="font-size:0.8rem; color:#888;">ZIEL</div>
                        <div style="font-size:1.2rem; font-weight:bold;">KIN {wave['end']}</div>
                        <div style="font-size:0.7rem;">(Flug)</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tages-Mission
        current_tone = wave['tone']
        wave_steps = {
            1: "Zweck definieren (Anziehen)",
            2: "Herausforderung annehmen (Stabilisieren)",
            3: "Dienst aktivieren (Verbinden)",
            4: "Form definieren (Messen)",
            5: "Ressourcen sammeln (Ermächtigen)",
            6: "Organisieren (Ausgleichen)",
            7: "Einstimmen (Kanalisieren)",
            8: "Integrität leben (Harmonisieren)",
            9: "Absicht pulsieren (Realisieren)",
            10: "Perfektionieren (Manifestieren)",
            11: "Loslassen (Auflösen)",
            12: "Kooperieren (Universalisieren)",
            13: "Transzendieren (Präsent sein)"
        }
        mission = wave_steps.get(current_tone, "Sein")
        
        st.markdown(f"""
            <div style="margin-top:10px; padding:10px; background:rgba(255,255,255,0.05); border-radius:4px;">
                <strong>📍 Deine Aufgabe heute (Ton {current_tone}):</strong><br>
                <span style="color:{wave['color_hex']}; font-size:1.1rem;">{mission}</span>
            </div>
        """, unsafe_allow_html=True)
