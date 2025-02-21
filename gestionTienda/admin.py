from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductReview, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'category', 'price', 'stock', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at', 'category')
    search_fields = ('name', 'description')
    actions = ['approve_products']

    def approve_products(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} producto(s) aprobado(s) exitosamente.")
    approve_products.short_description = "Aprobar productos seleccionados"

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'variant_name', 'variant_value', 'extra_price')
    search_fields = ('variant_name', 'variant_value')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'comment')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__email',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
