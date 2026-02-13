import streamlit as st

def render(kin_nr, data):
    """
    Rendert die TON-FREQUENZ als eigenes, kompaktes Modul.
    Style: 'System Control Bar' (3x kleiner als das Main-Modul).
    """

    # -------------------------------------------------------------------------
    # 0. DATEN & PSYCHOLOGIE FETCHEN
    # -------------------------------------------------------------------------
    if kin_nr == 0 or not data:
        return {} # Bei Hunab Ku macht der Ton keinen Sinn oder ist 0

    id_data = data.get('identity', {})
    tone = id_data.get('tone', {})
    seal = id_data.get('seal', {})
    
    # Wo versteckt sich die Ton-Psychologie? 
    # Laut Blueprint oft unter seal['psychology']['tone_psych'] oder direkt
    main_psych = seal.get('psychology', {})
    tone_psych = main_psych.get('tone_psych', {})

    # Fallback, falls die DB Struktur variiert
    if not tone_psych:
        # Versuch eines direkten Zugriffs, falls Schema abweicht
        tone_psych = data.get('tone_psych', {})

    # Basis Daten
    t_id = tone.get('id', 0)
    t_name = tone.get('name', 'Ton')
    t_action = tone.get('action', 'Tätigkeit')
    t_power = tone.get('power', 'Kraft')
    t_essence = tone.get('essence', 'Essenz')
    
    # Farbe vom Siegel borgen für das Theme (Konsistenz)
    s_color = seal.get('color', 'Weiß')

    # Export Data
    export_data = {
        "module": "daily_tone",
        "tone_id": t_id,
        "tone_name": t_name,
        "psych_core": tone_psych.get('light_potential', {}).get('core_trait', '-')
    }

    # -------------------------------------------------------------------------
    # 1. COMPACT DESIGN ENGINE
    # -------------------------------------------------------------------------
    colors = {
        "Rot":   "#FF3E3E",
        "Weiß":  "#E0E0E0",
        "Blau":  "#2A8CFF",
        "Gelb":  "#FFD700",
        "Grün":  "#00FF66"
    }
    theme_color = colors.get(s_color, "#E0E0E0")

    st.markdown(f"""
    <style>
        /* Compact System Bar Style */
        .tone-bar {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid {theme_color};
            border-radius: 4px;
            padding: 8px 12px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.2s ease;
        }}
        
        .tone-bar:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: {theme_color};
            cursor: pointer;
        }}

        /* Typography für Compact Mode */
        .tb-freq {{ font-family: monospace; color: {theme_color}; font-weight: bold; letter-spacing: 1px; }}
        .tb-name {{ font-weight: 700; text-transform: uppercase; margin-left: 10px; color: #fff; }}
        .tb-power {{ font-size: 0.8em; font-style: italic; opacity: 0.7; text-align: right; }}

        /* Dots Visualizer (Punkte statt Balken) */
        .tone-dots {{ display: flex; gap: 2px; }}
        .dot {{ width: 6px; height: 6px; border-radius: 50%; background: #333; }}
        .dot.active {{ background: {theme_color}; box-shadow: 0 0 5px {theme_color}; }}
        
        /* Expander Border Hack für dieses Modul */
        div[data-testid="stExpander"] details {{
            border-left: 2px solid {theme_color} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. RENDER: COMPACT VISUALIZER (Der "Button")
    # -------------------------------------------------------------------------
    # Wir bauen visuell Punkte für den Ton (1-13)
    dots_html = "".join([f"<div class='dot {'active' if i < t_id else ''}'></div>" for i in range(13)])

    # Die Leiste (Optik)
    st.markdown(f"""
    <div class='tone-bar'>
        <div style='display:flex; align-items:center;'>
            <div class='tb-freq'>TON {t_id:02d}</div>
            <div class='tb-name'>{t_name}</div>
        </div>
        <div style='display:flex; flex-direction:column; align-items:flex-end;'>
            <div class='tone-dots' style='margin-bottom:4px;'>{dots_html}</div>
            <div class='tb-power'>{t_power}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. DEEP DIVE: EXPANDER (Psychologie)
    # -------------------------------------------------------------------------
    with st.expander(f"📡 FREQUENZ-ANALYSE: {t_name}", expanded=False):
        
        # Oben: Die Dreifaltigkeit des Tons
        c1, c2, c3 = st.columns(3)
        c1.metric("Kraft", t_power)
        c2.metric("Aktion", t_action)
        c3.metric("Essenz", t_essence)
        
        st.divider()

        # Unten: Psychologie Tabs
        # Wir prüfen erst, ob wir Daten haben
        if tone_psych:
            t1, t2, t3 = st.tabs(["Licht", "Schatten", "Praxis"])
            
            with t1:
                st.markdown(f"**Fokus:** {tone_psych.get('light_potential', {}).get('core_trait', 'Keine Daten')}")
                for attr in tone_psych.get('light_potential', {}).get('attributes', []):
                    st.caption(f"✨ **{attr.get('name')}:** {attr.get('desc')}")
            
            with t2:
                st.markdown(f"**Herausforderung:** {tone_psych.get('shadow_integration', {}).get('core_fear', 'Keine Daten')}")
                for pat in tone_psych.get('shadow_integration', {}).get('patterns', []):
                    st.caption(f"🌑 **{pat.get('name')}:** {pat.get('desc')}")
            
            with t3:
                heal = tone_psych.get('healing_path', {})
                st.info(f"Strategie: {heal.get('strategy', '-')}")
                for p in heal.get('practices', []):
                    st.write(f"✅ {p}")
        else:
            st.warning("⚠️ Keine psychologischen Tiefendaten für diesen Ton in der Datenbank gefunden.")

    return export_data
