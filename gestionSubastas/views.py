from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# ViewSet para las subastas
class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    def retrieve(self, request, pk=None):
        try:
            auction = Auction.objects.get(pk=pk)
            serializer = AuctionSerializer(auction)
            return Response(serializer.data)
        except Auction.DoesNotExist:
            return Response({'error': 'Subasta no encontrada'}, status=404)


# ViewSet para las pujas
class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

    def perform_create(self, serializer):
        # Verificar que el usuario esté autenticado
        if not self.request.user or not self.request.user.is_authenticated:
            raise ValueError("El usuario debe estar autenticado para realizar una puja.")

        # Guardar la nueva puja y asignar el usuario autenticado
        bid = serializer.save(user=self.request.user)

        # Enviar mensaje al grupo de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'auction_{bid.auction.id}',
            {
                'type': 'auction_bid',
                'amount': str(bid.amount),
                'user': bid.user.username,
            }
        )
