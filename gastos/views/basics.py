from rest_framework import generics
from gastos.models import Gastos
from gastos.serializers import GastosSerializer

class GastosListView(generics.ListCreateAPIView):
    queryset = Gastos.objects.all()
    serializer_class = GastosSerializer

class GastosDetailView(generics.RetrieveUpdateAPIView):
    queryset = Gastos.objects.all()
    serializer_class = GastosSerializer
