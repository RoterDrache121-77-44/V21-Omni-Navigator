import streamlit as st

def render(state):
    """
    MODUL WAVESPELL (V3.0 Final)
    Nutzt das 'state' Objekt der App. Rechnet selbst nichts am Datum, nur an der Welle.
    """
    
    # 1. DATEN AUS DEM STATE HOLEN
    kin_nr = state.kin
    data = state.data
    db_tzolkin = state.db.get('tzolkin', [])

    # Abbruch wenn Hunab Ku oder keine Daten
    if kin_nr == 0 or not data or not db_tzolkin:
        return

    # 2. WELLEN-LOGIK
    try:
        # Aktuellen Ton holen (z.B. Ton 1 für Kin 66)
        current_tone = data['identity']['tone']['id']
        
        # Rückrechnung zum Wellen-Start (Ton 1)
        start_kin = kin_nr - (current_tone - 1)
        if start_kin <= 0: start_kin += 260
        
        # Daten des Wellen-Führers holen
        boss_data = db_tzolkin[start_kin - 1]
        
        wave_name = boss_data['identity']['seal']['name']
        wave_action = boss_data['identity']['seal']['action']
        wave_color = boss_data['identity']['seal']['color']
        
        # Psychologie laden
        wave_psych = boss_data['identity'].get('wavespell_psych', {}) or \
                     boss_data['identity']['seal'].get('psychology', {})

    except Exception as e:
        st.error(f"Berechnungsfehler Welle: {e}")
        return

    # 3. VISUALISIERUNG
    color_map = {"Rot": "border-rot", "Weiss": "border-weiss", "Blau": "border-blau", "Gelb": "border-gelb", "Grün": "border-gruen"}
    css = color_map.get(wave_color, "border-weiss")

    st.markdown(f"##### 🌊 WELLE DES {wave_name.upper()}")
    
    with st.expander(f"Mission: {wave_action} (Tag {current_tone}/13)", expanded=True):
        st.progress(current_tone / 13)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.caption("Führer:")
            st.markdown(f"**Kin {start_kin}**\n*{wave_name}*")
        
        with c2:
            if wave_psych:
                light = wave_psych.get('light_potential', {}).get('core_trait', '...')
                shadow = wave_psych.get('shadow_integration', {}).get('core_fear', '...')
                st.markdown(f"✨ **Ziel:** {light}")
                st.markdown(f"🛑 **Lernaufgabe:** {shadow}")
            else:
                st.info("Daten werden geladen...")

    # 4. SYNAPTISCHER SPEICHER (State Update)
    state.remember("wave_info", {
        "name": wave_name,
        "start_kin": start_kin,
        "tone": current_tone
    })
