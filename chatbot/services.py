"""
chatbot/services.py
Provides functionality to query the external LLM with streaming.
"""

import os
import httpx
import asyncio
import json

LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:8001/api/llm/stream")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

async def stream_llm_response(messages):
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages]) + "\nassistant:"

    payload = {
        "model": "orca-mini",
        "prompt": prompt,
        "stream": True
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", LLM_API_URL, json=payload) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    data = json.loads(line)
                    yield data.get("response", "")
