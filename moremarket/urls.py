from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestionTienda.views import ProductViewSet
from gestionSubastas.views import AuctionViewSet, BidViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Crear un router
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'auctions', AuctionViewSet, basename='auction')  # Agregar basename
router.register(r'bids', BidViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
