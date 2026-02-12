import streamlit as st
import json
import datetime
import os
import importlib.util
import sys
import inspect

# ==============================================================================
# 1. DAS GEHIRN (MathEngine & DB)
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
        except: return 1

@st.cache_data
def load_db():
    files = [f for f in os.listdir('.') if f.endswith('.json')]
    target = 'db_tzolkin_v21_enriched_FINAL.json'
    path = target if target in files else (files[0] if files else None)
    if not path: return None
    try:
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    except: return None

DB_TZ = load_db()

def get_base_data(kin):
    if kin <= 0 or not DB_TZ: return None
    return next((k for k in DB_TZ if k.get('kin') == kin), None)

# ==============================================================================
# 2. DER INTELLIGENTE SUCHTRUPP (Module Loader)
# ==============================================================================
def load_modules():
    """Scannt Ordner, lädt Module und gibt sie als Dictionary zurück."""
    modules = {}
    files = [f for f in os.listdir('.') if f.startswith('mod_') and f.endswith('.py')]
    
    for filename in files:
        module_key = filename[:-3] # Dateiname ohne .py
        try:
            spec = importlib.util.spec_from_file_location(module_key, filename)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_key] = mod
            spec.loader.exec_module(mod)
            
            if hasattr(mod, 'get_name') and hasattr(mod, 'render'):
                display_name = mod.get_name()
                # Wir speichern Referenz und Display-Name
                modules[display_name] = {"ref": mod, "key": module_key}
        except Exception as e:
            st.sidebar.error(f"Fehler in {filename}: {e}")
            
    return modules

# ==============================================================================
# 3. MYSTICAL UI DESIGN (CSS V22)
# ==============================================================================
st.set_page_config(page_title="V22 OMNI", layout="wide", page_icon="🛸")

st.markdown("""
    <style>
    /* 1. HINTERGRUND: Deep Space Gradient */
    .stApp { 
        background: radial-gradient(circle at 50% 10%, #1a1a1e 0%, #000000 90%);
        color: #E0E0E0; 
        font-family: 'Helvetica Neue', sans-serif; 
    }
    
    /* 2. GLOW BOXEN: Eleganter & Subtiler */
    .glow-box { 
        background: rgba(18, 18, 18, 0.7); /* Leicht transparent */
        border: 1px solid #333; 
        backdrop-filter: blur(10px); /* Milchglas-Effekt */
        padding: 15px; 
        border-radius: 12px; 
        text-align: center; 
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }
    .glow-box:hover {
        border-color: #555;
    }
    
    /* 3. TYPOGRAFIE */
    h1 { 
        font-weight: 200; 
        letter-spacing: 2px; 
        text-transform: uppercase; 
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    h2, h3 { color: #ccc; font-weight: 300; letter-spacing: 1px; }
    
    /* 4. FARB-AKZENTE (Leuchtend) */
    .Rot { border-left: 3px solid #FF3E3E; box-shadow: -5px 0 15px -5px rgba(255, 62, 62, 0.2); }
    .Weiß { border-left: 3px solid #FFFFFF; box-shadow: -5px 0 15px -5px rgba(255, 255, 255, 0.2); }
    .Blau { border-left: 3px solid #3E8EFF; box-shadow: -5px 0 15px -5px rgba(62, 142, 255, 0.2); }
    .Gelb { border-left: 3px solid #FFD700; box-shadow: -5px 0 15px -5px rgba(255, 215, 0, 0.2); }
    .Grün { border-left: 3px solid #00FF00; box-shadow: -5px 0 15px -5px rgba(0, 255, 0, 0.2); }
    
    /* 5. SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. HAUPT-PROGRAMM
# ==============================================================================

# A. SIDEBAR & KONTROLLE
with st.sidebar:
    st.header("🛸 CONTROL")
    # Zeit-Vektor
    d_in = st.date_input("Zeit-Vektor:", datetime.date.today())
    kin_nr = MathEngine.get_kin(d_in.day, d_in.month, d_in.year)
    
    st.markdown("---")
    st.caption("MODULE STREAM")
    
    # B. MODULE LADEN & SORTIEREN
    available_map = load_modules()
    
    if not available_map:
        st.warning("System leer. Bitte 'mod_' Dateien hochladen.")
        selected_names = []
    else:
        # Sortier-Liste erstellen
        all_names = list(available_map.keys())
        # Multiselect erlaubt Auswahl UND Reihenfolge
        selected_names = st.multiselect(
            "Anzeige wählen:", 
            options=all_names, 
            default=all_names
        )

# C. RENDERING (DER STREAM)
if DB_TZ is None:
    st.error("❌ Datenbank fehlt. Bitte JSON hochladen.")
    st.stop()

if kin_nr == 0:
    st.title("🟢 HUNAB KU")
    st.write("Der Tag außerhalb der Zeit. Alles ist Eins.")
else:
    full_data = get_base_data(kin_nr)
    
    if full_data:
        # HEADER BEREICH
        kin_name = full_data['identity']['name']
        st.markdown(f"<div style='text-align:center; padding:20px;'><h1>KIN {kin_nr}</h1><div style='color:#888; margin-top:5px; font-size:1.1em;'>{kin_name}</div></div>", unsafe_allow_html=True)
        
        # PORTAL CHECK
        if full_data.get('time', {}).get('gap'):
             st.markdown("<div style='text-align:center; color:#00FFA3; font-size:0.8em; letter-spacing:4px; margin-bottom:30px; text-shadow:0 0 10px rgba(0,255,163,0.5);'>⚡ GALAKTISCHES PORTAL ⚡</div>", unsafe_allow_html=True)

        # D. MODULE ABFEUERN (In der gewählten Reihenfolge)
        for name in selected_names:
            module_info = available_map[name]
            module = module_info['ref']
            
            try:
                # INTELLIGENTE INJEKTION:
                # Wir prüfen, welche Argumente die render-Funktion akzeptiert.
                # So können alte Module (nur KIN) und neue (mit Datum) koexistieren.
                
                sig = inspect.signature(module.render)
                params = sig.parameters
                
                # Argumente vorbereiten
                args = []
                if 'kin' in params: args.append(kin_nr)
                if 'data' in params: args.append(full_data)
                if 'db' in params: args.append(DB_TZ)
                
                # Der TIME FIX: Wenn das Modul 'date_obj' oder 'd_in' will, geben wir es ihm
                if 'date_obj' in params: 
                    # Wir rufen es explizit mit keyword auf, falls Position unsicher ist, 
                    # aber hier nutzen wir einfach args append logic wenn die Reihenfolge stimmt.
                    # Sicherer ist Keyword-Call, aber Streamlit Module sind meist position-based.
                    # Wir machen es einfach: Wenn 4 Argumente verlangt werden, ist das 4. das Datum.
                    if len(params) >= 4:
                        module.render(kin_nr, full_data, DB_TZ, d_in)
                    else:
                        module.render(kin_nr, full_data, DB_TZ)
                elif 'd_in' in params:
                     module.render(kin_nr, full_data, DB_TZ, d_in)
                else:
                    # Fallback für Module ohne Datum (wie Navigator/Orakel)
                    module.render(kin_nr, full_data, DB_TZ)
                
                # Eleganter Abstand
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Fehler im Modul '{name}': {e}")
                
        # FOOTER
        st.markdown("<div style='text-align:center; color:#333; margin-top:50px; font-size:0.7em;'>V22 OMNI STATION</div>", unsafe_allow_html=True)
            
    else:
        st.error("Kin Daten nicht gefunden.")
