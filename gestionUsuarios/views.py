from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken



from rest_framework.permissions import AllowAny  # Permitir acceso público





class RegisterView(APIView):
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


# class LoginView(APIView):
#     permission_classes = [AllowAny]  # Permitir acceso sin autenticación previa

#     def post(self, request):
#         print("Solicitud recibida en LoginView.")  # Depuración 1
#         email = request.data.get('email')
#         password = request.data.get('password')
#         print(f"Datos recibidos: email={email}, password={password}")  # Depuración 2

#         user = authenticate(request, username=email, password=password)
#         print(f"Resultado de authenticate: {user}")  # Depuración 3

#         if user is not None:
#             return Response({'message': 'Inicio de jj sesión exitoso'}, status=status.HTTP_200_OK)
#         return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Intentar autenticar al usuario
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)  # Aquí inicias la sesión

#             print(f"Usuario {user.username} ha iniciado sesión correctamente.")  # Confirmar en consola
#             return Response({'message': f'Inicio de sesión exitoso para {user.username}.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    permission_classes = []  # Permitir acceso público

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Autenticar usuario
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Inicio de sesión exitoso'
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

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
