from django.contrib.auth.models import User
from rest_framework import serializers
from empleados.models import Empleados
from rutas.models import Rutas


class FetchUserSerializer(serializers.ModelSerializer):
    empleado = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "empleado"
        ]
        
    def get_empleado(self, obj):
        try:
            empleado = Empleados.objects.get(user=obj)
        except:
            return {}
        else:
            try:
                ruta = Rutas.objects.get(id_empleado= empleado).id_ruta
            except:
                ruta = None
            return {
                "cedula": empleado.cedula,
                "numero_celular_1": empleado.numero_celular_1,
                "ruta": ruta
            }
        
    