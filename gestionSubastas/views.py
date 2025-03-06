from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import action  # Importar @action

# Clase de paginación estándar
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryViewSet(viewsets.ModelViewSet):
    # Si tienes categorías en otra app, esta vista se define allí.
    # Se deja aquí solo si es necesario.
    pass

class AuctionViewSet(viewsets.ModelViewSet):
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    parser_classes = [MultiPartParser, FormParser]

    # AGREGAMOS LOS FILTROS
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item_name']
    ordering_fields = ['start_time', 'end_time']
    
    def get_queryset(self):
        # Devuelve todas las subastas sin filtrar por is_active; la clasificación se hará en el frontend o mediante métodos del modelo.
        qs = Auction.objects.all().select_related('created_by').prefetch_related('bids')
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('-start_time'))
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by:
            raise PermissionDenied({'detail': 'No tienes permiso para editar esta subasta.'})
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=True,
            context={'request': request}
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
        bid = serializer.save(user=self.request.user)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'auction_{auction.id}',
            {
                'type': 'auction_bid',
                'message': {
                    'amount': str(bid.amount),
                    'user': bid.user.username,
                    'created_at': bid.created_at.isoformat(),
                    'auction_id': auction.id,
                }
            }
        )
