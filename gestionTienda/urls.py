from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, OrderViewSet,
    ProductVariantViewSet, ProductReviewViewSet, OrderItemViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'product-variants', ProductVariantViewSet, basename='product-variant')
router.register(r'product-reviews', ProductReviewViewSet, basename='product-review')
router.register(r'order-items', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/<int:pk>/products/', CategoryViewSet.as_view({'get': 'products'}), name='category-products'),
]
