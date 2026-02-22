import streamlit as st
import requests
import random

# --- SPACE THEME ---
st.set_page_config(page_title="Space Dash v5", page_icon="🛰️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505;
        color: #39FF14;
        font-family: 'Press Start 2P', cursive;
    }
    .stTab { border: 2px solid #39FF14 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ SPACE STATION: IRVINE")

tab1, tab2, tab3 = st.tabs(["🌤️ METEO", "📝 WRITING HUB", "🎮 STATION FUN"])

# --- TAB 1: WEATHER (Irvine, CA) ---
with tab1:
    st.header("Scanning Local Sector...")
    # Coordinates for Irvine, CA
    lat, lon = 33.68, -117.83
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"
        data = requests.get(url).json()
        temp = data['current_weather']['temperature']
        st.metric("OUTSIDE TEMP", f"{temp}°C")
        
        if temp < 13:
            st.error("ALERT: COLD SECTOR. STAY IN THE HUB.")
        else:
            st.success("STATUS: CLEAR FOR EXTERIOR MISSION.")
    except:
        st.warning("Satellite connection weak...")

# --- TAB 2: WRITING HUB (The New AI Paragraph Reviewer) ---
with tab2:
    st.header("📝 Writing Scan")
    st.write("Enter your text to find 'Power Words' and check length.")
    
    user_text = st.text_area("Input Log:", height=150)
    
    if st.button("RUN SCAN"):
        words = user_text.split()
        word_count = len(words)
        
        # Classroom-safe Review Features
        st.info(f"📊 Word Count: {word_count}")
        
        # Suggesting 'Power Words' (Classroom Appropriate)
        cool_words = {"big": "massive", "happy": "jubilant", "sad": "melancholy", "cool": "impressive"}
        replacements = [f"Instead of '{k}', try '{v}'" for k, v in cool_words.items() if k in user_text.lower()]
        
        if replacements:
            st.subheader("💡 Vocabulary Power-Ups:")
            for r in replacements:
                st.write(r)
        else:
            st.write("Your vocabulary is looking solid, Cadet!")

# --- TAB 3: CLASSROOM FUN ---
with tab3:
    st.header("🎮 Break-Time Generator")
    
    if st.button("GENERATE BRAIN BREAK"):
        breaks = [
            "Do 10 jumping jacks! 🏃‍♂️",
            "Sketch a 1-minute alien in your notebook. 👽",
            "Stare at the furthest thing you can see for 20 seconds. 👁️",
            "Write one thing you're excited for today. 🌟"
        ]
        st.info(random.choice(breaks))
