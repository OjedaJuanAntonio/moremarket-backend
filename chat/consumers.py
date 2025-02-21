import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import ChatMessage
from channels.db import database_sync_to_async  # ✅ Importa correctamente


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        sender = self.scope.get("user")
        sender_name = sender.username if sender and sender.is_authenticated else "Anon"

        await self.save_message(self.room_name, sender, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_name,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    @database_sync_to_async
    def save_message(self, room_name, sender, message):
        from chat.models import ChatRoom
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        return ChatMessage.objects.create(
            room=room,
            sender=sender if sender and sender.is_authenticated else None,
            message=message
        )