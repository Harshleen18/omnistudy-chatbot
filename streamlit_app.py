import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import io

# 1. Distraction-Free Calm Interface Design
st.set_page_config(page_title="ZenStudy AI", page_icon="🧘", layout="centered")

# Custom calming styles
st.markdown("""
    <style>
    .stApp { background-color: #F3F6F5; }
    h1, h2, h3 { color: #1E3A2F; font-family: 'Georgia', serif; }
    .stButton>button { background-color: #2D5A47; color: white; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧘 ZenStudy AI: Ultimate Smart Tutor")
st.caption("A peaceful, smart AI that handles Text, Diagrams, Files, Audio, and Video lectures.")

# 2. Your Secure Google AI Studio Key
API_KEY = "AQ.Ab8RN6IoyLI3TnLsXFuzRhx4kUfRZt6wG-JwM0RsxJTCRqhDkQi"
client = genai.Client(api_key=API_KEY)

# 3. System Blueprint Instructions for the Brain
zen_tutor_instructions = """
You are "ZenStudy AI", a highly cooperative, calm, and master-level universal student tutor.
Your voice is encouraging, clear, and perfectly descriptive.

Capabilities & Response Structure:
1. Support all streams (Medical, Non-Medical, Commerce, Arts) from school up to university.
2. If the student uploads an image, picture, or diagram, carefully explain its components step-by-step.
3. If analyzing files, videos, or audio lectures, summarize or answer directly based on that context.
4. For math formulas, always use clean LaTeX format (e.g. $A = \\pi r^2$ or block format $$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$) so it formats beautifully.
5. Keep explanations direct, deeply detailed, and very logical without ever skipping calculation steps.
"""

# 4. Multi-modal Study File Uploader
st.sidebar.header("📁 Upload Study Materials")
uploaded_material = st.sidebar.file_uploader(
    "Upload anything (Images, Diagrams, PDFs, Audio, Video):",
    type=["png", "jpg", "jpeg", "pdf", "txt", "mp3", "wav", "mp4"]
)

# Active media attachment container
media_attachment = None

if uploaded_material is not None:
    mime_type_str = uploaded_material.type
    st.sidebar.info(f"📁 Loaded file: {uploaded_material.name}")
    
    # Process byte content for the Gemini API
    file_bytes = uploaded_material.read()
    media_attachment = types.Part.from_bytes(
        data=file_bytes,
        mime_type=mime_type_str,
    )
    
    # Live previews on the side-panel
    if "image" in mime_type_str:
        st.sidebar.image(file_bytes, caption="Uploaded Diagram/Image")
    elif "audio" in mime_type_str:
        st.sidebar.audio(file_bytes)
    elif "video" in mime_type_str:
        st.sidebar.video(file_bytes)

# 5. Maintaining Chat Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display current chat stream
for index, msg in enumerate(st.session_state.chat_history):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Give a read-aloud playback option for any text answer from the AI tutor
        if msg["role"] == "assistant":
            if st.button("🔊 Listen to Explanation", key=f"tts_{index}"):
                with st.spinner("Preparing peaceful audio..."):
                    # Use Google TTS to create clean speech
                    clean_text_for_speech = msg["content"].replace("$", "").replace("#", "")
                    tts = gTTS(text=clean_text_for_speech, lang='en', tld='co.in')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    st.audio(audio_fp.getvalue(), format="audio/mp3", autoplay=True)

# 6. Capture Student Question
if user_question := st.chat_input("Ask ZenStudy AI anything or discuss your uploaded file..."):
    with st.chat_message("user"):
        st.markdown(user_question)
    
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    # Put attachments and text query into the payload vector
    api_payload = []
    if media_attachment:
        api_payload.append(media_attachment)
    api_payload.append(user_question)

    # 7. Generate Response using Gemini 2.5 Flash
    with st.chat_message("assistant"):
        with st.spinner("Thinking deeply..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=api_payload,
                    config=types.GenerateContentConfig(
                        system_instruction=zen_tutor_instructions,
                        temperature=0.3,
                    )
                )
                ai_answer = response.text
                st.markdown(ai_answer)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_answer})
                
                # Auto-rerun to render the updated state with the new Audio widget smoothly
                st.rerun()
                
            except Exception as error_msg:
                st.error(f"Processing Error: {error_msg}")
