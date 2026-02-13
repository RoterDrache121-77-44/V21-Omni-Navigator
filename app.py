import streamlit as st
import json
import datetime
import sys

# MODULE IMPORTE
# (Stelle sicher, dass mod_daily_kin.py im gleichen Ordner liegt)
import mod_daily_kin 

# ==============================================================================
# 🌌 CONFIG & GLOBAL CSS
# ==============================================================================
st.set_page_config(page_title="13:20 SYNC", page_icon="🧬", layout="centered")

def inject_global_css():
    st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 100%);
            color: #E0E0E0; font-family: 'Segoe UI', sans-serif;
        }
        /* Haptic Button Logic für Expander Global */
        .streamlit-expanderHeader {
            background-color: rgba(20, 20, 30, 0.8) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: transform 0.2s ease;
        }
        .streamlit-expanderHeader:hover { transform: scale(1.01); }
        .streamlit-expanderHeader:active { transform: scale(0.99); }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 📐 ENGINE (Die Logik bleibt hier oder in utils.py)
# ==============================================================================
class MathEngine:
    ANCHOR_DATE = datetime.date(1986, 5, 19) # Kin 121
    ANCHOR_KIN = 121

    @staticmethod
    def calculate_kin(day, month, year):
        if month == 2 and day == 29: return 0 
        target = datetime.date(year, month, day)
        current = MathEngine.ANCHOR_DATE
        days_diff = 0
        if target >= current:
            while current < target:
                current += datetime.timedelta(days=1)
                if not (current.month == 2 and current.day == 29): days_diff += 1
            return (MathEngine.ANCHOR_KIN + days_diff - 1) % 260 + 1
        else:
            while current > target:
                current -= datetime.timedelta(days=1)
                if not (current.month == 2 and current.day == 29): days_diff += 1
            return (MathEngine.ANCHOR_KIN - days_diff - 1) % 260 + 1

@st.cache_data
def load_db():
    try:
        with open('db_tzolkin_v21_enriched_FINAL.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return []

# ==============================================================================
# 🚀 MAIN CONTROLLER
# ==============================================================================
def main():
    inject_global_css()
    
    st.title("GALAXY SYNC 2.1")
    
    # 1. INPUT
    d_input = st.date_input("Datum wählen", datetime.date.today())
    
    # 2. LOGIC
    db = load_db()
    if not db: st.error("DB fehlt!"); st.stop()
    
    kin_today = MathEngine.calculate_kin(d_input.day, d_input.month, d_input.year)
    kin_data = db[kin_today - 1] if kin_today > 0 else None

    # 3. MODULE RENDERING
    # Hier rufen wir nur noch das Modul auf. App.py weiß nicht, wie es aussieht.
    export_stack = {}
    
    st.markdown("### 🔮 HEUTE")
    
    # MODUL 1: Daily Kin
    data_kin = mod_daily_kin.render(kin_today, kin_data)
    export_stack.update({"daily_kin": data_kin})

    # (Hier kommen später Modul 2, 3, 4 hin...)

if __name__ == "__main__":
    main()
