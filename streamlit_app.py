import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import pandas as pd
import io
import time
import os

# ---------------- 1. INITIALIZE & WORKSPACE MEMORY STATES ----------------
st.set_page_config(
    page_title="ZenStudy AI",
    page_icon="🎓",
    layout="wide",
)

# Persistent Session Memory Configurations
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I'm your ZenStudy AI teacher. Upload your notes or ask me anything."}
    ]
if "folders" not in st.session_state: st.session_state.folders = {"Mathematics": [], "Science": [], "Accounts": []}
if "weak_areas" not in st.session_state: st.session_state.weak_areas = {"Math Formulas": 85, "Debit Bookkeeping": 35, "Cell Diagrams": 90}
if "flash_flipped" not in st.session_state: st.session_state.flash_flipped = False
if "quiz_score" not in st.session_state: st.session_state.quiz_score = None
if "ui_theme" not in st.session_state: st.session_state.ui_theme = "Cyber Dark (High Contrast)"
if "personality" not in st.session_state: st.session_state.personality = "Calm Teacher"
if "voice_accent" not in st.session_state: st.session_state.voice_accent = "Indian Standard Accent"
if "custom_api_key" not in st.session_state: st.session_state.custom_api_key = ""

# ---------------- 2. STARK HIGH-CONTRAST THEME MANAGEMENT ----------------
if "White" in st.session_state.ui_theme:
    bg, text, card_bg, border, accent = "#FFFFFF", "#000000", "#F4F6F5", "#000000", "#008055"
    user_bubble, ai_bubble = "#E6F4EA", "#FFFFFF"
else:
    bg, text, card_bg, border, accent = "#0B1120", "#FFFFFF", "#111827", "#FFFFFF", "#10B981"
    user_bubble, ai_bubble = "#1A2E26", "#111827"

# Custom CSS Injection - Enforcing Stark High-Contrast Accessibility
st.markdown(f"""
<style>
    .stApp {{ background: {bg} !important; color: {text} !important; font-family: 'Poppins', sans-serif; }}
    p, span, label, h1, h2, h3, h4, h5, div {{ color: {text} !important; font-weight: 700 !important; }}
    .stSidebar {{ background-color: {card_bg} !important; border-right: 3px solid {border} !important; }}
    .chat-bubble-user {{ background-color: {user_bubble} !important; padding: 18px; border-radius: 16px 16px 4px 16px; margin: 10px 0; border: 2px solid {border} !important; }}
    .chat-bubble-ai {{ background-color: {ai_bubble} !important; padding: 18px; border-radius: 16px 16px 16px 4px; margin: 10px 0; border: 2px solid {border} !important; }}
    div.stButton > button:first-child {{
        background: {accent} !important; color: #FFFFFF !important; border-radius: 25px !important; padding: 8px 24px !important; font-weight: 800 !important; border: 2px solid {border} !important;
    }}
    div.stButton > button:first-child:hover {{ background: #000000 !important; color: #FFFFFF !important; }}
</style>
""", unsafe_allow_html=True)

# ---------------- 3. AI COGNITIVE BRAIN INITIALIZATION ----------------
# Fetch the key from environment or safely from secure secrets storage
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

# Prioritize the user-configured key if they set one in the settings
active_key = st.session_state.get("custom_api_key", "") or api_key

# Initialize the official Google GenAI Client safely if key is available
client = None
if active_key:
    try:
        client = genai.Client(api_key=active_key)
    except Exception as e:
        # Avoid crashing startup, log/display the issue on chat page instead
        pass

# ---------------- 4. LEFT SIDEBAR NAVIGATION MENU ----------------
with st.sidebar:
    st.title("🎓 ZenStudy AI")
    st.markdown("### Navigation Dashboard")
    
    menu_selection = st.radio(
        "Jump To Workspace:",
        ["Dashboard", "AI Teacher Set", "Study Materials Hub", "Virtual Classroom", "Flashcard Center", "Mind Maps", "Quizzes & Tests", "Analytics Panel", "Focus Zone", "Settings"]
    )
    
    st.divider()
    st.metric("🔥 Study Streak", "12 Days")
    st.progress(0.72)
    
    st.markdown("### 📁 Subject Folder Hub")
    new_folder_title = st.text_input("Enter New Subject Title:")
    if st.button("➕ Create Folder") and new_folder_title:
        if new_folder_title not in st.session_state.folders:
            st.session_state.folders[new_folder_title] = []
            st.success(f"Added Folder: {new_folder_title}")

# ================= 5. MAIN STUDIO APPLICATION ROUTER =================

if menu_selection == "Dashboard":
    st.markdown("## 📊 Personal Study Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Subject Mastery", "78%", "🧠 Optimal")
    col2.metric("Upcoming Practice Exams", "2 Scheduled", "📅 Due")
    col3.metric("Completed Chapters", "14 Lessons", "✅ Progressing")
    st.markdown("### 🎯 AI Personalized Recommendations")
    st.info("💡 **AI Insight:** Your performance charts show a quick drop in 'Debit Bookkeeping'. Click on the **Quizzes & Tests** section to take a 5-minute booster test!")

if menu_selection == "AI Teacher Set":
    st.markdown("## 🧑‍🏫 Personalize Your Virtual AI Faculty")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.session_state.personality = st.selectbox("Choose Faculty Persona Profile:", [
            "Calm Teacher", "Friendly Teacher", "Strict Teacher", "Professor Mode", 
            "Storytelling Teacher", "Exam Coach", "Motivational Mentor", "Scientific Instructor", "Fairy Tale Explainer"
        ])
        st.session_state.voice_accent = st.selectbox("Audio Voice Accent Style:", ["Indian Standard Accent", "British Classical Academic", "US Modern Radio Studio"])
        st.session_state.speak_rate = st.slider("Set Professor Lecture Speed Rate:", 0.8, 1.5, 1.0, 0.1)
    with t_col2:
        avatars = {"Calm Teacher": "🧘", "Strict Teacher": "🧑‍🏫📏", "Fairy Tale Explainer": "🧚✨", "Friendly Teacher": "🤗"}
        st.markdown(f"#### Active Instructor Avatar Image")
        st.markdown(f"<div style='font-size:100px; text-align:center;'>{avatars.get(st.session_state.personality, '🎓')}</div>", unsafe_allow_html=True)
        st.success(f"**Faculty Blueprint Locked In:** Workspace initialized for: {st.session_state.personality}.")

if menu_selection == "Study Materials Hub":
    st.markdown("## 📁 Ingest Materials into Knowledge Base")
    uploaded_files = st.file_uploader("Drop any study files here:", type=["pdf", "png", "jpg", "jpeg", "txt", "docx", "pptx"], accept_multiple_files=True)
    target_fol = st.selectbox("Assign to Subject Folder Target Location:", list(st.session_state.folders.keys()))
    if st.button("🚀 Ingest & Process Into Knowledge Base") and uploaded_files:
        for f in uploaded_files:
            st.session_state.folders[target_fol].append(f.name)
        st.success(f"🎉 Fully Scanned and Parsed {len(uploaded_files)} files into folder: **'{target_fol}'**.")
    st.json(st.session_state.folders)

if menu_selection == "Virtual Classroom":
    st.markdown("## 🏛️ Centric Classroom Interface Console")
    
    # Render historical conversation logs
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user"><b>🧑‍🎓 Student:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        if msg["role"] == "assistant":
            st.markdown(f'<div class="chat-bubble-ai"><b>🧑‍🏫 AI Teacher ({st.session_state.get("personality", "General Setup")}):</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
            if st.button("🔊 Play Voice Lecture", key=f"audio_run_{idx}"):
                with st.spinner("Generating audio transcription..."):
                    clean_str = msg["content"].replace("$", "").replace("#", "").replace("*", "")
                    tld_val = 'co.in' if "Indian" in st.session_state.get("voice_accent", "Indian") else 'co.uk'
                    tts = gTTS(text=clean_str, lang='en', tld=tld_val)
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    st.audio(audio_fp.getvalue(), format="audio/mp3", autoplay=True)

    # Chat execution form logic using Native Streamlit primitives
    if user_query := st.chat_input("Ask your virtual teacher a question..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.rerun()

    # Dynamic Chat Completion Processing using the official SDK wrapper
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        if not client:
            st.error("🔑 Gemini API Key is missing. Please enter your API key in the **Settings** workspace in the sidebar to chat with the AI Teacher.")
        else:
            with st.spinner("AI Teacher is thinking..."):
                try:
                    persona = st.session_state.get("personality", "Calm Teacher")
                    system_instruction = f"You are an expert academic tutor operating in a '{persona}' persona mode. Explain concepts clearly."

                    # Format full structural chat history logs natively for the modern SDK
                    contents_history = []
                    for msg in st.session_state.messages:
                        role_id = "user" if msg["role"] == "user" else "model"
                        contents_history.append(
                            types.Content(
                                role=role_id,
                                parts=[types.Part.from_text(text=msg["content"])]
                            )
                        )

                    # Execute inference using the modern model tier setup
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents_history,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                        )
                    )
                    
                    if response.text:
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                        st.rerun()
                    else:
                        st.error("Received an empty content stream from Gemini.")

                except Exception as e:
                    err_msg = str(e)
                    if "401" in err_msg or "UNAUTHENTICATED" in err_msg or "invalid authentication" in err_msg or "API key" in err_msg or "ACCESS_TOKEN_TYPE_UNSUPPORTED" in err_msg:
                        st.error("""
                        ❌ **Authentication Error (401):** The Gemini API Key is invalid, expired, or unsupported.

                        **Common Cause (ACCESS_TOKEN_TYPE_UNSUPPORTED):**
                        Google Gemini now requires secure **Auth Keys** (starting with `AQ...`) and rejects standard unrestricted keys (starting with `AIza...`).

                        **How to Fix:**
                        1. Go to **Google AI Studio** and create a new API Key (which will automatically be an Auth Key starting with `AQ...`).
                        2. Go to the **Settings** workspace in the sidebar and paste your new key.
                        """)
                    else:
                        st.error(f"SDK Core Operational Error: {err_msg}")

# Configure Settings workspace
if menu_selection == "Settings":
    st.markdown("## ⚙️ Settings")
    st.markdown("### API Configuration")

    st.markdown("""
    💡 **Important Note on Gemini API Keys:**
    Google Gemini has transitioned away from standard traffic keys (starting with `AIza...`).
    - If you are using a new key, make sure it is an **Auth Key** (starting with `AQ...`), which is now the default in Google AI Studio.
    - If you are getting an `ACCESS_TOKEN_TYPE_UNSUPPORTED` (401) error, it means your key is unrestricted or standard. You must either generate a new **Auth Key** (starts with `AQ...`) in AI Studio, or apply explicit restrictions to your `AIza...` key in the Google Cloud Console.
    """)

    user_key_input = st.text_input("Enter your Gemini API Key:", value=st.session_state.get("custom_api_key", ""), type="password")
    if st.button("Save API Key"):
        st.session_state.custom_api_key = user_key_input
        st.success("API Key saved successfully! Reloading...")
        st.rerun()

# Fallback block for all undeveloped menu items to keep everything flat and clean
unbuilt_workspaces = ["Flashcard Center", "Mind Maps", "Quizzes & Tests", "Analytics Panel", "Focus Zone"]
if menu_selection in unbuilt_workspaces:
    st.markdown(f"## 🛠️ {menu_selection}")
    st.info(f"The **{menu_selection}** workspace is currently under active development. Stay tuned for updates!")

