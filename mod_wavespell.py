import streamlit as st

def render(ctx):
    """
    MODUL WAVESPELL (Architecture: Context Pattern)
    Empfängt das 'ctx' Objekt und holt sich, was es braucht.
    """
    
    # 1. AUSPACKEN (Unpacking the Context)
    kin_nr = ctx.kin
    data = ctx.data
    db = ctx.db
    # Datum bräuchten wir hier nicht, aber es ist in ctx.date verfügbar

    # 2. VALIDIERUNG
    if not data or 'identity' not in data:
        return {}
    
    tzolkin_db = db.get('tzolkin', []) if isinstance(db, dict) else []
    if not tzolkin_db:
        st.warning("Keine Datenbank im Context gefunden.")
        return {}

    # 3. LOGIK (Wellen-Berechnung)
    try:
        current_tone = data['identity']['tone']['id']
        start_kin = kin_nr - (current_tone - 1)
        if start_kin <= 0: start_kin += 260
        
        # Lookup Ton 1
        magnetic_data = tzolkin_db[start_kin - 1]
        
        wave_name = magnetic_data['identity']['seal']['name']
        wave_action = magnetic_data['identity']['seal']['action']
        wave_color = magnetic_data['identity']['seal']['color']
        
        wave_psych = magnetic_data['identity'].get('wavespell_psych', {}) or \
                     magnetic_data['identity']['seal'].get('psychology', {})

    except Exception as e:
        st.error(f"Rechenfehler: {e}")
        return {}

    # 4. UI (Visualisierung)
    color_map = {"Rot": "border-rot", "Weiss": "border-weiss", "Blau": "border-blau", "Gelb": "border-gelb", "Grün": "border-gruen"}
    css_class = color_map.get(wave_color, "border-weiss")

    st.markdown(f"##### 🌊 WELLE DES {wave_name.upper()}")
    with st.expander(f"Mission: {wave_action} (Tag {current_tone}/13)", expanded=True):
        st.progress(current_tone / 13)
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.caption("Wellen-Führer:")
            st.markdown(f"**Kin {start_kin}**\n*{wave_name}*")
        
        with c2:
            if wave_psych:
                light = wave_psych.get('light_potential', {}).get('core_trait', '...')
                shadow = wave_psych.get('shadow_integration', {}).get('core_fear', '...')
                st.markdown(f"✨ **Ziel:** {light}")
                st.markdown(f"🛑 **Lernaufgabe:** {shadow}")
            else:
                st.info("Daten werden geladen...")

    # 5. RÜCKGABE (Ins Shared Memory)
    return {
        "wave_kin": start_kin,
        "wave_name": wave_name,
        "current_tone": current_tone
    }
