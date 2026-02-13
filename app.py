import streamlit as st
import json
import datetime
import os
import glob
import importlib.util
import sys

# ==============================================================================
# 🧬 THE GALACTIC STATE PROTOCOL (Fixed & Verified)
# ==============================================================================
class GalacticState:
    """
    Der synaptische Koffer. 
    Hält ALLE Daten bereit und erlaubt Modulen, untereinander zu sprechen.
    """
    def __init__(self, kin, kin_data, db, date_obj, moon_data=None):
        self.kin = kin              # Das berechnete Kin (z.B. 66)
        self.data = kin_data        # JSON Daten für dieses Kin
        self.db = db                # Die ganze Datenbank
        self.date = date_obj        # Das Kalender-Datum
        self.moon = moon_data       # Die 13-Monde Daten (Neu!)
        self.memory = {}            # Der Speicher für Module

    def remember(self, key, value):
        self.memory[key] = value

    def recall(self, key):
        return self.memory.get(key, None)

# ==============================================================================
# ⚙️ SYSTEM CONFIG
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
# 🧮 BRAIN ENGINE (Mit Dreamspell-Logik!)
# ==============================================================================
class Brain:
    @staticmethod
    def calculate_kin_dreamspell(target_date):
        """
        Echte Dreamspell-Berechnung:
        Zählt ab einem Ankerpunkt, IGNORIERT aber den 29.02. (0.0.Hunab Ku).
        """
        # Anker: 26.07.2025 war KIN 73 (Gelber Solare Samen)
        # Wir können auch einen älteren Anker nehmen, aber der hier ist nah dran.
        anchor_date = datetime.date(2025, 7, 26)
        anchor_kin = 73
        
        # Ist das Datum der 29.02.? Dann ist es Kin 0.
        if target_date.month == 2 and target_date.day == 29:
            return 0

        # Wir iterieren Tag für Tag, um Schalt-Tage sicher zu überspringen
        # (Bei weiten Distanzen in die Vergangenheit wäre das langsam, aber für +/- 50 Jahre ist es okay)
        
        current_date = anchor_date
        current_kin = anchor_kin
        
        # Richtung bestimmen
        if target_date > anchor_date:
            step = datetime.timedelta(days=1)
            while current_date < target_date:
                current_date += step
                # Wenn wir auf den 29.02. treffen, zählen wir das Kin NICHT hoch!
                if current_date.month == 2 and current_date.day == 29:
                    continue
                current_kin = (current_kin % 260) + 1
        
        elif target_date < anchor_date:
            step = datetime.timedelta(days=-1)
            while current_date > target_date:
                # Zuerst Schritt zurück
                current_date += step
                # War der Tag, von dem wir kommen, ein 29.02.? (Wir gehen rückwärts!)
                if current_date.month == 2 and current_date.day == 29:
                    continue
                current_kin -= 1
                if current_kin <= 0: current_kin = 260

        return current_kin

    @staticmethod
    @st.cache_data
    def load_memory_banks():
        data = {'tzolkin': [], 'moon': []}
        try:
            with open("db_tzolkin_v21_enriched_FINAL.json", "r", encoding="utf-8") as f: 
                data['tzolkin'] = json.load(f)
        except: st.error("🚨 Tzolkin DB fehlt!")
        
        try:
            with open("db_13moon_v22_enriched_FINAL.json", "r", encoding="utf-8") as f: 
                data['moon'] = json.load(f)
        except: pass
        
        return data

# ==============================================================================
# 🚀 MAIN APP
# ==============================================================================
def main():
    with st.sidebar:
        st.header("⚙️ NAVIGATOR")
        d_input = st.date_input("Datum", datetime.date.today())
        st.caption("Core: Dreamspell Logic v2.2")

    st.title("GALAXY SYNC 2.1")

    # 1. DB LADEN
    db = Brain.load_memory_banks()
    if not db['tzolkin']: st.stop()

    # 2. KIN BERECHNEN (Jetzt richtig!)
    kin_today = Brain.calculate_kin_dreamspell(d_input)
    
    # 3. DATEN HOLEN
    current_kin_data = {}
    if kin_today > 0:
        # DB ist 0-indexed, Kin ist 1-indexed
        idx = kin_today - 1
        if 0 <= idx < len(db['tzolkin']):
            current_kin_data = db['tzolkin'][idx]
    
    # 4. 13-MOON DATEN HOLEN (Lookup)
    current_moon_data = {}
    search_key = d_input.strftime("%d.%m") # "13.02"
    for entry in db['moon']:
        if entry.get('date_gregorian') == search_key:
            current_moon_data = entry
            break

    # 5. STATE ERSTELLEN (Alles verpacken)
    state = GalacticState(kin_today, current_kin_data, db, d_input, current_moon_data)

    # 6. HEADER ANZEIGEN
    if kin_today == 0:
        st.info("🌌 0.0.Hunab Ku - Der Tag außerhalb der Zeit (29.02.)")
    elif current_kin_data:
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
            
        # Debug / Vertrauen schaffen
        if current_moon_data:
            m_name = current_moon_data.get('moon', {}).get('name', '?')
            m_day = current_moon_data.get('day_of_moon', '?')
            st.caption(f"📅 Synchronometer: {m_name}, Tag {m_day} | Psi-Chrono: {current_moon_data.get('psi_chrono', '-')}")

    # 7. MODULE STARTEN
    st.markdown("---")
    st.caption("🔌 AKTIVE MODULE (State Protocol)")

    module_files = glob.glob("mod_*.py")
    if not module_files: st.info("Keine Module gefunden.")

    for mod_file in module_files:
        mod_name = os.path.basename(mod_file).replace(".py", "")
        try:
            spec = importlib.util.spec_from_file_location(mod_name, mod_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = module
            spec.loader.exec_module(module)

            if hasattr(module, 'render'):
                with st.container():
                    try:
                        module.render(state) # Hier geht der State rein!
                    except Exception as e:
                        st.error(f"⚠️ {mod_name}: {e}")
        except Exception as e:
            st.error(f"Load Error {mod_file}: {e}")

if __name__ == "__main__":
    main()
