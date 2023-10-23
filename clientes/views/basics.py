from rest_framework import generics
from ..models.clientes import Clientes
from ..serializers import ClienteSerializer
from rest_framework import permissions

class ClientesListView(generics.ListCreateAPIView):
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        # Obtener el usuario autenticado
        user = self.request.user
        # Verificar si es superusuario
        if user.is_superuser:
            # Si es superusuario, devolver todos los clientes
            return Clientes.objects.all()
        else:
            # Si no es superusuario, devolver solo los clientes que le pertenecen
            return Clientes.objects.filter(empleado_responsable=user)
    

class ClienteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
