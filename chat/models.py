from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="chat_rooms",
        blank=True
    )
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.email}: {self.message[:50]}"
