from rest_framework import generics, permissions
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        return ChatMessage.objects.filter(room_id=room_id).order_by("timestamp")
    
    def perform_create(self, serializer):
        room_id = self.kwargs.get("room_id")
        serializer.save(sender=self.request.user, room_id=room_id)
