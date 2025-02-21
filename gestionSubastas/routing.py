from django.urls import path
from gestionSubastas.consumers import AuctionConsumer

websocket_urlpatterns = [
    path('ws/auctions/<int:auction_id>/', AuctionConsumer.as_asgi()),
]
