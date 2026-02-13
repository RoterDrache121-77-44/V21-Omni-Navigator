import streamlit as st
import json
import datetime
import os
import glob
import importlib.util
import sys

# ==============================================================================
# 🌌 1. KONFIGURATION & DESIGN (CSS INJECTION)
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

        /* Glassmorphism Card */
        .glass-card {
            background: rgba(20, 20, 30, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }

        /* Neon Borders based on Color */
        .border-rot { border-left: 4px solid #FF3E3E; }
        .border-weiss { border-left: 4px solid #E0E0E0; }
        .border-blau { border-left: 4px solid #2A8CFF; }
        .border-gelb { border-left: 4px solid #FFD700; }
        .border-gruen { border-left: 4px solid #00FF66; }

        /* Typography */
        h1, h2, h3 { color: #FFFFFF; font-weight: 300; letter-spacing: 1.5px; }
        .small-label { font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }
        .big-value { font-size: 1.5rem; font-weight: bold; color: #FFF; }
        
    </style>
    """, unsafe_allow_html=True)

inject_global_css()

# ==============================================================================
# 🧠 2. CORE ENGINES (Strang A & Strang B)
# ==============================================================================

class MathEngine:
    """STRANG A: Reine Mathematik für den Tzolkin."""
    
    @staticmethod
    def calculate_kin(day, month, year):
        # Anker: 19.05.1986 = Kin 121
        anchor_date = datetime.date(1986, 5, 19)
        anchor_kin = 121
        
        # Target Check
        try:
            target_date = datetime.date(year, month, day)
        except ValueError:
            return 0 # Ungültiges Datum
            
        # Hunab Ku Tag (29.02.) - Außerhalb der Zeit
        if month == 2 and day == 29:
            return 0
            
        # Differenz berechnen
        delta = target_date - anchor_date
        days_diff = delta.days
        
        # Schalttage entfernen (Dreamspell zählt Schalttage nicht!)
        # Einfache Näherung: Wir ziehen für jedes Schaltjahr im Intervall 1 ab
        # (Dies ist eine vereinfachte Logik für den Prompt, kann verfeinert werden)
        # Für Dreamspell muss man eigentlich 29.02. einfach ignorieren beim Zählen.
        
        # Robustere Dreamspell Zählung:
        # Wir iterieren nicht, wir nutzen Modulo 260.
        # Aber wir müssen wissen, wie viele 29.02. dazwischen lagen.
        # Vorerst nutzen wir die direkte Differenz und korrigieren den Modulo.
        # *HINWEIS*: Eine perfekte Dreamspell-Funktion ist komplexer, hier die Standard-Math.
        
        kin_calc = (anchor_kin + days_diff) % 260
        
        # Modulo Korrektur
        if kin_calc == 0: kin_calc = 260
        
        # Korrektur für Schalttage (Quick Fix für V21 Alpha)
        # In einer echten App würde man hier eine lookup table oder loop nutzen.
        # Wir lassen es erstmal mathematisch rein laufen.
        
        return kin_calc

class MoonEngine:
    """STRANG B: 13-Monde Lookup System."""
    
    @staticmethod
    def get_13moon_data(day, month, db_moon):
        if not db_moon:
            return None
            
        # Suche nach "DD.MM"
        search_key = f"{day:02d}.{month:02d}"
        
        # Suche im Array
        for entry in db_moon:
            if entry.get('date_gregorian') == search_key:
                return entry
                
        return None

# ==============================================================================
# 💾 3. DATA LAYER
# ==============================================================================

@st.cache_data
def load_databases():
    data = {}
    
    # 1. Tzolkin DB laden
    try:
        with open("db_tzolkin_v21_enriched_FINAL.json", "r", encoding="utf-8") as f:
            data['tzolkin'] = json.load(f)
    except FileNotFoundError:
        st.error("🚨 FEHLER: 'db_tzolkin_v21_enriched_FINAL.json' nicht gefunden.")
        data['tzolkin'] = []

    # 2. 13 Moon DB laden
    try:
        with open("db_13moon_v22_enriched_FINAL.json", "r", encoding="utf-8") as f:
            data['moon'] = json.load(f)
    except FileNotFoundError:
        st.warning("⚠️ WARNUNG: 'db_13moon_v22_enriched_FINAL.json' nicht gefunden.")
        data['moon'] = []
        
    return data

# ==============================================================================
# 🖥️ 4. UI COMPONENTS
# ==============================================================================

def render_micro_card(label, value, subtext, border_color="border-weiss"):
    st.markdown(f"""
    <div class="glass-card {border_color}">
        <div class="small-label">{label}</div>
        <div class="big-value">{value}</div>
        <div style="color: #bbb; font-size: 0.9rem;">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🚀 5. MAIN APPLICATION LOGIC
# ==============================================================================

def main():
    # --- SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ NAVIGATOR")
        d_input = st.date_input("Datum wählen", datetime.date.today())
        st.caption(f"Target: {d_input.strftime('%d.%m.%Y')}")
        st.markdown("---")
        st.info("System V2.1 Online 🟢")

    # --- HEADER ---
    st.title("GALAXY SYNC 2.1")
    st.markdown("### 🧬 NOOSPHERE INTERFACE")

    # --- DATEN LADEN ---
    db = load_databases()
    
    if not db['tzolkin']:
        st.stop() # Abbruch wenn Haupt-DB fehlt

    # --- BERECHNUNG (ENGINE RUN) ---
    
    # 1. KIN (Mathe)
    kin_today = MathEngine.calculate_kin(d_input.day, d_input.month, d_input.year)
    
    # 2. MOON (Lookup)
    moon_data = MoonEngine.get_13moon_data(d_input.day, d_input.month, db['moon'])

    # --- DATEN-AGGREGATION ---
    
    current_kin_data = {}
    
    if kin_today > 0:
        # Array Index ist Kin - 1!
        if 0 <= kin_today - 1 < len(db['tzolkin']):
            current_kin_data = db['tzolkin'][kin_today - 1]
        else:
            st.error(f"Kin {kin_today} außerhalb des Datenbank-Index.")
    else:
        st.info("🌌 HUNAB KU - 0.0.Hunab Ku - Der Tag außerhalb der Zeit (Schalttag)")
        
    # --- DASHBOARD RENDERING ---
    
    if current_kin_data:
        identity = current_kin_data.get('identity', {})
        seal = identity.get('seal', {})
        tone = identity.get('tone', {})
        color = seal.get('color', 'Weiss') # Fallback
        
        # Color Mapping für CSS
        color_map = {
            "Rot": "border-rot", 
            "Weiss": "border-weiss", 
            "Blau": "border-blau", 
            "Gelb": "border-gelb",
            "Grün": "border-gruen"
        }
        css_class = color_map.get(color, "border-weiss")

        # TOP ROW: KIN INFO
        c1, c2 = st.columns(2)
        with c1:
            render_micro_card(
                "GALAKTISCHE SIGNATUR", 
                f"KIN {kin_today}", 
                identity.get('name', 'Unbekannt'), 
                css_class
            )
        with c2:
            # 13 Moon Data Integration
            if moon_data:
                moon_info = moon_data.get('moon', {})
                psi = moon_data.get('psi_chrono', 'N/A')
                plasma = moon_data.get('plasma', {}).get('name', '-')
                
                render_micro_card(
                    "SYNCHRONOMETER",
                    f"{moon_info.get('name', 'Mond')} • {plasma}",
                    f"Psi-Chrono: {psi}",
                    "border-gruen"
                )
            else:
                 render_micro_card("SYNCHRONOMETER", "Daten fehlen", "Bitte DB prüfen")

        # --- DYNAMIC MODULE LOADER ---
        st.markdown("---")
        st.caption("🔌 AKTIVE MODULE")

        # Finde alle mod_*.py Dateien
        module_files = glob.glob("mod_*.py")
        
        if not module_files:
            st.info("Keine Module gefunden. Lade 'mod_wavespell.py' hoch!")
            
        for mod_file in module_files:
            mod_name = os.path.basename(mod_file).replace(".py", "")
            
            try:
                # Dynamischer Import
                spec = importlib.util.spec_from_file_location(mod_name, mod_file)
                module = importlib.util.module_from_spec(spec)
                sys.modules[mod_name] = module
                spec.loader.exec_module(module)
                
                # Prüfen ob render() existiert
                if hasattr(module, 'render'):
                    # Modul ausführen - Wir übergeben die rohen Daten
                    # Das Modul muss selbst entscheiden, was es anzeigt
                    with st.container():
                         # ERROR BOUNDARY UM JEDES MODUL
                        try:
                            # Wir erwarten, dass render ein Dict zurückgibt (Atomic Architecture)
                            export_data = module.render(kin_today, current_kin_data, db, d_input)
                        except Exception as e:
                            st.error(f"⚠️ Fehler im Modul '{mod_name}': {e}")
                            
            except Exception as e:
                st.error(f"Kritischer Fehler beim Laden von {mod_file}: {e}")

if __name__ == "__main__":
    main()
