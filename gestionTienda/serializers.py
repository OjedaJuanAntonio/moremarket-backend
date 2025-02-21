from rest_framework import serializers
from .models import Category, Product, ProductVariant, ProductReview, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductVariantSerializer(serializers.ModelSerializer):
    # Ahora se define explícitamente el campo product para recibir el ID y convertirlo en instancia
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'variant_name', 'variant_value', 'extra_price']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'category', 'name', 'description', 'price',
            'image', 'stock', 'is_approved', 'created_at', 'variants'
        ]
    
    def get_seller(self, obj):
        return {
            'id': obj.seller.id,
            'email': obj.seller.email
        }

class ProductReviewSerializer(serializers.ModelSerializer):
    # Se añade el campo product para que se pueda enviar el ID del producto
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at']
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email
        }

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'total', 'status', 'created_at',
            'shipping_address', 'payment_method', 'items'
        ]
