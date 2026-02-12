import streamlit as st

def get_name():
    return "🔮 Orakel Stern (5-Kraft)"

def render(kin, data, db):
    # ==========================================================================
    # 1. MATHEMATIK ENGINE (Lokal für dieses Modul)
    # ==========================================================================
    def get_oracle_ids(k):
        # Basis-Werte (0-basiert für Mathe)
        s_idx = (k - 1) % 20
        t_idx = (k - 1) % 13
        
        # Helper: Kin aus Siegel-Index (0-19) und Ton-Index (0-12) finden
        def get_kin_from_st(s, t):
            return ((s * 13 + t * 240) % 260) + 1 # Chinesischer Restklassen-Trick oder Loop
            # Einfacher Loop zur Sicherheit:
            # for x in range(1, 261):
            #    if (x-1)%20 == s and (x-1)%13 == t: return x
            # return 0
        
        # Besserer Helper (Loop ist sicherer und schnell genug für 260)
        def find_k(s, t):
            for x in range(1, 261):
                if (x-1)%20 == s and (x-1)%13 == t: return x
            return k # Fallback

        # 1. ANALOG (Partner): Summe 19 (bei 0-Index) -> (19 - s)
        # Bsp: Drache(0) + Sonne(19) = 19. 
        analog_s = (19 - s_idx) % 20
        analog_k = find_k(analog_s, t_idx)

        # 2. ANTIPODE (Herausforderung): Differenz 10
        anti_s = (s_idx + 10) % 20
        anti_k = find_k(anti_s, t_idx)

        # 3. OCCULT (Verborgene Kraft): Summe 21 (Siegel) & 14 (Ton)
        # Kin Formel: 261 - Kin
        occ_k = 261 - k
        
        # 4. GUIDE (Führung): Abhängig vom Ton
        # Tabelle der Verschiebung (Siegel-Index Shift)
        # Ton 1,6,11: +0 | 2,7,12: +12 | 3,8,13: +4 | 4,9: -4 (+16) | 5,10: -12 (+8)
        shifts = {
            1:0, 6:0, 11:0,
            2:12, 7:12, 12:12,
            3:4, 8:4, 13:4,
            4:16, 9:16,
            5:8, 10:8
        }
        t_val = t_idx + 1
        shift = shifts.get(t_val, 0)
        guide_s = (s_idx + shift) % 20
        guide_k = find_k(guide_s, t_idx)

        return {
            "guide": guide_k,
            "analog": analog_k,
            "anti": anti_k,
            "occult": occ_k,
            "destiny": k
        }

    # ==========================================================================
    # 2. DATEN-ABRUF
    # ==========================================================================
    def get_full_obj(k_nr):
        return next((x for x in db if x.get('kin') == k_nr), None)

    ids = get_oracle_ids(kin)

    # ==========================================================================
    # 3. CSS DESIGN (Leuchtende Karten)
    # ==========================================================================
    st.markdown("""
    <style>
    /* Orakel Karte Design */
    .orc-card {
        background: #0e0e0e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        margin-bottom: 5px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .orc-role { font-size: 0.65em; text-transform: uppercase; color: #888; letter-spacing: 1px; margin-bottom: 4px; }
    .orc-kin { font-size: 1.1em; font-weight: bold; color: #fff; }
    .orc-name { font-size: 0.8em; color: #ccc; margin-top: 2px; height: 35px; display: flex; align-items: center; justify-content: center; line-height: 1.1;}
    
    /* Farb-Glows */
    .orc-Rot { border-top: 3px solid #FF3E3E; box-shadow: 0 -5px 15px rgba(255, 62, 62, 0.15); }
    .orc-Weiß { border-top: 3px solid #FFFFFF; box-shadow: 0 -5px 15px rgba(255, 255, 255, 0.15); }
    .orc-Blau { border-top: 3px solid #3E8EFF; box-shadow: 0 -5px 15px rgba(62, 142, 255, 0.15); }
    .orc-Gelb { border-top: 3px solid #FFD700; box-shadow: 0 -5px 15px rgba(255, 215, 0, 0.15); }
    
    /* Highlight für das Zentrum */
    .center-card { transform: scale(1.05); border: 1px solid #555; }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # 4. RENDER FUNKTION (Die Karte)
    # ==========================================================================
    def render_card(role, k_nr, is_center=False):
        obj = get_full_obj(k_nr)
        if not obj: return
        
        # Daten
        seal_name = obj['identity']['seal']['name']
        tone_name = obj['identity']['tone']['name']
        tone_rom = obj['identity']['tone']['name'] # Oder römische Zahl wenn verfügbar
        color = obj['identity']['seal']['color']
        
        # CSS Klasse
        extra_cls = "center-card" if is_center else ""
        
        # HTML Karte
        st.markdown(f"""
        <div class='orc-card orc-{color} {extra_cls}'>
            <div class='orc-role'>{role}</div>
            <div class='orc-kin'>KIN {k_nr}</div>
            <div class='orc-name'>{seal_name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Dropdown (Expander) mit ALLEN Fakten
        with st.expander("Details", expanded=False):
            # Identität
            st.markdown(f"**Ton:** {tone_name} ({obj['identity']['tone']['id']})")
            st.markdown(f"**Welle:** {obj['time']['wavespell']}")
            
            # Siegel Deep Dive
            s = obj['identity']['seal']
            st.caption("--- SIEGEL DATEN ---")
            st.write(f"🌍 **Familie:** {s.get('family', '-')}")
            st.write(f"🔥 **Clan:** {s.get('clan', '-')}")
            st.write(f"🪐 **Planet:** {s.get('planet', '-')}")
            st.write(f"🧘 **Chakra:** {s.get('chakra', '-')}")
            
            # Action/Power
            st.caption("--- ESSENZ ---")
            st.write(f"⚡ **Kraft:** {s.get('power', '-')}")
            st.write(f"🎬 **Aktion:** {s.get('action', '-')}")
            st.write(f"✨ **Essenz:** {s.get('essence', '-')}")

    # ==========================================================================
    # 5. LAYOUT (Das Stern/Kreuz Gitter)
    # ==========================================================================
    st.subheader("🔮 Orakel des Schicksals")
    
    # Reihe 1: GUIDE (Mitte)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        render_card("FÜHRUNG (Guide)", ids['guide'])
        
    # Reihe 2: ANTIPODE - DESTINY - ANALOG
    m1, m2, m3 = st.columns([1, 1.2, 1])
    with m1:
        render_card("HERAUSFORDERUNG", ids['anti'])
    with m2:
        render_card("DEIN KIN", ids['destiny'], is_center=True)
    with m3:
        render_card("PARTNER", ids['analog'])
        
    # Reihe 3: OCCULT (Mitte)
    b1, b2, b3 = st.columns([1, 1.2, 1])
    with b2:
        render_card("VERBORGENE KRAFT", ids['occult'])

