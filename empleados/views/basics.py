from rest_framework import generics
from empleados.models import Empleados
from empleados.serializers import EmpleadoSerializer
from rest_framework import permissions 


class EmpleadosListView(generics.ListCreateAPIView):
    queryset = Empleados.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes =[ permissions.IsAdminUser]
    pagination_class = None
    
class EmpleadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Empleados.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes =[ permissions.IsAdminUser]
