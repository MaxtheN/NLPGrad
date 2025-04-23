# chatbot/services.py

import os
from openai import OpenAI
from typing import AsyncGenerator

# Use the newer OpenAI client
client = OpenAI(api_key=os.getenv("LLM_API_KEY"))

MODEL_ID = "ft:gpt-4o-mini-2024-07-18:personal:gradpexp3:BMfKppPU"

async def stream_llm_response(messages) -> AsyncGenerator[str, None]:
    """
    Streams completion directly from OpenAI fine-tuned GPT-4o-mini.
    Only the latest user question is passed.
    """
    user_question = next((m["content"] for m in reversed(messages) if m["role"] == "user"), None)
    if not user_question:
        yield "No valid user input found."
        return

    try:
        stream = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are very helpful chatbot assistant. "
                        "Your only responsibility is to help user to answer questions related to python programming language. "
                        "If user tries to ask anything other than python programming language, just reply like this - "
                        "'Ask me about collections library'. "
                        "Your current language is English."
                    ),
                },
                {
                    "role": "user",
                    "content": user_question,
                },
            ],
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    except Exception as e:
        yield f"[ERROR] {str(e)}"
