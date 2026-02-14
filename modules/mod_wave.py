import streamlit as st

# ==============================================================================
# 1. VISUAL FX ENGINE (Isolierte Welle)
# ==============================================================================
def inject_wave_css(wave_color_hex, progress_pct):
    st.markdown(f"""
        <style>
        /* --- WILD FLUX ANIMATION (Lokal) --- */
        @keyframes flux-flow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* --- DER WAVE-CONTAINER (Ersetzt den Expander-Style) --- */
        .wave-visual-bar {{
            /* Hintergrund: Wilder Gradient */
            background: linear-gradient(90deg, 
                {wave_color_hex} 0%, 
                #000 50%, 
                {wave_color_hex} 100%);
            background-size: 200% 200%;
            animation: flux-flow 3s ease infinite;
            
            /* Form */
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px 6px 0 0; /* Oben rund, unten eckig (für Anschluss) */
            padding: 12px 15px;
            margin-bottom: 0px; /* Klebt am Expander */
            position: relative;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}

        /* Progress Linie (Unten im Balken) */
        .wave-progress-line {{
            position: absolute;
            bottom: 0;
            left: 0;
            height: 4px;
            background: #fff;
            box-shadow: 0 0 10px #fff;
            width: {progress_pct}%;
            transition: width 1s ease;
        }}

        /* Text im Balken */
        .wave-text {{
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            font-size: 1.1rem;
            color: #fff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
            display: flex;
            justify-content: space-between;
        }}
        
        /* --- INHALT STYLE (Wenn offen) --- */
        .wave-deep-content {{
            background: rgba(20,20,25,0.9);
            border: 1px solid rgba(255,255,255,0.1);
            border-top: none;
            border-radius: 0 0 6px 6px;
            padding: 15px;
            margin-top: -1px; /* Nahtloser Übergang */
        }}
        
        .wave-data-row {{
            display: flex; 
            justify-content: space-between; 
            border-bottom: 1px solid rgba(255,255,255,0.1); 
            padding: 5px 0;
            font-size: 0.9rem;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. LOGIC (Berechnung)
# ==============================================================================
def calculate_wave_data(current_kin):
    kin_idx = current_kin - 1
    
    # Wellen-Mathematik
    wave_start_idx = (kin_idx // 13) * 13
    wave_start_kin = wave_start_idx + 1
    current_tone = (kin_idx % 13) + 1
    progress = (current_tone / 13) * 100
    
    # Farbe bestimmen (Start-Siegel)
    start_seal_id = wave_start_idx % 20
    color_code = start_seal_id % 4
    
    color_map = {
        0: ("Rot", "#FF0040"),
        1: ("Weiß", "#E0E0E0"),
        2: ("Blau", "#0080FF"),
        3: ("Gelb", "#FFD700")
    }
    color_name, color_hex = color_map.get(color_code, ("Weiß", "#fff"))
    
    # Name der Welle
    seal_names = [
        "Drache", "Wind", "Nacht", "Samen", "Schlange", "Weltenüberbrücker", "Hand",
        "Stern", "Mond", "Hund", "Affe", "Mensch", "Himmelswanderer", "Magier",
        "Adler", "Krieger", "Erde", "Spiegel", "Sturm", "Sonne"
    ]
    wave_name = seal_names[start_seal_id]
    
    # Schloss
    castle_idx = kin_idx // 52
    castles = ["Rotes Schloss (Start)", "Weißes Schloss (Läuterung)", "Blaues Schloss (Transformation)", "Gelbes Schloss (Reifen)", "Grünes Schloss (Verzauberung)"]
    
    return {
        "name": f"Welle des {wave_name}",
        "raw_name": wave_name,
        "color_name": color_name,
        "color_hex": color_hex,
        "tone": current_tone,
        "progress": progress,
        "start": wave_start_kin,
        "end": wave_start_kin + 12,
        "castle": castles[castle_idx]
    }

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    meta = pulse['metadata']
    if meta['is_leap_day']: return

    # 1. Berechnen
    wave = calculate_wave_data(meta['kin'])
    
    # 2. CSS laden
    inject_wave_css(wave['color_hex'], wave['progress'])
    
    # 3. VISUAL HEADER (Das ist jetzt HTML, kein Streamlit-Widget -> Isoliert!)
    st.markdown(f"""
        <div class="wave-visual-bar">
            <div class="wave-text">
                <span>🌊 {wave['name']}</span>
                <span style="opacity:0.8">{wave['tone']}/13</span>
            </div>
            <div class="wave-progress-line"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # 4. DER GRIFF (Ein neutraler Expander direkt darunter)
    # Wir benutzen hier KEIN Styling für den Expander, damit er das Dashboard nicht kaputt macht.
    with st.expander("🔻 Tiefenanalyse ausklappen"):
        
        # --- DER INHALT (HTML Container für sauberen Look) ---
        st.markdown(f"""
            <div class="wave-deep-content">
                <div style="text-align:center; margin-bottom:15px;">
                    <strong style="font-size:1.2rem; color:{wave['color_hex']}">{wave['castle']}</strong><br>
                    <span style="color:#aaa; font-size:0.8rem;">Kontext der 52 Tage</span>
                </div>
                
                <div class="wave-data-row">
                    <span style="color:#888;">Energie-Farbe</span>
                    <strong>{wave['color_name']}</strong>
                </div>
                <div class="wave-data-row">
                    <span style="color:#888;">Start (Zweck)</span>
                    <strong>Kin {wave['start']} ({wave['raw_name']})</strong>
                </div>
                <div class="wave-data-row">
                    <span style="color:#888;">Ziel (Flug)</span>
                    <strong>Kin {wave['end']} (Kosmisch)</strong>
                </div>
                <div class="wave-data-row">
                    <span style="color:#888;">Aktueller Fokus</span>
                    <strong style="color:#fff;">Ton {wave['tone']}</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Mission Statement (Formatiert, kein Quelltext!)
        current_tone = wave['tone']
        wave_steps = {
            1: "Zweck definieren (Anziehen)", 2: "Herausforderung annehmen (Stabilisieren)",
            3: "Dienst aktivieren (Verbinden)", 4: "Form definieren (Messen)",
            5: "Ressourcen sammeln (Ermächtigen)", 6: "Organisieren (Ausgleichen)",
            7: "Einstimmen (Kanalisieren)", 8: "Integrität leben (Harmonisieren)",
            9: "Absicht pulsieren (Realisieren)", 10: "Perfektionieren (Manifestieren)",
            11: "Loslassen (Auflösen)", 12: "Kooperieren (Universalisieren)",
            13: "Transzendieren (Präsent sein)"
        }
        
        st.info(f"**Deine Mission heute:** {wave_steps.get(current_tone, 'Sein')}")
        
        # Synchronotron Link (Sicherer Check)
        if 'matrix' in pulse['tzolkin']:
            st.caption("📡 441-Matrix Daten verknüpft.")
