import streamlit as st
import json
import datetime
import os

# ==============================================================================
# 🌌 KONFIGURATION & DESIGN SYSTEM (CSS-INJEKTION)
# ==============================================================================
st.set_page_config(
    page_title="13:20 SYNC NODE",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    st.markdown("""
    <style>
        /* Deep Space Container */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 100%);
            color: #E0E0E0;
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Die mystische Glas-Box */
        .glass-card {
            background: rgba(20, 20, 30, 0.70);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }

        /* Neon-Akzente & Text */
        h1, h2, h3 { color: #E0E0E0 !important; font-weight: 300; letter-spacing: 2px; text-transform: uppercase; }
        .highlight { color: #00FF66; font-weight: bold; }
        .subtext { font-size: 0.8em; opacity: 0.7; }
        
        /* Custom Divider */
        hr { border-color: rgba(255,255,255,0.1); margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 📐 MASCHINENRAUM: STRANG A - TZOLKIN MATH ENGINE (Der Vektor)
# ==============================================================================
class MathEngine:
    ANCHOR_DATE = datetime.date(1986, 5, 19) # Kin 121
    ANCHOR_KIN = 121

    @staticmethod
    def calculate_kin(day, month, year):
        """
        Berechnet das Kin rein mathematisch. 
        Ignoriert Schaltjahre nicht, aber überspringt 29.02. in der Zählung.
        """
        # 0. Hunab Ku Check (Der Tag außerhalb der Matrix)
        if month == 2 and day == 29:
            return 0 
            
        target = datetime.date(year, month, day)
        current = MathEngine.ANCHOR_DATE
        days_diff = 0
        
        # Wir iterieren, um den 29.02. sauber zu überspringen (sicherste Methode)
        # Richtung: Zukunft
        if target >= current:
            while current < target:
                current += datetime.timedelta(days=1)
                if not (current.month == 2 and current.day == 29):
                    days_diff += 1
            # Modulo-Magie
            new_kin = (MathEngine.ANCHOR_KIN + days_diff - 1) % 260 + 1
            return new_kin
            
        # Richtung: Vergangenheit
        else:
            while current > target:
                current -= datetime.timedelta(days=1)
                if not (current.month == 2 and current.day == 29):
                    days_diff += 1
            new_kin = (MathEngine.ANCHOR_KIN - days_diff - 1) % 260 + 1
            return new_kin

# ==============================================================================
# 🗺️ MASCHINENRAUM: STRANG B - 13 MOON LOOKUP ENGINE (Der Raum)
# ==============================================================================
class MoonEngine:
    @staticmethod
    def get_moon_data(day, month, db_moon):
        """
        Sucht im statischen Raster (db_13moon) nach dem Eintrag.
        Ignoriert das Jahr.
        """
        if month == 2 and day == 29:
            return {"special": "HUNAB_KU_00", "name": "Hunab Ku (Schalttag)"}

        search_key = f"{day:02d}.{month:02d}"
        
        # Generator Expression für Speed (Next or None)
        entry = next((x for x in db_moon if x.get('date_gregorian') == search_key), None)
        
        if not entry:
            return None # Sollte nicht passieren, außer DB Fehler
            
        return entry

# ==============================================================================
# 💾 DATEN-LOGISTIK (Caching & Loading)
# ==============================================================================
@st.cache_data
def load_databases():
    """Lädt die heiligen JSONs in den Speicher."""
    try:
        with open('db_tzolkin_v21_enriched_FINAL.json', 'r', encoding='utf-8') as f:
            db_tzolkin = json.load(f)
        with open('db_13moon_v22_enriched_FINAL.json', 'r', encoding='utf-8') as f:
            db_13moon = json.load(f)
        return db_tzolkin, db_13moon
    except FileNotFoundError:
        st.error("🚨 KRITISCHER FEHLER: Datenbanken nicht gefunden!")
        return [], []

# ==============================================================================
# 🧩 UI-MODULE (Atomic & Data-First)
# ==============================================================================

def render_kin_header(kin_nr, tzolkin_data_entry):
    """
    Rendert die Haupt-Identität.
    """
    if kin_nr == 0:
        st.markdown("<div class='glass-card' style='border-left: 4px solid #00FF66;'><h3>🌀 KIN 0: HUNAB KU</h3><p>Der Tag ist rein. Keine Zeit. Kein Raum.</p></div>", unsafe_allow_html=True)
        return {"kin": 0, "name": "Hunab Ku"}

    # Daten extrahieren
    identity = tzolkin_data_entry['identity']
    seal = identity['seal']
    tone = identity['tone']
    
    # Farb-Mapping für CSS
    color_map = {
        "Rot": "#FF3E3E", "Weiß": "#E0E0E0", "Blau": "#2A8CFF", "Gelb": "#FFD700"
    }
    css_color = color_map.get(seal['color'], "#FFFFFF")

    # 1. UI RENDER
    st.markdown(f"""
    <div class='glass-card' style='border-left: 5px solid {css_color};'>
        <div class='subtext'>DESTINY KIN {kin_nr}</div>
        <h2 style='margin:0; color:white;'>{identity['name']}</h2>
        <div style='margin-top:5px; font-style:italic;'>"{seal['action']} um zu {seal['power']}..."</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. ATOMIC EXPANDER
    with st.expander(f"👁️ Analyse: {seal['name']} & {tone['name']}"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Siegel:** {seal['name']}")
            st.caption(f"Essenz: {seal['essence']}")
        with c2:
            st.markdown(f"**Ton:** {tone['name']} ({tone['id']})")
            st.caption(f"Kraft: {tone['power']}")
            
        st.markdown("---")
        st.write(f"**Affirmation:** Ich {seal['action']} um zu {seal['power']}, {seal['essence']} versiegelnd.")

    # 3. EXPORT DATA RETURN
    return {
        "kin": kin_nr,
        "name": identity['name'],
        "seal": seal['name'],
        "tone": tone['name']
    }

def render_moon_info(moon_entry):
    """
    Rendert die Raum-Zeit-Koordinaten (13 Monde).
    """
    if not moon_entry or "special" in moon_entry:
        return {}

    moon = moon_entry['moon']
    plasma = moon_entry['plasma']
    psi = moon_entry['psi_chrono']

    # 1. UI RENDER
    st.markdown(f"""
    <div class='glass-card'>
        <div class='subtext'>SYNCHRONOMETER</div>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <h3 style='margin:0;'>{moon['name']}</h3>
                <span class='highlight'>Tag {moon_entry['day_of_moon']}</span>
            </div>
            <div style='text-align:right;'>
                <div style='font-size:0.8em;'>PSI-CHRONO</div>
                <div style='font-weight:bold; color:#00FF66;'>KIN {psi}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. ATOMIC DETAILS
    with st.expander("📍 Koordinaten-Details"):
        st.write(f"**Plasma:** {plasma['name']} (Chakra: {plasma['chakra']})")
        st.write(f"**Woche:** {moon_entry['week']}")
        st.info(f"Psi-Chrono Einheit {psi} ist der Speicher-Chip für diesen Tag.")

    # 3. EXPORT
    return {
        "moon": moon['name'],
        "day": moon_entry['day_of_moon'],
        "plasma": plasma['name'],
        "psi_chrono": psi
    }

# ==============================================================================
# 🚀 MAIN APP CONTROLLER
# ==============================================================================
def main():
    inject_custom_css()
    
    # 1. HEADER
    st.title("GALAXY SYNC V2.1")
    st.markdown("---")

    # 2. DATA LOAD
    db_tzolkin, db_13moon = load_databases()
    if not db_tzolkin: st.stop()

    # 3. INPUT (SIDEBAR)
    with st.sidebar:
        st.header("⚙️ PARAMETER")
        d_input = st.date_input("Datum wählen", datetime.date.today())
        
        # Quick Debug Stats
        st.divider()
        st.caption(f"DB Tzolkin: {len(db_tzolkin)} Einträge")
        st.caption(f"DB 13Moon: {len(db_13moon)} Einträge")

    # 4. ENGINE RUN (LOGIC)
    # Strang A: Berechnen
    kin_today = MathEngine.calculate_kin(d_input.day, d_input.month, d_input.year)
    
    # Strang B: Nachschlagen
    moon_today = MoonEngine.get_moon_data(d_input.day, d_input.month, db_13moon)

    # Daten holen (Safe Lookup -1 weil Liste 0-indiziert ist, Kin aber 1-basiert)
    # Ausnahme: Kin 0
    if kin_today > 0:
        kin_data_full = db_tzolkin[kin_today - 1]
    else:
        kin_data_full = None

    # 5. RENDER UI (VIEW)
    # Wir sammeln die Rückgabewerte für einen späteren Export
    export_stack = {}

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.caption("DER ZEIT-VEKTOR (TZOLKIN)")
        if kin_data_full:
            data_a = render_kin_header(kin_today, kin_data_full)
            export_stack.update(data_a)
        else:
            st.warning("Hunab Ku - Der Tag außerhalb der Zeit.")

    with col2:
        st.caption("DER RAUM-CONTAINER (13 MOON)")
        if moon_today:
            data_b = render_moon_info(moon_today)
            export_stack.update(data_b)

    # Hier können später weitere Module wie Orakel, Partner-Check etc. angehängt werden
    # z.B. render_oracle(kin_today, db_tzolkin)

    # 6. EXPORT PREVIEW (Nur für Devs sichtbar aktuell)
    # with st.expander("🛠️ Developer Data-Dump"):
    #     st.json(export_stack)

if __name__ == "__main__":
    main()
