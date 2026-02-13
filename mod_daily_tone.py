import streamlit as st

def render(kin_nr, data):
    """
    Rendert die TON-FREQUENZ als kompaktes High-Tech Modul.
    
    ARGUMENTE:
    kin_nr (int): Die Nummer des Kins.
    data (dict): Der Datensatz aus der Tzolkin-DB (entspricht 'kin_data' in app.py).
    """

    # -------------------------------------------------------------------------
    # 0. DATEN-AKQUISE & MINING
    # -------------------------------------------------------------------------
    if kin_nr == 0 or not data:
        return {} 

    # Pfade navigieren
    identity = data.get('identity', {})
    tone = identity.get('tone', {})
    seal = identity.get('seal', {})
    
    # === INTELLIGENTE SUCHE NACH DER PSYCHOLOGIE ===
    # Strategie 1: Direkt in der Identität (Blueprint Standard)
    tone_psych = identity.get('tone_psych', {})
    
    # Strategie 2: Fallback - Falls es doch unter 'seal' -> 'psychology' liegt
    if not tone_psych:
        tone_psych = seal.get('psychology', {}).get('tone_psych', {})

    # Basis Daten (Tone 1-13)
    t_id = tone.get('id', 0)
    t_name = tone.get('name', 'Ton')
    t_action = tone.get('action', '-')
    t_power = tone.get('power', '-')
    t_essence = tone.get('essence', '-')

    # Export für die Pipeline
    export_data = {
        "module": "daily_tone",
        "tone_id": t_id,
        "tone_name": t_name,
        "psych_available": bool(tone_psych)
    }

    # -------------------------------------------------------------------------
    # 1. DESIGN ENGINE: "TACTICAL SLIM"
    # -------------------------------------------------------------------------
    # Wir leiten die Akzentfarbe vom Siegel ab, machen sie aber "elektrischer"
    base_color_map = {
        "Rot": "#FF2A2A", "Weiß": "#F0F0F0", "Blau": "#0099FF", "Gelb": "#FFCC00", "Grün": "#00FF66"
    }
    # Fallback auf Cyan, falls Farbe fehlt
    accent = base_color_map.get(seal.get('color'), "#00E5FF")

    st.markdown(f"""
    <style>
        /* Container Style: Slim, Tech, Clickable Feel */
        .tone-module-container {{
            background: linear-gradient(90deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 3px solid {accent};
            border-radius: 6px;
            padding: 10px 15px;
            margin-bottom: 15px;
            margin-top: -10px; /* Näher ans Hauptmodul rücken */
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
        }}
        
        .tone-module-container:hover {{
            background: rgba(255, 255, 255, 0.06);
            border-color: {accent};
            box-shadow: 0 0 10px {accent}40; /* 40 = Transparenz */
        }}

        /* Linke Seite: ID & Name */
        .tm-id {{
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 1.1em;
            font-weight: 700;
            color: {accent};
            margin-right: 12px;
        }}
        .tm-name {{
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1.5px;
            color: #E0E0E0;
        }}

        /* Rechte Seite: Visualizer Bar */
        .tm-viz {{
            display: flex;
            gap: 2px;
            align-items: center;
        }}
        .tm-seg {{
            width: 3px;
            height: 10px;
            background: rgba(255,255,255,0.15);
            border-radius: 1px;
        }}
        .tm-seg.on {{
            background: {accent};
            box-shadow: 0 0 4px {accent};
        }}
        
        /* Override Expander Border für dieses Modul */
        div[data-testid="stExpander"] details {{
            border-color: rgba(255,255,255,0.05) !important;
        }}
        
        /* Tab Styling Fine-Tuning */
        .stTabs [data-baseweb="tab-list"] {{ gap: 5px; }}
        .stTabs [data-baseweb="tab"] {{ height: 40px; font-size: 0.8em; }}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. RENDER: DIE SCHALTFLÄCHE (Visual)
    # -------------------------------------------------------------------------
    
    # 13 Segmente generieren
    segments_html = ""
    for i in range(1, 14):
        state = "on" if i <= t_id else ""
        segments_html += f"<div class='tm-seg {state}'></div>"

    # HTML Output
    st.markdown(f"""
    <div class='tone-module-container'>
        <div style='display:flex; align-items:center;'>
            <div class='tm-id'>{t_id:02d}</div>
            <div class='tm-name'>{t_name}</div>
        </div>
        <div style='display:flex; align-items:center;'>
             <div style='font-size:0.7em; margin-right:15px; opacity:0.6; font-style:italic;'>{t_power}</div>
            <div class='tm-viz'>
                {segments_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. RENDER: DER INHALT (Expander)
    # -------------------------------------------------------------------------
    
    # Label für den Expander (Kompakt und Informativ)
    expander_label = f"FREQUENZ-DETAILS ANZEIGEN ({t_action} & {t_essence})"
    
    with st.expander(expander_label):
        
        if tone_psych:
            # Layout mit Tabs
            t1, t2, t3 = st.tabs(["Licht", "Schatten", "Praxis"])
            
            # --- LICHT ---
            with t1:
                light = tone_psych.get('light_potential', {})
                st.markdown(f"**Fokus:** {light.get('core_trait', '-')}")
                for attr in light.get('attributes', []):
                    st.info(f"✨ **{attr.get('name')}:** {attr.get('desc')}")

            # --- SCHATTEN ---
            with t2:
                shadow = tone_psych.get('shadow_integration', {})
                st.markdown(f"**Herausforderung:** {shadow.get('core_fear', '-')}")
                for pat in shadow.get('patterns', []):
                    st.error(f"⚠️ **{pat.get('name')}:** {pat.get('desc')}")

            # --- HEILUNG ---
            with t3:
                heal = tone_psych.get('healing_path', {})
                st.success(f"🧬 **Strategie:** {heal.get('strategy', '-')}")
                st.markdown("**Praktische Anwendung:**")
                for p in heal.get('practices', []):
                    st.caption(f"✅ {p}")

        else:
            # Fallback Nachricht, schön formatiert
            st.warning(f"Keine psychologischen Tiefendaten für Ton {t_id} ({t_name}) verfügbar.")
            st.markdown(f"""
            *Basis-Daten:* **Kraft:** {t_power}  
            **Aktion:** {t_action}  
            **Essenz:** {t_essence}
            """)

    return export_data
