import streamlit as st

def get_name():
    return "🧬 Basis Navigator (Pro)"

def render(kin, data, db):
    # ==========================================================================
    # 1. CSS FÜR HIGH-DENSITY LAYOUT (KLEIN & FEIN)
    # ==========================================================================
    st.markdown("""
    <style>
    /* Kompakte Boxen */
    .mini-box {
        background: #121212;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 8px 5px; /* Weniger Padding für kompakten Look */
        text-align: center;
        margin-bottom: 8px;
        height: 100%;
        transition: all 0.2s;
    }
    .mini-box:hover {
        transform: translateY(-2px);
        border-color: #555;
    }
    
    /* Typografie verkleinert */
    .nav-label { font-size: 0.65em; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }
    .nav-val { font-size: 1.1em; font-weight: bold; color: #fff; line-height: 1.1; }
    .nav-sub { font-size: 0.7em; color: #aaa; margin-top: 3px; font-family: monospace; }
    
    /* Farb-Indikatoren (Linker Rand) */
    .Rot { border-left: 3px solid #FF3E3E !important; }
    .Weiß { border-left: 3px solid #FFFFFF !important; }
    .Blau { border-left: 3px solid #3E8EFF !important; }
    .Gelb { border-left: 3px solid #FFD700 !important; }
    .Grün { border-left: 3px solid #00FF00 !important; }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # 2. BERECHNUNGS-LOGIK (MÄCHTIG)
    # ==========================================================================
    try:
        # Basis Infos
        seal = data['identity']['seal']['name']
        tone_name = data['identity']['tone']['name']
        tone_val = data['identity']['tone']['id']
        seal_color = data['identity']['seal']['color']
        
        # --- Harmonik (4-Tage Zyklus) ---
        h_idx = ((kin - 1) // 4) + 1
        h_pos = ((kin - 1) % 4) + 1
        h_cols = ["Rot", "Weiß", "Blau", "Gelb"]
        h_col = h_cols[(h_idx - 1) % 4]
        
        # --- Chromatik (5-Tage Zyklus) ---
        # Chromatiken wechseln die Farbe basierend auf dem Start-Kin
        c_pos = ((kin - 1) % 5) + 1
        # Farbe der Chromatik bestimmt sich oft durch das leitende Siegel
        # Vereinfacht: Rot-Weiß-Blau-Gelb Rotation
        c_idx_abs = (kin - 1) // 5
        c_col = ["Rot", "Weiß", "Blau", "Gelb"][c_idx_abs % 4]
        
        # --- Welle (13-Tage Zyklus) ---
        w_pos = ((kin - 1) % 13) + 1
        w_name = data['time']['wavespell']
        # Die Farbe der Welle ist die Farbe des Siegels auf Ton 1
        w_start_kin = kin - (w_pos - 1)
        # Kurzer Hack um Farbe von Ton 1 zu bekommen:
        w_col = ["Rot", "Weiß", "Blau", "Gelb"][(w_start_kin - 1) % 4]

        # --- Zeitzelle (4 Siegel pro Zelle) ---
        # 1-4 (Eingang), 5-8 (Speicher), 9-12 (Prozess), 13-16 (Ausgang), 17-20 (Matrix)
        s_id = data['identity']['seal']['id']
        cell_idx = (s_id - 1) // 4
        cells = [
            ("Eingang", "Rot"), 
            ("Speicher", "Weiß"), 
            ("Prozess", "Blau"), 
            ("Ausgang", "Gelb"), 
            ("Matrix", "Grün")
        ]
        cell_dat = cells[cell_idx % 5]

        # --- Schloss (52-Tage Zyklus) ---
        cas_idx = (kin - 1) // 52
        cas_pos = ((kin - 1) % 52) + 1
        castles = [
            ("Drehung (Rot)", "Rot"), 
            ("Kreuzung (Weiß)", "Weiß"), 
            ("Verbrennung (Blau)", "Blau"), 
            ("Geben (Gelb)", "Gelb"), 
            ("Verzauberung (Grün)", "Grün")
        ]
        cas_dat = castles[cas_idx % 5]

        # --- Season (65-Tage Zyklus) ---
        # 4 Seasons im Tzolkin (260 / 4 = 65)
        sea_idx = (kin - 1) // 65
        sea_pos = ((kin - 1) % 65) + 1
        seasons = [
            ("Lebenskraft (Ost)", "Rot"),
            ("Liebe (Nord)", "Weiß"), # In manchen Logiken Nord=Weiß
            ("Magie (West)", "Blau"),
            ("Erleuchtung (Süd)", "Gelb")
        ]
        sea_dat = seasons[sea_idx % 4]

    except Exception as e:
        st.error(f"Berechnungsfehler: {e}")
        return

    # ==========================================================================
    # 3. HELPER FÜR GRID-ANZEIGE
    # ==========================================================================
    def mini_card(label, val, sub, color):
        st.markdown(f"""
        <div class='mini-box {color}'>
            <div class='nav-label'>{label}</div>
            <div class='nav-val'>{val}</div>
            <div class='nav-sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================================
    # 4. DAS HIGH-DENSITY GRID (4 Spalten)
    # ==========================================================================
    st.subheader("🧬 Zyklus-Matrix")
    
    # Reihe 1: Identität
    c1, c2, c3, c4 = st.columns(4)
    with c1: mini_card("Frequenz", f"KIN {kin}", "Tzolkin", seal_color)
    with c2: mini_card("Siegel", seal, f"Code {s_id}", seal_color)
    with c3: mini_card("Ton", tone_name, f"Power {tone_val}", "Weiß") # Ton ist meist neutral/Silber, hier Weiß
    with c4: mini_card("Farbe", seal_color, "Energie", seal_color)

    # Reihe 2: Kleine Zyklen
    c5, c6, c7, c8 = st.columns(4)
    with c5: mini_card("Harmonik", f"Index {h_idx}", f"{h_pos}/4 Takt", h_col)
    with c6: mini_card("Chromatik", f"{c_col}e", f"{c_pos}/5 Tag", c_col)
    with c7: mini_card("Welle", w_name, f"{w_pos}/13 Ton", w_col)
    with c8: mini_card("Zeitzelle", cell_dat[0], f"{((s_id-1)%4)+1}/4", cell_dat[1])

    # Reihe 3: Große Zyklen
    c9, c10, c11, c12 = st.columns(4)
    with c9: mini_card("Schloss", cas_dat[0].split(' ')[0], f"{cas_pos}/52 Tag", cas_dat[1])
    with c10: mini_card("Season", sea_dat[0].split(' ')[0], f"{sea_pos}/65 Tag", sea_dat[1])
    with c11: 
        # Galaktischer Spin (Hälfte)
        spin = "Erster" if kin <= 130 else "Zweiter"
        st.markdown(f"<div class='mini-box Weiß'><div class='nav-label'>Spin</div><div class='nav-val'>{spin}</div><div class='nav-sub'>{kin}/260</div></div>", unsafe_allow_html=True)
    with c12:
        # Gap Indikator
        is_gap = data.get('time', {}).get('gap', False)
        gap_txt = "AKTIV" if is_gap else "Inaktiv"
        gap_col = "Grün" if is_gap else "Weiß"
        mini_card("Portal", gap_txt, "Alpha/Omega", gap_col)

