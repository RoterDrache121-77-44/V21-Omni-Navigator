import streamlit as st

def render(pulse):
    # 1. Daten extrahieren
    tzolkin = pulse['tzolkin']
    meta = pulse['metadata']
    moon = pulse['moon']
    
    # Name für den kompakten Header (z.B. "KIN 67: Lunare Blaue Hand")
    header_title = f"KIN {meta['kin']}: {tzolkin['identity']['name']}"
    # Subtext (Datum & Mond)
    subtext = f"{meta['date_str']} • {moon['moon']['name']}"
    
    # 2. UI-Farbe bestimmen (Basis für den Puls-Effekt)
    ui_color_name = tzolkin.get('identity', {}).get('seal', {}).get('color', 'Weiß')
    
    # Definition der pulsierenden Gradienten
    # Wir nehmen die Hauptfarbe und verschieben sie leicht ins Helle/Dunkle für den Puls
    gradients = {
        "Rot": "linear-gradient(90deg, #FF3E3E, #FF6B6B, #FF3E3E)",
        "Weiß": "linear-gradient(90deg, #E0E0E0, #FFFFFF, #E0E0E0)",
        "Blau": "linear-gradient(90deg, #2A8CFF, #5CADFF, #2A8CFF)",
        "Gelb": "linear-gradient(90deg, #FFD700, #FFE066, #FFD700)",
        "Grün": "linear-gradient(90deg, #00FF66, #66FF99, #00FF66)" # Fallback
    }
    
    # Standard-Gradient wählen, falls Farbe nicht erkannt wird
    active_gradient = gradients.get(ui_color_name, gradients["Weiß"])

    # 3. Das animierte CSS & HTML
    st.markdown(f"""
        <style>
        /* Definition der Puls-Animation */
        @keyframes pulse-flux {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Der kompakte Header-Container */
        .header-flux-strip {{
            /* Hier wird der pulsierende Gradient als Hintergrund gesetzt */
            background: {active_gradient};
            background-size: 200% 200%; /* Wichtig für die Bewegung */
            animation: pulse-flux 3s ease infinite; /* Die Animation (3s Dauer) */
            
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 15px;
            
            /* Flexbox für eine saubere Zeile */
            display: flex;
            justify-content: space-between;
            align-items: center;
            
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        .flux-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            font-weight: bold;
            color: #000; /* Schwarze Schrift auf farbigem Grund */
            margin: 0;
        }}
        
        .flux-meta {{
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.9rem;
            color: #222; /* Dunkelgrau für Subtext */
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        </style>

        <div class="header-flux-strip">
            <div class="flux-title">{header_title}</div>
            <div class="flux-meta">{subtext}</div>
        </div>
    """, unsafe_allow_html=True)
