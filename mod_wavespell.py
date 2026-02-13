import streamlit as st

def render(kin_nr, data):
    """
    Rendert die WELLE (Wavespell) als Missions-Timeline.
    Style: 'Mission Control' Interface.
    """

    # -------------------------------------------------------------------------
    # 0. DATEN-SCAN
    # -------------------------------------------------------------------------
    if kin_nr == 0 or not data:
        return {}

    # Pfade extrahieren
    identity = data.get('identity', {})
    tone = identity.get('tone', {})
    seal = identity.get('seal', {})
    
    # === DIE WELLE IDENTIFIZIEREN ===
    # Der Name der Welle steht oft separat (z.B. unter 'time' oder muss berechnet werden).
    # Wir schauen, ob die DB den Namen liefert.
    # Oft ist die Welle definiert durch das Siegel des Tons 1.
    
    # Versuch 1: Explizites Feld
    ws_name = "Unbekannte Welle"
    if 'time' in data and 'wavespell' in data['time']:
        ws_name = data['time']['wavespell']
    
    # Psychologie der Welle (Laut Blueprint: identity -> wavespell_psych)
    ws_psych = identity.get('wavespell_psych', {})
    
    # Fallback: Wenn leer, schauen wir unter seal->psychology (manchmal dort versteckt)
    if not ws_psych:
         ws_psych = seal.get('psychology', {}).get('wavespell_psych', {})

    # Daten für die Timeline
    current_day = tone.get('id', 1)
    total_days = 13
    
    # Farbe bestimmen (Wir nehmen die Farbe des Siegels als Akzent)
    base_color_map = {
        "Rot": "#FF2A2A", "Weiß": "#F0F0F0", "Blau": "#0099FF", "Gelb": "#FFCC00", "Grün": "#00FF66"
    }
    accent = base_color_map.get(seal.get('color'), "#BD00FF") # Lila als Default für Zeit/Magie

    # Export Data
    export_data = {
        "module": "wavespell",
        "name": ws_name,
        "current_day": current_day,
        "mission_goal": ws_psych.get('light_potential', {}).get('core_trait', '-')
    }

    # -------------------------------------------------------------------------
    # 1. DESIGN ENGINE: MISSION CONTROL
    # -------------------------------------------------------------------------
    st.markdown(f"""
    <style>
        /* Container: Flux Tube Look */
        .ws-container {{
            background: rgba(15, 15, 20, 0.6);
            border: 1px dashed rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            position: relative;
            overflow: hidden;
        }}
        
        /* Header */
        .ws-header {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
        }}
        .ws-label {{ font-size: 0.7em; text-transform: uppercase; letter-spacing: 2px; opacity: 0.7; }}
        .ws-title {{ font-size: 1.1em; font-weight: bold; color: {accent}; text-transform: uppercase; }}

        /* Timeline Bar */
        .timeline-track {{
            width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; position: relative;
            margin-top: 5px; margin-bottom: 15px;
        }}
        .timeline-progress {{
            height: 100%; background: {accent}; border-radius: 3px;
            box-shadow: 0 0 10px {accent};
            width: {(current_day / 13) * 100}%;
            transition: width 1s ease-in-out;
        }}
        .timeline-marker {{
            position: absolute; top: -4px; right: 0; 
            width: 14px; height: 14px; background: #fff; border-radius: 50%;
            box-shadow: 0 0 10px {accent};
        }}

        /* Stats Grid */
        .ws-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.85em; }}
        .ws-box {{ background: rgba(255,255,255,0.05); padding: 8px; border-radius: 4px; border-left: 2px solid {accent}; }}
        
        /* Expander Override */
        div[data-testid="stExpander"] details {{ border-color: rgba(255,255,255,0.1) !important; }}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. RENDER: TIMELINE (Der visuelle Anker)
    # -------------------------------------------------------------------------
    st.markdown(f"""
    <div class='ws-container'>
        <div class='ws-header'>
            <div class='ws-label'>AKTIVE ZEITWELLE</div>
            <div class='ws-title'>{ws_name}</div>
        </div>
        
        <div style='display:flex; justify-content:space-between; font-size:0.7em; opacity:0.8;'>
            <span>START (Tag 1)</span>
            <span style='color:{accent}; font-weight:bold;'>HEUTE: TAG {current_day}</span>
            <span>ZIEL (Tag 13)</span>
        </div>
        <div class='timeline-track'>
            <div class='timeline-progress'>
                <div class='timeline-marker'></div>
            </div>
        </div>
        
        <div style='font-size:0.8em; text-align:center; font-style:italic; opacity:0.8;'>
            "Du befindest dich in der {current_day}. Phase der 13-tägigen Transformation."
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. MISSION BRIEFING (Content)
    # -------------------------------------------------------------------------
    label = f"🌊 MISSION-LOGBUCH: {ws_name}"
    
    with st.expander(label):
        if ws_psych:
            t1, t2 = st.tabs(["🎯 Missions-Ziel (Licht)", "⚠️ Hindernisse (Schatten)"])
            
            with t1:
                light = ws_psych.get('light_potential', {})
                st.markdown(f"**Übergeordneter Zweck:** {light.get('core_trait', '-')}")
                for attr in light.get('attributes', []):
                    st.info(f"⚡ **{attr.get('name')}:** {attr.get('desc')}")
                    
            with t2:
                shadow = ws_psych.get('shadow_integration', {})
                st.markdown(f"**Lernaufgabe:** {shadow.get('core_fear', '-')}")
                for pat in shadow.get('patterns', []):
                    st.error(f"🛑 **{pat.get('name')}:** {pat.get('desc')}")
            
            # Heilung/Strategie als Footer
            heal = ws_psych.get('healing_path', {})
            if heal:
                st.markdown("---")
                st.caption("🚀 **Navigations-Strategie:**")
                st.write(heal.get('strategy', '-'))

        else:
            # Fallback
            st.warning("Keine spezifischen Missions-Daten für diese Welle gefunden.")
            st.caption("Die Welle definiert den Kontext deiner aktuellen Entwicklung. Nutze die Energie des Siegels als Leitsatz.")

    return export_data
