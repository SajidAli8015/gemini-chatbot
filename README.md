# 🤖 Gemini 2.0 Basic Chatbot

A lightweight Streamlit chatbot interface powered by Google Gemini 2.0 Flash using LangGraph and LangChain.

---

## 🚀 Features

* 📌 Persona Selector (Friendly Assistant, Formal Expert, etc.)
* 🌐 Language Selector (English, Urdu, etc.)
* 💬 Continuous streaming conversation (like ChatGPT)
* 🧠 Memory-enabled via LangGraph threading
* ♻️ Reset conversation session
* 📥 Download chat history to `.txt`

---

## 📁 Project Structure

```
chatbot/
│
├── app/
│   ├── __init__.py
│   ├── core.py           # LangGraph + model + prompt logic
│   └── utils.py          # Streaming function
│
├── streamlit_chat.py     # Streamlit UI logic
├── requirements.txt
└── .gitignore
```

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/gemini-chatbot.git
cd gemini-chatbot
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # for Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set API Keys

Create a file called `.streamlit/secrets.toml`:

```toml
GOOGLE_API_KEY = "your_google_genai_key"
LANGSMITH_API_KEY = "your_langsmith_key"
```

### 5. Run the App

```bash
streamlit run streamlit_chat.py
```

---

## 📷 Screenshots

> *Add screenshots here if needed.*

---

## 📌 Future Improvements

* [ ] 🌐 **Deploy on HuggingFace Spaces, Render, or Vercel** for public access
* [ ] 📚 **RAG Integration**: Augment chatbot with custom document retrieval
* [ ] 🧠 **Session Persistence** across reloads
* [ ] 📊 **Analytics Dashboard** (user count, sessions)
* [ ] 🗂️ **Admin Panel for managing personas & responses**

---




## 🙋‍♂️ Acknowledgements

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [LangChain](https://www.langchain.com/)
* [Streamlit](https://streamlit.io/)
* [Gemini by Google](https://ai.google.dev/)

---


