from rest_framework import serializers
from .models import ChatRoom, ChatMessage

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'created_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'message', 'timestamp']
