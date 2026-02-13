import streamlit as st

# ==============================================================================
# 🔌 API SCHNITTSTELLE (Streng nach Protokoll)
# ==============================================================================
def render(kin_nr, data, db, date_obj):
    """
    MODUL WAVESPELL (Fix V2.2)
    Erwartet strikt 4 Argumente gemäß API-Definition.
    """
    
    # -------------------------------------------------------------------------
    # 1. SICHERHEITS-CHECK (Hält das Modul am Leben)
    # -------------------------------------------------------------------------
    if not data or 'identity' not in data:
        st.error("⚠️ Wavespell-Fehler: Keine Kin-Daten empfangen.")
        return {}

    # Wir brauchen die Datenbank für den Rückblick auf Ton 1
    # Check: Ist 'db' ein Dictionary mit 'tzolkin'? (So kommt es aus app.py)
    tzolkin_db = []
    if isinstance(db, dict) and 'tzolkin' in db:
        tzolkin_db = db['tzolkin']
    else:
        # Fallback, falls db direkt die Liste ist (Legacy Support)
        tzolkin_db = db if isinstance(db, list) else []

    if not tzolkin_db:
        st.warning("⚠️ Wavespell-Fehler: Datenbank nicht verfügbar.")
        return {}

    # -------------------------------------------------------------------------
    # 2. BERECHNUNG (Die Zeit-Reise zu Ton 1)
    # -------------------------------------------------------------------------
    try:
        # Wo stehen wir heute?
        current_tone = data['identity']['tone']['id']
        
        # Rückrechnung: Wo startete die Welle?
        # Formel: Heute - (Ton - 1)
        start_kin = kin_nr - (current_tone - 1)
        
        # Zyklus-Korrektur (Wenn wir rückwärts über 0 gehen, landen wir bei 260)
        if start_kin <= 0:
            start_kin += 260
            
        # ACHTUNG: Array-Index ist immer Kin - 1
        magnetic_data = tzolkin_db[start_kin - 1]
        
        # Daten aus dem Magnetischen Kin ziehen (Der "Boss" der Welle)
        wave_name = magnetic_data['identity']['seal']['name']
        wave_action = magnetic_data['identity']['seal']['action']
        wave_color = magnetic_data['identity']['seal']['color']
        
        # Psychologie suchen (Entweder im Wellen-Feld oder beim Siegel von Ton 1)
        wave_psych = magnetic_data['identity'].get('wavespell_psych', {})
        if not wave_psych:
            wave_psych = magnetic_data['identity']['seal'].get('psychology', {})

    except Exception as e:
        st.error(f"⚠️ Rechenfehler im Wellen-Modul: {e}")
        return {}

    # -------------------------------------------------------------------------
    # 3. UI DESIGN (Mission Control)
    # -------------------------------------------------------------------------
    
    # Rahmen-Farbe definieren
    color_map = {
        "Rot": "border-rot", 
        "Weiss": "border-weiss", 
        "Blau": "border-blau", 
        "Gelb": "border-gelb",
        "Grün": "border-gruen"
    }
    css_class = color_map.get(wave_color, "border-weiss")

    # EXPANDER RENDERN
    st.markdown(f"##### 🌊 WELLE DES {wave_name.upper()}")
    
    with st.expander(f"Mission: {wave_action} (Tag {current_tone}/13)", expanded=True):
        
        # Visueller Fortschrittsbalken
        st.progress(current_tone / 13)
        
        # Spalten für Details
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.caption("Führer (Ton 1):")
            st.markdown(f"**Kin {start_kin}**")
            st.markdown(f"*{wave_name}*")
            
        with c2:
            if wave_psych:
                # Wir zeigen nur das Wichtigste, um Platz zu sparen
                light = wave_psych.get('light_potential', {}).get('core_trait', 'Lädt...')
                shadow = wave_psych.get('shadow_integration', {}).get('core_fear', 'Lädt...')
                
                st.markdown(f"✨ **Ziel:** {light}")
                st.markdown(f"🛑 **Lernaufgabe:** {shadow}")
            else:
                st.info("Keine psychologischen Tiefendaten verfügbar.")

    # -------------------------------------------------------------------------
    # 4. EXPORT (Return Data)
    # -------------------------------------------------------------------------
    return {
        "module": "wavespell",
        "wave_kin": start_kin,
        "wave_name": wave_name,
        "current_tone": current_tone
    }
