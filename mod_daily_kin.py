import streamlit as st

def render(kin_nr, data):
    """
    Rendert das Tägliche KIN.
    FOKUS: Nur Kin, Farbe, Nummer.
    DETAILS: Vollständiges psychologisches Profil.
    """
    
    # -------------------------------------------------------------------------
    # 0. DATEN SICHERN
    # -------------------------------------------------------------------------
    if kin_nr == 0 or not data:
        st.info("🌀 HUNAB KU - 0.0. Der Tag außerhalb der Zeit.")
        return {"kin": 0, "name": "Hunab Ku"}

    id_data = data.get('identity', {})
    seal = id_data.get('seal', {})
    psych = seal.get('psychology', {})

    # Wir ignorieren Ton, Welle, Clan etc. wie gewünscht.
    # Wir holen nur Visuals & Psyche.

    s_name = id_data.get('name', 'Unbekannt')
    s_color = seal.get('color', 'Weiß')
    s_action = seal.get('action', 'Agieren')
    s_power = seal.get('power', 'Kraft')
    s_essence = seal.get('essence', 'Essenz')

    # Export für PDF (reduziert)
    export_data = {
        "kin": kin_nr,
        "name": s_name,
        "color": s_color,
        "psych_summary": psych.get('light_potential', {}).get('core_trait', '-')
    }

    # -------------------------------------------------------------------------
    # 1. DESIGN ENGINE (Reduziert & Clean)
    # -------------------------------------------------------------------------
    colors = {
        "Rot":   {"bg": "linear-gradient(135deg, #FF3E3E 0%, #800000 100%)", "border": "#FF3E3E", "glow": "rgba(255, 62, 62, 0.6)"},
        "Weiß":  {"bg": "linear-gradient(135deg, #E0E0E0 0%, #505050 100%)", "border": "#E0E0E0", "glow": "rgba(255, 255, 255, 0.6)"},
        "Blau":  {"bg": "linear-gradient(135deg, #2A8CFF 0%, #000080 100%)", "border": "#2A8CFF", "glow": "rgba(42, 140, 255, 0.6)"},
        "Gelb":  {"bg": "linear-gradient(135deg, #FFD700 0%, #8B6508 100%)", "border": "#FFD700", "glow": "rgba(255, 215, 0, 0.6)"},
        "Grün":  {"bg": "linear-gradient(135deg, #00FF66 0%, #004400 100%)", "border": "#00FF66", "glow": "rgba(0, 255, 102, 0.6)"}
    }
    
    style = colors.get(s_color, colors["Weiß"])

    st.markdown(f"""
    <style>
        /* Minimalist Hero Card */
        .psy-hero {{
            background: {style['bg']};
            border-left: 8px solid {style['border']};
            border-radius: 4px;
            padding: 20px;
            color: white;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }}
        .psy-kin-nr {{ font-size: 1.2em; letter-spacing: 3px; opacity: 0.8; font-weight: 300; }}
        .psy-name {{ font-size: 2.2em; font-weight: 800; text-transform: uppercase; line-height: 1.1; margin: 5px 0; }}
        .psy-mantra {{ font-style: italic; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 10px; margin-top: 10px; }}
        
        /* Listen Styles */
        .psy-list-item {{ background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 2px solid {style['border']}; }}
        .psy-label {{ color: {style['border']}; font-weight: bold; text-transform: uppercase; font-size: 0.8em; }}
        .psy-desc {{ color: #ddd; font-size: 0.95em; }}
        
        /* Expander Anpassung */
        div[data-testid="stExpander"] details {{ border-color: {style['border']} !important; }}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. HERO VISUAL (Only Kin, Color, Name)
    # -------------------------------------------------------------------------
    st.markdown(f"""
    <div class='psy-hero'>
        <div class='psy-kin-nr'>KIN {kin_nr} • {s_color.upper()}</div>
        <div class='psy-name'>{s_name}</div>
        <div class='psy-mantra'>
            "{s_action} um zu {s_power}, {s_essence} versiegelnd."
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. THE PSYCHOLOGICAL DEEP DIVE
    # -------------------------------------------------------------------------
    with st.expander("🧠 PSYCHOLOGISCHES PROFIL (Öffnen)", expanded=True):
        
        # Tabs für Übersichtlichkeit
        tab1, tab2, tab3 = st.tabs(["Licht-Aspekte", "Schatten-Arbeit", "Transformation"])

        # === TAB 1: LICHT (Potenzial) ===
        with tab1:
            light = psych.get('light_potential', {})
            st.info(f"**Kern-Qualität:** {light.get('core_trait', 'Nicht definiert')}")
            
            st.markdown("##### Attribute & Stärken")
            attributes = light.get('attributes', [])
            if attributes:
                for attr in attributes:
                    st.markdown(f"""
                    <div class='psy-list-item'>
                        <div class='psy-label'>{attr.get('name', '')}</div>
                        <div class='psy-desc'>{attr.get('desc', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Keine Attribute in der DB.")

        # === TAB 2: SCHATTEN (Herausforderung) ===
        with tab2:
            shadow = psych.get('shadow_integration', {})
            st.error(f"**Kern-Angst:** {shadow.get('core_fear', 'Nicht definiert')}")
            
            st.markdown("##### Dysfunktionale Muster")
            patterns = shadow.get('patterns', [])
            if patterns:
                for pat in patterns:
                    st.markdown(f"""
                    <div class='psy-list-item'>
                        <div class='psy-label'>⚠️ {pat.get('name', '')}</div>
                        <div class='psy-desc'>{pat.get('desc', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Neurose-Check (Tiefergehende Daten falls vorhanden)
            neurosis = shadow.get('neurosis', None)
            if neurosis:
                st.markdown("---")
                st.markdown(f"**Neurotische Tendenz: {neurosis.get('name', '')}**")
                st.caption(f"Mechanismus: {neurosis.get('mechanism', '')}")
                # Symptome auflisten
                symptoms = neurosis.get('symptoms', [])
                if symptoms:
                    st.write("Symptome:")
                    for sym in symptoms:
                        st.caption(f"• {sym}")

        # === TAB 3: TRANSFORMATION (Heilung) ===
        with tab3:
            heal = psych.get('healing_path', {})
            
            st.markdown("##### 🧬 Strategie zur Heilung")
            st.write(heal.get('strategy', 'Keine Strategie definiert.'))
            
            st.markdown("##### 🧘 Praktische Übungen")
            practices = heal.get('practices', [])
            if practices:
                for prac in practices:
                    st.success(f"✅ {prac}")
            else:
                st.caption("Keine Übungen hinterlegt.")

            # Affirmation fett am Ende
            aff = heal.get('affirmation', None)
            if aff:
                st.markdown("---")
                st.markdown(f"**Heil-Satz:** *\"{aff}\"*")

    return export_data
