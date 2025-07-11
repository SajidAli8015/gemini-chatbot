# ✅ streamlit_chat.py (UPDATED with Stable Multi-format RAG + Reliable Upload Handling)

import uuid
import os
import streamlit as st
from app.utils import stream_chat
import base64
from PyPDF2 import PdfReader
import docx
import pandas as pd
from io import StringIO
import hashlib
import time

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import streamlit.components.v1 as components

# === 1. Set API Keys ===
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]

# === 2. Streamlit UI Setup ===
st.set_page_config(page_title="Gemini Chatbot", layout="wide")
st.markdown("""
    <h1 style='text-align: center;'>🤖 Gemini 2.0: RAG-Powered Chatbot</h1>
    <p style='text-align: center;'>Hi, how can I help you today?</p>
""", unsafe_allow_html=True)

# === 3. Session Initialization ===
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "active_chat_id" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.active_chat_id = chat_id
    st.session_state.all_chats[chat_id] = {
        "title": "New Chat",
        "history": [],
        "use_doc_context": False,
        "vectorstore": None,
        "last_file_hash": None
    }

chat_id = st.session_state.active_chat_id
chat_data = st.session_state.all_chats[chat_id]

# === 4. Sidebar: Multi-Chat Support ===
st.sidebar.header("📂 Chat History")

selected = st.sidebar.radio(
    "Select Chat",
    options=list(st.session_state.all_chats.keys()),
    format_func=lambda cid: st.session_state.all_chats[cid]["title"],
    index=list(st.session_state.all_chats.keys()).index(chat_id)
)

if selected != chat_id:
    st.session_state.active_chat_id = selected
    st.rerun()

if st.sidebar.button("➕ New Chat"):
    new_id = str(uuid.uuid4())
    st.session_state.all_chats[new_id] = {
        "title": "New Chat",
        "history": [],
        "use_doc_context": False,
        "vectorstore": None,
        "last_file_hash": None
    }
    st.session_state.active_chat_id = new_id
    st.rerun()

## === 5. Document Upload & Embedding ===
def get_file_hash(file_obj):
    content = file_obj.read()
    file_obj.seek(0)
    return hashlib.md5(content).hexdigest()

st.sidebar.subheader("📄 Upload a Document")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "txt", "docx", "csv"])

if uploaded_file:
    current_file_hash = get_file_hash(uploaded_file)

    if chat_data.get("last_file_hash") != current_file_hash:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        uploaded_file.seek(0)

        if file_extension == "pdf":
            reader = PdfReader(uploaded_file)
            raw_text = "\n".join([page.extract_text() or "" for page in reader.pages])

        elif file_extension == "txt":
            raw_text = uploaded_file.read().decode("utf-8")

        elif file_extension == "docx":
            doc = docx.Document(uploaded_file)
            raw_text = "\n".join([para.text for para in doc.paragraphs])

        elif file_extension == "csv":
            df = pd.read_csv(StringIO(uploaded_file.read().decode("utf-8")))
            raw_text = df.to_string(index=False)

        else:
            raw_text = ""

        splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
        chunks = splitter.split_text(raw_text)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

        chat_data["use_doc_context"] = True
        chat_data["vectorstore"] = vectorstore
        chat_data["last_file_hash"] = current_file_hash

        st.sidebar.success(f"✅ {file_extension.upper()} file uploaded & embedded")
    else:
        st.sidebar.info("ℹ️ Same file already loaded. Skipping embedding.")

# === 7. Persona & Language ===
persona = st.selectbox("Choose a persona:", ["Friendly Assistant", "Formal Expert", "Tech Support"], key="persona")
language = st.selectbox("Choose language:", ["English", "Urdu"], key="language")

# === 8. Reset Conversation ===
if st.button("🔄 Reset Conversation"):
    chat_data["history"] = []
    st.rerun()

# === 9. Display Chat History ===
for sender, message in chat_data["history"]:
    with st.chat_message("user" if sender == "user" else "assistant"):
        st.markdown(message)

# === 10. Input Area ===
user_input = st.chat_input("Type your message here...")

if user_input:
    if chat_data["title"] == "New Chat":
        chat_data["title"] = user_input[:30] + "..."

    chat_data["history"].append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        from io import StringIO
        import sys

        buffer = StringIO()
        response_placeholder = st.empty()
        response_placeholder.markdown("*Analyzing...*")

        sys.stdout = buffer
        stream_chat(user_input, language, persona, thread_id=chat_id)
        sys.stdout = sys.__stdout__

        full_response = buffer.getvalue()
        response_placeholder.empty()

        displayed = ""
        for word in full_response.split(" "):
            displayed += word + " "
            response_placeholder.markdown(displayed + "▌")
            time.sleep(0.02)

        response_placeholder.markdown(displayed.strip())
        chat_data["history"].append(("ai", displayed.strip()))

# === 11. Download Button ===
conversation_text = "\n\n".join([
    f"{'You' if role == 'user' else 'AI'}: {message}"
    for role, message in chat_data["history"]
])
b64 = base64.b64encode(conversation_text.encode()).decode()

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
