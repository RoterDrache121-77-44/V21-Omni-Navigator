import streamlit as st
import json
import datetime
import sys
import os
import glob
import importlib.util
import inspect # <--- DAS IST DAS WERKZEUG FÜR INTELLIGENZ

# ==============================================================================
# 🌌 CONFIG
# ==============================================================================
st.set_page_config(page_title="13:20 SYNC NODE", page_icon="🧬", layout="centered", initial_sidebar_state="collapsed")

def inject_global_css():
    st.markdown("""
    <style>
        .stApp { background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 100%); color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
        [data-testid="stSidebar"] { background-color: rgba(10, 10, 15, 0.9); border-right: 1px solid rgba(255,255,255,0.1); }
        .streamlit-expanderHeader { background-color: rgba(20, 20, 30, 0.8) !important; border-radius: 8px !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; transition: all 0.2s ease; }
        .streamlit-expanderHeader:hover { transform: scale(1.01); z-index: 10; }
        .stDateInput input { background-color: rgba(255,255,255,0.1) !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 📐 MATH ENGINE
# ==============================================================================
class MathEngine:
    ANCHOR_DATE = datetime.date(1986, 5, 19) # Kin 121
    ANCHOR_KIN = 121
    @staticmethod
    def calculate_kin(day, month, year):
        if month == 2 and day == 29: return 0 
        target = datetime.date(year, month, day)
        current = MathEngine.ANCHOR_DATE
        days_diff = 0
        if target >= current:
            while current < target:
                current += datetime.timedelta(days=1)
                if not (current.month == 2 and current.day == 29): days_diff += 1
            return (MathEngine.ANCHOR_KIN + days_diff - 1) % 260 + 1
        else:
            while current > target:
                current -= datetime.timedelta(days=1)
                if not (current.month == 2 and current.day == 29): days_diff += 1
            return (MathEngine.ANCHOR_KIN - days_diff - 1) % 260 + 1

# ==============================================================================
# 💾 SMART LOADER
# ==============================================================================
@st.cache_data
def load_db():
    try:
        with open('db_tzolkin_v21_enriched_FINAL.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

def get_modules():
    files = glob.glob("mod_*.py")
    files.sort()
    return [os.path.basename(f)[:-3] for f in files]

def import_and_render_module(mod_name, kin_nr, kin_data, full_db, date_obj):
    """
    Intelligenter Adapter: Analysiert, was das Modul braucht, und liefert genau das.
    """
    try:
        if mod_name in sys.modules:
            module = sys.modules[mod_name]
            importlib.reload(module)
        else:
            module = importlib.import_module(mod_name)
            
        if hasattr(module, 'render'):
            # 🕵️ INSPEKTION: Was will die Funktion wissen?
            sig = inspect.signature(module.render)
            params = sig.parameters
            
            # Wir bauen das Argumenten-Paket zusammen
            kwargs = {}
            
            # MAPPING: Mögliche Parameternamen -> Unsere Variablen
            available_vars = {
                'kin_nr': kin_nr, 'kin': kin_nr, 'k_nr': kin_nr,
                'data': kin_data, 'data_entry': kin_data, 'kin_data': kin_data,
                'db': full_db, 'database': full_db, 'db_tzolkin': full_db, 'db_tz': full_db,
                'date_obj': date_obj, 'date': date_obj, 'd_input': date_obj, 'd_in': date_obj
            }
            
            for param_name in params:
                if param_name in available_vars:
                    kwargs[param_name] = available_vars[param_name]
                elif params[param_name].default == inspect.Parameter.empty:
                    # Wenn ein Parameter Pflicht ist, wir ihn aber nicht kennen -> Warnung
                    st.warning(f"⚠️ Modul '{mod_name}' verlangt unbekannten Parameter: '{param_name}'")
                    return {}

            # Aufruf mit den passenden Argumenten
            return module.render(**kwargs)
            
        else:
            st.warning(f"⚠️ Modul '{mod_name}' hat keine render() Funktion.")
            return {}
            
    except Exception as e:
        st.error(f"🔥 Fehler im Modul '{mod_name}': {e}")
        return {}

# ==============================================================================
# 🚀 MAIN
# ==============================================================================
def main():
    inject_global_css()
    
    with st.sidebar:
        st.title("⚙️ KONSOLE")
        d_input = st.date_input("Datum", datetime.date.today(), min_value=datetime.date(1, 1, 1), max_value=datetime.date(5000, 12, 31))
        st.caption(f"{d_input.strftime('%d.%m.%Y')}")

    st.title("GALAXY SYNC 2.1")
    
    db = load_db()
    if not db: st.error("DB fehlt!"); st.stop()

    kin_today = MathEngine.calculate_kin(d_input.day, d_input.month, d_input.year)
    kin_data = db[kin_today - 1] if kin_today > 0 else None

    # MODULE RENDERN
    module_list = get_modules()
    for mod_name in module_list:
        st.markdown(f"", unsafe_allow_html=True)
        # Wir übergeben ALLES an den Adapter, er sortiert es aus.
        import_and_render_module(mod_name, kin_today, kin_data, db, d_input)

if __name__ == "__main__":
    main()
