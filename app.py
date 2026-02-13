import streamlit as st
import json
import datetime
import os
import glob
import importlib.util
import sys

# ==============================================================================
# 🧬 DIE MONUMENTALE LÖSUNG: THE GALACTIC STATE
# ==============================================================================
class GalacticState:
    """
    Das Synaptische Nervensystem der App.
    Es hält ALLE Wahrheiten bereit. Jedes Modul bekommt Zugriff hierauf.
    """
    def __init__(self, kin, kin_data, db, date_obj):
        # 1. Die Harten Fakten (Read-Only empfohlen)
        self.kin = kin              # Das heutige Kin (int)
        self.data = kin_data        # Das JSON-Objekt des heutigen Tages
        self.db = db                # Die GESAMTE Datenbank (Tzolkin + Moon)
        self.date = date_obj        # Das Kalender-Datum
        
        # 2. Der Synaptische Speicher (Read/Write)
        # Hier können Module ihre Ergebnisse ablegen, damit andere sie nutzen können.
        self.memory = {} 

    def remember(self, key, value):
        """Ein Modul speichert hier sein Ergebnis."""
        self.memory[key] = value

    def recall(self, key):
        """Ein anderes Modul ruft das Ergebnis ab."""
        return self.memory.get(key, None)

# ==============================================================================
# 🎨 DESIGN & CONFIG
# ==============================================================================
st.set_page_config(page_title="13:20 SYNC NODE", page_icon="🧬", layout="centered", initial_sidebar_state="collapsed")

def inject_global_css():
    st.markdown("""
    <style>
        .stApp { background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 100%); color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
        .glass-card { background: rgba(20, 20, 30, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); backdrop-filter: blur(10px); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .border-rot { border-left: 4px solid #FF3E3E; } .border-weiss { border-left: 4px solid #E0E0E0; }
        .border-blau { border-left: 4px solid #2A8CFF; } .border-gelb { border-left: 4px solid #FFD700; } .border-gruen { border-left: 4px solid #00FF66; }
        h1, h2 { color: #FFF; font-weight: 300; letter-spacing: 2px; }
        .big-value { font-size: 1.8rem; font-weight: bold; color: #FFF; }
        .small-label { font-size: 0.8rem; color: #888; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

inject_global_css()

# ==============================================================================
# 🧮 INTERNE LOGIK (MATH & DB) - DIREKT IN DER APP
# ==============================================================================
class Brain:
    @staticmethod
    def calculate_kin(day, month, year):
        try:
            anchor = datetime.date(1986, 5, 19) # Kin 121
            target = datetime.date(year, month, day)
            if month == 2 and day == 29: return 0
            delta = (target - anchor).days
            kin = (121 + delta) % 260
            return 260 if kin == 0 else kin
        except: return 0

    @staticmethod
    @st.cache_data
    def load_memory_banks():
        data = {'tzolkin': [], 'moon': []}
        try:
            with open("db_tzolkin_v21_enriched_FINAL.json", "r", encoding="utf-8") as f: 
                data['tzolkin'] = json.load(f)
        except FileNotFoundError: st.error("🚨 Tzolkin DB fehlt!")
        
        try:
            with open("db_13moon_v22_enriched_FINAL.json", "r", encoding="utf-8") as f: 
                data['moon'] = json.load(f)
        except: pass
        return data

# ==============================================================================
# 🚀 HAUPT-PROGRAMM
# ==============================================================================
def main():
    # 1. UI INPUT
    with st.sidebar:
        st.header("⚙️ NAVIGATOR")
        d_input = st.date_input("Datum", datetime.date.today())
        st.caption("Architecture: Synaptic State")

    st.title("GALAXY SYNC 2.1")

    # 2. INTELLIGENZ STARTEN (Berechnen & Laden)
    db = Brain.load_memory_banks()
    if not db['tzolkin']: st.stop()

    kin_today = Brain.calculate_kin(d_input.day, d_input.month, d_input.year)
    
    current_kin_data = {}
    if kin_today > 0:
        current_kin_data = db['tzolkin'][kin_today - 1]

    # 3. DAS "LEBEN" ERSCHAFFEN (State Object)
    # Hier bündeln wir ALLE Intelligenz in ein Objekt
    state = GalacticState(kin_today, current_kin_data, db, d_input)

    # 4. STANDARD HEADER (App zeigt das Wichtigste selbst an)
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
    else:
        st.info("🌌 0.0.Hunab Ku - Der Tag außerhalb der Zeit")

    # 5. DIE MODULE AKTIVIEREN (The Synapse Loop)
    st.markdown("---")
    st.caption("🔌 SYNAPTISCHE MODULE")

    module_files = glob.glob("mod_*.py")
    if not module_files: st.info("Keine Module installiert.")

    for mod_file in module_files:
        mod_name = os.path.basename(mod_file).replace(".py", "")
        
        try:
            # Importieren
            spec = importlib.util.spec_from_file_location(mod_name, mod_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = module
            spec.loader.exec_module(module)

            # DIE GOLDENE REGEL: Wir übergeben nur noch 'state'
            if hasattr(module, 'render'):
                with st.container():
                    try:
                        # Modul ausführen
                        module.render(state)
                        
                    except Exception as e:
                        st.error(f"⚠️ {mod_name} Fehler: {e}")
        
        except Exception as e:
            st.error(f"Ladefehler bei {mod_file}: {e}")

if __name__ == "__main__":
    main()
