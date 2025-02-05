# # gestionSubastas/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class AuctionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.auction_id = self.scope['url_route']['kwargs']['auction_id']
#         self.room_group_name = f'auction_{self.auction_id}'

#         # Únete al grupo de la subasta
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Salir del grupo de la subasta
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Recibir mensaje del WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         amount = text_data_json['amount']
#         user = text_data_json['user']

#         # Enviar mensaje a la sala del grupo
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'auction_bid',
#                 'amount': amount,
#                 'user': user,
#             }
#         )

#     # Manejar evento de puja
#     async def auction_bid(self, event):
#         amount = event['amount']
#         user = event['user']

#         # Enviar mensaje al WebSocket
#         await self.send(text_data=json.dumps({
#             'amount': amount,
#             'user': user,
#         }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f'auction_{self.auction_id}'

        # Únete al grupo de la subasta
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de la subasta
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje de una puja
    async def receive(self, text_data):
        data = json.loads(text_data)
        amount = data.get('amount')
        user = data.get('user')

        # Enviar mensaje a la sala del grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'auction_bid',
                'amount': amount,
                'user': user,
            }
        )

    # Manejar evento de puja
    async def auction_bid(self, event):
        await self.send(text_data=json.dumps({
            'amount': event['amount'],
            'user': event['user'],
        }))
