# gestionSubastas/serializers.py
from rest_framework import serializers
from .models import Auction, Bid

class BidSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Muestra el nombre del usuario en el JSON

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'user', 'amount', 'created_at']

class AuctionSerializer(serializers.ModelSerializer):
    bids = BidSerializer(many=True, read_only=True)  # Incluye las pujas en el serializer
    created_by = serializers.StringRelatedField(read_only=True)  # Muestra el nombre del creador

    class Meta:
        model = Auction
        fields = ['id', 'item_name', 'item_description', 'item_image', 'starting_price',
                  'start_time', 'end_time', 'is_active', 'created_by', 'bids']
