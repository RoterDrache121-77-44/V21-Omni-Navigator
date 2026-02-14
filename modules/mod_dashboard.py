import streamlit as st

# ------------------------------------------------------------------------------
# 1. CSS VISUAL FX ENGINE (Tone Physics & Seal Glow)
# ------------------------------------------------------------------------------
def inject_fx_css(seal_color, tone_id):
    """
    Erzeugt dynamisches CSS für das Glühen der Siegel und die Bewegung der Töne.
    """
    # A. FARB-GLÜHEN (Siegel)
    colors = {
        "Rot": "rgba(255, 62, 62, 0.6)",
        "Weiß": "rgba(224, 224, 224, 0.6)",
        "Blau": "rgba(42, 140, 255, 0.6)",
        "Gelb": "rgba(255, 215, 0, 0.6)",
        "Grün": "rgba(0, 255, 102, 0.6)"
    }
    glow_color = colors.get(seal_color, colors["Weiß"])
    
    # B. TON-ANIMATIONEN (Die Physik der Zeit)
    # Wir mappen die 13 Töne auf Bewegungs-Muster
    animation_css = ""
    
    if tone_id in [1, 5, 9, 13]: # PUNKTE (Eingang/Tor) -> Pulsieren
        animation_css = """
            @keyframes tone-anim {
                0% { transform: scale(1); opacity: 0.8; }
                50% { transform: scale(1.05); opacity: 1; text-shadow: 0 0 15px white; }
                100% { transform: scale(1); opacity: 0.8; }
            }
        """
    elif tone_id in [2, 6, 10]: # POLARITÄT -> Balance/Wippen
        animation_css = """
            @keyframes tone-anim {
                0% { transform: translateX(0px); }
                25% { transform: translateX(-2px) rotate(-1deg); }
                75% { transform: translateX(2px) rotate(1deg); }
                100% { transform: translateX(0px); }
            }
        """
    elif tone_id in [3, 7, 11]: # FLUSS/STRUKTUR -> Vibrieren/Fließen
        animation_css = """
            @keyframes tone-anim {
                0% { transform: translateY(0px); filter: brightness(1); }
                50% { transform: translateY(-3px); filter: brightness(1.3); }
                100% { transform: translateY(0px); filter: brightness(1); }
            }
        """
    else: # STRUKTUR (4, 8, 12) -> Stabil/Festigen
        animation_css = """
            @keyframes tone-anim {
                0% { border-color: rgba(255,255,255,0.1); }
                50% { border-color: rgba(255,255,255,0.5); box-shadow: inset 0 0 10px rgba(255,255,255,0.2); }
                100% { border-color: rgba(255,255,255,0.1); }
            }
        """

    # CSS INJEKTION
    st.markdown(f"""
        <style>
        /* Die Siegel-Kapsel (Expander Header Hack) */
        div[data-testid="stExpander"] details summary {{
            background: linear-gradient(90deg, rgba(20,20,25,0.9) 0%, {glow_color} 150%);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: white !important;
            font-family: 'Orbitron', sans-serif;
            transition: all 0.3s ease;
        }}
        div[data-testid="stExpander"] details summary:hover {{
            border-color: {glow_color};
            box-shadow: 0 0 15px {glow_color};
            padding-left: 20px; /* Kleiner Ruck nach rechts beim Hover */
        }}
        
        /* Die Ton-Animation Klasse */
        {animation_css}
        .tone-active {{
            animation: tone-anim 3s infinite ease-in-out;
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. CONTENT RENDERER (Der Inhalt des Expanders)
# ------------------------------------------------------------------------------
def render_psychology_content(data):
    """Baut den Inhalt auf, der erscheint, wenn man klickt."""
    if not data:
        st.caption("Keine Daten in der Noosphäre gefunden.")
        return

    # Licht
    light = data.get('light_potential', {})
    st.markdown(f"**✨ LICHT:** {light.get('core_trait', '---')}")
    
    # Schatten
    shadow = data.get('shadow_integration', {})
    st.markdown(f"**🌑 SCHATTEN:** {shadow.get('core_fear', '---')}")
    
    # Heilung (Als Zitat-Block)
    healing = data.get('healing_path', {})
    st.info(f"🌿 **Heilung:** {healing.get('strategy', '---')}")

# ------------------------------------------------------------------------------
# 3. MAIN RENDER LOOP
# ------------------------------------------------------------------------------
def render(pulse):
    tzolkin = pulse['tzolkin']
    meta = pulse['metadata']
    
    # Hunab Ku Check
    if meta['is_leap_day']:
        st.markdown("<div class='glass-container' style='text-align:center'>🌀 HUNAB KU 0.0</div>", unsafe_allow_html=True)
        return

    # Datenvorbereitung
    seal = tzolkin['identity']['seal']
    tone = tzolkin['identity']['tone']
    
    # 1. CSS laden (Farbe des Siegels + Animation des Tons)
    inject_fx_css(seal['color'], tone['id'])

    # 2. Layout Grid
    c1, c2 = st.columns(2)
    
    # SPALTE 1: DAS SIEGEL (Der leuchtende Button)
    with c1:
        label = f"{seal['name'].upper()}"
        with st.expander(f"🔮 {label}"):
            st.caption(f"Code: {seal['id']} | Aktion: {seal.get('action', '')}")
            st.divider()
            render_psychology_content(seal.get('psychology'))

    # SPALTE 2: DER TON (Das animierte Objekt)
    with c2:
        # Hier nutzen wir HTML im Label, um die Animation einzubauen (Trick!)
        # Wir können Streamlit Expanders Label nicht animieren, aber wir können ein Icon davor setzen.
        # Aber wir machen den Expander-Inhalt animiert oder den Header "fluxy".
        
        # Ton Name
        label_tone = f"{tone['name'].upper()}"
        
        # Der Expander
        with st.expander(f"〰️ {label_tone}"):
            # Hier drin ist die Animation sichtbar!
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 10px;">
                    <span class="tone-active" style="font-size: 1.5rem; font-weight: bold;">
                        Ton {tone['id']}
                    </span>
                    <br><span style="font-size: 0.8rem; color: #888;">{tone.get('power', '')}</span>
                </div>
            """, unsafe_allow_html=True)
            st.divider()
            render_psychology_content(tone.get('psychology'))

    # Optional: Ein kleiner Hinweis für den User
    if 'shown_hint' not in st.session_state:
        st.caption("ℹ️ Tipp: Tippe auf die Namen, um die Akasha-Daten zu öffnen.")
        st.session_state['shown_hint'] = True
