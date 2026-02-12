import streamlit as st

def get_name():
    return "🧬 Basis Navigator"

def render(kin, data, db):
    # Eigene CSS Styles für dieses Modul (optional)
    st.markdown("""
    <style>
    .nav-val { font-size: 1.4em; font-weight: bold; color: #fff; }
    .nav-label { font-size: 0.8em; color: #888; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

    # Daten extrahieren (sicher)
    try:
        seal = data['identity']['seal']['name']
        tone = data['identity']['tone']['name']
        color = data['identity']['seal']['color']
        wave = data['time']['wavespell']
        
        # Berechnung Harmonik/Chromatik für die Anzeige
        h_idx = ((kin - 1) // 4) + 1
        h_pos = ((kin - 1) % 4) + 1
        h_col = ["Rot", "Weiß", "Blau", "Gelb"][(h_idx-1)%4]
        
    except:
        st.error("Datenfehler im Navigator")
        return

    st.subheader("🧬 Navigator")
    
    # Das Layout
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
        <div class='glow-box {color}'>
            <div class='nav-label'>Energie</div>
            <div class='nav-val'>{seal}</div>
            <div style='margin-top:5px;'>{tone}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='glow-box {h_col}'>
            <div class='nav-label'>Harmonik {h_idx}</div>
            <div class='nav-val'>Takt {h_pos}/4</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='glow-box {color}'>
            <div class='nav-label'>Welle</div>
            <div class='nav-val'>{wave}</div>
            <div style='margin-top:5px;'>Zweck & Ziel</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Ein kleines Extra: Zeitzelle
        cell_idx = (data['identity']['seal']['id'] - 1) // 4
        cells = ["Eingang", "Speicher", "Prozess", "Ausgang", "Matrix"]
        cell_name = cells[cell_idx % 5]
        
        st.markdown(f"""
        <div class='glow-box Weiß'>
            <div class='nav-label'>Zeitzelle</div>
            <div class='nav-val'>{cell_name}</div>
        </div>
        """, unsafe_allow_html=True)
