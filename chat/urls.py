from django.urls import path
from .views import ChatRoomListCreateView, ChatMessageListCreateView

urlpatterns = [
    path('rooms/', ChatRoomListCreateView.as_view(), name='chat-room-list'),
    path('rooms/<int:room_id>/messages/', ChatMessageListCreateView.as_view(), name='chat-message-list'),
]
