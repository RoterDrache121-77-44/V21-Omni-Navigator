# ==============================================================================
# 🛸 V21 GALACTIC INTERFACE (Haupt-Terminal)
# ------------------------------------------------------------------------------
# ZWECK:    UI/UX Layer, Orchestrierung der Module, Visualisierung des 'Pulse'
# AUTOR:    Hunab Ku 21 Mentor
# STATUS:   ALPHA 1.0 (Live System)
# ------------------------------------------------------------------------------
# ARCHITEKTUR:
# 1. Init (Page Config & CSS)
# 2. Input (Sidebar Date Picker)
# 3. Data Fetch (Engine Core -> Pulse)
# 4. Rendering (Atomic UI Components)
# ==============================================================================

import streamlit as st
import datetime
from engine_core import GalacticCore

# ------------------------------------------------------------------------------
# 1. KONFIGURATION & DESIGN-INJEKTION
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="V21 | 13-Moon Synchronizer",
    page_icon="🧬",
    layout="centered", # Mobil-optimiert: "centered" ist besser für Handy-Säulen
    initial_sidebar_state="collapsed"
)

def inject_css():
    """Lädt das 'Deep Space' Design-System in den Browser."""
    st.markdown("""
        <style>
        /* --- GLOBAL SPACE THEME --- */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 100%);
            color: #E0E0E0;
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* --- GLASSMORPHISM CARDS --- */
        .glass-card {
            background: rgba(20, 20, 25, 0.70);
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        
        /* --- NEON BORDERS (Energie-Indikatoren) --- */
        .border-Rot { border-left: 4px solid #FF3E3E; box-shadow: -2px 0 10px rgba(255, 62, 62, 0.2); }
        .border-Weiß { border-left: 4px solid #E0E0E0; box-shadow: -2px 0 10px rgba(224, 224, 224, 0.2); }
        .border-Blau { border-left: 4px solid #2A8CFF; box-shadow: -2px 0 10px rgba(42, 140, 255, 0.2); }
        .border-Gelb { border-left: 4px solid #FFD700; box-shadow: -2px 0 10px rgba(255, 215, 0, 0.2); }
        .border-Grün { border-left: 4px solid #00FF66; box-shadow: -2px 0 10px rgba(0, 255, 102, 0.2); }

        /* --- TYPOGRAPHIE --- */
        h1, h2, h3 { font-weight: 300; letter-spacing: 1px; color: #fff; }
        .label-small { font-size: 0.75rem; text-transform: uppercase; color: #888; letter-spacing: 1.5px; }
        .value-big { font-size: 1.2rem; font-weight: 600; color: #fff; }
        .kin-number { font-size: 3rem; font-weight: 800; opacity: 0.2; position: absolute; right: 20px; top: 10px; }
        
        /* --- TWEAKS --- */
        div.stButton > button { width: 100%; background: #2A2A35; border: 1px solid #444; color: white; }
        </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. HELPER (Atomic UI Builders)
# ------------------------------------------------------------------------------
def render_metric_card(label, value, subtext="", border_color="Weiß"):
    """Eine wiederverwendbare Micro-Komponente."""
    st.markdown(f"""
        <div class="glass-card border-{border_color}">
            <div class="label-small">{label}</div>
            <div class="value-big">{value}</div>
            <div style="font-size: 0.8rem; color: #aaa;">{subtext}</div>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. MAIN APP LOGIC
# ------------------------------------------------------------------------------
def main():
    inject_css()

    # --- SIDEBAR: Navigation & Zeitreise ---
    with st.sidebar:
        st.header("🛸 Navigation")
        target_date = st.date_input("Zeit-Koordinate", datetime.date.today())
        st.divider()
        st.caption(f"System V21 Alpha | {target_date.strftime('%d.%m.%Y')}")

    # --- ENGINE: Daten laden ---
    pulse = GalacticCore.get_pulse(target_date)
    
    # Extraktion für einfacheren Zugriff
    meta = pulse['metadata']
    tzolkin = pulse['tzolkin']
    moon = pulse['moon']
    
    # Farbe für das UI bestimmen
    if meta['is_leap_day'] or meta['is_day_out_of_time']:
        ui_color = "Grün"
    else:
        # Fallback falls DB mal leer ist
        ui_color = tzolkin.get('identity', {}).get('seal', {}).get('color', 'Weiß')

    # --------------------------------------------------------------------------
    # MODUL 1: HEADER (Das Galaktische Banner)
    # --------------------------------------------------------------------------
    st.markdown(f"""
        <div class="glass-card border-{ui_color}" style="text-align: center; padding: 30px;">
            <div class="label-small">{meta['date_str']} • {moon.get('moon', {}).get('name', 'Zeitlos')}</div>
            <h1 style="margin: 10px 0; font-size: 2.5rem;">{tzolkin['identity']['name']}</h1>
            <div style="color: #bbb; font-style: italic;">"{tzolkin.get('message', 'Ich harmonisiere um zu überleben...')}"</div>
            <div class="kin-number">{meta['kin']}</div>
        </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # MODUL 2: DASHBOARD (Die 4 Säulen)
    # --------------------------------------------------------------------------
    col1, col2 = st.columns(2)
    
    with col1:
        # Siegel Info
        seal_name = tzolkin['identity']['seal']['name']
        seal_action = tzolkin['identity']['seal'].get('action', '---')
        render_metric_card("Solares Siegel", seal_name, f"Aktion: {seal_action}", ui_color)
        
        # Mond Info
        moon_name = moon.get('moon', {}).get('name', '---')
        totem = moon.get('moon', {}).get('totem', '---')
        render_metric_card("Mond Frequenz", moon_name, f"Totem: {totem}", "Weiß")

    with col2:
        # Ton Info
        tone_name = tzolkin['identity']['tone']['name']
        tone_power = tzolkin['identity']['tone'].get('power', '---')
        render_metric_card("Galaktischer Ton", tone_name, f"Kraft: {tone_power}", ui_color)
        
        # Plasma / PSI
        plasma = moon.get('plasma', {}).get('name', '---')
        psi = moon.get('psi_chrono', '---')
        render_metric_card("Plasma & PSI", plasma, f"PSI-Chrono: Kin {psi}", "Blau")

    # --------------------------------------------------------------------------
    # MODUL 3: DEEP DIVE (Psychologie & Schattenarbeit)
    # --------------------------------------------------------------------------
    # Hier beweisen wir die Tiefe der Datenbank
    if not meta['is_leap_day']:
        with st.expander(f"🧬 DNA-Analyse: {seal_name}", expanded=False):
            psych = tzolkin['identity']['seal'].get('psychology', {})
            
            if psych:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### ✨ Licht-Potenzial")
                    light = psych.get('light_potential', {})
                    st.write(f"**Kern:** {light.get('core_trait', '')}")
                    for attr in light.get('attributes', [])[:2]:
                        st.info(f"**{attr['name']}:** {attr['desc']}")
                
                with c2:
                    st.markdown("#### 🌑 Schatten-Integration")
                    shadow = psych.get('shadow_integration', {})
                    st.write(f"**Angst:** {shadow.get('core_fear', '')}")
                    for pattern in shadow.get('patterns', [])[:2]:
                        st.warning(f"**{pattern['name']}:** {pattern['desc']}")
                
                st.markdown("---")
                st.caption("💡 Tipp: Nutze diese Daten für deine tägliche Meditation.")
            else:
                st.info("Keine psychologischen Detail-Daten für dieses Kin verfügbar.")

if __name__ == "__main__":
    main()
