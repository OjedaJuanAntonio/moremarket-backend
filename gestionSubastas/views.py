from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer


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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Asociar la puja con el usuario autenticado
        serializer.save(user=self.request.user)