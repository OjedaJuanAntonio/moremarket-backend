import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Conecta al WebSocket y se une a la sala de la subasta"""
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f'auction_{self.auction_id}'

        # Unirse al grupo de la subasta
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Salir del grupo de la subasta al desconectarse"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recibir mensaje desde el WebSocket del cliente"""
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        amount = data.get('amount')
        user = data.get('user')
        created_at = data.get('created_at', '')

        if not amount or not user:
            return  # Evita mensajes vacíos

        # Enviar mensaje al grupo de la subasta
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'auction_bid',
                'message': {
                    'amount': amount,
                    'user': user,
                    'created_at': created_at,
                    'auction_id': self.auction_id
                }
            }
        )

    async def auction_bid(self, event):
        """Maneja la distribución de la puja a los clientes conectados"""
        bid_data = event.get("message", {})

        await self.send(text_data=json.dumps({
            'amount': bid_data.get("amount", ""),
            'user': bid_data.get("user", ""),
            'created_at': bid_data.get("created_at", ""),
            'auction_id': bid_data.get("auction_id", ""),
        }))
