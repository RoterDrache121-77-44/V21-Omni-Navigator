import streamlit as st
import json
import datetime
import os

# ==============================================================================
# 1. CORE MATH-ENGINE (Das Gehirn)
# ==============================================================================
class MathEngine:
    ANCHOR_DATE = datetime.date(1986, 5, 19)
    ANCHOR_KIN = 121

    @staticmethod
    def get_kin(d, m, y):
        # 1. Hunab Ku Check
        if m == 2 and d == 29: return 0
        
        # 2. Iterative Berechnung (Präzision)
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

    @staticmethod
    def get_oracle_ids(kin):
        # Exakte Guide-Berechnung nach Tone-Tabelle
        if kin == 0: return None
        
        # Basis-Werte
        s_id = (kin - 1) % 20 + 1
        t_id = (kin - 1) % 13 + 1
        
        # Helper: Kin aus Siegel/Ton finden
        def get_k(s, t):
             # s und t müssen im Bereich 1-20 bzw 1-13 sein
             # Formel: ((s - 1) + 20 * (x)) % 13 == (t - 1) ... zu komplex für on-the-fly
             # Wir suchen einfach schnell:
             for k in range(1, 261):
                 if (k-1)%20+1 == s and (k-1)%13+1 == t: return k
             return 0

        # 1. ANALOG (Partner)
        # Ausnahme-Regel 19/20 gibt es oft in Skripten, aber Standard ist Summe 19 (oder 1+18=19)
        # Wir nutzen die Standard-Matrix-Logik:
        # 1(Rot) <-> 18(Weiß), 2(Weiß) <-> 17(Erde) ... Summe 19
        analog_s = (19 - s_id)
        if analog_s <= 0: analog_s += 20 # Korrektur für Siegel 19 und 20
        # Spezifische Korrektur falls nötig (manche nutzen 19-20 Paarung)
        # Hier Standard:
        analog_kin = get_k(analog_s, t_id)

        # 2. ANTIPODE (Herausforderung)
        # Differenz 10
        anti_s = (s_id + 10 - 1) % 20 + 1
        anti_kin = get_k(anti_s, t_id)

        # 3. OCCULT (Verborgene Kraft)
        # Siegel-Summe 21, Ton-Summe 14
        occ_s = 21 - s_id
        occ_t = 14 - t_id
        occ_kin = get_k(occ_s, occ_t)

        # 4. GUIDE (Führung)
        # Basierend auf Ton-Verschiebung
        shifts = {1:0, 6:0, 11:0, 2:12, 7:12, 12:12, 3:4, 8:4, 13:4, 4:16, 9:16, 5:8, 10:8}
        shift = shifts.get(t_id, 0)
        guide_s = (s_id + shift - 1) % 20 + 1
        guide_kin = get_k(guide_s, t_id)

        return {
            "guide": guide_kin,
            "analog": analog_kin,
            "anti": anti_kin,
            "occult": occ_kin
        }

# ==============================================================================
# 2. LOGIK & DATENBANK
# ==============================================================================
@st.cache_data
def load_db():
    path = 'db_tzolkin_v21_enriched_FINAL.json'
    if not os.path.exists(path): return []
    try:
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []

DB_TZ = load_db()

def get_v21_data(kin):
    if kin == 0 or not DB_TZ: return None
    k_dat = next((k for k in DB_TZ if k.get('kin') == kin), None)
    if not k_dat: return None
    
    # Harmonik & Chromatik (Logik: Kin 65 = Red 1)
    h_idx = ((kin - 1) // 4) + 1
    c_idx = ((kin - 1) // 5)
    c_pos = ((kin - 1) % 5) + 1
    c_cols = ["Rot", "Weiß", "Blau", "Gelb"]
    c_color = c_cols[c_idx % 4]
    
    # Seasons
    if 185 <= kin <= 249: sea = ("Rote Schlange", "Rot")
    elif 55 <= kin <= 119: sea = ("Blauer Adler", "Blau")
    elif 120 <= kin <= 184: sea = ("Gelbe Sonne", "Gelb")
    else: sea = ("Weißer Hund", "Weiß")

    # Zeitzellen (Input, Store, Process, Output, Matrix)
    s_id = k_dat['identity']['seal']['id']
    cell_types = [("Eingang", "Rot"), ("Speicher", "Weiß"), ("Prozess", "Blau"), ("Ausgang", "Gelb"), ("Matrix", "Grün")]
    cell = cell_types[((s_id - 1) // 4) % 5]

    return {
        "kin": kin, 
        "name": k_dat['identity']['name'],
        "seal": k_dat['identity']['seal']['name'], 
        "color": k_dat['identity']['seal']['color'],
        "tone": f"{k_dat['identity']['tone']['id']} ({k_dat['identity']['tone']['name']})",
        "h": {"idx": h_idx, "p": (kin-1)%4 + 1, "c": ["Rot", "Weiß", "Blau", "Gelb"][(h_idx-1)%4]},
        "c": {"p": c_pos, "c": c_color}, 
        "s": {"n": sea[0], "c": sea[1]},
        "w": {"n": k_dat['time']['wavespell'], "c": k_dat['identity']['seal']['color']},
        "cell": {"n": cell[0], "c": cell[1]},
        "gap": k_dat.get('time', {}).get('gap', False)
    }

# ==============================================================================
# 3. DESIGN & INTERFACE (Der "Look")
# ==============================================================================
st.set_page_config(page_title="V21 OMNI-STATION", layout="wide")

# CSS ENGINE
st.markdown("""
    <style>
    /* Basis */
    .stApp { background-color: #050505; color: #E0E0E0; font-family: monospace; }
    h1 { text-align: center; color: #00FFA3; text-shadow: 0 0 10px #00FFA3; }
    
    /* Boxen */
    .glow-box { 
        background: #0f0f0f; border: 1px solid #333; padding: 15px; 
        border-radius: 8px; text-align: center; margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .glow-box:hover { transform: scale(1.02); }
    
    /* Glow Farben */
    .Rot { border-color: #FF3E3E; box-shadow: 0 0 15px rgba(255, 62, 62, 0.3); color: #FFF; }
    .Weiß { border-color: #FFFFFF; box-shadow: 0 0 15px rgba(255, 255, 255, 0.2); color: #FFF; }
    .Blau { border-color: #3E8EFF; box-shadow: 0 0 15px rgba(62, 142, 255, 0.3); color: #FFF; }
    .Gelb { border-color: #FFD700; box-shadow: 0 0 15px rgba(255, 215, 0, 0.3); color: #FFF; }
    .Grün { border-color: #00FF00; box-shadow: 0 0 15px rgba(0, 255, 0, 0.3); color: #FFF; }
    
    /* Text */
    .label { color: #888; font-size: 0.75em; text-transform: uppercase; letter-spacing: 2px; }
    .val-big { font-size: 1.4em; font-weight: bold; margin: 5px 0; }
    </style>
""", unsafe_allow_html=True)

# UI LOGIK
with st.sidebar:
    st.header("🛸 CONTROL")
    d_in = st.date_input("Zeit-Vektor:", datetime.date.today())
    kn = MathEngine.get_kin(d_in.day, d_in.month, d_in.year)

if kn != 0:
    d = get_v21_data(kn)
    
    # Header Area
    st.markdown(f"<h1>KIN {d['kin']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center; margin-top:-15px; color:#aaa;'>{d['name']}</h3>", unsafe_allow_html=True)
    if d['gap']:
        st.markdown("<div style='text-align:center; color:#00FFA3; font-weight:bold; letter-spacing:3px; margin-bottom:20px;'>⚡ PORTAL TAG ⚡</div>", unsafe_allow_html=True)

    # TABS
    tab1, tab2 = st.tabs(["🧬 NAVIGATOR", "🔮 ORAKEL-STERN"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='glow-box {d['color']}'><div class='label'>Siegel</div><div class='val-big'>{d['seal']}</div><div class='label'>{d['tone']}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='glow-box {d['h']['c']}'><div class='label'>Harmonik</div><div class='val-big'>Takt {d['h']['p']}/4</div><div class='label'>Index {d['h']['idx']}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='glow-box {d['cell']['c']}'><div class='label'>Zeitzelle</div><div class='val-big'>{d['cell']['n']}</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='glow-box {d['color']}'><div class='label'>Welle</div><div class='val-big'>{d['w']['n']}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='glow-box {d['s']['c']}'><div class='label'>Season</div><div class='val-big'>{d['s']['n']}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='glow-box {d['c']['c']}'><div class='label'>{d['c']['c']}e Chromatik</div><div class='val-big'>Tag {d['c']['p']}/5</div></div>", unsafe_allow_html=True)

    with tab2:
        o_ids = MathEngine.get_oracle_ids(kn)
        
        # Helper zum Rendern mit Dropdown
        def render_o(role, k_nr):
            obj = next((k for k in DB_TZ if k.get('kin') == k_nr), None)
            if not obj: return
            
            col = obj['identity']['seal']['color']
            
            # Die Karte (immer sichtbar)
            st.markdown(f"""
            <div class='glow-box {col}' style='padding:10px; margin-bottom:5px;'>
                <div class='label' style='color:{col if col!='Weiß' else 'white'}'>{role}</div>
                <div style='font-size:1.2em; font-weight:bold;'>KIN {k_nr}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Das Dropdown (versteckt Details)
            with st.expander(f"Details {obj['identity']['name']}"):
                st.write(f"**Siegel:** {obj['identity']['seal']['name']}")
                st.write(f"**Ton:** {obj['identity']['tone']['name']}")
                st.write(f"**Welle:** {obj['time']['wavespell']}")
                st.write(f"**Kraft:** {obj['identity']['seal']['power']}")

        # Layout: Stern
        # Reihe 1: Guide
        r1_c1, r1_c2, r1_c3 = st.columns([1,1,1])
        with r1_c2: render_o("GUIDE", o_ids['guide'])

        # Reihe 2: Antipode - Zentrum - Analog
        r2_c1, r2_c2, r2_c3 = st.columns([1,1,1])
        with r2_c1: render_o("ANTIPODE", o_ids['anti'])
        with r2_c2: 
            st.markdown("<div style='text-align:center; color:#00FFA3; font-size:0.8em; margin-bottom:5px;'>DEIN KIN</div>", unsafe_allow_html=True)
            render_o("SCHICKSAL", kn)
        with r2_c3: render_o("ANALOG", o_ids['analog'])

        # Reihe 3: Occult
        r3_c1, r3_c2, r3_c3 = st.columns([1,1,1])
        with r3_c2: render_o("OCCULT", o_ids['occult'])

else:
    st.title("🟢 HUNAB KU")