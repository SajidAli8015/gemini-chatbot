# ✅ utils.py

from langchain_core.messages import HumanMessage, AIMessage
from app.core import app  # Import the compiled LangGraph app
import streamlit as st

def stream_chat(
    query: str,
    language: str,
    persona: str,
    thread_id: str,
):
    config = {"configurable": {"thread_id": thread_id}}

    input_data = {
        "messages": [HumanMessage(content=query)],
        "language": language,
        "persona": persona,
        "retrieved_context": ""
    }

    # 🧠 Use doc context if enabled in the current chat
    chat_data = st.session_state.all_chats.get(thread_id, {})
    use_doc_context = chat_data.get("use_doc_context", False)
    vectorstore = chat_data.get("vectorstore", None)

    if use_doc_context and vectorstore:
        try:
            
            #docs = vectorstore.max_marginal_relevance_search(query, k=5, fetch_k=20)
            docs = vectorstore.similarity_search(query, k=5)
            retrieved = "\n\n".join([doc.page_content for doc in docs])
            input_data["retrieved_context"] = retrieved
        except Exception as e:
            print("❌ Error during vectorstore similarity search:", e)
    elif use_doc_context:
        print("⚠️ Document context requested but vectorstore not found.")

    # 🧠 Stream the response from LangGraph app
    for chunk, metadata in app.stream(
        input_data,
        config,
        stream_mode="messages"
    ):
        if isinstance(chunk, AIMessage):
            print(chunk.content, end="", flush=True)