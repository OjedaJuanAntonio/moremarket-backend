from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    LoginView,
    ProtectedView,
    LogoutView,
    CookieTokenRefreshView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Registro de usuarios
    path('profile/', ProfileView.as_view(), name='profile'),  # Vista del perfil del usuario autenticado
    path('login/', LoginView.as_view(), name='login'),  # Inicio de sesión
    path('protected/', ProtectedView.as_view(), name='protected'),  # Ruta protegida de prueba
    path('logout/', LogoutView.as_view(), name='logout'),  # Cierre de sesión
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),  # Renovación del token de acceso
]
