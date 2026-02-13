import streamlit as st
import json
import datetime
import os
import glob
import importlib.util
import sys

# ==============================================================================
# 🧬 PROTOKOLL: GALACTIC STATE (Der Speicher)
# ==============================================================================
class GalacticState:
    """
    Der zentrale Speicher.
    Hält das Kin, die Daten und erlaubt Modulen, Ergebnisse zu teilen.
    """
    def __init__(self, kin, kin_data, db, date_obj):
        self.kin = kin              # Das KORREKTE Kin (z.B. 66)
        self.data = kin_data        # Die Daten aus der DB für dieses Kin
        self.db = db                # Die ganze Datenbank (Tzolkin + Moon)
        self.date = date_obj        # Das gewählte Datum
        self.memory = {}            # Shared Memory für Module

    def remember(self, key, value):
        """Ein Modul schreibt hier rein."""
        self.memory[key] = value

    def recall(self, key):
        """Ein anderes Modul liest hier raus."""
        return self.memory.get(key, None)

# ==============================================================================
# ⚙️ SYSTEM CONFIG & CSS
# ==============================================================================
st.set_page_config(page_title="13:20 SYNC NODE", page_icon="🧬", layout="centered", initial_sidebar_state="collapsed")

def inject_css():
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

inject_css()

# ==============================================================================
# 🧮 BRAIN ENGINE (KORRIGIERT: Dreamspell Logik)
# ==============================================================================
class Brain:
    @staticmethod
    def count_leap_days(start_date, end_date):
        """Zählt, wie viele 29. Februare zwischen Start und Ende liegen."""
        leap_days = 0
        # Wir gehen durch die Jahre
        for year in range(start_date.year, end_date.year + 1):
            # Ist es ein Schaltjahr?
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                # Haben wir den 29.02. in diesem Jahr passiert?
                leap_date = datetime.date(year, 2, 29)
                if start_date <= leap_date <= end_date:
                    leap_days += 1
        return leap_days

    @staticmethod
    def calculate_kin_dreamspell(target_date):
        # 0. SONDERFALL: 29.02. ist immer 0.0.Hunab Ku
        if target_date.month == 2 and target_date.day == 29:
            return 0
            
        # 1. ANKER SETZEN (Bewährter Anker)
        # 26.07.2019 war KIN 14 (Weißer Magier). Das ist ein sicherer Startpunkt.
        anchor_date = datetime.date(2019, 7, 26)
        anchor_kin = 14
        
        # 2. TAGE ZÄHLEN (Gregorianisch)
        delta_days = (target_date - anchor_date).days
        
        # 3. SCHALTTAGE RAUSRECHNEN (Das war der Fehler!)
        # Wir müssen wissen, wie viele 29.02. dazwischen lagen.
        if target_date > anchor_date:
            leaps = Brain.count_leap_days(anchor_date, target_date)
            # Wir ziehen die Schalttage ab, da Dreamspell sie ignoriert
            dreamspell_days = delta_days - leaps
        else:
            # Rückwärts rechnen
            leaps = Brain.count_leap_days(target_date, anchor_date)
            dreamspell_days = delta_days + leaps # Delta ist hier negativ, also addieren wir quasi

        # 4. MODULO RECHNEN
        kin_calc = (anchor_kin + dreamspell_days) % 260
        
        # Korrektur für Modulo 0
        while kin_calc <= 0: kin_calc += 260
        while kin_calc > 260: kin_calc -= 260
            
        return kin_calc

    @staticmethod
    @st.cache_data
    def load_db():
        data = {'tzolkin': [], 'moon': []}
        try:
            with open("db_tzolkin_v21_enriched_FINAL.json", "r", encoding="utf-8") as f: 
                data['tzolkin'] = json.load(f)
        except: pass
        try:
            with open("db_13moon_v22_enriched_FINAL.json", "r", encoding="utf-8") as f: 
                data['moon'] = json.load(f)
        except: pass
        return data

# ==============================================================================
# 🚀 MAIN APP LOOP
# ==============================================================================
def main():
    # 1. UI SIDEBAR
    with st.sidebar:
        st.header("⚙️ NAVIGATOR")
        d_input = st.date_input("Datum", datetime.date.today())
        st.caption("Engine: Dreamspell V2.4 (Leap-Skip)")

    st.title("GALAXY SYNC 2.1")

    # 2. DATENBANK LADEN
    db = Brain.load_db()
    if not db['tzolkin']:
        st.error("🚨 FEHLER: Datenbank nicht gefunden. Bitte JSON hochladen.")
        st.stop()

    # 3. KIN BERECHNEN (Jetzt korrekt!)
    kin_today = Brain.calculate_kin_dreamspell(d_input)

    # 4. DATEN FÜR HEUTE HOLEN
    current_kin_data = {}
    if kin_today > 0:
        current_kin_data = db['tzolkin'][kin_today - 1]

    # 5. STATE INITIALISIEREN (Synaptic Protocol)
    state = GalacticState(kin_today, current_kin_data, db, d_input)

    # 6. HEADER RENDERN (Native)
    if kin_today == 0:
        st.info("🌌 0.0.Hunab Ku - Der Tag außerhalb der Zeit")
    elif current_kin_data:
        id_dat = current_kin_data.get('identity', {})
        seal = id_dat.get('seal', {})
        tone = id_dat.get('tone', {})
        
        css = {"Rot": "border-rot", "Weiss": "border-weiss", "Blau": "border-blau", "Gelb": "border-gelb", "Grün": "border-gruen"}.get(seal.get('color'), "border-weiss")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="glass-card {css}"><div class="small-label">KIN {kin_today}</div><div class="big-value">{id_dat.get("name")}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="glass-card"><div class="small-label">TON {tone.get("id")}</div><div class="big-value">{tone.get("name")}</div></div>', unsafe_allow_html=True)

    # 7. MODULE LADEN UND AUSFÜHREN
    st.markdown("---")
    st.caption("🔌 SYNAPTIC MODULES")
    
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
                    # Hier übergeben wir nur den STATE!
                    module.render(state)
        except Exception as e:
            st.error(f"Fehler in {mod_name}: {e}")

if __name__ == "__main__":
    main()
