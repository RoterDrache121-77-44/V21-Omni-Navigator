import streamlit as st

# ==============================================================================
# 🛡️ FAILSAFE API (Nimmt was es kriegt, stürzt nicht ab)
# ==============================================================================
def render(kin_nr, data, db=None, date_obj=None):
    """
    MODUL WAVESPELL (V2.3 Bulletproof)
    Akzeptiert Argumente optional, damit es bei alter app.py nicht crasht.
    """
    
    # 1. NOTBREMSE: Wenn app.py die Datenbank vergessen hat
    if db is None:
        st.error("⚠️ ACHTUNG: Deine 'app.py' ist veraltet! Sie übergibt die Datenbank nicht an dieses Modul.")
        st.info("Bitte kopiere den Code aus Schritt 2 in deine app.py.")
        return {}

    # 2. SICHERHEITS-CHECK (Daten da?)
    if not data or 'identity' not in data:
        return {}

    # Datenbank-Check (Support für Dict und List Format)
    tzolkin_db = []
    if isinstance(db, dict) and 'tzolkin' in db:
        tzolkin_db = db['tzolkin']
    else:
        tzolkin_db = db if isinstance(db, list) else []

    if not tzolkin_db:
        st.warning("⚠️ Datenbank leer oder nicht lesbar.")
        return {}

    # -------------------------------------------------------------------------
    # 3. BERECHNUNG (Die Zeit-Reise zu Ton 1)
    # -------------------------------------------------------------------------
    try:
        current_tone = data['identity']['tone']['id']
        
        # Rückrechnung: Wo startete die Welle?
        start_kin = kin_nr - (current_tone - 1)
        
        # Zyklus-Korrektur
        if start_kin <= 0:
            start_kin += 260
            
        # Daten aus dem Magnetischen Kin ziehen
        magnetic_data = tzolkin_db[start_kin - 1]
        
        wave_name = magnetic_data['identity']['seal']['name']
        wave_action = magnetic_data['identity']['seal']['action']
        wave_color = magnetic_data['identity']['seal']['color']
        
        # Psychologie suchen
        wave_psych = magnetic_data['identity'].get('wavespell_psych', {})
        if not wave_psych:
            wave_psych = magnetic_data['identity']['seal'].get('psychology', {})

    except Exception as e:
        st.error(f"⚠️ Rechenfehler: {e}")
        return {}

    # -------------------------------------------------------------------------
    # 4. UI DESIGN
    # -------------------------------------------------------------------------
    color_map = {
        "Rot": "border-rot", "Weiss": "border-weiss", 
        "Blau": "border-blau", "Gelb": "border-gelb", "Grün": "border-gruen"
    }
    
    st.markdown(f"##### 🌊 WELLE DES {wave_name.upper()}")
    
    with st.expander(f"Mission: {wave_action} (Tag {current_tone}/13)", expanded=True):
        st.progress(current_tone / 13)
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.caption("Führer (Ton 1):")
            st.markdown(f"**Kin {start_kin}**\n*{wave_name}*")
            
        with c2:
            if wave_psych:
                light = wave_psych.get('light_potential', {}).get('core_trait', 'Lädt...')
                shadow = wave_psych.get('shadow_integration', {}).get('core_fear', 'Lädt...')
                st.markdown(f"✨ **Ziel:** {light}")
                st.markdown(f"🛑 **Lernaufgabe:** {shadow}")
            else:
                st.info("Keine Tiefendaten verfügbar.")

    return {"module": "wavespell", "wave_kin": start_kin}
