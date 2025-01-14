from rest_framework import serializers
from .models import Auction, Product, Bid

# Serializer para el modelo Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price']

# Serializer para el modelo Bid (Puja)
class BidSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Mostrar el nombre del usuario en el JSON

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'user', 'amount', 'created_at']

# Serializer para el modelo Auction
class AuctionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Anidamos los datos completos del producto
    bids = BidSerializer(many=True, read_only=True)  # Anidamos las pujas relacionadas

    class Meta:
        model = Auction
        fields = ['id', 'start_time', 'end_time', 'is_active', 'product', 'bids']
