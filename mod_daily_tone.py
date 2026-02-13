import streamlit as st

def render(kin_nr, data):
    """
    Rendert die TON-FREQUENZ als kompaktes 'System-Modul'.
    FIX: Korrekter Datenpfad für Tone-Psychologie.
    Style: High-Tech Slim Bar.
    """

    # -------------------------------------------------------------------------
    # 0. DATEN-MINE (Hier holen wir das Gold)
    # -------------------------------------------------------------------------
    if kin_nr == 0 or not data:
        return {} 

    # Navigieren durch die JSON-Struktur gemäß Blueprint
    identity = data.get('identity', {})
    tone = identity.get('tone', {})
    
    # === DER CRITICAL FIX ===
    # Laut Blueprint liegt 'tone_psych' direkt unter 'identity', 
    # NICHT unter 'seal' -> 'psychology'.
    tone_psych = identity.get('tone_psych', {})

    # Basis Daten (Tone 1-13)
    t_id = tone.get('id', 0)
    t_name = tone.get('name', 'Ton')
    t_action = tone.get('action', '-')
    t_power = tone.get('power', '-')
    t_essence = tone.get('essence', '-')

    # Export Data
    export_data = {
        "module": "daily_tone",
        "tone_id": t_id,
        "tone_name": t_name,
        "psych_found": bool(tone_psych) # Debug Info
    }

    # -------------------------------------------------------------------------
    # 1. DESIGN ENGINE (Slim & Cyber)
    # -------------------------------------------------------------------------
    # Wir berechnen eine "Frequenz-Farbe" basierend auf der Ton-Höhe
    # (Optional: Man könnte auch die Siegelfarbe übergeben, aber Silber/Cyan wirkt technischer)
    tech_color = "#00E5FF" # Cyan als Standard Tech Farbe
    
    st.markdown(f"""
    <style>
        /* Container: Slim Bar */
        .tone-interface {{
            background: linear-gradient(90deg, rgba(10,15,20,0.9) 0%, rgba(20,30,40,0.8) 100%);
            border: 1px solid rgba(255,255,255,0.1);
            border-left: 3px solid {tech_color};
            border-radius: 4px;
            padding: 8px 15px; /* Kompakt */
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            transition: all 0.2s;
        }}
        .tone-interface:hover {{
            border-color: {tech_color};
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
        }}

        /* Linke Seite: Zahl & Name */
        .ti-number {{ 
            font-family: 'Courier New', monospace; 
            font-size: 1.2em; 
            font-weight: bold; 
            color: {tech_color}; 
            margin-right: 10px;
        }}
        .ti-name {{ 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            font-size: 0.9em; 
            color: #fff; 
        }}

        /* Rechte Seite: Tech-Visualizer (Balken) */
        .ti-viz-wrapper {{
            display: flex;
            gap: 3px;
            align-items: center;
        }}
        .ti-seg {{
            width: 4px;
            height: 12px;
            background: rgba(255,255,255,0.1);
            border-radius: 1px;
        }}
        .ti-seg.active {{
            background: {tech_color};
            box-shadow: 0 0 5px {tech_color};
        }}
        
        /* Expander Styling Override */
        div[data-testid="stExpander"] details {{
            border-color: rgba(255,255,255,0.1) !important;
            background: rgba(0,0,0,0.2);
        }}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. RENDER: SLIM BAR (Das sieht man immer)
    # -------------------------------------------------------------------------
    
    # Wir bauen 13 Segmente
    segments_html = ""
    for i in range(1, 14):
        state = "active" if i <= t_id else ""
        segments_html += f"<div class='ti-seg {state}'></div>"

    st.markdown(f"""
    <div class='tone-interface'>
        <div style='display:flex; align-items:center;'>
            <div class='ti-number'>{t_id:02d}</div>
            <div class='ti-name'>{t_name}</div>
        </div>
        <div class='ti-viz-wrapper'>
            <div style='font-size:0.7em; color:#aaa; margin-right:10px; text-transform:uppercase;'>{t_power}</div>
            {segments_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. DEEP DIVE: PSYCHOLOGIE (Im Expander)
    # -------------------------------------------------------------------------
    # Label für den Expander
    label = f"📡 FREQUENZ-DETAILS: {t_action} & {t_essence}"
    
    with st.expander(label):
        
        # Grid Layout für die 3 Aspekte
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Kraft:** `{t_power}`")
        c2.markdown(f"**Aktion:** `{t_action}`")
        c3.markdown(f"**Essenz:** `{t_essence}`")
        
        st.divider()

        # Jetzt die ECHTEN Daten aus tone_psych
        if tone_psych:
            # Tabs für saubere Struktur
            tab_l, tab_s, tab_h = st.tabs(["Licht-Frequenz", "Schatten-Frequenz", "Harmonisierung"])
            
            # --- LICHT ---
            with tab_l:
                light = tone_psych.get('light_potential', {})
                core = light.get('core_trait', 'Daten werden geladen...')
                st.info(f"✨ **Fokus:** {core}")
                
                # Attribute Loop
                for attr in light.get('attributes', []):
                    st.markdown(f"**• {attr.get('name')}:** {attr.get('desc')}")

            # --- SCHATTEN ---
            with tab_s:
                shadow = tone_psych.get('shadow_integration', {})
                fear = shadow.get('core_fear', '-')
                st.error(f"🌑 **Herausforderung:** {fear}")
                
                # Patterns Loop
                for pat in shadow.get('patterns', []):
                    st.markdown(f"**⚠️ {pat.get('name')}:** {pat.get('desc')}")

            # --- HEILUNG ---
            with tab_h:
                heal = tone_psych.get('healing_path', {})
                st.success(f"🧬 **Strategie:** {heal.get('strategy', '-')}")
                
                st.markdown("**Praxis:**")
                for prac in heal.get('practices', []):
                    st.write(f"✅ {prac}")
        else:
            # Fallback, falls die DB an dieser Stelle wirklich leer ist
            st.warning("⚠️ Keine tiefenpsychologischen Daten für diesen Ton gefunden. (Check DB 'tone_psych' key)")

    return export_data
