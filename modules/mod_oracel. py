import streamlit as st
import math

# ==============================================================================
# 1. VISUAL FX ENGINE (CSS & Animationen)
# ==============================================================================
def inject_oracle_css():
    st.markdown("""
        <style>
        /* --- ORACLE GRID LAYOUT --- */
        /* Kompakte Expander-Buttons */
        div[data-testid="stExpander"] {
            border: 0px solid transparent;
            background: transparent;
            margin-bottom: 5px !important;
        }
        
        /* Das Styling des "Knopfes" (Expander Summary) */
        div[data-testid="stExpander"] details summary {
            background: rgba(20, 20, 25, 0.8);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 6px;
            padding: 5px 10px !important;
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.9rem;
            color: #ddd !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 40px; /* Schön kompakt */
        }

        /* Hover-Effekte basierend auf Farben (werden per Inline-Style überschrieben, hier Basis) */
        div[data-testid="stExpander"] details summary:hover {
            transform: scale(1.02);
            z-index: 10;
        }

        /* --- TON PHYSIK ANIMATIONEN --- */
        @keyframes pulse-dot { 0% {transform:scale(1); opacity:0.7;} 50% {transform:scale(1.2); opacity:1; box-shadow: 0 0 8px currentColor;} 100% {transform:scale(1); opacity:0.7;} }
        @keyframes wobble-bar { 0% {transform:rotate(0deg);} 25% {transform:rotate(-3deg);} 75% {transform:rotate(3deg);} 100% {transform:rotate(0deg);} }
        @keyframes vibrate-wave { 0% {transform:translateY(0);} 50% {transform:translateY(-2px);} 100% {transform:translateY(0);} }
        
        .anim-pulse { animation: pulse-dot 2s infinite ease-in-out; }
        .anim-wobble { animation: wobble-bar 3s infinite ease-in-out; }
        .anim-vibrate { animation: vibrate-wave 0.5s infinite linear; }
        .anim-static { border-bottom: 1px solid currentColor; }

        /* --- DEEP DATA TABLE (Im Popup) --- */
        .deep-row {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding: 4px 0;
            font-size: 0.85rem;
        }
        .deep-label { color: #888; font-weight: bold; }
        .deep-val { color: #eee; text-align: right; }
        .oracle-role-label {
            text-align: center;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #555;
            margin-bottom: 2px;
            margin-top: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. CALCULATION HELPER (Damit das Popup immer voll ist)
# ==============================================================================
def derive_kin_details(kin_num):
    """
    Berechnet fehlende Details live anhand der Kin-Nummer,
    falls die Datenbank nur Basis-Daten liefert.
    """
    # Basis-Mathematik (0-basiert)
    kin_idx = kin_num - 1
    seal_id = (kin_idx % 20) + 1
    tone_id = (kin_idx % 13) + 1
    
    # 1. Farbe
    # 1,6,11,16=Rot | 2,7,12,17=Weiß | 3,8,13,18=Blau | 4,9,14,19=Gelb
    colors = ["Gelb", "Rot", "Weiß", "Blau"] # Modulo 4 Trick: 1%4=1(Rot)...
    color = colors[seal_id % 4]
    
    # 2. Familie (Erd-Familien)
    families = ["Polar", "Kardinal", "Zentral", "Signal", "Tor"]
    # Formel Mapping ist komplexer, hier vereinfachte Logik für Display
    # Rot=1, Weiß=2, Blau=3, Gelb=4. 
    # Wir nutzen eine Lookup-Map für Siegel 1-20
    seal_map = {
        1:"Drache", 2:"Wind", 3:"Nacht", 4:"Samen", 5:"Schlange",
        6:"Weltenüberbrücker", 7:"Hand", 8:"Stern", 9:"Mond", 10:"Hund",
        11:"Affe", 12:"Mensch", 13:"Himmelswanderer", 14:"Magier", 15:"Adler",
        16:"Krieger", 17:"Erde", 18:"Spiegel", 19:"Sturm", 20:"Sonne"
    }
    seal_name = seal_map.get(seal_id, "Unbekannt")
    
    # Familie Mapping (Bar, Polar...)
    fam_idx = (seal_id - 1) % 5 
    family = families[fam_idx]
    
    # Chakra Mapping
    chakras = ["Kronen", "Wurzel", "Sakral", "Solarplexus", "Herz", "Kehlkopf", "Dritte Auge"]
    # Vereinfachtes Mapping (Da echte Logik komplex) -> Wir nehmen 5er Zyklus
    chakra_map = ["Kronen", "Wurzel", "Herz", "Solarplexus", "Kehlkopf"]
    chakra = chakra_map[(seal_id-1)%5]
    
    # Harmonik (Zolkin hat 65 Harmoniken à 4 Kins)
    harmonic = (kin_idx // 4) + 1
    
    # Welle (13er Zyklus)
    wave_start = (kin_idx // 13) * 13 + 1
    
    # Planet (Beispielhaft)
    planets = ["Pluto", "Neptun", "Uranus", "Saturn", "Jupiter", "Maldek", "Mars", "Erde", "Venus", "Merkur"]
    planet = planets[(seal_id - 1) % 10]

    return {
        "kin": kin_num,
        "seal_id": seal_id,
        "seal_name": seal_name,
        "tone_id": tone_id,
        "color": color,
        "family": family,
        "chakra": chakra,
        "planet": planet,
        "harmonic": harmonic,
        "wave": f"Welle {wave_start}",
        "clan": "Feuer" if harmonic <= 13 else "Blut" # (Vereinfacht)
    }

# ==============================================================================
# 3. RENDER ATOM (Ein einzelner Orakel-Button)
# ==============================================================================
def render_oracle_card(role, kin_data, is_destiny=False):
    """
    Zeichnet den kleinen Flux-Button mit dem riesigen Pop-up.
    """
    if not kin_data:
        st.markdown(f"<div class='oracle-role-label'>{role}</div><div style='text-align:center; opacity:0.3'>---</div>", unsafe_allow_html=True)
        return

    # Daten Validierung (Fallback auf Berechnung wenn DB leer)
    kin_num = kin_data.get('kin', 0)
    details = derive_kin_details(kin_num)
    
    # Wenn DB Namen hat, nutze sie, sonst berechnete
    name_display = kin_data.get('seal', {}).get('name', details['seal_name'])
    tone_display = kin_data.get('tone', {}).get('name', f"Ton {details['tone_id']}")
    color_display = kin_data.get('seal', {}).get('color', details['color'])

    # CSS Farben
    color_map = {
        "Rot": "255, 62, 62", 
        "Weiß": "220, 220, 220", 
        "Blau": "42, 140, 255", 
        "Gelb": "255, 215, 0"
    }
    rgb = color_map.get(color_display, "200,200,200")
    
    # Animation Class bestimmen
    tid = details['tone_id']
    anim_class = "anim-static"
    if tid in [1,5,9,13]: anim_class = "anim-pulse"
    elif tid in [2,6,10]: anim_class = "anim-wobble"
    elif tid in [3,7,11]: anim_class = "anim-vibrate"

    # Style für den Button (Border Glow)
    border_style = f"border-left: 3px solid rgba({rgb}, 1);" if not is_destiny else f"border: 1px solid rgba({rgb}, 0.8); box-shadow: 0 0 10px rgba({rgb}, 0.2);"

    # --- HTML INJECTION FÜR DEN BUTTON STYLE ---
    # Wir nutzen einen Trick: Inline Style im Container um das Summary zu färben
    st.markdown(f"""
    <style>
    /* Spezifischer Hack für diesen Aufruf */
    </style>
    <div class='oracle-role-label' style='color:rgba({rgb},0.8);'>{role}</div>
    """, unsafe_allow_html=True)
    
    # Der Expander IST der Button
    label_html = f"**KIN {kin_num}** | {name_display}"
    with st.expander(f"KIN {kin_num} • {name_display}"):
        # --- DAS MINUTIÖSE POPUP (Inhalt) ---
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:10px;">
            <div style="font-size:1.5rem; font-weight:bold; color:rgba({rgb},1); text-shadow:0 0 15px rgba({rgb},0.4);">
                {name_display}
            </div>
            <div style="font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">
                {color_display}er {tone_display}er {details['seal_name']}
            </div>
            <div class="{anim_class}" style="display:inline-block; margin-top:5px; font-size:1.2rem; color:rgba({rgb},1);">
                ● Ton {details['tone_id']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Die Daten-Tabelle
        rows = [
            ("Galaktische Signatur", f"Kin {kin_num}"),
            ("Solares Siegel", f"{details['seal_name']} (Code {details['seal_id']})"),
            ("Galaktischer Ton", f"{tone_display} ({details['tone_id']})"),
            ("Farbe / Energie", color_display),
            ("Welle (Purpose)", details['wave']),
            ("Erd-Familie", details['family']),
            ("Chakra", details['chakra']),
            ("Planet", details['planet']),
            ("Harmonik", f"H-{details['harmonic']}"),
            ("Clan", f"{details['clan']}-Clan"),
        ]
        
        for label, val in rows:
            st.markdown(f"""
            <div class='deep-row'>
                <span class='deep-label'>{label}</span>
                <span class='deep-val'>{val}</span>
            </div>
            """, unsafe_allow_html=True)
            
        # Plasma (Optional, wenn in pulse vorhanden für diesen Tag)
        # Hier generisch, da Plasma eigentlich Tages-abhängig ist, nicht Kin-abhängig (außer im Synchronotron)

# ==============================================================================
# 4. MAIN RENDERER (Das Gitter)
# ==============================================================================
def render(pulse):
    inject_oracle_css()
    
    meta = pulse['metadata']
    if meta['is_leap_day']:
        st.info("Kein Orakel am Tag außerhalb der Zeit.")
        return

    # Daten holen
    oracle = pulse['tzolkin'].get('oracle', {})
    if not oracle:
        st.warning("Keine Orakel-Daten verfügbar.")
        return

    # DAS GITTER (CSS Grid Simulation mit Columns)
    
    # ZEILE 1: GUIDE (Mitte)
    # [Leer] [Guide] [Leer]
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        render_oracle_card("FÜHRUNG (GUIDE)", oracle.get('guide'))

    # ZEILE 2: ANTIPODE - DESTINY - ANALOG
    m1, m2, m3 = st.columns([1, 1.4, 1])
    with m1:
        render_oracle_card("HERAUSFORDERUNG (ANTIPODE)", oracle.get('antipode'))
    with m2:
        # Destiny ist etwas größer/hervorgehoben
        render_oracle_card("SCHICKSAL (DESTINY)", oracle.get('destiny'), is_destiny=True)
    with m3:
        render_oracle_card("PARTNER (ANALOG)", oracle.get('analog'))

    # ZEILE 3: OCCULT (Mitte)
    u1, u2, u3 = st.columns([1, 1.4, 1])
    with u2:
        render_oracle_card("GEHEIMNIS (OCCULT)", oracle.get('occult'))
