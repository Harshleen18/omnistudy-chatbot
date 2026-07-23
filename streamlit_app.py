
import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import pandas as pd
import io
import random

# 1. Premium App Aesthetics and Layout Setup
st.set_page_config(page_title="ZenStudy Elite Academy", page_icon="🎓", layout="wide")

# Studio CSS Injection for Chat Bars, Plus Icons, Microphone Emulation & Calm Mood UI
st.markdown("""
    <style>
    .stApp { background-color: #F7FAF8; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #153226; font-family: 'Georgia', serif; }
    
    /* Premium Sidebar Teacher Profile Card */
    .teacher-card { background: white; padding: 15px; border-radius: 16px; border: 1px solid #E6ECE8; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .teacher-avatar { font-size: 70px; margin-bottom: 5px; }
    .teacher-name { font-weight: bold; color: #1E3A2F; font-size: 1.2rem; }
    .teacher-badge { background: #E2ECE9; color: #1E3A2F; padding: 2px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; }
    
    /* Native Chat Input Interface with Plus Icon Styling */
    .custom-input-container { display: flex; align-items: center; background: white; border: 1px solid #DCE4E1; border-radius: 30px; padding: 8px 15px; margin-top: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }
    .plus-icon { font-size: 20px; color: #3A6B56; margin-right: 15px; cursor: pointer; font-weight: bold; }
    .mic-icon { font-size: 20px; color: #3A6B56; margin-left: 15px; cursor: pointer; }
    
    /* Interactive Flashcard Deck UI */
    .flashcard { background: linear-gradient(135deg, #FFFFFF 0%, #F9FBF9 100%); border: 2px solid #DCE4E1; border-radius: 20px; padding: 30px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.02); min-height: 150px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: #1E3A2F; font-weight: 500; font-family: 'Georgia', serif; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# 2. Secure Initialization using the provided API Key
API_KEY = "AQ.Ab8RN6IeciOdOo6ppwDAvP5_YnfGAEanztvhrr-7EN6PNGLg5w"
client = genai.Client(api_key=API_KEY)

# 3. Sidebar Configuration: The Dynamic AI Teacher Dashboard Selector
st.sidebar.markdown("### 🧑‍🏫 AI Virtual Faculty")

teacher_persona = st.sidebar.selectbox(
    "Choose Your Professor Style:",
    ["Calm & Reflective Tutor", "Fairy Tale Magical Teacher", "Strict Disciplined Academic"]
)

# System configurations mapped dynamically based on selection
teacher_profiles = {
    "Calm & Reflective Tutor": {"avatar": "🧘", "name": "Professor Aria", "voice_type": "Soft Calm Voice", "prompt_add": "Maintain an incredibly peaceful, friendly, slow, encouraging tone like a meditation guide."},
    "Fairy Tale Magical Teacher": {"avatar": "🧚✨", "name": "Guardian Eldon", "voice_type": "Enchanted Story Voice", "prompt_add": "Teach using magical analogies, fairytale settings, imaginative metaphors, and storytelling components."},
    "Strict Disciplined Academic": {"avatar": "🧑‍🏫📏", "name": "Dr. Vance", "voice_type": "Formal Direct Voice", "prompt_add": "Be extremely precise, analytical, highly disciplined, formal, and authoritative. Highlight absolute logical strictness."}
}

active_profile = teacher_profiles[teacher_persona]

# Render Custom Beautiful Profile Card for the Teacher
st.sidebar.markdown(f"""
<div class="teacher-card">
    <div class="teacher-avatar">{active_profile['avatar']}</div>
    <div class="teacher-name">{active_profile['name']}</div>
    <div><span class="teacher-badge">{active_profile['voice_type']}</span></div>
</div>
""", unsafe_allow_html=True)

# 4. Upload System for Lecture Notes / Old Documents Analysis
st.sidebar.markdown("### 📁 Student Materials Core")
uploaded_material = st.sidebar.file_uploader(
    "Upload older lecture notes, syllabi, or textbook snaps:",
    type=["png", "jpg", "jpeg", "pdf", "txt"]
)

media_attachment = None
notes_context_text = ""
if uploaded_material is not None:
    st.sidebar.success(f"📚 Knowledge Base Loaded: {uploaded_material.name}")
    if "image" in uploaded_material.type:
        media_attachment = types.Part.from_bytes(data=uploaded_material.read(), mime_type=uploaded_material.type)
        st.sidebar.image(uploaded_material, use_container_width=True)
    else:
        notes_context_text = f"\n[The student has uploaded textbook files / old data named: {uploaded_material.name}. Analyze this context data for accurate processing.]"

# 5. Core Platform Navigation Hub Tabs
tab_classroom, tab_flashcards, tab_analytics = st.tabs(["🏛️ Virtual Classroom", "🃏 Smart Flashcards & Quiz", "📈 Analytics & Mindmaps"])

# Core System Memory States Initialization
if "messages" not in st.session_state: st.session_state.messages = []
if "weak_areas" not in st.session_state: st.session_state.weak_areas = {"Math Formulae": 80, "Accounting Debits": 45, "Biology Diagrams": 90, "Grammar Structure": 60}
if "flashcard_flipped" not in st.session_state: st.session_state.flashcard_flipped = False

# ================= TAB 1: PREMIUM VIRTUAL CLASSROOM =================
with tab_classroom:
    st.markdown(f"### 🏛️ Interactive Lectures with {active_profile['name']}")
    
    # Display Existing Lecture Dialogues
    for idx, msg in enumerate(st.session_state.messages):
        role_label = f"🧑‍🎓 Student" if msg["role"] == "user" else f"{active_profile['avatar']} {active_profile['name']}"
        st.write(f"**{role_label}:** {msg['content']}")
        
        if msg["role"] == "assistant":
            if st.button("🔊 Play Voice Lecture", key=f"voice_{idx}"):
                with st.spinner("Modulating voice frequency..."):
                    clean = msg["content"].replace("$", "").replace("#", "").replace("*", "")
                    tts = gTTS(text=clean, lang='en', tld='co.uk' if "Strict" in teacher_persona else 'co.in')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    st.audio(audio_fp.getvalue(), format="audio/mp3", autoplay=True)
                    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Premium Native-Emulating UI Entry Structure
    st.markdown('<div class="custom-input-container"><span class="plus-icon">📎</span> <span style="color:#A0AEC0; flex-grow:1;">Chat console active. Type in the primary input block below.</span> <span class="mic-icon">🎙️</span></div>', unsafe_allow_html=True)
    
    # Primary Chat Hook Input box
    if text_query := st.chat_input("Ask your AI Teacher anything or prompt: 'Give me a summary of Chapter 1'..."):
        st.session_state.messages.append({"role": "user", "content": text_query})
        
        # Build prompt payload vector injection
        master_system_prompt = f"You are {active_profile['name']}. {active_profile['prompt_add']} Analyze all inputs, explain core concepts dynamically, and format equations cleanly using LaTeX math parameters."
        
        payload = []
        if media_attachment: payload.append(media_attachment)
        payload.append(text_query + notes_context_text)
        
        with st.spinner(f"{active_profile['name']} is preparing explanation..."):
            try:
                res = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=payload,
                    config=types.GenerateContentConfig(system_instruction=master_system_prompt, temperature=0.4)
                )
                st.session_state.messages.append({"role": "assistant", "content": res.text})
                st.rerun()
            except Exception as e:
                st.error(f"Classroom Processing Link Down: {e}")

# ================= TAB 2: SMART FLASHCARDS & EXAMS =================
with tab_flashcards:
    st.markdown("### 🃏 Smart Active Recall Modules")
    
    cards = [
        {"q": "What is the primary rule of Accounting Debits?", "a": "Debit what comes in, credit what goes out. Increase assets with debits."},
        {"q": "Explain the concept of Mitochondria for a Grade 9 Student.", "a": "It is the powerhouse of the cell, generating chemical energy (ATP) like a mini battery bank."},
        {"q": "What is the formula to extract roots from a quadratic equation?", "a": "The formula is $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$"}
    ]
    
    # Selected dynamic single card frame processing
    selected_idx = st.slider("Select Flashcard Slide No:", 0, len(cards)-1, 0)
    current_card = cards[selected_idx]
    
    if st.session_state.flashcard_flipped:
        st.markdown(f'<div class="flashcard" style="background:#EBF8F4; border-color:#9AE6B4;">💡 {current_card["a"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flashcard">❓ {current_card["q"]}</div>', unsafe_allow_html=True)
        
    if st.button("🔄 Flip/Reveal Flashcard Content"):
        st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
        st.rerun()

    st.markdown("<hr>### 📝 Diagnostic Mini Quiz Check")
    quiz_ans = st.radio("Question: If Assets increase, what happens in accounting bookkeeping metrics?", ["It is recorded as a Debit", "It is recorded as a Credit", "No change occurs"])
    if st.button("Submit Quiz Response Check"):
        if quiz_ans == "It is recorded as a Debit":
            st.success("🎯 100% Correct! This subject area is highly optimized.")
            st.session_state.weak_areas["Accounting Debits"] = 95
        else:
            st.error("📉 Incorrect! Your profile score dropped. Focus closely on this core module.")
            st.session_state.weak_areas["Accounting Debits"] = 20
            st.rerun()

# ================= TAB 3: DIAGNOSTIC ANALYTICS & MINDMAPS =================
with tab_analytics:
    st.markdown("### 📈 Real-Time Weakness Tracking Profile")
    st.write("ZenStudy automatically parses your lecture interactions to pinpoint exactly where you need to study more:")
    

