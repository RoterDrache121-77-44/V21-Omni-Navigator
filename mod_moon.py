import streamlit as st
import json
import os
import datetime

def get_name():
    return "🌕 13-Monde (Live-DB)"

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
    
    # DB laden
    db_moon = load_moon_db()
    
    if not db_moon:
        st.error("Datenbank 'db_13moon_v22_enriched_FINAL.json' fehlt.")
        return

    # Datum suchen (Format DD.MM)
    search_str = date_obj.strftime("%d.%m")
    
    # Eintrag finden
    entry = next((item for item in db_moon if item.get('date_gregorian') == search_str), None)

    if not entry:
        # Fallback für Schaltjahr oder Fehler
        st.warning(f"Keine Daten für {search_str}")
        return

    # ==========================================================================
    # 3. DATEN VORBEREITEN (Auslesen)
    # ==========================================================================
    # Wir holen alle Daten VOR dem HTML, damit der f-string sauber bleibt.
    
    # Mond
    moon = entry.get('moon', {})
    m_id = moon.get('id', 0)
    m_name = moon.get('name', 'Unbekannt')
    m_totem = moon.get('totem', '-')
    
    # Tag
    d_num = entry.get('day_of_moon', 0)
    
    # Woche (Parsing: "Rot (Wissen)" -> Farbe: Rot, Text: Wissen)
    w_raw = entry.get('week', 'Weiß')
    w_col = "Weiß"
    w_txt = "-"
    if "(" in w_raw:
        parts = w_raw.split("(")
        w_col = parts[0].strip() # z.B. "Rot"
        w_txt = parts[1].replace(")", "").strip() # z.B. "Wissen"
    else:
        w_col = w_raw
    
    # Plasma & Chakra
    p_data = entry.get('plasma', {})
    p_name = p_data.get('name', '-')
    p_chakra = p_data.get('chakra', '-')
    
    # Psi Chrono
    psi = entry.get('psi_chrono', '-')

    # CSS Klassen Vorbereitung
    # Wir mappen deutsche Farben auf CSS Klassen
    color_map = {
        "Rot": "m-Rot", "Weiß": "m-Weiß", "Blau": "m-Blau", 
        "Gelb": "m-Gelb", "Grün": "m-Grün"
    }
    css_week = color_map.get(w_col, "m-Weiß")

    # Mond Farbe bestimmen (Rot/Weiß/Blau/Gelb Zyklus basierend auf ID)
    # Mond 1=Rot, 2=Weiß, 3=Blau, 4=Gelb, 5=Rot...
    moon_colors = ["m-Grün", "m-Rot", "m-Weiß", "m-Blau", "m-Gelb"] # 0 ist Grün (Day out of time)
    css_moon = moon_colors[m_id % 5] if m_id <= 13 else "m-Weiß"
    
    if m_id == 0: css_moon = "m-Grün" # Day out of time fix

    # ==========================================================================
    # 4. CSS DESIGN (Micro & Mystical)
    # ==========================================================================
    st.markdown("""
    <style>
    /* Container Style */
    .moon-container {
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Header Leiste */
    .m-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(90deg, #1a1a1a, #0d0d0d);
        border: 1px solid #333;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 8px;
    }
    
    /* Das 4-Spalten Grid */
    .m-grid {
        display: flex;
        gap: 5px;
        margin-bottom: 8px;
    }
    
    /* Die einzelnen Daten-Zellen (Micro) */
    .m-cell {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #222;
        border-radius: 4px;
        padding: 5px 2px;
        text-align: center;
        backdrop-filter: blur(4px);
    }
    
    /* Typografie (Sehr klein wie gewünscht) */
    .lbl { font-size: 0.55em; color: #666; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 2px; }
    .val { font-size: 0.85em; font-weight: bold; color: #eee; display: block; }
    .sub { font-size: 0.55em; color: #999; display: block; margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    
    /* Farb-Indikatoren (Unterstrich) */
    .m-Rot { border-bottom: 2px solid #D13030; }
    .m-Weiß { border-bottom: 2px solid #E0E0E0; }
    .m-Blau { border-bottom: 2px solid #2D7AD6; }
    .m-Gelb { border-bottom: 2px solid #D4B215; }
    .m-Grün { border-bottom: 2px solid #00C853; }
    
    </style>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # 5. HTML OUTPUT (Sauber getrennt)
    # ==========================================================================
    
    st.subheader("🌕 13-Monde Synchronometer")

    # Sonderfall: Tag außerhalb der Zeit
    if m_id == 0:
        st.markdown(f"""
        <div class='m-header m-Grün'>
            <div style='font-weight:bold; color:#00FF00;'>TAG AUSSERHALB DER ZEIT</div>
            <div style='font-size:0.8em;'>25. Juli</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # A. HEADER
    st.markdown(f"""
    <div class='moon-container'>
        <div class='m-header {css_moon}'>
            <div>
                <span class='lbl' style='color:#aaa;'>MOND {m_id}</span>
                <span style='font-weight:bold; color:#fff; font-size:1em;'>{m_name}</span>
            </div>
            <div style='text-align:right;'>
                <span class='lbl' style='color:#aaa;'>TOTEM</span>
                <span style='color:#ddd; font-size:0.9em;'>{m_totem}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # B. GRID (4 Spalten: Tag, Woche, Plasma, Psi)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""<div class='m-cell m-Weiß'><span class='lbl'>TAG</span><span class='val'>{d_num} / 28</span><span class='sub'>Im Mond</span></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='m-cell {css_week}'><span class='lbl'>WOCHE</span><span class='val'>{w_col}</span><span class='sub'>{w_txt}</span></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='m-cell'><span class='lbl'>PLASMA</span><span class='val'>{p_name}</span><span class='sub'>{p_chakra}</span></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='m-cell m-Gelb'><span class='lbl'>PSI CHRONO</span><span class='val'>{psi}</span><span class='sub'>Speicher</span></div>""", unsafe_allow_html=True)

    # C. PROGRESS BAR (Manuell gebaut für volle Kontrolle)
    # Zeigt die 4 Wochen à 7 Tage
    bars = []
    for i in range(1, 29):
        col = "#222" # Leer
        if i < d_num: col = "#555" # Vergangenheit
        if i == d_num: col = "#00FFA3" # Heute (Neon)
        
        # Style für den einzelnen Balken
        margin = "margin-right:3px;" if i % 7 == 0 else "margin-right:1px;"
        bars.append(f"<div style='flex:1; height:3px; background:{col}; {margin}'></div>")
    
    bar_html = "".join(bars)

    st.markdown(f"""
    <div style='margin-top:5px; display:flex; width:100%; opacity:0.8;'>
        {bar_html}
    </div>
    <div style='display:flex; justify-content:space-between; width:100%; margin-top:2px;'>
        <span class='lbl' style='color:#444;'>WOCHE 1</span>
        <span class='lbl' style='color:#444;'>WOCHE 2</span>
        <span class='lbl' style='color:#444;'>WOCHE 3</span>
        <span class='lbl' style='color:#444;'>WOCHE 4</span>
    </div>
    """, unsafe_allow_html=True)
