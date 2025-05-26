
# ✅ utils.py

from langchain_core.messages import HumanMessage, AIMessage
import time
from app.core import app # Import the compiled LangGraph app

# === Shared Defaults ===
language = "English"
thread_id = "sajid_testing_26th_May_3"

# === Streaming Chat Function ===
def stream_chat(query: str, language: str = language, thread_id: str = thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    input_messages = [HumanMessage(content=query)]

    for chunk, metadata in app.stream(
        {"messages": input_messages, "language": language},
        config,
        stream_mode="messages",
    ):
        if isinstance(chunk, AIMessage):
            print(chunk.content, end="", flush=True)

