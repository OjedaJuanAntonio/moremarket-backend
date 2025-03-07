from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.http import JsonResponse

# Registro de usuario
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if CustomUser.objects.filter(email=data['email']).exists():
            return Response({'error': 'Este correo ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(
            username=data['email'],  # Usa el email como nombre de usuario
            email=data['email'],
            phone=data.get('phone', ''),
            full_name=data.get('full_name', ''),
            address=data.get('address', ''),
            password=make_password(data['password']),
        )
        return Response({'message': 'Usuario registrado con éxito.'}, status=status.HTTP_201_CREATED)

# Inicio de sesión y generación de tokens
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            response = JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'phone': user.phone,
                    'address': user.address,
                },
                'message': 'Inicio de sesión exitoso'
            })
            response.set_cookie(
                'refresh_token',
                str(refresh),
                httponly=True,  # Solo accesible por el servidor
                secure=False,   # Cambiar a True en producción
                samesite='Lax', # Restringe el acceso a la cookie en solicitudes de terceros
                max_age=7 * 24 * 60 * 60  # 7 días de duración
            )
            return response

        return Response({'error': 'Credenciales inválidas'}, status=401)

# Vista protegida para probar autenticación
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def get(self, request):
        user = request.user  # Obtiene el usuario autenticado
        return Response({
            'message': f'Bienvenido, {user.email}',
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)

# Perfil del usuario autenticado
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'full_name': user.full_name,
            'phone': user.phone,
            'address': user.address,
        })
    def put(self, request):  # Permite actualizar el perfil
        user = request.user
        data = request.data

        # Validar y actualizar los campos permitidos
        user.full_name = data.get('full_name', user.full_name)
        user.phone = data.get('phone', user.phone)
        user.address = data.get('address', user.address)
        user.save()

        return Response({
            'message': 'Perfil actualizado correctamente',
            'user': {
                'email': user.email,
                'full_name': user.full_name,
                'phone': user.phone,
                'address': user.address,
            }
        }, status=status.HTTP_200_OK)


# Cierre de sesión y blacklist del token de refresco
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Obtén el token de refresco desde las cookies
            refresh_token = request.COOKIES.get('refresh_token')

            if not refresh_token:
                return Response({'error': 'Token de refresco no encontrado en las cookies'}, status=400)

            # Añadir el token a la lista negra
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Elimina la cookie del token de refresco
            response = JsonResponse({'message': 'Cierre de sesión exitoso'})
            response.delete_cookie('refresh_token')
            return response

        except Exception as e:
            return Response({'error': f'Error al cerrar sesión: {str(e)}'}, status=400)

# Renovación del token de acceso usando el token de refresco
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Obtener el token de refresco desde las cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Token de refresco no encontrado.'}, status=400)

        try:
            # Validar el token y generar uno nuevo de acceso
            token = RefreshToken(refresh_token)
            return Response({'access': str(token.access_token)}, status=200)
        except InvalidToken:
            return Response({'error': 'Token inválido o expirado.'}, status=401)
