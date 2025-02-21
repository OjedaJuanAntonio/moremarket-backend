from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.select_related('created_by').all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimiza consultas con prefetch_related para bids"""
        return super().get_queryset().prefetch_related('bids')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(is_active=True).order_by('-start_time')
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if request.user != instance.created_by:
            raise PermissionDenied(
                {'detail': 'No tienes permiso para editar esta subasta.'}
            )
            
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.select_related('user', 'auction').all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        auction = serializer.validated_data['auction']
        new_bid_amount = serializer.validated_data['amount']
        highest_bid = auction.get_highest_bid()

        if highest_bid and new_bid_amount <= highest_bid.amount:
            raise ValidationError({'detail': f'La puja debe ser mayor que ${highest_bid.amount}.'})

        if new_bid_amount < auction.starting_price:
            raise ValidationError({'detail': f'La puja debe ser al menos de ${auction.starting_price}.'})

        # Guardar la puja con el usuario autenticado
        bid = serializer.save(user=self.request.user)

        # 🔹 Corrección: Enviar el mensaje WebSocket con los datos correctos
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'auction_{auction.id}',
            {
                'type': 'auction_bid',
                'message': {
                    'amount': str(bid.amount),
                    'user': bid.user.username,
                    'created_at': bid.created_at.isoformat(),  # 🔹 Agregar `created_at`
                    'auction_id': auction.id,
                }
            }
        )
