import streamlit as st

def render(kin_nr, data):
    """
    Rendert das Tägliche KIN als High-End 'Atomic Module'.
    Style: Glassmorphismus & Neon-HUD.
    """
    
    # -------------------------------------------------------------------------
    # 0. SAFETY CHECK & EXPORT PREP
    # -------------------------------------------------------------------------
    if kin_nr == 0 or not data:
        st.info("🌀 HUNAB KU - 0.0. Der Tag außerhalb der Zeit.")
        return {"kin": 0, "name": "Hunab Ku"}

    id_data = data['identity']
    seal = id_data['seal']
    tone = id_data['tone']
    psych = seal['psychology']

    # Export-Daten (Clean Data First)
    export_data = {
        "kin": kin_nr,
        "name": id_data['name'],
        "affirmation": f"Ich {seal['action']} um zu {seal['power']}, {seal['essence']} versiegelnd.",
        "light_core": psych.get('light_potential', {}).get('core_trait', '-'),
        "shadow_core": psych.get('shadow_integration', {}).get('core_fear', '-')
    }

    # -------------------------------------------------------------------------
    # 1. DESIGN ENGINE (CSS-Variables)
    # -------------------------------------------------------------------------
    # Farb-Palette (Neon-Varianten)
    colors = {
        "Rot":   {"bg": "linear-gradient(135deg, #FF3E3E 0%, #800000 100%)", "border": "#FF3E3E", "glow": "rgba(255, 62, 62, 0.6)"},
        "Weiß":  {"bg": "linear-gradient(135deg, #E0E0E0 0%, #505050 100%)", "border": "#E0E0E0", "glow": "rgba(255, 255, 255, 0.6)"},
        "Blau":  {"bg": "linear-gradient(135deg, #2A8CFF 0%, #000080 100%)", "border": "#2A8CFF", "glow": "rgba(42, 140, 255, 0.6)"},
        "Gelb":  {"bg": "linear-gradient(135deg, #FFD700 0%, #8B6508 100%)", "border": "#FFD700", "glow": "rgba(255, 215, 0, 0.6)"},
        "Grün":  {"bg": "linear-gradient(135deg, #00FF66 0%, #004400 100%)", "border": "#00FF66", "glow": "rgba(0, 255, 102, 0.6)"}
    }
    
    # Fallback auf Weiß, falls Farbe fehlt
    style = colors.get(seal.get('color', 'Weiß'), colors["Weiß"])
    
    # Custom CSS für dieses Modul
    st.markdown(f"""
    <style>
        /* Hero Card Style */
        .kin-hero-card {{
            background: {style['bg']};
            border-radius: 15px;
            padding: 20px;
            color: white;
            box-shadow: 0 0 20px {style['glow']};
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.2);
            position: relative;
            overflow: hidden;
        }}
        
        /* Glass Panel für Stats */
        .stat-panel {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
        }}
        .stat-label {{ font-size: 0.7em; text-transform: uppercase; opacity: 0.7; letter-spacing: 1px; }}
        .stat-value {{ font-size: 1.1em; font-weight: bold; color: {style['border']}; }}

        /* Typography */
        .hero-kin {{ font-size: 0.9em; letter-spacing: 3px; opacity: 0.9; font-weight: 300; }}
        .hero-name {{ font-size: 1.8em; font-weight: 800; text-transform: uppercase; margin: 5px 0; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }}
        .hero-quote {{ font-style: italic; font-size: 0.95em; opacity: 0.9; border-left: 3px solid rgba(255,255,255,0.5); padding-left: 10px; }}
        
        /* Expander Hack (Rahmen färben) */
        div[data-testid="stExpander"] details {{
            border-left: 5px solid {style['border']} !important;
            background: rgba(10, 10, 15, 0.8);
        }}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. UI RENDER: HERO CARD (Der "Hingucker")
    # -------------------------------------------------------------------------
    # Das ist das, was der User IMMER sieht.
    st.markdown(f"""
    <div class='kin-hero-card'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div class='hero-kin'>KIN {kin_nr}</div>
            <div style='font-size:1.5em;'>{seal.get('maya', '')}</div>
        </div>
        <div class='hero-name'>{id_data['name']}</div>
        <div class='hero-quote'>
            "{seal['action']} um zu {seal['power']}..."
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. INTERACTIVE DEEP DIVE (Der Expander)
    # -------------------------------------------------------------------------
    with st.expander("🧬 ANALYSE DATEN-UPLINK", expanded=False):
        
        # A) HUD - TECHNISCHE DATEN
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='stat-panel'><div class='stat-label'>Familie</div><div class='stat-value'>{seal.get('family', '-')}</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-panel'><div class='stat-label'>Clan</div><div class='stat-value'>{seal.get('clan', '-')}</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-panel'><div class='stat-label'>Planet</div><div class='stat-value'>{seal.get('planet', '-')}</div></div>", unsafe_allow_html=True)
        
        st.markdown("") # Spacer

        # B) TON-FREQUENZ VISUALIZER
        st.caption(f"Frequenz-Modulation: Ton {tone['id']} ({tone['name']})")
        st.progress(tone['id'] / 13)
        
        st.markdown("---")

        # C) PSYCHOLOGIE TABS
        tab_light, tab_shadow, tab_heal = st.tabs(["✨ LICHT", "🌑 SCHATTEN", "💊 HEILUNG"])
        
        with tab_light:
            st.success(f"**Kern-Qualität:** {psych.get('light_potential', {}).get('core_trait', '-')}")
            light_attrs = psych.get('light_potential', {}).get('attributes', [])
            for attr in light_attrs:
                st.markdown(f"**+ {attr['name']}:** {attr['desc']}")

        with tab_shadow:
            st.error(f"**Kern-Angst:** {psych.get('shadow_integration', {}).get('core_fear', '-')}")
            shadow_pats = psych.get('shadow_integration', {}).get('patterns', [])
            for pat in shadow_pats:
                st.markdown(f"**- {pat['name']}:** {pat['desc']}")

        with tab_heal:
            healing = psych.get('healing_path', {})
            st.info(f"**Strategie:** {healing.get('strategy', '-')}")
            
            # Die Affirmation als Zitat
            st.markdown("### 🧘 Affirmation")
            st.markdown(f"""
            > "Ich {seal['action']} um zu {seal['power']}, {seal['essence']} versiegelnd.  
            > Mit dem {tone['name']} Ton der {tone['power']}."
            """)

    # Return für Export
    return export_data
