from django.urls import path
from .views import RegisterView, ProfileView, LoginView, ProtectedView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),  # Ruta para la vista de perfil
    path('login/', LoginView.as_view(), name='login'),  # Login
    path('protected/', ProtectedView.as_view(), name='protected'),  # Ruta protegida
    path('logout/', LogoutView.as_view(), name='logout'),  # Nueva ruta para logout
]
