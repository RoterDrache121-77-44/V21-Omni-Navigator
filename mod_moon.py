import streamlit as st
import json
import os
import datetime

def get_name():
    return "🌕 13-Monde (Dashboard)"

# ==============================================================================
# 1. DATENBANK (Cache & Load)
# ==============================================================================
@st.cache_data
def load_moon_db():
    target = 'db_13moon_v22_enriched_FINAL.json'
    files = [f for f in os.listdir('.') if f == target]
    if not files:
        files = [f for f in os.listdir('.') if 'moon' in f and f.endswith('.json')]
    if not files: return None
    try:
        with open(files[0], 'r', encoding='utf-8') as f: return json.load(f)
    except: return None

# ==============================================================================
# 2. RENDER ENGINE
# ==============================================================================
def render(kin, data, db_tz, date_obj):
    
    db_moon = load_moon_db()
    if not db_moon:
        st.error("Moon DB fehlt.")
        return

    # Suche nach Datum (DD.MM)
    search_str = date_obj.strftime("%d.%m")
    entry = next((item for item in db_moon if item.get('date_gregorian') == search_str), None)

    if not entry:
        st.warning(f"Keine Daten für {search_str}")
        return

    # ==========================================================================
    # 3. DATEN VORBEREITUNG
    # ==========================================================================
    
    # Mond Infos
    moon_data = entry.get('moon', {})
    moon_id = moon_data.get('id', 0)
    moon_name = moon_data.get('name', 'Unbekannt')
    totem = moon_data.get('totem', '-')
    action = moon_data.get('action', '-')
    
    day_of_moon = entry.get('day_of_moon', 0)
    
    # Woche (Farbe extrahieren)
    week_raw = entry.get('week', 'Weiß')
    if '(' in week_raw:
        week_col = week_raw.split('(')[0].strip()
        week_txt = week_raw.split('(')[1].replace(')', '')
    else:
        week_col = week_raw
        week_txt = "Unbekannt"
        
    # Plasma & Psi
    plasma = entry.get('plasma', {})
    psi = entry.get('psi_chrono', '-')
    
    # CSS Mapping für die Wochenfarbe
    css_col_map = {
        "Rot": "#FF3E3E", 
        "Weiß": "#FFFFFF", 
        "Blau": "#3E8EFF", 
        "Gelb": "#FFD700",
        "Grün": "#00FF00"
    }
    hex_col = css_col_map.get(week_col, "#FFFFFF")

    # ==========================================================================
    # 4. PROGRESS BAR GENERATOR (HTML)
    # ==========================================================================
    bar_html = ""
    for i in range(1, 29):
        # Style Logik
        bg = "rgba(255,255,255,0.1)" # Zukunft (Leer)
        h = "3px" # Standard Höhe
        
        if i == day_of_moon: 
            bg = hex_col # HEUTE: Leuchtet in Wochenfarbe
            h = "6px" # Etwas dicker
        elif i < day_of_moon: 
            bg = "rgba(255,255,255,0.4)" # Vergangenheit (Gedimmt)
        
        # Wochen-Trenner (Abstand nach Tag 7, 14, 21)
        margin = "margin-right:3px;" if i % 7 == 0 and i != 28 else "margin-right:1px;"
        
        bar_html += f"<div style='flex:1; height:{h}; background:{bg}; border-radius:1px; {margin} transition:all 0.3s;'></div>"

    # ==========================================================================
    # 5. CSS (Mystical & Micro)
    # ==========================================================================
    st.markdown(f"""
    <style>
    /* DAS SUPER-PANEL (Teil 1) */
    .super-panel {{
        background: linear-gradient(180deg, rgba(20,20,20,0.95) 0%, rgba(10,10,10,0.8) 100%);
        border: 1px solid #333;
        border-top: 2px solid {hex_col}; /* Wochenfarbe oben */
        border-bottom: 1px solid {hex_col}; /* Wochenfarbe unten fein */
        box-shadow: 0 0 15px -5px {hex_col}40; /* Glow in Wochenfarbe */
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
        backdrop-filter: blur(8px);
    }}
    
    .panel-top {{ display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px; }}
    .moon-title {{ font-size: 1.1em
