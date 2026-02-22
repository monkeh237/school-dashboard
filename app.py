import streamlit as st
import requests
import datetime

# --- SPACE PIXEL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b0e14;
        background-image: radial-gradient(#ffffff 1px, transparent 1px);
        background-size: 50px 50px;
        color: #00ff00 !important;
        font-family: 'Press Start 2P', cursive;
    }
    
    h1, h2, h3, p, span, label {
        color: #00ff00 !important;
        text-shadow: 2px 2px #ff00ff;
    }

    .stButton>button {
        background-color: #ff00ff;
        color: white;
        border: 4px solid #ffffff;
        font-family: 'Press Start 2P', cursive;
        image-rendering: pixelated;
    }
    
    /* Scratch Block Style for Builder */
    .scratch-block {
        background: #4c97ff;
        border: 2px solid #3373cc;
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        color: white !important;
        text-shadow: none !important;
        font-size: 10px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SPACE DASH v2.0")

# --- OPEN-METEO WEATHER LOGIC ---
def get_meteo_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"
    try:
        response = requests.get(url).json()
        current = response['current_weather']
        return current['temperature'], current['windspeed']
    except:
        return 0, 0

# --- TABS ---
tab_weather, tab_scratch = st.tabs(["🌤️ METEO SCAN", "🧩 SCRATCH BUILDER"])

with tab_weather:
    st.header("PLANET EARTH STATUS")
    # Change these to your city's Lat/Lon
    lat = st.number_input("LATITUDE", value=40.71, step=0.01)
    lon = st.number_input("LONGITUDE", value=-74.00, step=0.01)
    
    temp, wind = get_meteo_weather(lat, lon)
    
    col1, col2 = st.columns(2)
    col1.metric("TEMP", f"{temp}°C")
    col2.metric("WIND", f"{wind} km/h")
    
    if temp > 10 and wind < 20:
        st.success("STATION STATUS: GO OUTSIDE 👨‍🚀")
    else:
        st.error("STATION STATUS: STAY INSIDE 🛰️")

with tab_scratch:
    st.header("SCRATCH 3.0 BUILDER")
    st.write("Drag (type) blocks to build a custom tool message!")
    
    # Simulate Scratch blocks with a dropdown
    block_type = st.selectbox("CHOOSE BLOCK", ["When Green Flag Clicked", "Say [Text]", "Wait [1] Secs"])
    input_text = st.text_input("BLOCK INPUT", "Hello Space!")
    
    if st.button("SNAP BLOCKS"):
        if 'blocks' not in st.session_state: st.session_state.blocks = []
        st.session_state.blocks.append(f"{block_type}: {input_text}")
    
    # Display the "Code Stack"
    for b in st.session_state.blocks:
        st.markdown(f'<div class="scratch-block">{b}</div>', unsafe_allow_html=True)
    
    if st.button("CLEAR CODE"):
        st.session_state.blocks = []
        st.rerun()
