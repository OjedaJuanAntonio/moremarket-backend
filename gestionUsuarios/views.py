from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
# import logging
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

# logger = logging.getLogger(__name__)

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         print("Login endpoint alcanzado")  # Agrega este log
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Autenticar usuario
#         user = authenticate(request, username=email, password=password)
#         print(f"Usuario autenticado: {user}")  # Log adicional

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'message': 'Inicio de sesión exitoso'
#             }, status=status.HTTP_200_OK)

#         return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


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
                'message': 'Inicio de sesión exitoso'
            })
            response.set_cookie(
                'refresh_token',
                str(refresh),
                httponly=True,  # Solo accesible por el servidor
                secure=True,    # Usar solo en HTTPS (importante para producción)
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



# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             # Obtén el token de refresco del cuerpo de la solicitud
#             refresh_token = request.data.get('refresh')

#             if not refresh_token:
#                 return Response({'error': 'Token de refresco no proporcionado'}, status=400)

#             # Añadir el token a la lista negra
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response({'message': 'Cierre de sesión exitoso'}, status=200)

#         except Exception as e:
#             return Response({'error': 'Error al cerrar sesión: {}'.format(str(e))}, status=400)
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
        


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Obtener el token de refresco desde las cookies
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is not None:
            return Response({'error': 'No se encontró token de refresco'}, status=400)

        try:
            # Validar el token y generar uno nuevo de acceso
            token = RefreshToken(refresh_token)
            return Response({'access': str(token.access_token)}, status=200)
        except InvalidToken:
            return Response({'error': 'Token inválido o expirado'}, status=401)
