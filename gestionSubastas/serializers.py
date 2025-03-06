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
    created_by = UserSerializer(read_only=True)
    item_image = serializers.ImageField(allow_null=True, required=False)
    status = serializers.SerializerMethodField()

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
            'status',
            'created_by',
            'bids'
        ]

    def get_status(self, obj):
        return obj.get_status()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image = representation.get('item_image')
        if image:
            # Si la imagen no es externa, se construye la URL absoluta
            if not image.startswith("http"):
                request = self.context.get("request")
                if request:
                    representation['item_image'] = request.build_absolute_uri(image)
        return representation
