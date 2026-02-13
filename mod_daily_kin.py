import streamlit as st

def render(state):
    """
    MODUL DAILY KIN (Synaptic Protocol V1.0)
    Visualisiert das Tages-Kin mit tiefenpsychologischen Details.
    Greift direkt auf das GalacticState Objekt zu.
    """
    
    # 1. AUSPACKEN (Aus dem zentralen Nervensystem)
    kin_nr = state.kin
    data = state.data
    
    # 2. SONDERFALL: HUNAB KU (Der Tag außerhalb der Zeit)
    if kin_nr == 0 or not data:
        st.info("🌌 0.0. HUNAB KU - Der Tag außerhalb der Zeit (29.02.)")
        st.caption("Heute existiert keine Zeit. Alles ist möglich.")
        return

    # 3. DATEN EXTRAHIEREN
    # Wir navigieren sicher durch das JSON
    id_data = data.get('identity', {})
    seal = id_data.get('seal', {})
    tone = id_data.get('tone', {})
    
    # Psychologie liegt meist unter 'seal', manchmal direkt unter 'identity' (Blueprint check)
    psych_data = seal.get('psychology', {})
    if not psych_data:
        psych_data = id_data.get('psychology', {})

    kin_name = id_data.get('name', 'Unbekannt')
    seal_color = seal.get('color', 'Weiss')
    
    # 4. VISUALISIERUNG (UI)
    # CSS Mapping für die Rahmenfarbe
    color_map = {
        "Rot": "border-rot", 
        "Weiss": "border-weiss", 
        "Blau": "border-blau", 
        "Gelb": "border-gelb", 
        "Grün": "border-gruen"
    }
    css_class = color_map.get(seal_color, "border-weiss")

    # Wir nutzen einen Container für sauberes Layout
    st.markdown(f"### 🌞 TAGES-ENERGIE: {kin_name}")

    with st.expander("🧠 Psychologisches Profil öffnen", expanded=True):
        
        if psych_data:
            # Die 3 heiligen Tabs
            t1, t2, t3 = st.tabs(["✨ LICHT (Potenzial)", "🌑 SCHATTEN (Lernaufgabe)", "🔥 TRANSFORMATION"])
            
            # TAB 1: LICHT
            with t1:
                light = psych_data.get('light_potential', {})
                core_trait = light.get('core_trait', 'Lädt...')
                st.markdown(f"**Superkraft:** {core_trait}")
                
                for attr in light.get('attributes', []):
                    st.success(f"💎 **{attr.get('name')}:** {attr.get('desc')}")

            # TAB 2: SCHATTEN
            with t2:
                shadow = psych_data.get('shadow_integration', {})
                core_fear = shadow.get('core_fear', 'Lädt...')
                st.markdown(f"**Widerstand:** {core_fear}")
                
                for pattern in shadow.get('patterns', []):
                    st.error(f"⚠️ **{pattern.get('name')}:** {pattern.get('desc')}")
                    
                # Neurosen-Check (Falls vorhanden)
                neurosis = shadow.get('neurosis', {})
                if neurosis:
                    st.caption(f"**Neurotische Falle:** {neurosis.get('name')} – {neurosis.get('mechanism')}")

            # TAB 3: HEILUNG
            with t3:
                heal = psych_data.get('healing_path', {})
                strategy = heal.get('strategy', 'Keine Daten.')
                st.info(f"🛠 **Strategie:** {strategy}")
                
                st.write("---")
                st.write("**Praktische Übungen:**")
                for practice in heal.get('practices', []):
                    st.markdown(f"✅ *{practice}*")
                    
                affirmation = heal.get('affirmation')
                if affirmation:
                    st.markdown(f"**Mantra:** *»{affirmation}«*")

        else:
            st.warning("Keine psychologischen Tiefendaten für dieses Kin verfügbar.")

    # 5. SYNAPTISCHES GEDÄCHTNIS (Memory Store)
    # Wir speichern die Infos, falls ein anderes Modul (z.B. ein PDF-Export) sie braucht.
    state.remember("daily_kin", {
        "kin": kin_nr,
        "name": kin_name,
        "color": seal_color,
        "tone": tone.get('id')
    })
