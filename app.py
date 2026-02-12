import streamlit as st
import json
import datetime
import os

# ==============================================================================
# 1. CORE LOGIK (Crash-Sicher & Monolith)
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
        except: return 1 # Fallback

    @staticmethod
    def get_oracle_ids(kin):
        if kin <= 0: return None
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
    # DIAGNOSE: Suche nach der JSON-Datei
    files = [f for f in os.listdir('.') if f.endswith('.json')]
    # Wir suchen eine Datei die "tzolkin" im Namen hat, oder nehmen die erste JSON
    target = 'db_tzolkin_v21_enriched_FINAL.json'
    
    if target in files:
        path = target
    elif len(files) > 0:
        path = files[0] # Nimm die erste gefundene Datei als Fallback
    else:
        return None # Keine Datei gefunden

    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

DB_TZ = load_db()

def safe_get(data, path, default="-"):
    curr = data
    try:
        for key in path:
            if isinstance(curr, dict): curr = curr.get(key, {})
            else: return default
        return curr if curr not in [None, {}, ""] else default
    except: return default

def get_v21_data(kin):
    if kin <= 0 or not DB_TZ: return None
    k_dat = next((k for k in DB_TZ if k.get('kin') == kin), None)
    if not k_dat: return None
    
    h_idx = ((kin - 1) // 4) + 1
    c_pos = (kin - 65) % 5 + 1
    c_col = ["Rot", "Weiß", "Blau", "Gelb"][((kin - 65) // 5) % 4]
    
    if 185 <= kin <= 249: sea = ("Rote Schlange", "Rot")
    elif 55 <= kin <= 119: sea = ("Blauer Adler", "Blau")
    elif 120 <= kin <= 184: sea = ("Gelbe Sonne", "Gelb")
    else: sea = ("Weißer Hund", "Weiß")

    return {
        "kin": kin,
        "name": safe_get(k_dat, ['identity', 'name']),
        "seal": safe_get(k_dat, ['identity', 'seal', 'name']),
        "color": safe_get(k_dat, ['identity', 'seal', 'color'], "Weiß"),
        "tone": safe_get(k_dat, ['identity', 'tone', 'name']),
        "h": {"idx": h_idx, "p": (kin-1)%4 + 1, "c": ["Rot", "Weiß", "Blau", "Gelb"][(h_idx-1)%4]},
        "c": {"p": c_pos, "c": c_color}, "s": {"n": sea[0], "c": sea[1]},
        "w": {"n": safe_get(k_dat, ['time', 'wavespell']), "c": safe_get(k_dat, ['identity', 'seal', 'color'])},
        "gap": safe_get(k_dat, ['time', 'gap'], False)
    }

# ==============================================================================
# 2. UI & DESIGN (Mobile First)
# ==============================================================================
st.set_page_config(page_title="V21 STATION", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #eee; font-family: sans-serif; }
    .glow-box { 
        background: #111; border: 1px solid #333; padding: 12px; 
        border-radius: 8px; text-align: center; margin-bottom: 8px;
    }
    .Rot { border-left: 5px solid #FF3E3E; }
    .Weiß { border-left: 5px solid #FFFFFF; }
    .Blau { border-left: 5px solid #3E8EFF; }
    .Gelb { border-left: 5px solid #FFD700; }
    .label { color: #888; font-size: 0.7em; text-transform: uppercase; display: block; }
    .val { font-size: 1.2em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🛸 SETTINGS")
    d_in = st.date_input("Datum:", datetime.date.today())
    kn = MathEngine.get_kin(d_in.day, d_in.month, d_in.year)

# ------------------------------------------------------------------------------
# DIAGNOSE-CHECK (Verhindert den Absturz)
# ------------------------------------------------------------------------------
if DB_TZ is None:
    st.error("❌ FEHLER: Die Datenbank-Datei (.json) wurde nicht gefunden!")
    st.info("Bitte lade die Datei 'db_tzolkin_v21_enriched_FINAL.json' bei GitHub hoch.")
    st.stop() # Stoppt hier, damit nichts abstürzt

if kn != 0:
    d = get_v21_data(kn)
    
    # TITAN-CHECK: Sind die Daten wirklich da?
    if d: 
        st.markdown(f"<div style='text-align:center;'><h1>KIN {d['kin']}</h1><p>{d['name']}</p></div>", unsafe_allow_html=True)
        
        if d.get('gap'):
            st.warning("⚡ GALAKTISCHES PORTAL AKTIV")

        t1, t2 = st.tabs(["🧬 NAVIGATOR", "🔮 ORAKEL"])

        with t1:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='glow-box {d['color']}'><span class='label'>Siegel</span><span class='val'>{d['seal']}</span><br>{d['tone']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='glow-box {d['h']['c']}'><span class='label'>Harmonik</span><span class='val'>Takt {d['h']['p']}/4</span></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='glow-box {d['color']}'><span class='label'>Welle</span><span class='val'>{d['w']['n']}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='glow-box {d['s']['c']}'><span class='label'>Season</span><span class='val'>{d['s']['n']}</span></div>", unsafe_allow_html=True)

        with t2:
            o_ids = MathEngine.get_oracle_ids(kn)
            def render_o(role, knr):
                obj = next((k for k in DB_TZ if k.get('kin') == knr), None)
                if not obj: return
                col = safe_get(obj, ['identity', 'seal', 'color'], "Weiß")
                st.markdown(f"<div class='glow-box {col}'><span class='label'>{role}</span><span class='val'>KIN {knr}</span></div>", unsafe_allow_html=True)
                with st.expander("Details"):
                    st.write(f"**Name:** {safe_get(obj, ['identity', 'name'])}")
                    st.write(f"**Siegel:** {safe_get(obj, ['identity', 'seal', 'name'])}")
            
            render_o("GUIDE", o_ids['guide'])
            c_a, c_b = st.columns(2)
            with c_a: render_o("ANTIPODE", o_ids['anti'])
            with c_b: render_o("ANALOG", o_ids['analog'])
            render_o("ZENTRUM", kn)
            render_o("OCCULT", o_ids['occult'])
    else:
        st.error("Daten-Fehler: Das KIN konnte in der Datenbank nicht gefunden werden.")
else:
    st.title("🟢 HUNAB KU")
