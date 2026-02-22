import streamlit as st
import requests
import os

# --- NEW: AUTOMATIC FIX FOR TEXTBLOB ERRORS ---
try:
    from textblob import TextBlob
    # This line forces the download of the "brains" TextBlob needs
    import nltk
    nltk.download('punkt_set')
    nltk.download('punkt')
    nltk.download('wordnet')
except Exception:
    # If it fails, we try to run the official download command
    os.system("python -m textblob.download_corpora")
    from textblob import TextBlob

# --- THEME & SETUP ---
st.set_page_config(page_title="Space Dash v4", page_icon="🛸")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505;
        color: #00FFCC;
        font-family: 'Press Start 2P', cursive;
    }
    .stMetric { background: #111; border: 2px solid #00FFCC; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛸 SPACE DASH v4.0")

tab1, tab2 = st.tabs(["🌤️ METEO SCAN", "📝 TEXT ANALYZER"])

# --- WEATHER ---
with tab1:
    st.header("Sector: Irvine, CA")
    try:
        res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=33.68&longitude=-117.83&current_weather=True").json()
        temp = res['current_weather']['temperature']
        st.metric("CURRENT TEMP", f"{temp}°C")
        if temp > 15: st.success("STATUS: GO OUTSIDE 👨‍🚀")
        else: st.error("STATUS: STAY INSIDE 🛰️")
    except:
        st.warning("Satellite connection lost. Check internet.")

# --- TEXT ANALYZER ---
with tab2:
    st.header("📝 Writing Scan")
    user_input = st.text_area("Paste paragraph:", placeholder="Enter mission logs...")
    
    if st.button("RUN ANALYSIS"):
        if user_input:
            blob = TextBlob(user_input)
            
            # 1. Spelling Check
            st.subheader("🛠️ Correction:")
            st.write(str(blob.correct()))
            
            # 2. Tone Check
            st.subheader("📊 Tone:")
            polarity = blob.sentiment.polarity
            if polarity > 0: st.write("Positive Vibes! 🚀")
            elif polarity < 0: st.write("Negative Vibes... 🌑")
            else: st.write("Neutral Tone. 🛰️")
        else:
            st.info("Input data required for scan.")
