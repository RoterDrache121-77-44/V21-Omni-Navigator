import streamlit as st
import json
import datetime
import sys
import os
import glob
import importlib.util

# ==============================================================================
# 🌌 CONFIG & GLOBAL SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="13:20 SYNC NODE", 
    page_icon="🧬", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

def inject_global_css():
    st.markdown("""
    <style>
        /* Deep Space Background */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 100%);
            color: #E0E0E0; 
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 10, 15, 0.9);
            border-right: 1px solid rgba(255,255,255,0.1);
        }

        /* Global Expander Haptic Feedback */
        .streamlit-expanderHeader {
            background-color: rgba(20, 20, 30, 0.8) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: all 0.2s ease;
        }
        .streamlit-expanderHeader:hover { transform: scale(1.01); z-index: 10; }
        .streamlit-expanderHeader:active { transform: scale(0.99); }
        
        /* Inputs */
        .stDateInput input {
            background-color: rgba(255,255,255,0.1) !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 📐 MATH ENGINE (Core Logic)
# ==============================================================================
class MathEngine:
    ANCHOR_DATE = datetime.date(1986, 5, 19) # Kin 121
    ANCHOR_KIN = 121

    @staticmethod
    def calculate_kin(day, month, year):
        # 1. Hunab Ku Check (Schalttag)
        if month == 2 and day == 29: 
            return 0 
            
        target = datetime.date(year, month, day)
        current = MathEngine.ANCHOR_DATE
        days_diff = 0
        
        # Performance-Optimierung für große Zeiträume wäre möglich, 
        # aber wir bleiben bei der sicheren Iteration, um den 29.02. sauber zu skippen.
        # Bei Jahr 1 bis 5000 kann das kurz dauern, ist aber präzise.
        
        if target >= current:
            # Zukunft
            while current < target:
                current += datetime.timedelta(days=1)
                if not (current.month == 2 and current.day == 29):
                    days_diff += 1
            return (MathEngine.ANCHOR_KIN + days_diff - 1) % 260 + 1
        else:
            # Vergangenheit
            while current > target:
                current -= datetime.timedelta(days=1)
                if not (current.month == 2 and current.day == 29):
                    days_diff += 1
            return (MathEngine.ANCHOR_KIN - days_diff - 1) % 260 + 1

# ==============================================================================
# 💾 DATA & MODULE LOADER
# ==============================================================================
@st.cache_data
def load_db():
    """Lädt die Tzolkin-Datenbank."""
    db_path = 'db_tzolkin_v21_enriched_FINAL.json'
    if not os.path.exists(db_path):
        return None
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"DB Error: {e}")
        return None

def get_modules():
    """
    Scannt das Verzeichnis nach Dateien, die mit 'mod_' beginnen.
    Gibt eine Liste von Modul-Namen zurück (ohne .py).
    """
    files = glob.glob("mod_*.py")
    # Wir sortieren sie alphabetisch. 
    # Tipp: Wenn du eine Reihenfolge willst, benenne sie mod_01_..., mod_02_...
    files.sort()
    
    modules = []
    for f in files:
        mod_name = os.path.basename(f)[:-3] # .py entfernen
        modules.append(mod_name)
    return modules

def import_and_render_module(mod_name, kin_nr, data_entry):
    """
    Importiert ein Modul dynamisch und führt die render() Funktion aus.
    """
    try:
        # Dynamischer Import
        if mod_name in sys.modules:
            module = sys.modules[mod_name]
            importlib.reload(module) # Reload für Live-Coding Updates
        else:
            module = importlib.import_module(mod_name)
            
        # Check ob render existiert
        if hasattr(module, 'render'):
            # Ausführen und Daten zurückbekommen
            return module.render(kin_nr, data_entry)
        else:
            st.warning(f"⚠️ Modul '{mod_name}' hat keine render() Funktion.")
            return {}
            
    except Exception as e:
        st.error(f"🔥 Fehler im Modul '{mod_name}': {e}")
        return {}

# ==============================================================================
# 🚀 MAIN CONTROLLER
# ==============================================================================
def main():
    inject_global_css()
    
    # 1. SIDEBAR INPUT
    with st.sidebar:
        st.title("⚙️ KONSOLE")
        st.markdown("---")
        
        # Datumswähler mit erweitertem Bereich (Jahr 1 bis 5000)
        d_input = st.date_input(
            "Datum wählen", 
            datetime.date.today(),
            min_value=datetime.date(1, 1, 1),
            max_value=datetime.date(5000, 12, 31)
        )
        
        st.caption(f"Gewählt: {d_input.strftime('%d.%m.%Y')}")
        st.markdown("---")
        st.info("System Status: Online 🟢")

    # 2. LOGIC CORE
    st.title("GALAXY SYNC 2.1")
    
    db = load_db()
    if not db:
        st.error("🚨 Datenbank 'db_tzolkin_v21_enriched_FINAL.json' nicht gefunden!")
        st.stop()

    # Kin Berechnung
    with st.spinner("Berechne Zeit-Vektor..."):
        kin_today = MathEngine.calculate_kin(d_input.day, d_input.month, d_input.year)
    
    # Daten Fetch
    kin_data = None
    if kin_today > 0:
        # Array Index ist Kin - 1
        kin_data = db[kin_today - 1]

    # 3. DYNAMIC MODULE RENDERING
    export_stack = {}
    
    # Scanner starten
    module_list = get_modules()
    
    if not module_list:
        st.warning("Keine Module (mod_*.py) gefunden. Bitte Module hochladen.")
    
    # Jedes Modul rendern
    for mod_name in module_list:
        # Container für sauberen Abstand
        st.markdown(f"", unsafe_allow_html=True)
        
        # Modul ausführen
        result_data = import_and_render_module(mod_name, kin_today, kin_data)
        
        # Daten sammeln (wenn das Modul Daten liefert)
        if result_data:
            export_stack[mod_name] = result_data

    # 4. EXPORT CHECK (Optional für Developer)
    # with st.sidebar.expander("🛠️ Data Export Check"):
    #     st.json(export_stack)

if __name__ == "__main__":
    main()
