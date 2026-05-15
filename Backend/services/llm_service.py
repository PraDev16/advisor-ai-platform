import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


def generate_ai_response(user_query, conversation_history=None):

    if conversation_history is None:
        conversation_history = []

    messages = [
        {
            "role": "system",
            "content":
                "You are a professional financial advisor AI assistant."
        }
    ]

    # -----------------------------
    # ADD MEMORY
    # -----------------------------
    for msg in conversation_history:

        messages.append({

            "role": msg["role"],

            "content": msg["content"]
        })

    # -----------------------------
    # CURRENT USER QUERY
    # -----------------------------
    messages.append({

        "role": "user",

        "content": user_query
    })

    payload = {

        "model": "openai/gpt-3.5-turbo",

        "messages": messages,

        "max_tokens": 200
    }

    try:

        response = requests.post(

            API_URL,

            headers=headers,

            json=payload,

            timeout=30
        )

        result = response.json()

        print("\n[OPENROUTER RESPONSE]")
        print(result)

        # -----------------------------
        # HANDLE API ERRORS
        # -----------------------------
        if "choices" not in result:

            error_message = result.get(
                "error",
                {}
            ).get(
                "message",
                "Unknown API error"
            )

            return f"LLM API Error: {error_message}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        print("[LLM ERROR]", str(e))

        return f"System Error: {str(e)}"