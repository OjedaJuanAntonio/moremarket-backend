import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

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
# class LoginView(APIView):
#     permission_classes = [AllowAny]  # Permitir acceso público

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Autenticar usuario
#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             # Generar tokens JWT
#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'message': 'Inicio de sesión exitoso'
#             }, status=status.HTTP_200_OK)

#         return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Login endpoint alcanzado")  # Agrega este log
        email = request.data.get('email')
        password = request.data.get('password')

        # Autenticar usuario
        user = authenticate(request, username=email, password=password)
        print(f"Usuario autenticado: {user}")  # Log adicional

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Inicio de sesión exitoso'
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

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



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Obtén el token de refresco del cuerpo de la solicitud
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({'error': 'Token de refresco no proporcionado'}, status=400)

            # Añadir el token a la lista negra
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Cierre de sesión exitoso'}, status=200)

        except Exception as e:
            return Response({'error': 'Error al cerrar sesión: {}'.format(str(e))}, status=400)
