import streamlit as st
import math

# ==============================================================================
# 1. VISUAL FX ENGINE (Wild Wave CSS)
# ==============================================================================
def inject_wave_css():
    st.markdown("""
        <style>
        /* --- WILD WAVE ANIMATION --- */
        @keyframes wild-flux {
            0% { background-position: 0% 50%; }
            25% { background-position: 100% 0%; }
            50% { background-position: 100% 100%; }
            75% { background-position: 0% 100%; }
            100% { background-position: 0% 50%; }
        }

        /* Der Container für den Button */
        .wave-container {
            position: relative;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.2);
        }

        /* Der wilde Hintergrund */
        .wave-bg {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            /* Neon-Wildheit */
            background: linear-gradient(120deg, #ff0080, #ff8c00, #40e0d0, #9932cc, #ff0080);
            background-size: 300% 300%;
            animation: wild-flux 3s linear infinite;
            opacity: 0.8;
            z-index: 0;
        }

        /* Overlay für Lesbarkeit */
        .wave-overlay {
            position: relative;
            z-index: 1;
            background: rgba(0,0,0,0.6); /* Abdunklung */
            padding: 15px;
            backdrop-filter: blur(2px);
        }

        /* Progress Bar Container */
        .progress-track {
            background: rgba(255,255,255,0.2);
            height: 6px;
            border-radius: 3px;
            margin-top: 10px;
            overflow: hidden;
        }

        /* Der Füllstand */
        .progress-fill {
            height: 100%;
            background: #fff;
            box-shadow: 0 0 10px #fff;
            transition: width 0.5s ease;
        }

        /* Text Styles */
        .wave-label {
            font-family: 'Rajdhani', sans-serif;
            text-transform: uppercase;
            font-size: 0.85rem;
            color: #ccc;
            letter-spacing: 2px;
        }
        .wave-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.4rem;
            font-weight: bold;
            color: #fff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
            margin: 2px 0;
        }
        
        /* Expander Clean-Up */
        div[data-testid="stExpander"] {
            border: none;
            background: transparent;
        }
        /* Verstecke den Standard-Expander Header komplett, wir bauen einen eigenen */
        div[data-testid="stExpander"] > details > summary {
            display: none !important; /* Brutal hidden */
        }
        /* Für Browser die das nicht mögen, machen wir ihn unsichtbar */
        div[data-testid="stExpander"] > details > summary:first-child {
            list-style: none;
            visibility: hidden;
            height: 0;
            padding: 0;
        }
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. WAVE LOGIC (Die Mathematik der 13)
# ==============================================================================
def calculate_wave_context(current_kin_num):
    """
    Berechnet Start, Ziel und Charakter der Welle basierend auf dem aktuellen Kin.
    """
    # 1. Wo sind wir? (0-basiert rechnen)
    kin_idx = current_kin_num - 1
    
    # 2. Start der Welle (Der Magnetische Ton 1)
    # Formel: Abrunden auf das nächste Vielfache von 13
    wave_start_idx = (kin_idx // 13) * 13
    wave_start_kin = wave_start_idx + 1
    
    # 3. Position in der Welle (1-13)
    current_tone = (kin_idx % 13) + 1
    progress_percent = (current_tone / 13) * 100
    
    # 4. Charakter der Welle (Bestimmt durch das Magnetische Siegel)
    # Wir müssen das Siegel des Start-Kins berechnen
    # Kin 1=Imix(0), Kin 2=Ik(1)... 
    start_seal_id = (wave_start_idx % 20) 
    
    seal_names = [
        "Drache", "Wind", "Nacht", "Samen", "Schlange", "Weltenüberbrücker", "Hand",
        "Stern", "Mond", "Hund", "Affe", "Mensch", "Himmelswanderer", "Magier",
        "Adler", "Krieger", "Erde", "Spiegel", "Sturm", "Sonne"
    ]
    
    wave_name = f"Welle des {seal_names[start_seal_id]}"
    
    # Castle (Schloss) Berechnung (52 Tage Zyklen)
    castle_idx = kin_idx // 52
    castles = ["Rot (Start)", "Weiß (Läuterung)", "Blau (Transformation)", "Gelb (Reifen)", "Grün (Verzauberung)"]
    castle_name = castles[castle_idx]

    return {
        "name": wave_name,
        "start_kin": wave_start_kin,
        "end_kin": wave_start_kin + 12,
        "current_tone": current_tone,
        "progress": progress_percent,
        "castle": castle_name,
        "magnetic_seal_id": start_seal_id + 1 # 1-basiert für Ausgabe
    }

# ==============================================================================
# 3. RENDERER
# ==============================================================================
def render(pulse):
    inject_wave_css()
    
    meta = pulse['metadata']
    if meta['is_leap_day']:
        st.info("Hunab Ku: Keine Welle. Die Zeit steht still.")
        return

    # Daten berechnen
    wave = calculate_wave_context(meta['kin'])
    
    # --- DER "CUSTOM" BUTTON (Container) ---
    # Wir nutzen einen Trick: Ein Container, der aussieht wie der Button.
    # Darunter ein Expander, der standardmäßig "unsichtbar" ist, aber wir nutzen
    # Streamlits Expander Logik.
    # Da wir den Button visuell komplett customizen wollen, nutzen wir den Expander
    # als "Wrapper", aber wir müssen akzeptieren, dass man auf den kleinen Pfeil klicken muss
    # ODER wir bauen den Header direkt IN den Expander Label (was wir vorher gemacht haben).
    # Lass uns die bewährte Methode nehmen: Expander Label stylen.
    
    # Aber du wolltest "wild". Standard Expander Labels sind limitiert.
    # Neuer Ansatz: Wir rendern HTML für den Button.
    
    # A. DIE VISUELLE BAR (HTML)
    st.markdown(f"""
        <div class="wave-container">
            <div class="wave-bg"></div>
            <div class="wave-overlay">
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div class="wave-label">ZEIT-WELLE {wave['start_kin']} - {wave['end_kin']}</div>
                        <div class="wave-title">{wave['name']}</div>
                    </div>
                    <div style="font-size:2rem; font-weight:bold; color:#fff;">{wave['current_tone']}<span style="font-size:1rem; opacity:0.6;">/13</span></div>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: {wave['progress']}%;"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # B. DER DEEP DIVE (Expander darunter)
    # Wir beschriften ihn "Wellen-Analyse öffnen", damit man weiß wo man klicken muss
    with st.expander(f"🌊 ANALYSE: {wave['name']} öffnen", expanded=False):
        
        # 1. Die Strategie der Welle
        st.markdown(f"### 🏰 {wave['castle']} Schloss")
        st.caption("Der übergeordnete 52-Tage-Kontext")
        
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**🏁 START (Magnetisch)**\n\nKin {wave['start_kin']}\nDefiniert das Ziel und den Zweck der 13 Tage.")
        with c2:
            st.success(f"**🚀 ZIEL (Kosmisch)**\n\nKin {wave['end_kin']}\nDer Flug ins nächste Level (Transzendenz).")
            
        st.divider()
        
        # 2. Psychologie der Welle (Abgeleitet vom Magnetischen Siegel)
        # Wir holen uns die Daten des AKTUELLEN Siegels aus dem Pulse, 
        # aber eigentlich bräuchten wir die Daten des MAGNETISCHEN Siegels.
        # Da wir im Pulse nur das aktuelle Kin haben, geben wir eine generelle Deutung
        # oder nutzen das aktuelle Siegel als "Beitrag zur Welle".
        
        # Smart Move: Wir erklären, was der HEUTIGE Tag für die Welle bedeutet.
        
        tone_data = pulse['tzolkin']['identity']['tone']
        seal_data = pulse['tzolkin']['identity']['seal']
        
        st.markdown(f"### 📍 Heute: Tag {wave['current_tone']} ({tone_data['name']})")
        st.write(f"Die Funktion des heutigen Tages in der Welle:")
        
        # Dynamische Deutung basierend auf dem Ton
        wave_functions = {
            1: "Zweck finden. Was zieht mich an?",
            2: "Herausforderung erkennen. Was sind die Hindernisse?",
            3: "Aktivierung. Der erste Schritt ins Tun.",
            4: "Formgebung. Den Plan definieren.",
            5: "Strahlkraft. Die Ressourcen sammeln (Empowerment).",
            6: "Balance. Den Rhythmus finden und organisieren.",
            7: "Einstimmung. Der Kanal öffnet sich (Mystik).",
            8: "Harmonisierung. Die Integrität prüfen (Walk your Talk).",
            9: "Absicht. Der letzte Schub vor der Manifestation.",
            10: "Perfektionierung. Das Ergebnis wird sichtbar.",
            11: "Auflösung. Loslassen und Bereinigen (Dissonanz).",
            12: "Zusammenkunft. Das Fazit ziehen (Kristallklar).",
            13: "Präsenz. Der magische Flug (Feiern & Ruhe)."
        }
        
        daily_mission = wave_functions.get(wave['current_tone'], "Sein.")
        
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.1); padding:15px; border-left:4px solid #fff; border-radius:4px;">
            <strong style="font-size:1.1rem; color:#fff;">"{daily_mission}"</strong>
            <p style="margin-top:5px; color:#ccc;">
                Heute trägt der <strong>{seal_data['name']}</strong> diese Energie bei.<br>
                <em>Kraft: {seal_data.get('power','')} | Aktion: {seal_data.get('action','')}</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # 3. DNA / I-Ging Link (Wenn vorhanden)
        # Das ist "Alles was in der Datenbank steht"
        matrix = pulse['tzolkin'].get('matrix', [])
        if matrix:
            st.caption("📡 Synchronotron Daten-Link aktiv")
