# ==============================================================================
# 🌀 CORE MODULE 1: MATH-ENGINE (Ultimate Logic)
# Aufgabe: Berechnung nach 'Ultimative Dreamspell Logik.md'.
# Iterative Zählung (Tag für Tag) mit Hunab Ku (29.2.) Filter.
# ==============================================================================
import datetime

class MathEngine:
    """Die mathematische Konstante der Zeit (Dreamspell Logic)."""

    ANCHOR_DATE = datetime.date(1986, 5, 19)
    ANCHOR_KIN = 121

    @staticmethod
    def get_kin(d, m, y):
        """
        Berechnet das KIN. Schalttage (29.2.) ergeben 0 (Hunab Ku).
        Nutzt die iterative Zählmethode für maximale Präzision.
        """
        # Hunab Ku Check
        if m == 2 and d == 29:
            return 0
            
        target_date = datetime.date(y, m, d)
        current = MathEngine.ANCHOR_DATE
        
        # Zähler für die "Dreamspell-Tage" (ohne 29.2.)
        delta_days = 0
        
        # Fall 1: Ziel liegt in der Zukunft (nach Anker)
        if target_date >= MathEngine.ANCHOR_DATE:
            while current < target_date:
                # Wenn heute NICHT der 29.2. ist, erhöhen wir den Zähler
                if not (current.month == 2 and current.day == 29):
                    delta_days += 1
                current += datetime.timedelta(days=1)
            
            # Formel: (Start + Delta - 1) % 260 + 1
            kin = (MathEngine.ANCHOR_KIN + delta_days - 1) % 260 + 1
            
        # Fall 2: Ziel liegt in der Vergangenheit (vor Anker)
        else:
            while current > target_date:
                current -= datetime.timedelta(days=1)
                # Rückwärts zählen, aber 29.2. ignorieren
                if not (current.month == 2 and current.day == 29):
                    delta_days += 1
            
            # Formel Rückwärts: (Start - Delta - 1) % 260 + 1
            kin = (MathEngine.ANCHOR_KIN - delta_days - 1) % 260 + 1
            
        return int(kin)

    @staticmethod
    def get_ids(kin):
        """Wandelt KIN in Siegel-ID (1-20) und Ton-ID (1-13)."""
        if kin == 0: return 0, 0
        s_id = (kin - 1) % 20 + 1
        t_id = (kin - 1) % 13 + 1
        return int(s_id), int(t_id)

    @staticmethod
    def _find_kin(s_id, t_id):
        """Hilfsfunktion: Findet KIN aus Siegel & Ton."""
        for k in range(1, 261):
            if (k - 1) % 20 + 1 == s_id and (k - 1) % 13 + 1 == t_id:
                return k
        return 0

    @staticmethod
    def get_oracle_kin_ids(kin):
        """
        Berechnet das Orakel basierend auf der 'Ultimative Dreamspell Logik'.
        Gibt KIN-Nummern zurück (wichtig für spätere 3D-Positionierung).
        """
        if kin == 0: return None
        s_id, t_id = MathEngine.get_ids(kin)

        # 1. ANALOG (Partner)
        # Logik aus Datei: 19 - Seal. Ausnahme 19/20.
        if s_id == 19:
            analog_s = 20
        elif s_id == 20:
            analog_s = 19
        else:
            analog_s = 19 - s_id
        
        # Analog hat im Dreamspell denselben Ton
        analog_kin = MathEngine._find_kin(analog_s, t_id)

        # 2. ANTIPODE (Herausforderung)
        # Logik aus Datei: (Seal + 10) % 20
        antipode_s = (s_id + 10) % 20
        if antipode_s == 0: antipode_s = 20
        # Antipode hat denselben Ton
        antipode_kin = MathEngine._find_kin(antipode_s, t_id)

        # 3. OKKULT (Verborgene Kraft)
        # Logik aus Datei: 21 - Seal
        occ_s = 21 - s_id
        # Okkulter Ton: Summe muss 14 ergeben
        occ_t = 14 - t_id
        occ_kin = MathEngine._find_kin(occ_s, occ_t)

        # 4. GUIDE (Führung)
        # Logik aus Datei: Shift-Tabelle
        guide_shift = {
            1: 0, 6: 0, 11: 0,
            2: 12, 7: 12, 12: 12,
            3: 4, 8: 4, 13: 4,
            4: 16, 9: 16,
            5: 8, 10: 8
        }
        guide_s = (s_id + guide_shift.get(t_id, 0) - 1) % 20 + 1
        # Guide hat denselben Ton
        guide_kin = MathEngine._find_kin(guide_s, t_id)

        return {
            "guide": guide_kin,
            "analog": analog_kin,
            "anti": antipode_kin,
            "occult": occ_kin
        }

# ==============================================================================
# 🛠 INTERAKTIVES TERMINAL (Admin-Modus)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "═"*50)
    print("🌀 MATH-ENGINE (ULTIMATE LOGIC CHECK)")
    print("Berechnung: Iterativ (Tag für Tag) ab Anker 19.5.1986")
    print("═"*50)

    while True:
        entry = input("\nDatum eingeben (DD.MM.YYYY) oder 'exit': ").strip()
        if entry.lower() == 'exit': break
        
        try:
            d, m, y = map(int, entry.split('.'))
            k = MathEngine.get_kin(d, m, y)
            
            if k == 0:
                print("-> 🟢 HUNAB KU (29.02. - Tag außerhalb der Zeit)")
            else:
                s, t = MathEngine.get_ids(k)
                o = MathEngine.get_oracle_kin_ids(k)
                print(f"-> KIN {k} | Siegel {s} | Ton {t}")
                print(f"   GUIDE:  Kin {o['guide']}")
                print(f"   ANALOG: Kin {o['analog']} | ANTI: Kin {o['anti']}")
                print(f"   OKKULT: Kin {o['occult']}")
                
        except ValueError:
            print("❌ Fehler: Bitte Format DD.MM.YYYY nutzen.")
        except Exception as e:
            print(f"❌ Systemfehler: {e}")
