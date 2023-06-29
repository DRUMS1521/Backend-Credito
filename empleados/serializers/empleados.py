from rest_framework import serializers
from empleados.models import Empleados

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleados
        fields = '__all__'
