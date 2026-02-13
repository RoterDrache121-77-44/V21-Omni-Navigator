import streamlit as st

def render(state):
    """
    MODUL ORACLE (Synaptic Version)
    Berechnet das 5-teilige Schicksals-Orakel (Destiny, Analog, Antipode, Occult, Guide).
    """

    # -------------------------------------------------------------------------
    # 0. STATE UNPACKING
    # -------------------------------------------------------------------------
    kin_current = state.kin
    db_tzolkin = state.db.get('tzolkin', [])

    if kin_current == 0 or not db_tzolkin:
        return

    # -------------------------------------------------------------------------
    # 1. MATHEMATIK ENGINE (Lokal)
    # -------------------------------------------------------------------------
    def get_oracle_ids(k):
        # Basis-Werte (0-basiert für Mathe)
        # Kin 1 = Index 0
        s_idx = (k - 1) % 20
        t_idx = (k - 1) % 13
        
        # Helper: Finde KIN basierend auf Siegel-Index (0-19) und Ton-Index (0-12)
        # Wir nutzen Brute-Force über 260 Kins, das ist rasend schnell.
        def find_kin_by_st(target_s_idx, target_t_idx):
            for x in range(1, 261):
                if (x-1) % 20 == target_s_idx and (x-1) % 13 == target_t_idx:
                    return x
            return k # Fallback

        # 1. ANALOG (Partner / Support): Summe Siegel immer 19 (bei 0-Index)
        # Bsp: Drache(0) + Sonne(19) = 19
        analog_s = (19 - s_idx) % 20
        analog_k = find_kin_by_st(analog_s, t_idx)

        # 2. ANTIPODE (Herausforderung): Differenz 10
        anti_s = (s_idx + 10) % 20
        anti_k = find_kin_by_st(anti_s, t_idx)

        # 3. OCCULT (Verborgene Kraft): Magische Summe 261
        occ_k = 261 - k
        
        # 4. GUIDE (Führung): Abhängig vom Ton
        # Formel: Der Ton bleibt gleich. Das Siegel verschiebt sich.
        shifts = {
            1:0, 6:0, 11:0,         # Kraft des eigenen Siegels
            2:12, 7:12, 12:12,      # +12 Siegel
            3:4, 8:4, 13:4,         # +4 Siegel
            4:16, 9:16,             # +16 Siegel (oder -4)
            5:8, 10:8               # +8 Siegel
        }
        # Ton ist hier 1-basiert für das Dictionary
        shift = shifts.get(t_idx + 1, 0)
        guide_s = (s_idx + shift) % 20
        guide_k = find_kin_by_st(guide_s, t_idx)

        return {
            "destiny": k,
            "guide": guide_k,
            "analog": analog_k,
            "anti": anti_k,
            "occult": occ_k
        }

    # Berechnung durchführen
    ids = get_oracle_ids(kin_current)

    # -------------------------------------------------------------------------
    # 2. HELPER: DATEN HOLEN
    # -------------------------------------------------------------------------
    def get_kin_data(k_nr):
        # Direkter Index-Zugriff (Viel schneller als Suche)
        if 0 < k_nr <= 260:
            return db_tzolkin[k_nr - 1]
        return None

    # -------------------------------------------------------------------------
    # 3. CSS DESIGN (Glowing Cards)
    # -------------------------------------------------------------------------
    st.markdown("""
    <style>
    /* Orakel Karte Container */
    .orc-card {
        background: rgba(14, 14, 14, 0.8);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        margin-bottom: 5px;
        backdrop-filter: blur(5px);
        transition: transform 0.2s;
    }
    .orc-card:hover {
        transform: translateY(-2px);
    }
    
    /* Typografie */
    .orc-role { font-size: 0.65em; text-transform: uppercase; color: #888; letter-spacing: 1.5px; margin-bottom: 4px; }
    .orc-kin { font-size: 1.2em; font-weight: bold; color: #fff; text-shadow: 0 0 10px rgba(0,0,0,0.5); }
    .orc-name { font-size: 0.8em; color: #ccc; margin-top: 2px; height: 30px; display: flex; align-items: center; justify-content: center; line-height: 1.1;}
    
    /* Farb-Glows (Passend zur App) */
    .orc-Rot { border-top: 3px solid #FF3E3E; box-shadow: 0 -5px 20px rgba(255, 62, 62, 0.2); }
    .orc-Weiß { border-top: 3px solid #E0E0E0; box-shadow: 0 -5px 20px rgba(255, 255, 255, 0.15); }
    .orc-Blau { border-top: 3px solid #2A8CFF; box-shadow: 0 -5px 20px rgba(42, 140, 255, 0.2); }
    .orc-Gelb { border-top: 3px solid #FFD700; box-shadow: 0 -5px 20px rgba(255, 215, 0, 0.2); }
    .orc-Grün { border-top: 3px solid #00FF66; box-shadow: 0 -5px 20px rgba(0, 255, 102, 0.2); }
    
    /* Highlight für das Zentrum (Destiny Kin) */
    .center-card { 
        transform: scale(1.05); 
        border: 1px solid rgba(255,255,255,0.3); 
        background: rgba(30, 30, 40, 0.9);
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 4. RENDER FUNKTION (Einzelne Karte)
    # -------------------------------------------------------------------------
    def render_card(role, k_nr, is_center=False):
        obj = get_kin_data(k_nr)
        if not obj: return
        
        # Daten extrahieren
        seal_name = obj['identity']['seal']['name']
        tone_name = obj['identity']['tone']['name']
        color = obj['identity']['seal']['color']
        
        # CSS Klasse bauen
        extra_cls = "center-card" if is_center else ""
        
        # HTML Render
        st.markdown(f"""
        <div class='orc-card orc-{color} {extra_cls}'>
            <div class='orc-role'>{role}</div>
            <div class='orc-kin'>KIN {k_nr}</div>
            <div class='orc-name'>{seal_name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mini-Details (Expander)
        with st.expander("Info", expanded=False):
            st.caption(f"**Ton:** {tone_name}")
            st.caption(f"**Essenz:** {obj['identity']['seal'].get('essence', '-')}")
            st.caption(f"**Kraft:** {obj['identity']['seal'].get('power', '-')}")

    # -------------------------------------------------------------------------
    # 5. LAYOUT (Das Gitter)
    # -------------------------------------------------------------------------
    st.markdown("##### 🔮 ORAKEL DES SCHICKSALS")
    
    # Grid Layout: Das klassische Orakel-Kreuz
    # Reihe 1: GUIDE (Mitte)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        render_card("FÜHRUNG", ids['guide'])
        
    # Reihe 2: ANTIPODE - DESTINY - ANALOG
    m1, m2, m3 = st.columns([1, 1.2, 1])
    with m1:
        render_card("HERAUSFORDERUNG", ids['anti'])
    with m2:
        render_card("DESTINY KIN", ids['destiny'], is_center=True)
    with m3:
        render_card("PARTNER", ids['analog'])
        
    # Reihe 3: OCCULT (Mitte)
    b1, b2, b3 = st.columns([1, 1.2, 1])
    with b2:
        render_card("VERBORGENE KRAFT", ids['occult'])

    # -------------------------------------------------------------------------
    # 6. SYNAPTIC MEMORY (Für PDF Export)
    # -------------------------------------------------------------------------
    state.remember("oracle", ids)
