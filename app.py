# ==============================================================================
# 🛸 V21 HOST SYSTEM (Ultimate Edition)
# ------------------------------------------------------------------------------
# ZWECK:    High-End Container für galaktische Module.
# UPDATES:  Fix für Datum-Lesbarkeit, Pulse-Inspector integriert.
# ==============================================================================

import streamlit as st
import datetime
import os
import importlib
import time
import sys
from engine_core import GalacticCore

# 1. SYSTEM INITIALISIERUNG
st.set_page_config(
    page_title="V21 | Chrono-Architecture",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. DESIGN ENGINE (CSS Injection)
def inject_advanced_css():
    st.markdown("""
        <style>
        /* --- FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

        /* --- GLOBAL THEME --- */
        .stApp {
            background: radial-gradient(circle at 50% 10%, #1a1a2e 0%, #000000 90%);
            color: #E0E0E0;
            font-family: 'Rajdhani', sans-serif;
        }

        /* --- INPUT FIX (BRUTAL FORCE CONTRAST) --- */
        /* Wir zwingen alle Eingabefelder auf hellen Hintergrund mit dunkler Schrift */
        input {
            background-color: #e0e0e0 !important; 
            color: #000000 !important;
            font-weight: bold !important;
            border-radius: 4px !important;
        }
        /* Datum-Picker Icon */
        div[data-baseweb="input"] {
            background-color: #e0e0e0 !important;
            border: 1px solid #fff !important;
        }
        /* Dropdown Menüs */
        div[data-baseweb="select"] > div {
            background-color: #222 !important;
            color: #fff !important;
        }

        /* --- SIDEBAR STYLE --- */
        [data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #333;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
            color: #eeeeee !important;
        }
        
        /* --- MODULE CONTAINER --- */
        .glass-container {
            background: rgba(15, 15, 20, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            backdrop-filter: blur(15px);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        /* --- ERROR BOX --- */
        .error-box { border: 1px solid #ff4b4b; background: rgba(50,0,0,0.5); }
        </style>
    """, unsafe_allow_html=True)

# 3. INFRASTRUKTUR
def get_available_modules():
    if not os.path.exists("modules"):
        os.makedirs("modules")
        return []
    
    files = [f[:-3] for f in os.listdir("modules") if f.startswith("mod_") and f.endswith(".py")]
    
    # Sortierung: Header & Dashboard zuerst
    priority = ["mod_header", "mod_dashboard"]
    sorted_files = [p for p in priority if p in files] + [f for f in files if f not in priority]
    
    return sorted_files

def run_module_safely(mod_name, pulse, debug_mode):
    try:
        start_time = time.time()
        module_path = f"modules.{mod_name}"
        
        if module_path in sys.modules:
            module = importlib.import_module(module_path)
            importlib.reload(module)
        else:
            module = importlib.import_module(module_path)
        
        if hasattr(module, "render"):
            module.render(pulse)
            duration = (time.time() - start_time) * 1000
            if debug_mode:
                st.caption(f"⏱️ [SYS] {mod_name}: {duration:.1f}ms")
        else:
            st.error(f"⚠️ {mod_name}: Keine render()-Funktion!")

    except Exception as e:
        st.markdown(f"<div class='glass-container error-box'><h4>💥 Crash: {mod_name}</h4><p>{e}</p></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. MAIN COCKPIT
# ------------------------------------------------------------------------------
def main():
    inject_advanced_css()

    with st.sidebar:
        st.header("🛸 V21 MISSION CONTROL")
        
        st.subheader("1. Zeit-Koordinate")
        # Datumseingabe - jetzt lesbar!
        target_date = st.date_input("Datum wählen", datetime.date.today(), 
                                    min_value=datetime.date(1700, 1, 1), 
                                    max_value=datetime.date(2300, 12, 31))
        
        st.divider()
        
        st.subheader("2. Module")
        avail = get_available_modules()
        active_mods = st.multiselect("Aktivierte Systeme", options=avail, default=avail)
        
        st.divider()

        st.subheader("3. System-Kern")
        debug_mode = st.toggle("Ingenieur-Modus (Debug)", value=False)
        
        if st.button("♻️ RELOAD ALL"):
            st.cache_data.clear()
            st.rerun()

    # --- ENGINE ---
    with st.spinner("Lade Daten-Puls..."):
        pulse = GalacticCore.get_pulse(target_date)

    # --- RENDER PIPELINE ---
    for mod_name in active_mods:
        run_module_safely(mod_name, pulse, debug_mode)
        
    # --- PULSE INSPECTOR (Integriert!) ---
    # Das wolltest du sehen: Den nackten Puls.
    if debug_mode:
        st.markdown("---")
        st.subheader("🔍 Core Pulse Inspector")
        with st.expander("JSON Datenstrom ansehen (Raw Pulse)", expanded=True):
            st.json(pulse)

if __name__ == "__main__":
    main()
