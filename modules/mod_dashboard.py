import streamlit as st

# ------------------------------------------------------------------------------
# 1. VISUAL FX ENGINE (CSS Magie)
# ------------------------------------------------------------------------------
def inject_fx_css(seal_color, tone_id):
    """
    Erzeugt das Design: Leuchtende Buttons & tanzende Töne.
    """
    # Farben-Mapping (mit Transparenz für Glow)
    colors = {
        "Rot": "rgba(255, 62, 62, 0.7)",
        "Weiß": "rgba(224, 224, 224, 0.7)",
        "Blau": "rgba(42, 140, 255, 0.7)",
        "Gelb": "rgba(255, 215, 0, 0.7)",
        "Grün": "rgba(0, 255, 102, 0.7)"
    }
    glow_color = colors.get(seal_color, colors["Weiß"])
    
    # Animations-Logik für die Töne
    animation_css = ""
    if tone_id in [1, 5, 9, 13]: # PULSIEREN (Tore)
        animation_css = "@keyframes tone-anim { 0% {transform:scale(1);} 50% {transform:scale(1.05); text-shadow:0 0 10px white;} 100% {transform:scale(1);} }"
    elif tone_id in [2, 6, 10]: # WIPPEN (Polarität)
        animation_css = "@keyframes tone-anim { 0% {transform:translateX(0);} 25% {transform:rotate(-2deg);} 75% {transform:rotate(2deg);} 100% {transform:translateX(0);} }"
    elif tone_id in [3, 7, 11]: # VIBRIEREN (Fluss)
        animation_css = "@keyframes tone-anim { 0% {transform:translateY(0);} 50% {transform:translateY(-2px); opacity:0.8;} 100% {transform:translateY(0);} }"
    else: # LEUCHTEN (Struktur)
        animation_css = "@keyframes tone-anim { 0% {border-color:rgba(255,255,255,0.2);} 50% {border-color:rgba(255,255,255,0.8); box-shadow:inset 0 0 15px rgba(255,255,255,0.3);} 100% {border-color:rgba(255,255,255,0.2);} }"

    st.markdown(f"""
        <style>
        /* 1. DER EXPANDER-BUTTON (Das leuchtende Siegel) */
        div[data-testid="stExpander"] details summary {{
            background: linear-gradient(90deg, #111 0%, {glow_color} 150%);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px;
            color: white !important;
            font-family: 'Orbitron', sans-serif;
            font-weight: bold;
            letter-spacing: 1px;
            transition: all 0.4s ease;
            margin-bottom: 5px;
        }}
        div[data-testid="stExpander"] details summary:hover {{
            border-color: {glow_color};
            box-shadow: 0 0 20px {glow_color};
            padding-left: 25px; /* Interaktiver Ruck */
        }}
        
        /* 2. DER ANIMIERTE TON */
        {animation_css}
        .tone-obj {{
            display: inline-block;
            animation: tone-anim 3s infinite ease-in-out;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid rgba(255,255,255,0.1);
        }}

        /* 3. INHALT DESIGN (Markdown Styling im Expander) */
        .psy-header {{ color: {glow_color}; font-family: 'Rajdhani'; font-weight: bold; font-size: 1.1rem; margin-top: 10px; margin-bottom: 5px; text-transform: uppercase; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .psy-core {{ font-weight: bold; color: #fff; margin-bottom: 8px; font-size: 1.05rem; }}
        .psy-list {{ font-size: 0.95rem; color: #ccc; margin-left: 10px; }}
        .psy-box {{ background: rgba(255,255,255,0.05); border-left: 3px solid {glow_color}; padding: 10px; border-radius: 0 8px 8px 0; margin: 10px 0; }}
        </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. CONTENT ENGINE (Die volle psychologische Auswertung)
# ------------------------------------------------------------------------------
def render_full_psychology(data):
    """
    Rendert ALLES, was in der Datenbank steht. Keine Zusammenfassungen.
    """
    if not data:
        st.caption("Daten-Link unterbrochen...")
        return

    # --- A. LICHT (POTENZIAL) ---
    light = data.get('light_potential', {})
    st.markdown('<div class="psy-header">✨ LICHT & POTENZIAL</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="psy-core">{light.get("core_trait", "---")}</div>', unsafe_allow_html=True)
    
    # Attribute im Detail
    for attr in light.get('attributes', []):
        st.markdown(f"""
        <div style="margin-bottom:6px;">
            <strong style="color:#eee;">◈ {attr['name']}:</strong> 
            <span style="color:#aaa;">{attr['desc']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- B. SCHATTEN (HERAUSFORDERUNG) ---
    shadow = data.get('shadow_integration', {})
    st.markdown('<div class="psy-header">🌑 SCHATTEN & ARBEIT</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="psy-core">{shadow.get("core_fear", "---")}</div>', unsafe_allow_html=True)
    
    # Schatten-Muster
    for pattern in shadow.get('patterns', []):
        st.markdown(f"""
        <div style="margin-bottom:6px;">
            <strong style="color:#ffcccc;">⚠ {pattern['name']}:</strong> 
            <span style="color:#aaa;">{pattern['desc']}</span>
        </div>
        """, unsafe_allow_html=True)
        
    # Die Neurose (Der tiefe psychologische Mechanismus)
    neurosis = shadow.get('neurosis', {})
    if neurosis:
        st.markdown(f"""
        <div class="psy-box" style="border-color: #ff4b4b;">
            <strong style="color:#ff4b4b;">Zentrale Neurose: {neurosis.get('name', '')}</strong><br>
            <em style="font-size:0.9rem;">"{neurosis.get('mechanism', '')}"</em>
            <ul style="margin-top:5px; margin-bottom:0; color:#ccc; font-size:0.85rem;">
                {''.join([f'<li>{s}</li>' for s in neurosis.get('symptoms', [])])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- C. HEILUNGSWEG (TRANSFORMATION) ---
    healing = data.get('healing_path', {})
    st.markdown('<div class="psy-header">🌿 WEG DER HEILUNG</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="psy-core">{healing.get("strategy", "---")}</div>', unsafe_allow_html=True)
    
    # Praktische Übungen
    if 'practices' in healing:
        for practice in healing['practices']:
            st.markdown(f"<div style='color:#aaddaa; margin-bottom:4px;'>✓ {practice}</div>", unsafe_allow_html=True)
            
    # Die Affirmation (Der Kraftsatz)
    affirmation = healing.get('affirmation')
    if affirmation:
        st.markdown(f"""
        <div style="margin-top:15px; text-align:center; font-style:italic; font-family:'Georgia'; color:#fff; padding:10px; border:1px dashed #555; border-radius:8px;">
            "{affirmation}"
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. MAIN RENDERER
# ------------------------------------------------------------------------------
def render(pulse):
    tzolkin = pulse['tzolkin']
    meta = pulse['metadata']
    
    # 0. Hunab Ku Check
    if meta['is_leap_day']:
        st.markdown("<div style='text-align:center; padding:20px; border:1px solid #0f6; color:#0f6;'>🌀 HUNAB KU 0.0 - Der Tag außerhalb der Zeit</div>", unsafe_allow_html=True)
        return

    # 1. Datenvorbereitung
    seal = tzolkin['identity']['seal']
    tone = tzolkin['identity']['tone']
    
    # 2. Styles injizieren
    inject_fx_css(seal['color'], tone['id'])

    # 3. Layout Grid
    c1, c2 = st.columns(2)
    
    # --- SPALTE 1: DAS SIEGEL ---
    with c1:
        # Button Label
        label = f"{seal['name'].upper()}"
        
        # Der interaktive Container
        with st.expander(f"🔮 {label}"):
            # Header Info
            st.caption(f"Code {seal['id']} • {seal.get('family', '')} • {seal.get('chakra', '')}")
            st.divider()
            # VOLLE PSYCHOLOGIE
            render_full_psychology(seal.get('psychology'))

    # --- SPALTE 2: DER TON ---
    with c2:
        # Button Label mit Animationstrick
        tone_name = tone['name'].upper()
        
        # Der interaktive Container
        with st.expander(f"〰️ {tone_name}"):
            # Header Info (Animiert)
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 15px;">
                    <div class="tone-obj" style="font-size: 2rem; font-weight: 800; color: #fff;">
                        {tone['id']}
                    </div>
                    <div style="color: #aaa; font-size: 0.8rem; margin-top: 5px;">
                        KRAFT: {tone.get('power', '---').upper()}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.divider()
            # VOLLE PSYCHOLOGIE
            render_full_psychology(tone.get('psychology'))
