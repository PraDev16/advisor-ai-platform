from Backend.rag.vector_store import search_docs
from Backend.services.llm_service import generate_ai_response
from Backend.memory.chat_memory import add_message, get_history
from Backend.logging.audit_logger import log_event


def ask_rag(question, session_id="default"):

    print("\n[RAG] Question received:", question)

    # -----------------------------
    # 1. STORE USER MESSAGE
    # -----------------------------
    add_message(session_id, "user", question)

    # -----------------------------
    # 2. GET CHAT HISTORY
    # -----------------------------
    history = get_history(session_id)

    # -----------------------------
    # 3. RAG RETRIEVAL
    # -----------------------------
    docs = search_docs(question)

    print("[RAG] Retrieved docs:", len(docs))

    context = "\n\n".join([d.page_content for d in docs])

    # -----------------------------
    # 4. BUILD FINAL PROMPT (IMPORTANT FIX)
    # -----------------------------
    prompt = f"""
You are a professional financial advisor AI.

You MUST use:
- conversation history
- retrieved context

Conversation history:
{history}

Context:
{context}

User question:
{question}

Rules:
- Be precise
- Use only provided context when possible
- If history helps, use it

Answer:
"""

    print("\n[LLM] Sending prompt...")

    # -----------------------------
    # 5. CALL LLM (FIXED)
    # -----------------------------
    response = generate_ai_response(prompt, history)
    
    # -----------------------------
    # AUDIT LOGGING
    # -----------------------------
    log_event(
        "advisor_chat",
        {
            "session_id": session_id,
            "question": question,
            "response": response
        }
    )

    # -----------------------------
    # 6. STORE ASSISTANT RESPONSE
    # -----------------------------
    add_message(session_id, "assistant", response)

    return response