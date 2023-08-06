from rest_framework import generics
from ..models.clientes import Clientes
from ..serializers import ClienteSerializer
from rest_framework import permissions

class ClientesListView(generics.ListCreateAPIView, generics.CreateAPIView):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    

class ClienteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
