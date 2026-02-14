# ==============================================================================
# 🧬 GALACTIC ENGINE CORE (V21)
# ------------------------------------------------------------------------------
# ZWECK:    Zentrale Daten-Verwaltung & Berechnung ("The Single Source of Truth")
# AUTOR:    Hunab Ku 21 Mentor
# STATUS:   SOLID STATE (Production Ready)
# ------------------------------------------------------------------------------
# HIER GILT DAS GESETZ DER TRENNUNG:
# Strang A (Tzolkin) = Berechnet via MathEngine
# Strang B (13 Moon) = Nachgeschlagen via JSON Lookup
# ==============================================================================

import json
import datetime
import streamlit as st
from pathlib import Path
from math_engine import MathEngine  # Wir importieren deinen existierenden Rechner

# ------------------------------------------------------------------------------
# KONFIGURATION & PFADE
# ------------------------------------------------------------------------------
DB_PATH_TZOLKIN = "db_tzolkin_v21_enriched_FINAL.json"
DB_PATH_MOON = "db_13moon_v22_enriched_FINAL.json"

class GalacticCore:
    """
    Der Maschinenraum. Lädt Datenbanken und erstellt den 'Pulse'.
    """

    @staticmethod
    @st.cache_data
    def load_databases():
        """
        Lädt die JSON-Akasha-Chroniken in den Speicher.
        Nutzt Streamlit-Caching für maximale Performance.
        """
        try:
            with open(DB_PATH_TZOLKIN, 'r', encoding='utf-8') as f:
                tzolkin_db = json.load(f)
            
            with open(DB_PATH_MOON, 'r', encoding='utf-8') as f:
                moon_db = json.load(f)
                
            return tzolkin_db, moon_db
            
        except FileNotFoundError as e:
            st.error(f"❌ KRITISCHER FEHLER: Datenbank nicht gefunden! {e}")
            st.stop()
        except json.JSONDecodeError as e:
            st.error(f"❌ SYNTAX FEHLER: JSON ist beschädigt. {e}")
            st.stop()

    @staticmethod
    def get_pulse(target_date: datetime.date):
        """
        Die MAGISCHE FUNKTION.
        Erstellt das 'pulse' Objekt (Data Contract), das die ganze App versorgt.
        """
        # 1. Datenbanken holen (Cached)
        db_tzolkin, db_moon = GalacticCore.load_databases()

        # ----------------------------------------------------------------------
        # STRANG A: TZOLKIN (Das "WER") -> Mathematik
        # ----------------------------------------------------------------------
        kin_num = MathEngine.get_kin(target_date.day, target_date.month, target_date.year)
        
        # Sonderfall: Hunab Ku (0.0. Hunab Ku)
        is_leap_day = (kin_num == 0)
        
        if is_leap_day:
            # Notfall-Daten für den Schalttag (damit die App nicht crasht)
            tzolkin_data = {
                "kin": 0,
                "identity": {
                    "name": "Hunab Ku (0.0)", 
                    "seal": {"name": "Hunab Ku", "color": "Grün"},
                    "tone": {"name": "Null", "id": 0}
                },
                "oracle": None, # Kein Orakel am Schalttag
                "message": "Der Tag außerhalb der Zeitmatrix."
            }
        else:
            # Normaler Lookup (Kin 1 = Index 0)
            # Sicherheits-Check: Kin muss zwischen 1 und 260 liegen
            safe_index = (kin_num - 1) % 260
            tzolkin_data = db_tzolkin[safe_index]

        # ----------------------------------------------------------------------
        # STRANG B: 13 MOON (Das "WO") -> Kalender-Lookup
        # ----------------------------------------------------------------------
        # Wir suchen den Eintrag für "DD.MM"
        search_key = f"{target_date.day:02d}.{target_date.month:02d}"
        
        # Linearer Scan durch die 13-Monde-DB (Schnell genug für 366 Einträge)
        moon_data = next((item for item in db_moon if item["date_gregorian"] == search_key), None)

        if not moon_data:
            # Fallback, falls DB unvollständig
            moon_data = {"error": f"Kein Eintrag für {search_key} gefunden."}

        # ----------------------------------------------------------------------
        # PULSE ASSEMBLIERUNG (Der Daten-Vertrag)
        # ----------------------------------------------------------------------
        pulse = {
            "metadata": {
                "date_object": target_date,
                "date_str": target_date.strftime("%d.%m.%Y"),
                "kin": kin_num,
                "is_leap_day": is_leap_day,
                "is_day_out_of_time": moon_data.get("special_markers", {}).get("is_day_out_of_time", False)
            },
            "tzolkin": tzolkin_data,
            "moon": moon_data
        }

        return pulse

# ==============================================================================
# 🛠 TERMINAL-CHECK (Nur ausführbar, wenn Datei direkt gestartet wird)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "═"*60)
    print("🔋 ENGINE CORE TEST (Boot Sequence)")
    print("═"*60)
    
    # Test 1: Heute
    today = datetime.date.today()
    print(f"Test für Heute ({today}):")
    try:
        p = GalacticCore.get_pulse(today)
        print(f"✅ Pulse generiert.")
        print(f"   -> Kin: {p['metadata']['kin']}")
        print(f"   -> Name: {p['tzolkin']['identity']['name']}")
        print(f"   -> Mond: {p['moon']['moon']['name']}")
        print(f"   -> PSI:  {p['moon']['psi_chrono']}")
    except Exception as e:
        print(f"❌ FEHLER: {e}")

    # Test 2: Schalttag
    leap = datetime.date(2024, 2, 29)
    print(f"\nTest für Schalttag ({leap}):")
    p_leap = GalacticCore.get_pulse(leap)
    print(f"   -> Kin: {p_leap['metadata']['kin']} (Erwarte 0)")
    print(f"   -> Name: {p_leap['tzolkin']['identity']['name']}")
