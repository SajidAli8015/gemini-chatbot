# ✅ streamlit_chat.py
import os
import streamlit as st
from app.utils import stream_chat, thread_id, language

# === 1. Set API Keys ===
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]

# === 2. Streamlit UI Setup ===
st.markdown(
    """
    <h1 style='text-align: center;'>🤖 Gemini 2.0 Basic Chatbot</h1>
    <p style='text-align: center;'>Hi, How can I help you today?.</p>
    """,
    unsafe_allow_html=True
)


# === 3. Initialize Chat History ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === 4. Display All Chat Messages (Continuous Chat View) ===
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "user" else "assistant"):
        st.markdown(message)
    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

# === 5. Input Area ===
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add and display user message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Stream and display assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        # Capture streamed response
        import sys
        from io import StringIO
        buffer = StringIO()
        sys.stdout = buffer
        stream_chat(user_input, language, thread_id)
        sys.stdout = sys.__stdout__
        full_response = buffer.getvalue()

        st.markdown(full_response)
        st.session_state.chat_history.append(("ai", full_response))
