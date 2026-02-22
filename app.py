import streamlit as st
import requests
from textblob import TextBlob

# --- PIXEL THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000505;
        color: #00FFCC;
        font-family: 'Press Start 2P', cursive;
    }
    .stTextArea textarea { background-color: #111; color: #00FFCC; border: 2px solid #00FFCC; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛸 KEYLESS SPACE DASH")

tab_weather, tab_review, tab_fun = st.tabs(["🌤️ METEO", "📝 SCAN TEXT", "🎲 RANDOMIZER"])

# --- TAB 1: METEO (Still Keyless!) ---
with tab_weather:
    st.header("Sector: Irvine, CA")
    # No key needed for Open-Meteo
    res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=33.68&longitude=-117.83&current_weather=True").json()
    temp = res['current_weather']['temperature']
    st.metric("OUTSIDE TEMP", f"{temp}°C")

# --- TAB 2: AI TEXT SCANNER (No Key Needed) ---
with tab_review:
    st.header("📝 Paragraph Scanner")
    user_text = st.text_area("Drop your paragraph for a local scan:", placeholder="Type here...")
    
    if st.button("RUN ANALYSIS"):
        blob = TextBlob(user_text)
        
        # Spelling Correction
        corrected = blob.correct()
        st.subheader("🛠️ Auto-Correction:")
        st.write(str(corrected))
        
        # Sentiment Analysis (Is it positive or negative?)
        sentiment = blob.sentiment.polarity
        st.subheader("📊 Tone Scan:")
        if sentiment > 0.1: st.success("Mood: POSITIVE 🚀")
        elif sentiment < -0.1: st.error("Mood: NEGATIVE 🛰️")
        else: st.warning("Mood: NEUTRAL 🌑")

# --- TAB 3: COOL STUFF (No-Key Public APIs) ---
with tab_fun:
    st.header("🎲 Space boredom?)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("GET DOG IMAGE"):
            # Public API: No key needed
            dog_url = requests.get("https://dog.ceo/api/breeds/image/random").json()['message']
            st.image(dog_url, width=300)
            
    with col2:
        if st.button("RANDOM ACTIVITY"):
            # Public API: No key needed
            act = requests.get("https://www.boredapi.com/api/activity").json()['activity']
            st.info(f"TRY THIS: {act}")
