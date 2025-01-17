# from rest_framework import viewsets, permissions
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
# from .models import Auction, Bid
# from .serializers import AuctionSerializer, BidSerializer
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# # ✅ ViewSet para las subastas (CRUD completo)
# class AuctionViewSet(viewsets.ModelViewSet):
#     queryset = Auction.objects.all()
#     serializer_class = AuctionSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def retrieve(self, request, pk=None):
#         try:
#             auction = Auction.objects.get(pk=pk)
#             serializer = AuctionSerializer(auction)
#             return Response(serializer.data)
#         except Auction.DoesNotExist:
#             return Response({'error': 'Subasta no encontrada'}, status=404)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response({"detail": "Subasta eliminada con éxito."})


# # ✅ ViewSet para las pujas (con validación y WebSocket)
# class BidViewSet(viewsets.ModelViewSet):
#     queryset = Bid.objects.all()
#     serializer_class = BidSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         auction = serializer.validated_data['auction']
#         new_bid_amount = serializer.validated_data['amount']

#         # Validar que la nueva puja sea mayor que la más alta actual o el precio inicial
#         highest_bid = auction.bids.order_by('-amount').first()
#         starting_price = auction.product.price

#         if highest_bid:
#             if new_bid_amount <= highest_bid.amount:
#                 raise ValidationError({'detail': f'La puja debe ser mayor que ${highest_bid.amount}.'})
#         else:
#             if new_bid_amount < starting_price:
#                 raise ValidationError({'detail': f'La puja debe ser al menos de ${starting_price}.'})

#         # Guardar la nueva puja
#         bid = serializer.save(user=self.request.user)

#         # Enviar mensaje al grupo de WebSocket
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f'auction_{bid.auction.id}',
#             {
#                 'type': 'auction_bid',
#                 'amount': str(bid.amount),
#                 'user': bid.user.username,
#             }
#         )



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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, pk=None):
        try:
            auction = Auction.objects.get(pk=pk)
            serializer = AuctionSerializer(auction)
            return Response(serializer.data)
        except Auction.DoesNotExist:
            return Response({'error': 'Subasta no encontrada'}, status=404)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Subasta eliminada con éxito."})

# ViewSet para las pujas
class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        auction = serializer.validated_data['auction']
        new_bid_amount = serializer.validated_data['amount']

        highest_bid = auction.bids.order_by('-amount').first()
        starting_price = auction.product.price

        if highest_bid:
            if new_bid_amount <= highest_bid.amount:
                raise ValidationError({'detail': f'La puja debe ser mayor que ${highest_bid.amount}.'})
        else:
            if new_bid_amount < starting_price:
                raise ValidationError({'detail': f'La puja debe ser al menos de ${starting_price}.'})

        bid = serializer.save(user=self.request.user)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'auction_{bid.auction.id}',
            {
                'type': 'auction_bid',
                'amount': str(bid.amount),
                'user': bid.user.username,
            }
        )
