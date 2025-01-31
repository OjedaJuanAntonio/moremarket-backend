# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from .models import Auction, Bid
# from .serializers import AuctionSerializer, BidSerializer
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# class AuctionViewSet(viewsets.ModelViewSet):
#     queryset = Auction.objects.all()
#     serializer_class = AuctionSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]  # GET público, otros métodos requieren autenticación

#     def list(self, request, *args, **kwargs):
#         """
#         Lista todas las subastas activas, ordenadas por la fecha de inicio.
#         """
#         queryset = Auction.objects.filter(is_active=True).order_by('-start_time')  # Solo subastas activas
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     def perform_create(self, serializer):
#         """
#         Asigna automáticamente el usuario autenticado como creador de la subasta.
#         """
#         serializer.save(created_by=self.request.user)


# class BidViewSet(viewsets.ModelViewSet):
#     queryset = Bid.objects.all()
#     serializer_class = BidSerializer
#     permission_classes = [IsAuthenticated]  # Requiere autenticación para realizar una puja

#     def perform_create(self, serializer):
#         """
#         Valida y crea una nueva puja, asociándola al usuario autenticado.
#         """
#         auction = serializer.validated_data['auction']
#         new_bid_amount = serializer.validated_data['amount']

#         # Obtener la puja más alta actual
#         highest_bid = auction.get_highest_bid()

#         # Validar la cantidad de la nueva puja
#         if highest_bid and new_bid_amount <= highest_bid.amount:
#             raise ValidationError({'detail': f'La puja debe ser mayor que ${highest_bid.amount}.'})
#         elif new_bid_amount < auction.starting_price:
#             raise ValidationError({'detail': f'La puja debe ser al menos de ${auction.starting_price}.'})

#         # Crear la nueva puja asociada al usuario autenticado
#         serializer.save(user=self.request.user)

#         # Notificar mediante WebSocket
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f'auction_{auction.id}',  # Canal basado en la ID de la subasta
#             {
#                 'type': 'auction_bid',
#                 'message': {
#                     'amount': str(new_bid_amount),
#                     'user': self.request.user.username,
#                     'auction_id': auction.id,
#                 }
#             }
#         )


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # GET público, otros métodos requieren autenticación

    def list(self, request, *args, **kwargs):
        """
        Lista todas las subastas activas, ordenadas por la fecha de inicio.
        """
        queryset = Auction.objects.filter(is_active=True).order_by('-start_time')  # Solo subastas activas
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Asigna automáticamente el usuario autenticado como creador de la subasta.
        """
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Permite editar una subasta solo si el usuario es el creador.
        """
        instance = self.get_object()  # Obtener la subasta actual

        # Verificar si el usuario actual es el creador de la subasta
        if request.user != instance.created_by:
            raise PermissionDenied({'detail': 'No tienes permiso para editar esta subasta.'})

        # Validar y actualizar la subasta
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación para realizar una puja

    def perform_create(self, serializer):
        """
        Valida y crea una nueva puja, asociándola al usuario autenticado.
        """
        auction = serializer.validated_data['auction']
        new_bid_amount = serializer.validated_data['amount']

        # Obtener la puja más alta actual
        highest_bid = auction.get_highest_bid()

        # Validar la cantidad de la nueva puja
        if highest_bid and new_bid_amount <= highest_bid.amount:
            raise ValidationError({'detail': f'La puja debe ser mayor que ${highest_bid.amount}.'})
        elif new_bid_amount < auction.starting_price:
            raise ValidationError({'detail': f'La puja debe ser al menos de ${auction.starting_price}.'})

        # Crear la nueva puja asociada al usuario autenticado
        serializer.save(user=self.request.user)

        # Notificar mediante WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'auction_{auction.id}',  # Canal basado en la ID de la subasta
            {
                'type': 'auction_bid',
                'message': {
                    'amount': str(new_bid_amount),
                    'user': self.request.user.username,
                    'auction_id': auction.id,
                }
            }
        )