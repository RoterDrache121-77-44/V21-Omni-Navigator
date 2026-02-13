import streamlit as st

def render(kin_nr, full_data, db, d_in=None):
    """
    MODUL WAVESPELL (V2.1 Fixed)
    Logik: Berechnet den Start der Welle (Ton 1) und zeigt das 13-Tage-Thema.
    """
    
    # -------------------------------------------------------------------------
    # 1. CALCULATE WAVE (Rechnen)
    # -------------------------------------------------------------------------
    
    # Sicherstellen, dass Daten da sind
    if not full_data or 'identity' not in full_data:
        return {}

    # Aktueller Ton und Index holen
    try:
        current_tone = full_data['identity']['tone']['id']
        
        # Rückrechnung: Wo startete diese Welle? (Das Magnetische Tor)
        # Formel: Aktuelles Kin - (Aktueller Ton - 1)
        # Beispiel: Kin 121 (Ton 4). Start = 121 - 3 = 118.
        wave_start_kin = kin_nr - (current_tone - 1)
        
        # Zyklus-Korrektur (falls wir über 0/260 rutschen)
        if wave_start_kin <= 0:
            wave_start_kin += 260
            
        # Datenbank-Lookup für den Wellen-Herrscher (Ton 1)
        # Achtung: Array Index ist Kin - 1
        magnetic_data = db['tzolkin'][wave_start_kin - 1]
        
        # Daten extrahieren
        ws_name = f"Welle des {magnetic_data['identity']['seal']['name']}"
        ws_purpose = magnetic_data['identity']['seal']['action']
        ws_color = magnetic_data['identity']['seal']['color']
        
        # Psychologie der Welle (liegt oft im 'wavespell_psych' Feld des Magnetischen Kins)
        # Falls dort leer, nehmen wir die 'seal psychology' des Magnetischen Kins als Thema
        ws_psych = magnetic_data['identity'].get('wavespell_psych', {})
        if not ws_psych:
             ws_psych = magnetic_data['identity']['seal'].get('psychology', {})

    except Exception as e:
        st.error(f"⚠️ Rechenfehler in der Wellen-Logik: {e}")
        return {}

    # -------------------------------------------------------------------------
    # 2. UI DESIGN (Zeichnen)
    # -------------------------------------------------------------------------
    
    # CSS Farb-Mapping für den Rahmen
    color_map = {
        "Rot": "border-rot", 
        "Weiss": "border-weiss", 
        "Blau": "border-blau", 
        "Gelb": "border-gelb",
        "Grün": "border-gruen"
    }
    css_class = color_map.get(ws_color, "border-weiss")

    # VISUALISIERUNG
    # Wir nutzen einen Expander als "Mission Log"
    
    label = f"🌊 13-TAGE MISSION: {ws_name}"
    
    with st.expander(label, expanded=False):
        
        # Header: Wo sind wir?
        st.progress(current_tone / 13, text=f"Fortschritt: Tag {current_tone} von 13")
        
        st.markdown(f"""
        <div style="margin-bottom:10px;">
            <b>Thema:</b> {ws_purpose} <br>
            <span style="color:#888; font-size:0.8em;">(Definiert durch Kin {wave_start_kin})</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs für Deep Dive
        if ws_psych:
            t1, t2, t3 = st.tabs(["🎯 ZIEL", "⚠️ SCHATTEN", "🚀 HEILUNG"])
            
            with t1:
                light = ws_psych.get('light_potential', {})
                st.markdown(f"**Höheres Ziel:** {light.get('core_trait', 'Daten werden geladen...')}")
                for attr in light.get('attributes', []):
                     st.info(f"✨ **{attr.get('name')}:** {attr.get('desc')}")

            with t2:
                shadow = ws_psych.get('shadow_integration', {})
                st.markdown(f"**Lernaufgabe:** {shadow.get('core_fear', 'Unbekannt')}")
                for pat in shadow.get('patterns', []):
                    st.error(f"🛑 **{pat.get('name')}:** {pat.get('desc')}")
            
            with t3:
                heal = ws_psych.get('healing_path', {})
                st.write(f"**Strategie:** {heal.get('strategy', '-')}")
                for prac in heal.get('practices', []):
                    st.success(f"🛠 {prac}")
        else:
            st.warning("Keine psychologischen Tiefendaten für diese Welle verfügbar.")

    # -------------------------------------------------------------------------
    # 3. EXPORT (Daten liefern)
    # -------------------------------------------------------------------------
    return {
        "module": "wavespell",
        "wave_name": ws_name,
        "wave_start_kin": wave_start_kin,
        "current_step": current_tone,
        "purpose": ws_purpose
    }
