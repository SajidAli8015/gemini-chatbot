# ✅ streamlit_chat.py

import uuid
import os
import streamlit as st
from app.utils import stream_chat
import base64
import streamlit.components.v1 as components

# === 1. Set API Keys ===
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]

# === 2. Streamlit UI Setup ===
st.set_page_config(page_title="My Gemini Chatbot", layout="wide")
st.markdown("""
    <h1 style='text-align: center;'>🤖 Gemini 2.0 Basic Chatbot</h1>
    <p style='text-align: center;'>Hi, how can I help you today?</p>
""", unsafe_allow_html=True)

# === 3. Initialize Thread ID (Generated once per session) ===
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
thread_id = st.session_state.thread_id

# === 4. Initialize Chat History ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === 5. Dropdowns for Persona and Language (always visible) ===
persona = st.selectbox(
    "Choose a persona:",
    ["Friendly Assistant", "Formal Expert", "Tech Support"],
    key="persona_selector"
)

language = st.selectbox(
    "Choose language:",
    ["English", "Urdu"],
    key="language_selector"
)

# === 5.5 Reset Button ===
if st.button("🔄 Reset Conversation"):
    st.session_state.chat_history = []
    st.session_state.thread_id = str(uuid.uuid4())  # optional: regenerate new thread id
    st.rerun()

# === 6. Display Chat History in One Continuous Flow ===
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "user" else "assistant"):
        st.markdown(message)

# === 7. Input Area ===
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user's message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant streaming response
    with st.chat_message("assistant"):
        from io import StringIO
        import sys

        buffer = StringIO()
        sys.stdout = buffer
        stream_chat(user_input, language, persona, thread_id)
        sys.stdout = sys.__stdout__
        full_response = buffer.getvalue()

        st.markdown(full_response)
        st.session_state.chat_history.append(("ai", full_response))


# === 9. Floating Persistent Download Button ===

# Prepare conversation text (even if empty)
conversation_text = "\n\n".join([
    f"{'You' if role == 'user' else 'AI'}: {message}"
    for role, message in st.session_state.get("chat_history", [])
])

# Safely encode in base64
b64 = base64.b64encode(conversation_text.encode()).decode()

# Floating HTML button injected using absolute positioning
components.html(f"""
    <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
    ">
        <a download="chat_history.txt" href="data:text/plain;base64,{b64}" 
           style="
               background-color: #4CAF50;
               color: white;
               padding: 10px 16px;
               border-radius: 6px;
               text-decoration: none;
               font-size: 14px;
               font-family: sans-serif;
               box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
           ">
            📥 Download
        </a>
    </div>
""", height=60)
