from rest_framework import serializers
from empleados.models import Empleados
from django.contrib.auth.models import User
from datetime import datetime
import pdb
from rutas.models import Rutas

class EmpleadoSerializer(serializers.Serializer):

    id_empleado = serializers.IntegerField(read_only=True)
    cedula = serializers.CharField(
        required=True, allow_null=False, allow_blank=False)
    numero_celular_1 = serializers.CharField(
        required=True, allow_null=False, allow_blank=False)
    fecha_inicio = serializers.DateField(read_only=True)
    email_write = serializers.EmailField(
        required=True, allow_null=False, allow_blank=False, write_only=True)
    first_name_write = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, write_only=True)
    last_name_write = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, write_only=True)
    password = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    ruta_write = serializers.IntegerField(write_only=True, allow_null=False, required=True)
    ruta = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        fields = [
            "id_empleado",
            "cedula",
            "numero_celular_1",
            "fecha_inicio",
            "email_write",
            "first_name",
            "last_name",
            "password",
            "user",
            'first_name',
            'last_name',
            'email',
            'ruta',
            'ruta_write'
        ]

    def get_ruta(self, obj):
        try:
            ruta = Rutas.objects.get(id_empleado=obj)
        except:
            return None
        else:
            return ruta.id_ruta

    def validate(self, attrs):
        try:
            Empleados.objects.get(cedula=attrs["cedula"])
            #pdb.set_trace()
            
        except:
            pass
        else:
            raise serializers.ValidationError("cedula ya Existe")
        try:
            Empleados.objects.get(numero_celular_1=attrs["numero_celular_1"])
            
        except:
            pass
        else:
            raise serializers.ValidationError("numero de Celular ya existe")
        try:
            User.objects.get(email=attrs["email_write"])
        except:
            pass
        else:
            raise serializers.ValidationError("email ya existe")
        #validate that this route is not already assigned to another employee
        try:
            this_route = Rutas.objects.get(id_ruta=attrs["ruta_write"])
        except:
            raise serializers.ValidationError("ruta no existe")
        return attrs

    def create(self, validated_data):

        user = User.objects.create(username=validated_data["email_write"], email=validated_data["email_write"], first_name=validated_data["first_name_write"], last_name=validated_data["last_name_write"])
        user.set_password(validated_data["password"])
        user.save()
        empledo = Empleados.objects.create(
            cedula=validated_data["cedula"], numero_celular_1=validated_data["numero_celular_1"], fecha_inicio=datetime.now(), user=user)
        ruta = Rutas.objects.get(id_ruta=validated_data["ruta_write"])
        ruta.id_empleado = empledo
        ruta.save()
        return empledo
