import streamlit as st
import json
import datetime
import os
import importlib.util
import sys

# ==============================================================================
# 1. DAS GEHIRN (MathEngine & DB) - Bleibt fest im Kern
# ==============================================================================
class MathEngine:
    ANCHOR_DATE = datetime.date(1986, 5, 19)
    ANCHOR_KIN = 121
    @staticmethod
    def get_kin(d, m, y):
        if m == 2 and d == 29: return 0
        try:
            target = datetime.date(y, m, d)
            current = MathEngine.ANCHOR_DATE
            days = 0
            if target >= current:
                while current < target:
                    if not (current.month == 2 and current.day == 29): days += 1
                    current += datetime.timedelta(days=1)
                return (MathEngine.ANCHOR_KIN + days - 1) % 260 + 1
            else:
                while current > target:
                    current -= datetime.timedelta(days=1)
                    if not (current.month == 2 and current.day == 29): days += 1
                return (MathEngine.ANCHOR_KIN - days - 1) % 260 + 1
        except: return 1

@st.cache_data
def load_db():
    files = [f for f in os.listdir('.') if f.endswith('.json')]
    target = 'db_tzolkin_v21_enriched_FINAL.json'
    path = target if target in files else (files[0] if files else None)
    if not path: return None
    try:
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    except: return None

DB_TZ = load_db()

def get_base_data(kin):
    if kin <= 0 or not DB_TZ: return None
    return next((k for k in DB_TZ if k.get('kin') == kin), None)

# ==============================================================================
# 2. DIE PLUGIN-LOGIK (Der "Suchtrupp")
# ==============================================================================
def load_modules():
    """Scannt das Verzeichnis nach Dateien, die mit 'mod_' beginnen."""
    modules = {}
    # Wir suchen im aktuellen Ordner
    files = [f for f in os.listdir('.') if f.startswith('mod_') and f.endswith('.py')]
    
    for filename in files:
        module_name = filename[:-3] # .py entfernen
        try:
            spec = importlib.util.spec_from_file_location(module_name, filename)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)
            
            # Check: Hat das Modul die nötigen Funktionen?
            if hasattr(mod, 'get_name') and hasattr(mod, 'render'):
                # Erfolgreich geladen
                display_name = mod.get_name()
                modules[module_name] = {"name": display_name, "ref": mod}
        except Exception as e:
            st.sidebar.error(f"Fehler beim Laden von {filename}: {e}")
            
    return modules

# ==============================================================================
# 3. UI SETUP (Globales Design)
# ==============================================================================
st.set_page_config(page_title="V21 MAINBOARD", layout="wide", page_icon="🛸")

st.markdown("""
    <style>
    /* Globaler Darkmode & Font */
    .stApp { background-color: #000000; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
    
    /* Die Standard Glow-Box (Module können das nutzen) */
    .glow-box { 
        background: #111; border: 1px solid #333; padding: 15px; 
        border-radius: 12px; text-align: center; margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Farb-Klassen für CSS Injektion */
    .Rot { border-left: 4px solid #FF3E3E; }
    .Weiß { border-left: 4px solid #FFFFFF; }
    .Blau { border-left: 4px solid #3E8EFF; }
    .Gelb { border-left: 4px solid #FFD700; }
    
    h1, h2, h3 { color: #fff; font-weight: 300; }
    .highlight { color: #00FFA3; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. MAIN PROGRAMM
# ==============================================================================

# A. Header & Kontrolle
with st.sidebar:
    st.header("🛸 V21 SYSTEM")
    d_in = st.date_input("Zeit-Vektor:", datetime.date.today())
    kin_nr = MathEngine.get_kin(d_in.day, d_in.month, d_in.year)
    
    st.divider()
    st.caption("MODULE MANAGER")
    
    # B. Suchtrupp losschicken
    available_modules = load_modules()
    active_modules = []
    
    if not available_modules:
        st.warning("Keine Module gefunden! Lade Dateien hoch, die mit 'mod_' beginnen.")
    else:
        # Erstelle Checkboxen für jedes gefundene Modul
        for mod_key, info in available_modules.items():
            # Standardmäßig aktiviert
            if st.checkbox(info['name'], value=True, key=mod_key):
                active_modules.append(info['ref'])

# C. Rendering (Der unendliche Stream)
if DB_TZ is None:
    st.error("⚠️ Datenbank fehlt (JSON).")
    st.stop()

if kin_nr == 0:
    st.title("🟢 HUNAB KU")
    st.write("Tag außerhalb der Zeit")
else:
    # Basis Daten holen
    full_data = get_base_data(kin_nr)
    
    if full_data:
        # Titel
        kin_name = full_data['identity']['name']
        st.markdown(f"<h1 style='text-align:center;'>KIN {kin_nr} <span style='color:#666'>|</span> {kin_name}</h1>", unsafe_allow_html=True)
        
        # Gap Check
        if full_data.get('time', {}).get('gap'):
             st.markdown("<div style='text-align:center; color:#00FFA3; letter-spacing:4px; margin-bottom:20px;'>⚡ GALAKTISCHES PORTAL ⚡</div>", unsafe_allow_html=True)

        # D. Module abfeuern
        for module in active_modules:
            try:
                # Wir rufen die render() Funktion des Moduls auf
                # Wir übergeben: Die Kin-Nummer, das volle Daten-Objekt und die Datenbank
                module.render(kin_nr, full_data, DB_TZ)
                
                # Abstand zwischen Modulen
                st.markdown("---") 
            except Exception as e:
                st.error(f"Fehler im Modul '{module.get_name()}': {e}")
    else:
        st.error("Kin Daten nicht gefunden.")
