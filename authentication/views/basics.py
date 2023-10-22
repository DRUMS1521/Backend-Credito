from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveAPIView
from authentication.serializers import FetchUserSerializer
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView



class LoginView(APIView):
    def post(self, request):
        # Obtener los datos de inicio de sesión del cuerpo de la solicitud
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Realizar la autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        # Verificar si las credenciales son válidas
        if user is not None:
            # Generar tokens de acceso y actualización
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Establecer la expiración del token de acceso en 2 minutos
            access_token.set_exp(lifetime=timedelta(hours=24))
            
            # Devolver los tokens de acceso y actualización en la respuesta
            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
            })
        else:
            # Devolver un mensaje de error si las credenciales son inválidas
            return Response({'detail': 'Credenciales inválidas.'}, status=400)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Obtener el token de acceso actual del encabezado de autorización
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = authorization_header.split(' ')[1]
            
            # Invalidar el token de acceso estableciendo su fecha de expiración en el pasado
            access_token.set_exp(when=timezone.now() - timedelta(seconds=1))
            
            # Devolver un mensaje de éxito
            return Response({'detail': 'Cierre de sesión exitoso.'})
        else:
            # Devolver un mensaje de error si no se proporciona un token de acceso
            return Response({'detail': 'Token de acceso no proporcionado.'}, status=400)

class FetchUserView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FetchUserSerializer
    queryset = User.objects.all()
    
    def get_object(self):
        return self.request.user
    
class ChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FetchUserSerializer
    queryset = User.objects.all()
    
    def post(self, request):
        user = request.user
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        return Response({'detail': 'Contraseña actualizada con éxito.'})
    
class ResetEmployeePassword(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FetchUserSerializer
    queryset = User.objects.all()
    
    def post(self, request):
        if request.user.is_superuser == False:
            return Response({'detail': 'No tienes permiso para realizar esta acción.'})
        user = User.objects.get(id=request.data.get('user_id'))
        user.set_password('1234')
        user.save()
        return Response({'detail': 'Contraseña actualizada con éxito.'})
    
class DeactivateOrActivateEmployee(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FetchUserSerializer
    queryset = User.objects.all()
    
    def post(self, request):
        if request.user.is_superuser == False:
            return Response({'detail': 'No tienes permiso para realizar esta acción.'})
        user = User.objects.get(id=request.data.get('user_id'))
        if user.is_active == False:
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        return Response({'detail': 'Estado actualizado con éxito.'})