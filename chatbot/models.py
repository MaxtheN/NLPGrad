"""
chatbot/models.py
Django models for storing chat logs.
"""

from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    """
    Stores a single message in a conversation.
    """
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_id = models.CharField(max_length=100)  # Or a UUID
    role = models.CharField(max_length=10)  # "user" or "assistant" or "system"
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_id} [{self.role}] {self.content[:30]}..."
