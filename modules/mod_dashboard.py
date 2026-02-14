import streamlit as st

def render_psychology_section(data, title):
    """Interne Hilfsfunktion für die Psychologie-Expander"""
    if not data:
        return
    
    with st.expander(f"👁️ Psychologie: {title}"):
        # 1. LICHTPOTENZIAL
        light = data.get('light_potential', {})
        st.markdown(f"**✨ Lichtpotential: {light.get('core_trait', 'N/A')}**")
        for attr in light.get('attributes', []):
            st.caption(f"• {attr['name']}: {attr['desc']}")
        
        st.divider()
        
        # 2. SCHATTEN
        shadow = data.get('shadow_integration', {})
        st.markdown(f"**🌑 Schattenarbeit: {shadow.get('core_fear', 'N/A')}**")
        for pattern in shadow.get('patterns', []):
            st.caption(f"• {pattern['name']}: {pattern['desc']}")
            
        st.divider()
        
        # 3. HEILUNGSWEG
        healing = data.get('healing_path', {})
        st.markdown(f"**🌿 Heilungsweg: {healing.get('strategy', 'N/A')}**")
        for practice in healing.get('practices', []):
            st.info(practice)

def render(pulse):
    tzolkin = pulse['tzolkin']
    meta = pulse['metadata']
    
    if meta['is_leap_day']:
        st.info("Hunab Ku: Die Psychologie der Leere.")
        return

    # Layout: Zwei Spalten für Siegel und Ton
    col1, col2 = st.columns(2)
    
    with col1:
        seal = tzolkin['identity']['seal']
        st.markdown(f"### {seal['name']}")
        # Hier rufen wir die Psychologie für das Siegel auf
        render_psychology_section(seal.get('psychology'), seal['name'])

    with col2:
        tone = tzolkin['identity']['tone']
        st.markdown(f"### {tone['name']}")
        # Hier rufen wir die Psychologie für den Ton auf
        render_psychology_section(tone.get('psychology'), tone['name'])
