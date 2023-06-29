from rest_framework import generics
from ..models.clientes import Clientes
from ..serializers import ClienteSerializer

class ClientesListView(generics.ListCreateAPIView):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer

class ClienteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer
