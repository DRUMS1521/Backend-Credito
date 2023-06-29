from rest_framework import generics
from rutas.models import Rutas
from rutas.serializers import RutasSerializer

class RutasListView(generics.ListCreateAPIView):
    queryset = Rutas.objects.all()
    serializer_class = RutasSerializer

class RutasDetailView(generics.RetrieveUpdateAPIView):
    queryset = Rutas.objects.all()
    serializer_class = RutasSerializer
