# ✅ utils.py
from langchain_core.messages import HumanMessage, AIMessage
from app.core import app  # Import the compiled LangGraph app

# === Streaming Chat Function ===
def stream_chat(query: str, language: str, persona: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    input_messages = [HumanMessage(content=query)]

    for chunk, metadata in app.stream(
        {"messages": input_messages, "language": language, "persona": persona},
        config,
        stream_mode="messages",
    ):
        if isinstance(chunk, AIMessage):
            print(chunk.content, end="", flush=True)
