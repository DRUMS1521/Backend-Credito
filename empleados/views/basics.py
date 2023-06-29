from rest_framework import generics
from empleados.models import Empleados
from empleados.serializers import EmpleadoSerializer

class EmpleadosListView(generics.ListCreateAPIView):
    queryset = Empleados.objects.all()
    serializer_class = EmpleadoSerializer

class EmpleadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Empleados.objects.all()
    serializer_class = EmpleadoSerializer
