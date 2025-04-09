"""
chatbot/consumers.py
Handles WebSocket events, context, and streaming LLM responses.
"""

import json
import uuid
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .services import stream_llm_response

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.session_id = str(uuid.uuid4())
        self.history = [{"role": "system", "content": "You are a helpful assistant."}]

        # Import AnonymousUser here
        from django.contrib.auth.models import AnonymousUser
        self.user = self.scope["user"] if self.scope["user"].is_authenticated else AnonymousUser()

        await self.send(json.dumps({"role": "assistant", "content": "Hello! Ask me anything."}))
        await self._log_message("system", self.history[0]["content"])

    async def disconnect(self, close_code):
        logger.info(f"Disconnected session={self.session_id}")

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        data = json.loads(text_data)
        user_message = data.get("message", "").strip()
        if not user_message:
            return

        self.history.append({"role": "user", "content": user_message})
        await self._log_message("user", user_message)

        try:
            assistant_reply = ""
            async for chunk in stream_llm_response(self.history):
                assistant_reply += chunk
                await self.send(json.dumps({"role": "assistant", "content": chunk, "partial": True}))
        except Exception as e:
            logger.exception(e)
            await self.send(json.dumps({"role": "assistant", "content": "Sorry, there was an error."}))
            return

        self.history.append({"role": "assistant", "content": assistant_reply})
        await self._log_message("assistant", assistant_reply)

    @database_sync_to_async
    def _log_message(self, role, content):
        from .models import ChatMessage
        ChatMessage.objects.create(session_id=self.session_id, role=role, content=content)
