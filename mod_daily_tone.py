import streamlit as st

def render(state):
    """
    MODUL TONE FREQUENCY (Synaptic Version)
    Visualisiert den Galaktischen Ton mit 'Deep Search' Algorithmus.
    """

    # -------------------------------------------------------------------------
    # 0. STATE UNPACKING & DATEN-AKQUISE
    # -------------------------------------------------------------------------
    kin_nr = state.kin
    data = state.data

    # Abbruch bei Hunab Ku oder fehlenden Daten
    if kin_nr == 0 or not data:
        return 

    # Wir navigieren schrittweise
    identity = data.get('identity', {})
    tone = identity.get('tone', {})
    seal = identity.get('seal', {})
    
    # === DIE SUCHE NACH DEM VERLORENEN SCHATZ (Deep Search) ===
    tone_psych = {}
    source_found = "Nicht gefunden"

    # Pfad 1: Blueprint Standard (identity -> tone_psych)
    if 'tone_psych' in identity and identity['tone_psych']:
        tone_psych = identity['tone_psych']
        source_found = "identity -> tone_psych"
    
    # Pfad 2: Verschachtelt im Siegel (seal -> psychology -> tone_psych)
    elif 'psychology' in seal and 'tone_psych' in seal['psychology']:
        tone_psych = seal['psychology']['tone_psych']
        source_found = "seal -> psych -> tone_psych"

    # Pfad 3: Direkt im Ton (tone -> psychology) - Logische Alternative
    elif 'psychology' in tone:
        tone_psych = tone['psychology']
        source_found = "tone -> psychology"

    # Basis Daten extrahieren
    t_id = tone.get('id', 0)
    t_name = tone.get('name', 'Ton')
    t_action = tone.get('action', '-')
    t_power = tone.get('power', '-')
    t_essence = tone.get('essence', '-')

    # Export-Daten vorbereiten
    export_data = {
        "module": "daily_tone",
        "tone_id": t_id,
        "tone_name": t_name,
        "action": t_action,
        "source": source_found
    }

    # -------------------------------------------------------------------------
    # 1. DESIGN ENGINE (CSS Injection)
    # -------------------------------------------------------------------------
    base_color_map = {
        "Rot": "#FF2A2A", "Weiß": "#F0F0F0", "Blau": "#0099FF", "Gelb": "#FFCC00", "Grün": "#00FF66"
    }
    # Fallback auf Cyan, falls Farbe fehlt
    accent = base_color_map.get(seal.get('color'), "#00E5FF")

    st.markdown(f"""
    <style>
        .tone-module-container {{
            background: linear-gradient(90deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 3px solid {accent};
            border-radius: 6px; padding: 10px 15px; margin-bottom: 15px; margin-top: 5px;
            display: flex; align-items: center; justify-content: space-between; transition: all 0.3s ease;
        }}
        .tone-module-container:hover {{
            background: rgba(255, 255, 255, 0.06); border-color: {accent}; box-shadow: 0 0 10px {accent}40;
        }}
        .tm-id {{ font-family: 'Consolas', monospace; font-size: 1.1em; font-weight: 700; color: {accent}; margin-right: 12px; }}
        .tm-name {{ font-weight: 600; text-transform: uppercase; font-size: 0.85em; letter-spacing: 1.5px; color: #E0E0E0; }}
        .tm-viz {{ display: flex; gap: 2px; align-items: center; }}
        .tm-seg {{ width: 3px; height: 10px; background: rgba(255,255,255,0.15); border-radius: 1px; }}
        .tm-seg.on {{ background: {accent}; box-shadow: 0 0 4px {accent}; }}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. RENDER BAR (Visuelle Frequenz)
    # -------------------------------------------------------------------------
    # Erzeugt 13 Balken, aktiviert basierend auf Ton-ID
    segments_html = "".join([f"<div class='tm-seg {'on' if i <= t_id else ''}'></div>" for i in range(1, 14)])

    st.markdown(f"""
    <div class='tone-module-container'>
        <div style='display:flex; align-items:center;'>
            <div class='tm-id'>{t_id:02d}</div>
            <div class='tm-name'>{t_name}</div>
        </div>
        <div style='display:flex; align-items:center;'>
             <div style='font-size:0.7em; margin-right:15px; opacity:0.6; font-style:italic;'>{t_power}</div>
            <div class='tm-viz'>{segments_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. RENDER CONTENT (MIT DEBUGGER)
    # -------------------------------------------------------------------------
    with st.expander(f"FREQUENZ-DETAILS ({t_action} & {t_essence})"):
        
        # === FALL 1: WIR HABEN DATEN ===
        if tone_psych:
            t1, t2, t3 = st.tabs(["Licht", "Schatten", "Praxis"])
            
            with t1:
                light = tone_psych.get('light_potential', {})
                st.markdown(f"**Fokus:** {light.get('core_trait', '-')}")
                for attr in light.get('attributes', []):
                    st.info(f"✨ **{attr.get('name')}:** {attr.get('desc')}")
            
            with t2:
                shadow = tone_psych.get('shadow_integration', {})
                st.markdown(f"**Herausforderung:** {shadow.get('core_fear', '-')}")
                for pat in shadow.get('patterns', []):
                    st.error(f"⚠️ **{pat.get('name')}:** {pat.get('desc')}")
            
            with t3:
                heal = tone_psych.get('healing_path', {})
                st.success(f"🧬 **Strategie:** {heal.get('strategy', '-')}")
                for p in heal.get('practices', []):
                    st.caption(f"✅ {p}")
        
        # === FALL 2: KEINE DATEN (DEBUGGER STARTEN) ===
        else:
            st.warning(f"⚠️ Keine Psychologie-Daten gefunden. Gesucht an Pfad: {source_found}")
            
            # DER RETTUNGSANKER: Wir zeigen dir, was DA ist.
            st.markdown("### 🕵️ DEBUG: DATABASE INSPECTOR")
            st.markdown("Das System sieht folgende Keys in `identity`:")
            st.write(list(identity.keys()))
            
            if 'seal' in identity:
                st.markdown("Keys in `identity['seal']`:")
                st.write(list(identity['seal'].keys()))
                if 'psychology' in identity['seal']:
                    st.markdown("Keys in `identity['seal']['psychology']`:")
                    st.write(list(identity['seal']['psychology'].keys()))
            
            st.error("Bitte prüfe anhand dieser Liste, wo 'tone_psych' versteckt ist!")

    # -------------------------------------------------------------------------
    # 4. SYNAPTIC MEMORY (Daten speichern)
    # -------------------------------------------------------------------------
    state.remember("daily_tone", export_data)
