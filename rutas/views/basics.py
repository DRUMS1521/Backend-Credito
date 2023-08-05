from rest_framework import generics
from rutas.models import Rutas
from rutas.serializers import RutasSerializer
from rest_framework import permissions 


class RutasListView(generics.ListCreateAPIView):
    queryset = Rutas.objects.all()
    serializer_class = RutasSerializer
    permission_classes =[ permissions.IsAdminUser]

class RutasDetailView(generics.RetrieveUpdateAPIView):
    queryset = Rutas.objects.all()
    serializer_class = RutasSerializer
    permission_classes =[ permissions.IsAdminUser]

