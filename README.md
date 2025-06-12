# 🤖 Gemini 2.0 Basic Chatbot

A lightweight Streamlit chatbot interface powered by Google Gemini 2.0 Flash using LangGraph and LangChain.

---

## 🚀 Features

- 🧠 **Retrieval-Augmented Generation (RAG)** from uploaded PDF documents
- 📄 **Document Upload & Embedding** with FAISS vector store
- 📌 **Persona Selector** (Friendly Assistant, Formal Expert, Tech Support)
- 🌐 **Language Selector** (English, Urdu)
- 💬 **Streaming Chat Interface** with memory (like ChatGPT)
- 🧾 **Multi-Chat Sidebar**: Supports multiple parallel conversations
- ♻️ **Reset Conversation** with unique chat ID
- 📥 **Download Conversation** (.txt format)

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

## 📚 RAG Workflow

- Upload a PDF in the sidebar.  
- Check the **"Use PDF for context"** checkbox (once per chat) to activate RAG.  
- Ask document-specific questions — the chatbot retrieves relevant chunks using FAISS.  
- For generic questions, uncheck the box (or open a new chat).  
- PDF state is stored per session, and chat context persists until reset.  

---

## ✅ Future Enhancements

- 🌐 **Deploy** to HuggingFace / Render / Vercel  
- 🧠 **Use memory / database** for storing chat history  
- 🖼️ **Multimodal file support** (images, docs)  
- 🔒 **User authentication / login system**  
- 📊 **Admin dashboard** for usage & file analytics  
- ⚙️ **Function-calling capabilities** for real tools  

---

## 🙋‍♂️ Acknowledgements

- **LangGraph**  
- **LangChain**  
- **FAISS** by Meta  
- **Streamlit**  
- **Google Generative AI**  

---

## 🧑‍💻 Maintainer

**Sajid Ali**  
*Data Scientist | GitHub*



