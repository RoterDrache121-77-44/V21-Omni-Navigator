import streamlit as st
import json
import datetime
import os
import glob
import importlib.util
import sys

# ==============================================================================
# 🧠 ARCHITEKTUR-CORE: THE CONTEXT PATTERN
# ==============================================================================
class ModuleContext:
    """
    Der 'Koffer', der alle Daten sicher an die Module trägt.
    Ersetzt die fehleranfällige Einzel-Argument-Übergabe.
    """
    def __init__(self, kin_nr, kin_data, db, date_obj):
        self.kin = kin_nr           # Die Nummer (int)
        self.data = kin_data        # Die Daten des Tages (dict)
        self.db = db                # Die ganze Datenbank (dict)
        self.date = date_obj        # Das Datum (date object)
        self.shared_storage = {}    # Speicher für Kommunikation zwischen Modulen
    
    def set(self, key, value):
        self.shared_storage[key] = value
    
    def get(self, key, default=None):
        return self.shared_storage.get(key, default)

# ==============================================================================
# 🌌 KONFIGURATION & DESIGN
# ==============================================================================
st.set_page_config(page_title="13:20 SYNC NODE", page_icon="🧬", layout="centered", initial_sidebar_state="collapsed")

def inject_global_css():
    st.markdown("""
    <style>
        .stApp { background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 100%); color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
        .glass-card { background: rgba(20, 20, 30, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); backdrop-filter: blur(10px); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .border-rot { border-left: 4px solid #FF3E3E; } .border-weiss { border-left: 4px solid #E0E0E0; }
        .border-blau { border-left: 4px solid #2A8CFF; } .border-gelb { border-left: 4px solid #FFD700; } .border-gruen { border-left: 4px solid #00FF66; }
        h1, h2, h3 { color: #FFFFFF; font-weight: 300; letter-spacing: 1.5px; }
        .big-value { font-size: 1.5rem; font-weight: bold; color: #FFF; }
        .small-label { font-size: 0.8rem; color: #888; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

inject_global_css()

# ==============================================================================
# 🧮 LOGIC ENGINES
# ==============================================================================
class MathEngine:
    @staticmethod
    def calculate_kin(day, month, year):
        try:
            anchor = datetime.date(1986, 5, 19) # Kin 121
            target = datetime.date(year, month, day)
            if month == 2 and day == 29: return 0
            delta = (target - anchor).days
            kin = (121 + delta) % 260
            return 260 if kin == 0 else kin
        except ValueError: return 0

@st.cache_data
def load_databases():
    data = {'tzolkin': [], 'moon': []}
    try:
        with open("db_tzolkin_v21_enriched_FINAL.json", "r", encoding="utf-8") as f: data['tzolkin'] = json.load(f)
    except: pass
    try:
        with open("db_13moon_v22_enriched_FINAL.json", "r", encoding="utf-8") as f: data['moon'] = json.load(f)
    except: pass
    return data

# ==============================================================================
# 🚀 MAIN APPLICATION
# ==============================================================================
def main():
    with st.sidebar:
        st.header("⚙️ NAVIGATOR")
        d_input = st.date_input("Datum", datetime.date.today())
        st.caption("Architecture: Context-Pattern")

    st.title("GALAXY SYNC 2.1")
    
    # 1. Init Data
    db = load_databases()
    if not db['tzolkin']: st.stop()

    # 2. Compute Kin
    kin_today = MathEngine.calculate_kin(d_input.day, d_input.month, d_input.year)
    current_kin_data = {}
    if kin_today > 0 and (kin_today - 1) < len(db['tzolkin']):
        current_kin_data = db['tzolkin'][kin_today - 1]

    # 3. KIN HEADER (Native UI)
    if current_kin_data:
        id_dat = current_kin_data.get('identity', {})
        seal = id_dat.get('seal', {})
        tone = id_dat.get('tone', {})
        color_map = {"Rot": "border-rot", "Weiss": "border-weiss", "Blau": "border-blau", "Gelb": "border-gelb", "Grün": "border-gruen"}
        css = color_map.get(seal.get('color'), "border-weiss")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="glass-card {css}"><div class="small-label">KIN {kin_today}</div><div class="big-value">{id_dat.get("name")}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="glass-card"><div class="small-label">TON {tone.get("id")}</div><div class="big-value">{tone.get("name")}</div></div>', unsafe_allow_html=True)

    # ==========================================================================
    # 🔌 THE MODULE LOOP (CONTEXT POWERED)
    # ==========================================================================
    st.markdown("---")
    st.caption("🔌 AKTIVE MODULE")

    # 4. Context erstellen (Der Koffer wird gepackt)
    ctx = ModuleContext(kin_today, current_kin_data, db, d_input)

    module_files = glob.glob("mod_*.py")
    if not module_files: st.info("Keine Module gefunden.")

    for mod_file in module_files:
        mod_name = os.path.basename(mod_file).replace(".py", "")
        try:
            # Import
            spec = importlib.util.spec_from_file_location(mod_name, mod_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = module
            spec.loader.exec_module(module)

            # Render mit Context!
            if hasattr(module, 'render'):
                with st.container():
                    try:
                        # HIER PASSIERT DIE MAGIE: Nur noch 1 Argument!
                        result = module.render(ctx)
                        
                        # Ergebnis im Context speichern für nachfolgende Module
                        if result:
                            ctx.set(mod_name, result)
                            
                    except Exception as e:
                        st.error(f"⚠️ Fehler im Modul '{mod_name}': {e}")
        except Exception as e:
            st.error(f"Ladefehler {mod_file}: {e}")

if __name__ == "__main__":
    main()
