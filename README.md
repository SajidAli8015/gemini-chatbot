# 🤖 Gemini 2.0: RAG-Powered Chatbot

🚀 [Live App](https://gemini-chatbot-ah6paoheh5n4z3k96zgudu.streamlit.app)

A dynamic, multi-chat **Streamlit chatbot** powered by **Google Gemini 2.0 Flash**, enhanced with **RAG (Retrieval-Augmented Generation)** using **LangGraph**, **LangChain**, and **FAISS**.

---

## 🚀 Features

- 📄 **Upload PDF Documents** for contextual Q&A
- 🧠 **RAG** with embedded document chunks via FAISS vector store
- 🧑‍🎤 **Persona Selector** (Friendly Assistant, Formal Expert, Tech Support)
- 🌐 **Language Selector** (English, Urdu)
- 💬 **Streaming Chat Interface** with memory
- 🗂️ **Multi-Chat Sidebar**: Switch between sessions
- 🔄 **Reset Chat** while retaining context
- 📅 **Download Conversation** as `.txt` file
- 📌 Smart handling of file re-upload & persistence per chat session

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
- The app ***automatically embeds*** the document (using FAISS) once uploaded.  
- The chatbot will use the embedded content to answer document-specific questions.  
- Chat history, PDF context, and embeddings are ***stored per chat*** (isolated sessions). 
- You can switch to a new chat anytime and upload a different PDF.
- You can still ask generic questions with or without a document.  

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
