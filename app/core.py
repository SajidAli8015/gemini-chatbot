# ✅ core.py
import os
from typing import Sequence
from typing_extensions import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import trim_messages
from langgraph.checkpoint.memory import MemorySaver

# === 1. Environment Setup ===
#os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my-gemini-rag-bot"

# === 2. Initialize Model ===
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

# === 3. Trimmer ===
trimmer = trim_messages(
    max_tokens=100000,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human"
)

# === 4. Prompt Template with optional doc context ===

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
You are a highly intelligent, helpful, and detailed {persona}.
Your role is to assist users in {language} by answering their questions thoroughly, clearly, and accurately.

If any context from documents is provided, you must:
- Carefully analyze the information.
- Extract all relevant points needed to answer the user's question completely.
- Prioritize factual correctness based on the document.
- Provide complete responses (not too short).
- Use bullet points or numbered lists for clarity when applicable.
- Do NOT simply repeat information or say “based on the document” unless asked.

Even if the context is short, give the best possible answer using your knowledge and the context available.

-------------------------------
📄 Document Context:
{retrieved_context}
-------------------------------
"""),
    MessagesPlaceholder(variable_name="messages")
])





# === 5. State Definition ===
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str
    persona: str
    retrieved_context: str  # Optional doc context

# === 6. Node Logic ===
def call_model(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke({
        "messages": trimmed_messages,
        "language": state["language"],
        "persona": state["persona"],
        "retrieved_context": state.get("retrieved_context", "")
    })
    response = model.invoke(prompt)
    return {"messages": response}

# === 7. Graph Setup ===
workflow = StateGraph(state_schema=State)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# === 8. Compile Application ===
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)