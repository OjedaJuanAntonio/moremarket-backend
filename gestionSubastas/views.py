from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
            raise ValidationError("El usuario debe estar autenticado para realizar una puja.")

        bid = serializer.validated_data['amount']
        auction = serializer.validated_data['auction']

        # Obtener la puja más alta existente
        highest_bid = auction.bids.order_by('-amount').first()

        # Validar que la nueva puja sea mayor que la más alta
        if highest_bid and bid <= highest_bid.amount:
            raise ValidationError("La puja debe ser mayor que la puja más alta actual.")

        # Guardar la nueva puja
        bid_instance = serializer.save(user=self.request.user)

        # Enviar mensaje al grupo de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'auction_{bid_instance.auction.id}',
            {
                'type': 'auction_bid',
                'amount': str(bid_instance.amount),
                'user': bid_instance.user.username,
            }
        )
