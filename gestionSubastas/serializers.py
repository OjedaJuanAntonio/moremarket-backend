from rest_framework import serializers
from .models import Auction, Bid
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class BidSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'user', 'amount', 'created_at']

class AuctionSerializer(serializers.ModelSerializer):
    bids = BidSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)  # Ahora muestra id y email

    class Meta:
        model = Auction
        fields = [
            'id', 
            'item_name', 
            'item_description', 
            'item_image', 
            'starting_price',
            'start_time', 
            'end_time', 
            'is_active', 
            'created_by', 
            'bids'
        ]