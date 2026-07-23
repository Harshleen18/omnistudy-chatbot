import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import pandas as pd
import io
import time

# ================= 1. ABSOLUTE CONTRAST INTERFACE CONFIGURATION =================
st.set_page_config(page_title="ZenStudy AI", page_icon="🎓", layout="wide")

# Theme state tracking
if "ui_theme" not in st.session_state: st.session_state.ui_theme = "Minimal White (Stark High-Contrast Light)"

# High-Contrast Color Variables Engine
if "White" in st.session_state.ui_theme:
    bg, text, card_bg, border, accent = "#FFFFFF", "#000000", "#F4F6F5", "#000000", "#008055"
    user_bubble, ai_bubble = "#E6F4EA", "#FFFFFF"
else:
    bg, text, card_bg, border, accent = "#000000", "#FFFFFF", "#111111", "#FFFFFF", "#10B981"
    user_bubble, ai_bubble = "#1A2E26", "#111111"

st.markdown(f"""
    <style>
    /* Absolute Contrast Global Rule Overrides */
    .stApp {{ background-color: {bg} !important; color: {text} !important; font-family: 'Poppins', 'Inter', sans-serif; }}
    p, span, label, h1, h2, h3, h4, h5, div {{ color: {text} !important; font-weight: 700 !important; }}
    
    /* Crisp Sidebar Formatting */
    .stSidebar {{ background-color: {card_bg} !important; border-right: 3px solid {border} !important; }}
    
    /* Highly Visible Custom Chat Cards */
    .chat-bubble-user {{ background-color: {user_bubble} !important; padding: 22px; border-radius: 20px 20px 4px 20px; margin: 15px 0; border: 3px solid {border} !important; }}
    .chat-bubble-ai {{ background-color: {ai_bubble} !important; padding: 22px; border-radius: 20px 20px 20px 4px; margin: 15px 0; border: 3px solid {border} !important; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }}
    
    /* Sleek Native Input Console Row with Emulated Plus & Speaker Nodes */
    .sleek-input-bar {{ display: flex; align-items: center; background: {card_bg}; border: 3px solid {border}; border-radius: 40px; padding: 12px 30px; margin: 25px 0; }}
    .bar-icon {{ font-size: 24px; margin: 0 15px; cursor: pointer; color: {accent} !important; }}
    
    /* Solid High Contrast Studio Buttons */
    div.stButton > button:first-child {{
        background: {accent} !important; color: #FFFFFF !important; border-radius: 35px !important; padding: 12px 32px !important; font-weight: 800 !important; border: 3px solid {border} !important; font-size: 1.1rem !important;
    }}
    div.stButton > button:first-child:hover {{ background: #000000 !important; color: #FFFFFF !important; transform: translateY(-1px); }}
    </style>
""", unsafe_allow_html=True)

# ================= 2. SECURE INTUITION AI CORE KEY HUB =================
API_KEY = "AQ.Ab8RN6IeciOdOo6ppwDAvP5_YnfGAEanztvhrr-7EN6PNGLg5w"
client = genai.Client(api_key=API_KEY)

# ================= 3. SYSTEM STATE CONTROLLER VARIABLES =================
if "messages" not in st.session_state: st.session_state.messages = []
if "folders" not in st.session_state: st.session_state.folders = {"Mathematics": ["Calculus_Formulae.pdf"], "Biology Streams": ["Cell_Notes.docx"]}
if "saved_chats" not in st.session_state: st.session_state.saved_chats = ["Session 1: Introduction to Calculus"]
if "weaknesses" not in st.session_state: st.session_state.weaknesses = {"Math Formulas": 85, "Debit Bookkeeping": 35, "Cell Diagrams": 90}
if "flash_flipped" not in st.session_state: st.session_state.flash_flipped = False
if "streak" not in st.session_state: st.session_state.streak = 7

# ================= 4. PREMIUM NAVIGATION SIDEBAR HUB =================
st.sidebar.markdown(f"## 🎓 ZenStudy AI")
st.sidebar.markdown(f"🔥 **Learning Streak:** {st.session_state.streak} Days Active")

# Main Navigation Matrix
menu_selection = st.sidebar.radio(
    "Academy Workspace Menu",
    [
        "Dashboard", "AI Teacher Core", "Study Materials Hub", "Virtual Classroom", 
        "Flashcard Center", "Mind Maps", "Quizzes & Tests", "Analytics Dashboard", 
        "Focus Zone", "Notes", "Saved Chats", "Settings"
    ]
)

# Folder Organizer Node inside Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("📁 **Subject Folder Hub**")
new_folder_title = st.sidebar.text_input("Enter New Subject Title:")
if st.sidebar.button("➕ Create Folder") and new_folder_title:
    if new_folder_title not in st.session_state.folders:
        st.session_state.folders[new_folder_title] = []
        st.sidebar.success(f"Added Folder: {new_folder_title}")

# ================= 5. CORE WORKSPACE ENVIRONMENT CONTROLLER ROUTER =================

# --- COMPONENT 1: DASHBOARD ---
if menu_selection == "Dashboard":
    st.markdown("## 📊 Personal Study Dashboard")
    d_col1, d_col2, d_col3 = st.columns(3)
    d_col1.metric("Overall Subject Mastery", "76%", "🔥 Scaling Up")
    d_col2.metric("Target Study Goals Due", "3 Tasks", "⚠️ Action Required")
    d_col3.metric("Recent Activities Logged", "12 Lessons", "✅ Highly Active")
    
    st.markdown("### 🎯 AI Recommendations & Learning Journey Insights")
    st.info("💡 **AI Teacher Insight:** Your diagnostic data shows vulnerability in 'Debit Bookkeeping'. Click on the 'Quizzes & Tests' section to run a customized practice mock exam.")

# --- COMPONENT 2: CUSTOMIZABLE AI TEACHER CORE ---
elif menu_selection == "AI Teacher Core":
    st.markdown("## 🧑‍🏫 Personalize and Build Your Virtual Teacher Profile")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        personality = st.selectbox("Choose Faculty Persona Profile:", [
            "Calm Teacher", "Friendly Teacher", "Strict Teacher", "Professor Mode", 
            "Storytelling Teacher", "Exam Coach", "Motivational Mentor", "Scientific Instructor", "Fairy Tale Explainer"
        ])
        voice_accent = st.selectbox("Choose Audio Voice Accent Style:", ["Indian Standard Accent", "British Classical Academic", "US Modern Radio Studio"])
        speak_rate = st.slider("Set Professor Lecture Speed Rate:", 0.8, 1.5, 1.0, 0.1)
    
    with t_col2:
        avatars = {"Calm Teacher": "🧘", "Strict Teacher": "🧑‍🏫📏", "Fairy Tale Explainer": "🧚✨", "Friendly Teacher": "🤗"}
        st.markdown(f"#### Active Instructor Image Avatar")
        st.markdown(f"<div style='font-size:120px; text-align:center;'>{avatars.get(personality, '🎓')}</div>", unsafe_allow_html=True)
        st.success(f"**Instructor Core Parameters Locked:** All classroom vectors initialized for teaching personality: **{personality}**.")

# --- COMPONENT 3: STUDY MATERIALS KNOWLEDGE INGESTION HUB ---
elif menu_selection == "Study Materials Hub":
    st.markdown("## 📁 Smart Multi-Format Knowledge Base Ingestion")
    st.write("Upload folders, assignments, previous year questions, handwritten snaps, or presentations to build your custom AI brain indexing segment:")
    
    uploaded_files = st.file_uploader("Drop any files here (PDFs, Notes, Snaps, PPTs):", type=["pdf", "png", "jpg", "jpeg", "txt", "docx", "pptx"], accept_multiple_files=True)
    target_fol = st.selectbox("Select Target Course Folder Allocation Slot:", list(st.session_state.folders.keys()))
    
    if st.button("🚀 Ingest Materials into Knowledge Base") and uploaded_files:
        for f in uploaded_files:
            st.session_state.folders[target_fol].append(f.name)
        st.success(f"🎉 Fully Scanned and Parsed {len(uploaded_files)} objects! Customized study roadmap created inside your folder slot: **'{target_fol}'**.")
        
    st.markdown("### 🗄️ System Ingested Repository Index Map")
    st.json(st.session_state.folders)

# --- COMPONENT 4: MAIN CENTRIC VIRTUAL CLASSROOM CHAT STATIONS ---
elif menu_selection == "Virtual Classroom":
    st.markdown("## 🏛️ High-Contrast Centric Virtual Classroom")
    
    # Display Chat
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user"><b>🧑‍🎓 Student Input:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-ai"><b>🧑‍🏫 ZenStudy Teacher Response:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
            
            # Sound Synthesis Action Node Row Button
            if st.button("🔊 Listen to Audio Lecture", key=f"tts_run_{idx}"):
                with st.spinner("Synthesizing audio output stream..."):
                    clean = msg["content"].replace("$", "").replace("#", "").replace("*", "")
                    tts = gTTS(text=clean, lang='en', tld='co.in' if "Light" in st.session_state.ui_theme else 'co.uk')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    st.audio(audio_fp.getvalue(), format="audio/mp3", autoplay=True)

    # Sleek Accessibility-Emulating Input Dashboard Bar Layout
    st.markdown(f"""
    <div class="sleek-input-bar">
        <span class="bar-icon">📎 <b>+ Upload</b></span>
        <span class="bar-icon">🎙️ <b>Mic Input</b></span>
        <span style="color: {text}; font-size: 1.1rem; flex-grow: 1;">ZenStudy AI Core Terminal Active. Type query in input field down below:</span>
        <span class="bar-icon">🔊 <b>Speaker On</b></span>
    </div>
    """, unsafe_allow_html=True)
    
    if user_prompt := st.chat_input("Ask anything about your studies..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        tutor_blueprint = "You are ZenStudy AI, an elite next-generation automated educator. Explain technical items slowly and step-by-step. Render formulas explicitly inside crisp standard LaTeX blocks."
        
        with st.spinner("AI Professor is generating comprehensive analysis lecture data..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(system_instruction=tutor_blueprint, temperature=0.3)
                )


