# Backend/memory/chat_memory.py

from collections import defaultdict

# In-memory store (session_id → conversation list)
chat_store = defaultdict(list)


def add_message(session_id, role, content):
    """
    role: 'user' or 'assistant'
    """
    chat_store[session_id].append({
        "role": role,
        "content": content
    })


def get_history(session_id):
    return chat_store.get(session_id, [])


def clear_history(session_id):
    chat_store[session_id] = []