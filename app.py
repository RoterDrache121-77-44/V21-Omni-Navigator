# ==============================================================================
# 🛸 V21 HOST SYSTEM (Pro Infrastructure)
# ------------------------------------------------------------------------------
# ZWECK:    High-End Container für galaktische Module.
# FEATURE:  Hot-Reload, Error-Containment, Performance-Metriken, Sci-Fi UI.
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
        /* --- FONTS IMPORTIEREN --- */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

        /* --- GLOBAL THEME --- */
        .stApp {
            background: radial-gradient(circle at 50% 10%, #1a1a2e 0%, #000000 90%);
            color: #E0E0E0;
            font-family: 'Rajdhani', sans-serif;
        }

        /* --- HEADINGS --- */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 2px;
            color: #fff;
            text-shadow: 0 0 10px rgba(255,255,255,0.2);
        }

        /* --- SIDEBAR STYLE --- */
        [data-testid="stSidebar"] {
            background-color: #0b0b10;
            border-right: 1px solid #333;
        }

        /* --- CONTAINER STYLE (Standard für Module) --- */
        .glass-container {
            background: rgba(15, 15, 20, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            backdrop-filter: blur(15px);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .glass-container:hover {
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 15px rgba(42, 140, 255, 0.1);
        }

        /* --- UTILS --- */
        .debug-info { font-family: monospace; font-size: 0.7rem; color: #555; }
        .error-box { border: 1px solid #ff4b4b; background: rgba(50,0,0,0.5); padding: 10px; border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)

# 3. MODUL MANAGER (Die Infrastruktur)
def get_available_modules():
    """Scannt den Ordner und gibt saubere Namen zurück."""
    if not os.path.exists("modules"):
        os.makedirs("modules")
        return []
    
    files = [f[:-3] for f in os.listdir("modules") if f.startswith("mod_") and f.endswith(".py")]
    # Sortierung: Header immer zuerst, wenn vorhanden
    if "mod_header" in files:
        files.remove("mod_header")
        files.insert(0, "mod_header")
    return files

def run_module_safely(mod_name, pulse, debug_mode):
    """Führt ein Modul in einer isolierten Sandbox aus."""
    placeholder = st.empty()
    
    try:
        # Performance Tracking Start
        start_time = time.time()
        
        # 1. Import / Reload
        module_path = f"modules.{mod_name}"
        
        if module_path in sys.modules:
            module = importlib.import_module(module_path)
            importlib.reload(module) # Hot-Reload für Live-Coding!
        else:
            module = importlib.import_module(module_path)
        
        # 2. Render Check
        if hasattr(module, "render"):
            # Der Render-Aufruf
            module.render(pulse)
            
            # Performance Tracking Ende
            duration = (time.time() - start_time) * 1000
            if debug_mode:
                st.markdown(f"<div class='debug-info'>[SYS] {mod_name} geladen in {duration:.1f}ms</div>", unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ Modul '{mod_name}' hat keine render()-Funktion.")

    except Exception as e:
        # Crash Containment: Zeige den Fehler schön an, statt App-Crash
        st.markdown(f"""
            <div class='glass-container error-box'>
                <h4 style='color:#ff4b4b'>💥 System Failure: {mod_name}</h4>
                <p>{str(e)}</p>
            </div>
        """, unsafe_allow_html=True)
        if debug_mode:
            st.exception(e)

# ------------------------------------------------------------------------------
# 4. MAIN COCKPIT
# ------------------------------------------------------------------------------
def main():
    inject_advanced_css()

    # --- SIDEBAR: MISSION CONTROL ---
    with st.sidebar:
        st.header("🛸 V21 MISSION CONTROL")
        
        # A. Navigation
        st.subheader("1. Zeit-Koordinate")
        target_date = st.date_input(
            "Datumssprung", 
            datetime.date.today(),
            min_value=datetime.date(1700, 1, 1),
            max_value=datetime.date(2300, 12, 31)
        )
        
        st.divider()
        
        # B. Modul Sequencer
        st.subheader("2. Modul-Sequenz")
        available_mods = get_available_modules()
        
        if not available_mods:
            st.error("Keine Module in /modules gefunden!")
        
        active_mods = st.multiselect(
            "Systeme aktivieren", 
            options=available_mods, 
            default=available_mods
        )
        
        st.divider()

        # C. System Diagnostics
        st.subheader("3. Core Diagnostics")
        debug_mode = st.toggle("Ingenieur-Modus (Debug)", value=False)
        
        if st.button("♻️ CACHE LEEREN & RELOAD"):
            st.cache_data.clear()
            st.rerun()

        # Footer
        st.divider()
        st.caption("Hunab Ku 21 | Version Alpha 1.5 Pro")

    # --- ENGINE START ---
    # Ladeanimation nur wenn nicht gecached
    with st.spinner("Synchronisiere mit Noosphäre..."):
        pulse = GalacticCore.get_pulse(target_date)

    # --- DATA INJECTION (Optionaler Header im Debug Mode) ---
    if debug_mode:
        st.info(f"🧬 KIN {pulse['metadata']['kin']} | PSI {pulse['moon'].get('psi_chrono', '?')} | {pulse['metadata']['date_str']}")

    # --- RENDER PIPELINE ---
    # Hier laufen die Module durch die Sicherheits-Schleuse
    for mod_name in active_mods:
        run_module_safely(mod_name, pulse, debug_mode)

if __name__ == "__main__":
    main()
