import streamlit as st

def render(kin_nr, data):
    """
    Rendert das Tägliche KIN als High-End 'Atomic Module'.
    Style: Glassmorphismus & Neon-HUD.
    """
    
    # 0. SAFETY CHECK
    if kin_nr == 0 or not data:
        st.info("🌀 HUNAB KU - 0.0. Der Tag außerhalb der Zeit.")
        return {"kin": 0, "name": "Hunab Ku"}

    id_data = data.get('identity', {})
    seal = id_data.get('seal', {})
    tone = id_data.get('tone', {})
    psych = seal.get('psychology', {})

    # SAFE ACCESS: Wir holen Werte mit Fallback, falls die DB Lücken hat
    s_action = seal.get('action', 'Agieren')
    s_power = seal.get('power', 'Kraft') # <--- HIER WAR DER FEHLER
    s_essence = seal.get('essence', 'Essenz')
    s_color = seal.get('color', 'Weiß')
    
    t_name = tone.get('name', str(tone.get('id', 0)))
    t_power = tone.get('power', 'Kraft')

    # Export-Daten
    export_data = {
        "kin": kin_nr,
        "name": id_data.get('name', f"Kin {kin_nr}"),
        "affirmation": f"Ich {s_action} um zu {s_power}, {s_essence} versiegelnd.",
        "light_core": psych.get('light_potential', {}).get('core_trait', '-'),
        "shadow_core": psych.get('shadow_integration', {}).get('core_fear', '-')
    }

    # 1. DESIGN ENGINE
    colors = {
        "Rot":   {"bg": "linear-gradient(135deg, #FF3E3E 0%, #800000 100%)", "border": "#FF3E3E", "glow": "rgba(255, 62, 62, 0.6)"},
        "Weiß":  {"bg": "linear-gradient(135deg, #E0E0E0 0%, #505050 100%)", "border": "#E0E0E0", "glow": "rgba(255, 255, 255, 0.6)"},
        "Blau":  {"bg": "linear-gradient(135deg, #2A8CFF 0%, #000080 100%)", "border": "#2A8CFF", "glow": "rgba(42, 140, 255, 0.6)"},
        "Gelb":  {"bg": "linear-gradient(135deg, #FFD700 0%, #8B6508 100%)", "border": "#FFD700", "glow": "rgba(255, 215, 0, 0.6)"},
        "Grün":  {"bg": "linear-gradient(135deg, #00FF66 0%, #004400 100%)", "border": "#00FF66", "glow": "rgba(0, 255, 102, 0.6)"}
    }
    
    style = colors.get(s_color, colors["Weiß"])
    
    # Custom CSS
    st.markdown(f"""
    <style>
        .kin-hero-card {{
            background: {style['bg']};
            border-radius: 15px; padding: 20px; color: white;
            box-shadow: 0 0 20px {style['glow']}; margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.2); position: relative; overflow: hidden;
        }}
        .stat-panel {{
            background: rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 10px;
            text-align: center; border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(5px);
        }}
        .stat-label {{ font-size: 0.7em; text-transform: uppercase; opacity: 0.7; letter-spacing: 1px; }}
        .stat-value {{ font-size: 1.1em; font-weight: bold; color: {style['border']}; }}
        .hero-name {{ font-size: 1.8em; font-weight: 800; text-transform: uppercase; margin: 5px 0; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }}
        .hero-quote {{ font-style: italic; font-size: 0.95em; opacity: 0.9; border-left: 3px solid rgba(255,255,255,0.5); padding-left: 10px; }}
        div[data-testid="stExpander"] details {{
            border-left: 5px solid {style['border']} !important; background: rgba(10, 10, 15, 0.8);
        }}
    </style>
    """, unsafe_allow_html=True)

    # 2. UI RENDER
    st.markdown(f"""
    <div class='kin-hero-card'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div style='font-size:0.9em; letter-spacing:3px; opacity:0.9;'>KIN {kin_nr}</div>
            <div style='font-size:1.5em;'>{seal.get('maya', '')}</div>
        </div>
        <div class='hero-name'>{id_data.get('name', 'Unknown')}</div>
        <div class='hero-quote'>"{s_action} um zu {s_power}..."</div>
    </div>
    """, unsafe_allow_html=True)

    # 3. INTERACTIVE DEEP DIVE
    with st.expander("🧬 ANALYSE DATEN-UPLINK", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-panel'><div class='stat-label'>Familie</div><div class='stat-value'>{seal.get('family', '-')}</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-panel'><div class='stat-label'>Clan</div><div class='stat-value'>{seal.get('clan', '-')}</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-panel'><div class='stat-label'>Planet</div><div class='stat-value'>{seal.get('planet', '-')}</div></div>", unsafe_allow_html=True)
        
        st.markdown("")
        st.caption(f"Frequenz-Modulation: Ton {tone.get('id', 0)} ({t_name})")
        st.progress(min(tone.get('id', 1) / 13, 1.0))
        
        st.markdown("---")
        t1, t2, t3 = st.tabs(["✨ LICHT", "🌑 SCHATTEN", "💊 HEILUNG"])
        
        with t1:
            st.success(f"**Kern:** {psych.get('light_potential', {}).get('core_trait', '-')}")
            for attr in psych.get('light_potential', {}).get('attributes', []):
                st.markdown(f"+ {attr.get('name','')}: {attr.get('desc','')}")
        with t2:
            st.error(f"**Angst:** {psych.get('shadow_integration', {}).get('core_fear', '-')}")
            for pat in psych.get('shadow_integration', {}).get('patterns', []):
                st.markdown(f"- {pat.get('name','')}: {pat.get('desc','')}")
        with t3:
            st.info(f"**Strategie:** {psych.get('healing_path', {}).get('strategy', '-')}")
            st.markdown(f"> *Ich {s_action} um zu {s_power}, {s_essence} versiegelnd.*")

    return export_data
