import streamlit as st
import datetime
import google.generativeai as genai

# --- CONFIGURATION ---
# Get your free key from https://aistudio.google.com/
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Student Dash", page_icon="🎓")

# Initialize custom tools memory
if 'custom_tools' not in st.session_state:
    st.session_state.custom_tools = []

st.title("🎒 My School Dashboard")

# Define Tabs
standard_tabs = ["🌤️ Weather", "🤖 AI Builder"]
dynamic_tabs = standard_tabs + [t['name'] for t in st.session_state.custom_tools]
all_tabs = st.tabs(dynamic_tabs)

# --- TAB 1: WEATHER (Existing) ---
with all_tabs[0]:
    st.header("Recess & Lunch Status")
    st.info("Check if it's an outdoor day!")
    # (Existing weather logic goes here)

# --- TAB 2: AI BUILDER (The New AI) ---
with all_tabs[1]:
    st.header("🤖 AI Tool Builder")
    st.write("Describe a new tool you want (e.g., 'a simple diary' or 'a coin flipper').")
    
    user_prompt = st.text_input("What should I build?")
    
    if st.button("Generate Tool"):
        if not user_prompt:
            st.warning("Tell me what to build first!")
        else:
            with st.spinner("Thinking..."):
                # SYSTEM INSTRUCTIONS: The "Filter"
                system_prompt = (
                    "You are a Python UI builder. Your only job is to write a brief 'st.write' "
                    "or 'st.text_input' style summary for a Streamlit app. "
                    "CRITICAL RULE: If the user asks a school-related question (homework, math, "
                    "essays, science facts), say: 'I cannot help with schoolwork. I only build tools.'"
                )
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{system_prompt}\n\nUser request: {user_prompt}")
                
                # Save the new tool
                st.session_state.custom_tools.append({
                    "name": user_prompt[:15], # Shorten name for the tab
                    "content": response.text
                })
                st.success("Tool created! Check the new tab at the top.")
                st.rerun()

# --- DYNAMIC TABS (Where the AI tools live) ---
for i, tool in enumerate(st.session_state.custom_tools):
    with all_tabs[len(standard_tabs) + i]:
        st.header(tool['name'])
        st.markdown(tool['content'])
