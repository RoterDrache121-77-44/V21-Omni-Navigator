import streamlit as st

def get_name():
    return "🔊 Galaktische Frequenz (Ton)"

def render(kin_nr, full_data, db_tz, date_obj=None):
    """
    Rendert die TON-FREQUENZ basierend auf der Tzolkin-Datenbank-Struktur.
    Pfad: identity -> tone -> psychology
    """
    
    # 1. DATEN-SICHERHEIT (Safe Access)
    if not full_data or 'identity' not in full_data:
        st.error("Keine Identitäts-Daten gefunden.")
        return {}

    # Der Pfad aus deinem JSON-Schnipsel:
    identity = full_data.get('identity', {})
    tone_data = identity.get('tone', {})
    
    # Hier liegt der Schatz:
    psych_data = tone_data.get('psychology', {}) 
    
    # Basis-Werte extrahieren
    t_id = tone_data.get('id', 0)
    t_name = tone_data.get('name', 'Unbekannt')
    t_power = tone_data.get('power', '-')
    t_action = tone_data.get('action', '-')
    t_essence = tone_data.get('essence', '-')
    
    # 2. UI-DARSTELLUNG (Atomic Design)
    
    # Header: Die Frequenz
    st.markdown(f"### 🔊 Ton {t_id}: {t_name}")
    
    # Die "Drei Worte" (Power, Action, Essence) als schnelle Übersicht
    c1, c2, c3 = st.columns(3)
    c1.metric("Kraft", t_power)
    c2.metric("Aktion", t_action)
    c3.metric("Essenz", t_essence)
    
    st.markdown("---")

    # 3. DER TIEFEN-SCAN (Psychologie)
    # Wir nutzen einen Expander, um das UI sauber zu halten
    with st.expander(f"🧠 {t_name} Frequenz: Tiefenanalyse", expanded=False):
        
        # Tabs für Licht, Schatten und Heilung
        tab_light, tab_shadow, tab_heal = st.tabs(["✨ Licht-Potenzial", "🌑 Schatten-Arbeit", "🧬 Heilungs-Weg"])
        
        # --- TAB: LICHT ---
        with tab_light:
            light = psych_data.get('light_potential', {})
            if light:
                st.info(f"**Kern-Qualität:** {light.get('core_trait', '-')}")
                for attr in light.get('attributes', []):
                    st.markdown(f"**• {attr.get('name')}:** {attr.get('desc')}")
            else:
                st.caption("Keine Licht-Daten verfügbar.")

        # --- TAB: SCHATTEN ---
        with tab_shadow:
            shadow = psych_data.get('shadow_integration', {})
            if shadow:
                st.error(f"**Kern-Angst:** {shadow.get('core_fear', '-')}")
                for pat in shadow.get('patterns', []):
                    st.markdown(f"**⚠️ {pat.get('name')}:** {pat.get('desc')}")
            else:
                st.caption("Keine Schatten-Daten verfügbar.")

        # --- TAB: HEILUNG ---
        with tab_heal:
            heal = psych_data.get('healing_path', {})
            if heal:
                st.success(f"**Strategie:** {heal.get('strategy', '-')}")
                st.markdown("**Praxis & Fokus:**")
                for prac in heal.get('practices', []):
                    st.write(f"✅ {prac}")
            else:
                st.caption("Keine Heilungs-Daten verfügbar.")

        # Zusatz-Info: Gelenk & Pulsar
        st.caption(f"📍 Somatik: {tone_data.get('joint', '-')} | 🌀 Dimension: {tone_data.get('pulsar', '-')}")

    # 4. EXPORT-DATEN (Return für PDF/JSON)
    export_data = {
        "module": "daily_tone",
        "title": f"Ton {t_id} - {t_name}",
        "keywords": [t_power, t_action, t_essence],
        "psychology": psych_data # Wir geben das rohe Objekt zurück für den Export
    }
    
    return export_data
