# ==============================================================================
# 🛸 V21 GALACTIC INTERFACE (Haupt-Terminal)
# ------------------------------------------------------------------------------
# ZWECK:    UI/UX Layer, Orchestrierung der Module, Visualisierung des 'Pulse'
# AUTOR:    Hunab Ku 21 Mentor
# STATUS:   ALPHA 1.2 (Modular Reordering Enabled)
# ==============================================================================

import streamlit as st
import datetime
from engine_core import GalacticCore

# ------------------------------------------------------------------------------
# 1. KONFIGURATION & DESIGN
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="V21 | 13-Moon Synchronizer",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="expanded" 
)

def inject_css():
    """Lädt das 'Deep Space' Design-System."""
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
        
        /* --- NEON BORDERS --- */
        .border-Rot { border-left: 4px solid #FF3E3E; box-shadow: -2px 0 10px rgba(255, 62, 62, 0.2); }
        .border-Weiß { border-left: 4px solid #E0E0E0; box-shadow: -2px 0 10px rgba(224, 224, 224, 0.2); }
        .border-Blau { border-left: 4px solid #2A8CFF; box-shadow: -2px 0 10px rgba(42, 140, 255, 0.2); }
        .border-Gelb { border-left: 4px solid #FFD700; box-shadow: -2px 0 10px rgba(255, 215, 0, 0.2); }
        .border-Grün { border-left: 4px solid #00FF66; box-shadow: -2px 0 10px rgba(0, 255, 102, 0.2); }

        /* --- TYPO --- */
        h1, h2, h3 { font-weight: 300; letter-spacing: 1px; color: #fff; }
        .label-small { font-size: 0.75rem; text-transform: uppercase; color: #888; letter-spacing: 1.5px; }
        .value-big { font-size: 1.2rem; font-weight: 600; color: #fff; }
        .kin-number { font-size: 3rem; font-weight: 800; opacity: 0.2; position: absolute; right: 20px; top: 10px; }
        
        /* --- TWEAKS --- */
        /* Sidebar Design */
        [data-testid="stSidebar"] {
            background-color: #0e0e14;
            border-right: 1px solid #222;
        }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, subtext="", border_color="Weiß"):
    st.markdown(f"""
        <div class="glass-card border-{border_color}">
            <div class="label-small">{label}</div>
            <div class="value-big">{value}</div>
            <div style="font-size: 0.8rem; color: #aaa;">{subtext}</div>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. ATOMARE MODULE (Die Bausteine)
# ------------------------------------------------------------------------------

def render_header(pulse, ui_color):
    """Modul: Das große Banner oben."""
    meta = pulse['metadata']
    tzolkin = pulse['tzolkin']
    moon = pulse['moon']
    
    moon_name = moon.get('moon', {}).get('name', 'Zeitlos')
    kin_name = tzolkin.get('identity', {}).get('name', 'Hunab Ku')
    message = tzolkin.get('message', 'Harmonisierung der Zeit...')
    
    st.markdown(f"""
        <div class="glass-card border-{ui_color}" style="text-align: center; padding: 30px;">
            <div class="label-small">{meta['date_str']} • {moon_name}</div>
            <h1 style="margin: 10px 0; font-size: 2.2rem;">{kin_name}</h1>
            <div style="color: #bbb; font-style: italic;">"{message}"</div>
            <div class="kin-number">{meta['kin']}</div>
        </div>
    """, unsafe_allow_html=True)

def render_dashboard(pulse, ui_color):
    """Modul: Die 4 Säulen (Siegel, Ton, Mond, Plasma)."""
    tzolkin = pulse['tzolkin']
    moon = pulse['moon']
    meta = pulse['metadata']

    if meta['is_leap_day']:
        st.info("🌀 Hunab Ku Modus: Keine Standard-Parameter am Tag außerhalb der Zeitmatrix.")
        return

    col1, col2 = st.columns(2)
    
    with col1:
        # Siegel
        s = tzolkin['identity']['seal']
        render_metric_card("Solares Siegel", s['name'], f"Aktion: {s.get('action','?')}", ui_color)
        # Mond
        m = moon.get('moon', {})
        render_metric_card("Mond Frequenz", m.get('name','?'), f"Totem: {m.get('totem','?')}", "Weiß")

    with col2:
        # Ton
        t = tzolkin['identity']['tone']
        render_metric_card("Galaktischer Ton", t['name'], f"Kraft: {t.get('power','?')}", ui_color)
        # Plasma
        p = moon.get('plasma', {})
        psi = moon.get('psi_chrono', '?')
        render_metric_card("Plasma & PSI", p.get('name','?'), f"PSI-Chrono: Kin {psi}", "Blau")

def render_deep_dive(pulse, ui_color):
    """Modul: DNA & Psychologie Expander."""
    meta = pulse['metadata']
    tzolkin = pulse['tzolkin']
    
    if meta['is_leap_day']: 
        return

    seal_name = tzolkin['identity']['seal']['name']
    
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
        else:
            st.info("Daten werden geladen...")

def render_raw_data(pulse, ui_color):
    """Modul: Für Debugging (zeigt das rohe JSON)."""
    with st.expander("🛠️ System-Daten (Raw Pulse)"):
        st.json(pulse)

# ------------------------------------------------------------------------------
# 3. MAIN ORCHESTRATOR
# ------------------------------------------------------------------------------
def main():
    inject_css()

    # --- SIDEBAR: Navigation & Setup ---
    with st.sidebar:
        st.header("🛸 V21 Cockpit")
        
        # 1. Datum (Erweitert: 1700 - 2300)
        st.subheader("1. Zeit-Koordinate")
        min_d = datetime.date(1700, 1, 1)
        max_d = datetime.date(2300, 12, 31)
        target_date = st.date_input(
            "Datum wählen", 
            datetime.date.today(),
            min_value=min_d,
            max_value=max_d
        )
        
        st.divider()

        # 2. Layout Manager (Reihenfolge anpassen)
        st.subheader("2. Modul-Sequenz")
        
        # Dictionary der verfügbaren Module
        # Key = Name in der Liste, Value = Die Funktion
        module_registry = {
            "Banner (Header)": render_header,
            "4-Säulen Dashboard": render_dashboard,
            "DNA Analyse (Deep Dive)": render_deep_dive,
            "System Daten (Debug)": render_raw_data
        }
        
        # Standard-Auswahl
        default_modules = ["Banner (Header)", "4-Säulen Dashboard", "DNA Analyse (Deep Dive)"]
        
        selected_modules = st.multiselect(
            "Layout anpassen (Drag & Drop in Liste)",
            options=module_registry.keys(),
            default=default_modules
        )
        
        st.caption("Ändere die Reihenfolge oben, um die App neu zu sortieren.")
        st.divider()
        st.caption(f"System Status: ONLINE\nDatum: {target_date.strftime('%d.%m.%Y')}")

    # --- ENGINE START ---
    pulse = GalacticCore.get_pulse(target_date)
    
    # Farbe bestimmen
    meta = pulse['metadata']
    if meta['is_leap_day'] or meta['is_day_out_of_time']:
        ui_color = "Grün"
    else:
        ui_color = pulse['tzolkin'].get('identity', {}).get('seal', {}).get('color', 'Weiß')

    # --- RENDER LOOP ---
    # Hier passiert die Magie: Wir loopen durch die User-Auswahl
    for module_name in selected_modules:
        render_func = module_registry[module_name]
        render_func(pulse, ui_color)

if __name__ == "__main__":
    main()
