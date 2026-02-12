import streamlit as st
import json
import datetime
import os

# ==============================================================================
# 1. CORE LOGIK (Crash-Sicher & Alles Integriert)
# ==============================================================================
class MathEngine:
    ANCHOR_DATE = datetime.date(1986, 5, 19)
    ANCHOR_KIN = 121
    @staticmethod
    def get_kin(d, m, y):
        if m == 2 and d == 29: return 0
        target, current = datetime.date(y, m, d), MathEngine.ANCHOR_DATE
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

    @staticmethod
    def get_oracle_ids(kin):
        s_id = (kin - 1) % 20 + 1
        t_id = (kin - 1) % 13 + 1
        analog = (19 - (s_id - 1)) % 20 + 1
        anti = (s_id + 10 - 1) % 20 + 1
        def k_from_st(s, t): return ((s - 1) * 13 + (t - 1)) % 260 + 1
        return {
            "guide": (kin + 52 - 1) % 260 + 1,
            "analog": k_from_st(analog, t_id),
            "anti": k_from_st(anti, t_id),
            "occult": (261 - kin)
        }

@st.cache_data
def load_db():
    # Intelligente Suche nach der JSON Datei
    possible_files = [f for f in os.listdir('.') if f.endswith('.json') and 'tzolkin' in f]
    if not possible_files: return []
    # Nimm die erste gefundene Datei (wahrscheinlich deine enriched DB)
    path = possible_files[0]
    try:
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []

DB_TZ = load_db()

def safe_get(data, path, default="-"):
    """Holt Daten sicher aus verschachtelten Dictionaries"""
    curr = data
    try:
        for key in path:
            if isinstance(curr, dict):
                curr = curr.get(key, {})
            else:
                return default
        # Wenn am Ende ein leeres Dict oder None steht, gib default zurück (außer bei False/0)
        if curr is None or (isinstance(curr, dict) and not curr) and curr is not False: 
            return default
        return curr
    except: return default

def get_v21_data(kin):
    if kin == 0 or not DB_TZ: return None
    k_dat = next((k for k in DB_TZ if k.get('kin') == kin), None)
    if not k_dat: return None
    
    h_idx = ((kin - 1) // 4) + 1
    c_pos = (kin - 65) % 5 + 1
    c_col = ["Rot", "Weiß", "Blau", "Gelb"][((kin - 65) // 5) % 4]
    
    if 185 <= kin <= 249: sea = ("Rote Schlange", "Rot")
    elif 55 <= kin <= 119: sea = ("Blauer Adler", "Blau")
    elif 120 <= kin <= 184: sea = ("Gelbe Sonne", "Gelb")
    else: sea = ("Weißer Hund", "Weiß")

    # Wir nutzen safe_get für ALLES, was abstürzen könnte
    return {
        "kin": kin,
        "name": safe_get(k_dat, ['identity', 'name']),
        "seal": safe_get(k_dat, ['identity', 'seal', 'name']),
        "color": safe_get(k_dat, ['identity', 'seal', 'color'], "Weiß"),
        "tone": safe_get(k_dat, ['identity', 'tone', 'name']),
        "h": {"idx": h_idx, "p": (kin-1)%4 + 1, "c": ["Rot", "Weiß", "Blau", "Gelb"][(h_idx-1)%4]},
        "c": {"p": c_pos, "c": c_col}, "s": {"n": sea[0], "c": sea[1]},
        "w": {"n": safe_get(k_dat, ['time', 'wavespell']), "c": safe_get(k_dat, ['identity', 'seal', 'color'])},
        "gap": safe_get(k_dat, ['time', 'gap'], False)
    }

# ==============================================================================
# 2. DESIGN & INTERFACE (Mobile Friendly)
# ==============================================================================
st.set_page_config(page_title="V21", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #E0E0E0; font-family: sans-serif; }
    
    /* Box-Design für Handy optimiert */
    .glow-box { 
        background: #111; border: 1px solid #333; padding: 12px; 
        border-radius: 8px; text-align: center; margin-bottom: 8px;
    }
    
    /* Glow Farben - dickerer Rand links für bessere Sichtbarkeit */
    .Rot { border-left: 4px solid #FF3E3E; }
    .Weiß { border-left: 4px solid #FFFFFF; }
    .Blau { border-left: 4px solid #3E8EFF; }
    .Gelb { border-left: 4px solid #FFD700; }
    
    .label { color: #888; font-size: 0.7em; text-transform: uppercase; letter-spacing: 1px; display:block; margin-bottom:4px;}
    .val-big { font-size: 1.2em; font-weight: bold; color: #fff; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🛸 CONTROL")
    d_in = st.date_input("Datum:", datetime.date.today())
    kn = MathEngine.get_kin(d_in.day, d_in.month, d_in.year)

if kn != 0:
    d = get_v21_data(kn)
    
    # Kompakter Header
    st.markdown(f"<div style='text-align:center; margin-bottom:10px;'><h1>KIN {d['kin']}</h1><div style='color:#ccc'>{d['name']}</div></div>", unsafe_allow_html=True)
    
    if d['gap']:
        st.info("⚡ PORTAL TAG AKTIV")

    tab1, tab2 = st.tabs(["🧬 NAVIGATOR", "🔮 ORAKEL"])

    with tab1:
        # Stapel-Layout für Handy (Container statt Spalten wo möglich)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='glow-box {d['color']}'><span class='label'>Siegel</span><span class='val-big'>{d['seal']}</span><br><span style='font-size:0.8em'>{d['tone']}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='glow-box {d['h']['c']}'><span class='label'>Harmonik</span><span class='val-big'>Takt {d['h']['p']}/4</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='glow-box {d['color']}'><span class='label'>Welle</span><span class='val-big'>{d['w']['n']}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='glow-box {d['s']['c']}'><span class='label'>Season</span><span class='val-big'>{d['s']['n']}</span></div>", unsafe_allow_html=True)

    with tab2:
        o_ids = MathEngine.get_oracle_ids(kn)
        
        def render_o(role, k_nr):
            obj = next((k for k in DB_TZ if k.get('kin') == k_nr), None)
            if not obj: return
            
            # Sicheres Laden aller Werte
            col = safe_get(obj, ['identity', 'seal', 'color'], "Weiß")
            name = safe_get(obj, ['identity', 'name'])
            tone = safe_get(obj, ['identity', 'tone', 'name'])
            seal = safe_get(obj, ['identity', 'seal', 'name'])
            
            # Versuch verschiedene Keys für "Kraft" zu finden
            id_data = obj.get('identity', {}).get('seal', {})
            # Suche nach 'power', 'action' oder 'essence'. Wenn nichts da, nimm '-'
            power = id_data.get('power') or id_data.get('action') or id_data.get('essence') or "-"

            # Karte
            st.markdown(f"""
            <div class='glow-box {col}'>
                <span class='label'>{role}</span>
                <span style='font-weight:bold; font-size:1.1em;'>KIN {k_nr}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Dropdown
            with st.expander(f"Details anzeigen"):
                st.write(f"**Name:** {name}")
                st.write(f"**Ton:** {tone}")
                st.write(f"**Siegel:** {seal}")
                st.write(f"**Kraft:** {power}")

        # Orakel Layout (Handy-Optimiert: Untereinander)
        st.markdown("### 👑 FÜHRUNG")
        render_o("GUIDE", o_ids['guide'])
        
        st.markdown("### ⚡ ENERGIE-FELD")
        c_a, c_b = st.columns(2)
        with c_a: render_o("ANTIPODE", o_ids['anti'])
        with c_b: render_o("ANALOG", o_ids['analog'])
            
        st.markdown("### 🌟 ZENTRUM")
        render_o("DEIN KIN", kn)
        
        st.markdown("### 🗝️ OCCULT")
        render_o("OCCULT", o_ids['occult'])

else:
    st.title("🟢 HUNAB KU")
