import streamlit as st
import requests
import google.generativeai as genai

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="Space Dash v3", page_icon="🚀", layout="wide")

# Pixel-Space CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505;
        color: #39FF14;
        font-family: 'Press Start 2P', cursive;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #111;
        border: 2px solid #39FF14;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# API Keys (Set these in Streamlit Secrets!)
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.sidebar.warning("⚠️ Enter Gemini Key in Secrets to use AI features")

# --- 2. TABS ---
tab1, tab2, tab3 = st.tabs(["🌤️ METEO SCAN", "📝 AI REVIEW", "🌌 FOCUS MODE"])

# --- TAB 1: WEATHER (METEO) ---
with tab1:
    st.header("🛰️ Sector Weather Scan")
    # Default to Irvine, CA
    lat, lon = 33.68, -117.83
    
    res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True").json()
    temp = res['current_weather']['temperature']
    wind = res['current_weather']['windspeed']
    
    c1, c2 = st.columns(2)
    c1.metric("TEMP", f"{temp}°C")
    c2.metric("WIND", f"{wind} km/h")
    
    if temp < 10 or wind > 25:
        st.error("⚠️ STATION ALERT: INDOOR RECESS RECOMMENDED")
    else:
        st.success("✅ SCAN CLEAR: OUTDOOR ACTIVITY AUTHORIZED")

# --- TAB 2: AI PARAGRAPH REVIEWER ---
with tab2:
    st.header("📝 AI Writing Advisor")
    st.write("Paste your paragraph below for a friendly peer review.")
    
    text_input = st.text_area("Your Paragraph:", height=150, placeholder="Once upon a time in space...")
    
    if st.button("RUN SCAN"):
        if text_input and "GEMINI_KEY" in st.secrets:
            model = genai.GenerativeModel("gemini-1.5-flash")
            # Strict instructions for the AI
            prompt = (
                f"You are a helpful school writing assistant. Review this paragraph for grammar, "
                f"clarity, and flow. Give 3 short bullet points of advice. "
                f"STRICT RULE: Do NOT write the essay for the student. Do NOT answer test questions. "
                f"Text to review: {text_input}"
            )
            response = model.generate_content(prompt)
            st.info("📊 FEEDBACK SCAN COMPLETE:")
            st.markdown(response.text)
        else:
            st.warning("Please enter text and ensure API key is set.")

# --- TAB 3: FOCUS MODE ---
with tab3:
    st.header("🌌 Focus Deep Space")
    st.write("Turn on your shield and get to work.")
    
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        focus_time = st.slider("SET TIMER (MINS)", 5, 60, 25)
        if st.button("START MISSION"):
            st.toast("🚀 MISSION STARTED. STAY FOCUSED!")
            
    with col_r:
        # A simple embedded pixel-art or lofi video player
        st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk") # Lofi hip hop radio
