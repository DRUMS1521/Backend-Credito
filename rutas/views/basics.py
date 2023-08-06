from rest_framework import generics
from rutas.models import Rutas
from rutas.serializers import RutasSerializer
from rest_framework import permissions 


class RutasListView(generics.ListCreateAPIView):
    queryset = Rutas.objects.all()
    serializer_class = RutasSerializer
    permission_classes =[ permissions.IsAdminUser]
    pagination_class = None

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class RutasDetailView(generics.RetrieveUpdateAPIView):
    queryset = Rutas.objects.all()
    serializer_class = RutasSerializer
    permission_classes =[ permissions.IsAdminUser]

