import streamlit as st
import json
import os
import datetime

def get_name():
    return "🌕 13-Monde (Datenbank)"

# ==============================================================================
# 1. DATENBANK LADEN (Lokal für dieses Modul)
# ==============================================================================
@st.cache_data
def load_moon_db():
    # Wir suchen exakt deine Datei
    target = 'db_13moon_v22_enriched_FINAL.json'
    files = [f for f in os.listdir('.') if f == target]
    
    if not files:
        # Fallback: Suche irgendeine JSON mit 'moon' im Namen
        files = [f for f in os.listdir('.') if 'moon' in f and f.endswith('.json')]
        
    if not files: return None
    
    try:
        with open(files[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

# ==============================================================================
# 2. RENDER ENGINE
# ==============================================================================
def render(kin, data, db_tz, date_obj):
    
    # DB laden
    db_moon = load_moon_db()
    
    if not db_moon:
        st.error("Fehler: 'db_13moon_v22_enriched_FINAL.json' nicht gefunden.")
        return

    # --- Such-Logik: Finde den Tag in der DB ---
    # Die DB nutzt das Format "DD.MM" (z.B. "26.07")
    search_str = date_obj.strftime("%d.%m")
    
    # Schaltjahr-Fix: 29.02 ist oft "0.0.Hunab Ku" oder fehlt.
    # Wir suchen den Eintrag.
    entry = next((item for item in db_moon if item.get('date_gregorian') == search_str), None)

    if not entry:
        st.warning(f"Kein Eintrag für {search_str} gefunden (Evtl. Schaltjahr-Logik prüfen).")
        return

    # ==========================================================================
    # 3. CSS (Ultra-Kompakt & Mystisch)
    # ==========================================================================
    st.markdown("""
    <style>
    /* Das Gitter für die kleinen Felder */
    .moon-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        margin-bottom: 10px;
    }
    
    /* Die winzige Box */
    .micro-box {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #333;
        border-radius: 4px;
        padding: 6px 2px;
        text-align: center;
        backdrop-filter: blur(5px);
    }
    
    .micro-label { font-size: 0.6em; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px; }
    .micro-val { font-size: 0.9em; font-weight: bold; color: #eee; white-space: nowrap; }
    .micro-sub { font-size: 0.6em; color: #aaa; margin-top: 1px; }

    /* Farben */
    .m-Rot { border-bottom: 2px solid #FF3E3E; }
    .m-Weiß { border-bottom: 2px solid #FFFFFF; }
    .m-Blau { border-bottom: 2px solid #3E8EFF; }
    .m-Gelb { border-bottom: 2px solid #FFD700; }
    .m-Grün { border-bottom: 2px solid #00FF00; }
    
    /* Header Box */
    .moon-header {
        background: linear-gradient(90deg, #111, #222);
        border: 1px solid #444;
        border-radius: 8px;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # 4. DATEN AUFBEREITUNG
    # ==========================================================================
    
    # Sicheres Auslesen mit .get()
    moon_data = entry.get('moon', {})
    moon_id = moon_data.get('id', 0)
    moon_name = moon_data.get('name', '-')
    totem = moon_data.get('totem', '-')
    
    day_of_moon = entry.get('day_of_moon', 0)
    
    # Woche / Heptade
    # Format in DB ist oft "Rot (Wissen)" -> Wir splitten es
    week_raw = entry.get('week', 'Weiß')
    if '(' in week_raw:
        week_col = week_raw.split('(')[0].strip()
        week_txt = week_raw.split('(')[1].replace(')', '')
    else:
        week_col = week_raw
        week_txt = "-"
        
    # Plasma
    plasma_data = entry.get('plasma', {})
    p_name = plasma_data.get('name', '-')
    p_chakra = plasma_data.get('chakra', '-')
    
    # Psi Chrono (Oft nur eine Zahl oder Text)
    psi = entry.get('psi_chrono', '-')
    
    # Farbe für CSS mappen
    css_col = week_col if week_col in ["Rot", "Weiß", "Blau", "Gelb", "Grün"] else "Weiß"

    # ==========================================================================
    # 5. UI OUTPUT
    # ==========================================================================
    
    st.subheader("🌕 Synchronometer")

    # Sonderfall: Tag außerhalb der Zeit
    if moon_id == 0:
        st.markdown(f"""
        <div class='glow-box Grün'>
            <h2 style='color:#00FF00; margin:0;'>💚 {moon_name}</h2>
            <div>{p_name} • {p_chakra}</div>
            <div style='font-size:0.8em; margin-top:5px;'>GALAKTISCHE FREIHEIT</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # A. HEADER (Mond Info)
    st.markdown(f"""
    <div class='moon-header'>
        <div>
            <div class='micro-label'>MOND {moon_id}/13</div>
            <div style='font-weight:bold; font-size:1.1em; color:#fff;'>{moon_name}</div>
        </div>
        <div style='text-align:right;'>
            <div class='micro-label'>TOTEM</div>
            <div style='color:#ccc;'>{totem}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # B. DATA GRID (4 Spalten, sehr klein)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
        <div class='micro-box m-Weiß'>
            <div class='micro-label'>TAG</div>
            <div class='micro-val'>{day_of_moon} / 28</div>
            <div class='micro-sub'>Im Mond</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class='micro-box m-{css_col}'>
            <div class='micro-label'>WOCHE</div>
            <div class='micro-val'>{week_col}</div>
            <div class='micro-sub'>{week_txt}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class='micro-box'>
            <div class='micro-label'>PLASMA</div>
            <div class='micro-val'>{p_name}</div>
            <div class='micro-sub'>{p_chakra}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class='micro-box m-Gelb'>
            <div class='micro-label'>PSI CHRONO</div>
            <div class='micro-val'>{psi}</div>
            <div class='micro-sub'>Speicher</div>
        </div>
        """, unsafe_allow_html=True)

    # C. PROGRESS BAR (28 Tage Leiste)
    # Zeigt visuell, wo wir stehen
    bar_html = ""
    for i in range(1, 29):
        # Farbe bestimmen
        color = "#333" # Inaktiv
        if i == day_of_moon: color = "#00FFA3" # Heute (Neon Grün)
        elif i < day_of_moon: color = "#666"   # Vorbei
        
        # Abstände für Wochen (7, 14, 21)
        margin = "margin-right:2px;" if i % 7 == 0 and i != 28 else ""
        
        bar_html += f"<div style='flex:1; height:4px; background:{color}; border-radius:1px; {margin}'></div>"

    st.markdown(f"""
    <div style='margin-top:8px; display:flex; gap:1px;'>
        {bar_html}
    </div>
    <div style='display:flex; justify-content:space-between; font-size:0.6em; color:#666; margin-top:2px;'>
        <span>Woche 1</span><span>Woche 2</span><span>Woche 3</span><span>Woche 4</span>
    </div>
    """, unsafe_allow_html=True)
