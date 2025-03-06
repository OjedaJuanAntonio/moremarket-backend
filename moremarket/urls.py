from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestionSubastas.views import AuctionViewSet, BidViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from gestionTienda.views import CategoryViewSet, ProductViewSet, OrderViewSet, ProductReviewViewSet, ProductVariantViewSet, OrderItemViewSet
from django.conf import settings
from django.conf.urls.static import static



router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'product-variants', ProductVariantViewSet, basename='product-variant')
router.register(r'product-reviews', ProductReviewViewSet, basename='product-review')
router.register(r'order-items', OrderItemViewSet, basename='order-item')



router.register(r'auctions', AuctionViewSet, basename='auction')
router.register(r'bids', BidViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/dashboard/', include('dashboard.urls')),
    path('api/chat/', include('chat.urls')),  # Rutas REST de chat
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('gestionUsuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
