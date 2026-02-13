import streamlit as st
import json
import os
import datetime

def get_name():
    return "🌕 13-Monde (Mystic)"

# ==============================================================================
# 1. DATENBANK LADEN
# ==============================================================================
@st.cache_data
def load_moon_db():
    target = 'db_13moon_v22_enriched_FINAL.json'
    files = [f for f in os.listdir('.') if f == target]
    if not files: return None
    try:
        with open(files[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

# ==============================================================================
# 2. RENDER ENGINE
# ==============================================================================
def render(kin, data, db_tz, date_obj):
    
    db_moon = load_moon_db()
    
    if not db_moon:
        st.error("⚠️ JSON Datenbank fehlt.")
        return

    # Datum Formatierung für Suche (DD.MM)
    search_str = date_obj.strftime("%d.%m")
    
    # Eintrag suchen
    entry = next((item for item in db_moon if item.get('date_gregorian') == search_str), None)

    if not entry:
        st.warning(f"Keine Daten für {search_str}")
        return

    # ==========================================================================
    # 3. DATEN EXTRAKTION (Robust)
    # ==========================================================================
    
    # MOND
    moon = entry.get('moon', {})
    m_id = moon.get('id', 0)
    m_name = moon.get('name', 'Unbekannt')
    m_totem = moon.get('totem', '-')
    m_action = moon.get('action', '-')
    
    # TAG
    d_num = entry.get('day_of_moon', 0)
    
    # WOCHE (Parsing "Rot (Wissen)")
    w_raw = entry.get('week', 'Weiß')
    if '(' in w_raw:
        w_col = w_raw.split('(')[0].strip()
        w_txt = w_raw.split('(')[1].replace(')', '').strip()
    else:
        w_col = w_raw
        w_txt = "-"
        
    # PLASMA & CHAKRA
    p_data = entry.get('plasma', {})
    p_name = p_data.get('name', '-')
    p_chakra = p_data.get('chakra', '-')
    p_img = p_data.get('img', '') # Falls Bilder in JSON sind, sonst leer
    
    # PSI CHRONO (Hier war das Problem)
    # Wir suchen nach 'psi_chrono' oder 'psi' oder 'kin_psi'
    psi = entry.get('psi_chrono') or entry.get('psi') or entry.get('kin_psi') or "N/A"

    # CSS Mapping für Farben
    col_map = {"Rot": "#FF2A2A", "Weiß": "#E0E0E0", "Blau": "#2A8CFF", "Gelb": "#FFD700", "Grün": "#00FF66"}
    
    css_w_col = col_map.get(w_col, "#888")
    
    # Mond Farbe für den Header (Zyklus 1=Rot...)
    m_cols = ["#00FF66", "#FF2A2A", "#E0E0E0", "#2A8CFF", "#FFD700"] 
    header_col = m_cols[m_id % 5] if m_id <= 13 else "#888"

    # ==========================================================================
    # 4. MYSTICAL CSS (High End)
    # ==========================================================================
    st.markdown(f"""
    <style>
    /* Container Reset */
    .mystic-container {{
        font-family: 'Segoe UI', sans-serif;
        color: #ddd;
    }}
    
    /* Header: Dunkel, Glas, Neon-Akzent links */
    .mystic-header {{
        background: rgba(10, 10, 14, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 3px solid {header_col};
        border-radius: 4px;
        padding: 8px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(8px);
        margin-bottom: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }}
    
    /* Grid Layout 4-Spaltig */
    .mystic-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 4px;
        margin-bottom: 6px;
    }}
    
    /* Die winzigen Zellen */
    .mystic-cell {{
        background: rgba(5, 5, 5, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 3px;
        padding: 6px 2px;
        text-align: center;
        transition: border 0.2s;
    }}
    .mystic-cell:hover {{ border-color: rgba(255,255,255,0.2); }}

    /* Typografie - Fein & Edel */
    .lbl {{ font-size: 0.5em; color: #777; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px; display:block; }}
    .val {{ font-size: 0.85em; color: #fff; font-weight: 600; display:block; letter-spacing: 0.5px; }}
    .sub {{ font-size: 0.55em; color: #aaa; margin-top: 2px; display:block; font-style: italic; }}
    
    /* Wochen-Indikator (Unterstrich) */
    .week-indicator {{ border-bottom: 2px solid {css_w_col}; }}
    
    </style>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # 5. HTML STRUKTUR
    # ==========================================================================
    
    st.subheader("🌕 13-Monde")

    # Day out of time Check
    if m_id == 0:
        st.markdown(f"""
        <div class='mystic-header' style='border-left-color:#00FF66;'>
            <div style='color:#00FF66; font-weight:bold;'>TAG AUSSERHALB DER ZEIT</div>
            <div style='font-size:0.8em;'>Freiheit • Kunst • Frieden</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # HEADER
    st.markdown(f"""
    <div class='mystic-container'>
        <div class='mystic-header'>
            <div>
                <span class='lbl'>MOND {m_id} / 13</span>
                <span style='font-size:1em; font-weight:bold; color:#fff;'>{m_name}</span>
            </div>
            <div style='text-align:right;'>
                <span class='lbl'>TOTEM</span>
                <span style='font-size:0.9em; color:{header_col};'>{m_totem}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # GRID (Tag, Woche, Plasma, Psi)
    # Beachte: psi ist jetzt "N/A" wenn leer, damit die Box nicht kollabiert
    st.markdown(f"""
    <div class='mystic-grid'>
        <div class='mystic-cell'>
            <span class='lbl'>TAG</span>
            <span class='val' style='color:#fff;'>{d_num} / 28</span>
            <span class='sub'>Im Mond</span>
        </div>
        
        <div class='mystic-cell week-indicator'>
            <span class='lbl'>WOCHE</span>
            <span class='val'>{w_col}</span>
            <span class='sub'>{w_txt}</span>
        </div>
        
        <div class='mystic-cell'>
            <span class='lbl'>PLASMA</span>
            <span class='val'>{p_name}</span>
            <span class='sub'>{p_chakra}</span>
        </div>
        
        <div class='mystic-cell' style='border-color:rgba(255, 215, 0, 0.15);'>
            <span class='lbl' style='color:#C9A000;'>PSI CHRONO</span>
            <span class='val' style='color:#FFD700;'>{psi}</span>
            <span class='sub'>Einheit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # PROGRESS BAR (Ultra Thin Neon)
    # Erzeugt eine durchgehende Leiste mit feinen Unterbrechungen
    bars = []
    for i in range(1, 29):
        col = "#222" # Zukunft
        if i < d_num: col = "#444" # Vergangenheit
        if i == d_num: col = "#00FFA3" # HEUTE (Neon)
        
        # Woche Separator (Lücke)
        margin = "margin-right:2px;" if i % 7 == 0 else "margin-right:0px;"
        
        bars.append(f"<div style='flex:1; height:2px; background:{col}; {margin}'></div>")
    
    st.markdown(f"""
    <div style='display:flex; width:100%; margin-top:4px; opacity:0.9;'>
        {"".join(bars)}
    </div>
    <div style='display:flex; justify-content:space-between; width:100%; margin-top:2px;'>
        <span class='lbl' style='font-size:0.45em; color:#444;'>INITIIEREN</span>
        <span class='lbl' style='font-size:0.45em; color:#444;'>VERFEINERN</span>
        <span class='lbl' style='font-size:0.45em; color:#444;'>TRANSFORMIEREN</span>
        <span class='lbl' style='font-size:0.45em; color:#444;'>REIFEN</span>
    </div>
    """, unsafe_allow_html=True)
