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
    email = serializers.EmailField(
        required=True, allow_null=False, allow_blank=False, write_only=True)
    first_name = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, write_only=True)
    last_name = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, write_only=True)
    password = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    

    class Meta:
        fields = [
            "id_empleado",
            "cedula",
            "numero_celular_1",
            "fecha_inicio",
            "email",
            "first_name",
            "last_name",
            "password",
            "user",
            'first_name',
            'last_name',
            'email',
        ]

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
            User.objects.get(email=attrs["email"])
            
        except:
            pass
        else:
            raise serializers.ValidationError("email ya existe")

        return attrs

    def create(self, validated_data):

        user = User.objects.create(email=validated_data["email"], username=validated_data["email"],
                                first_name=validated_data["first_name"], last_name=validated_data["last_name"])
        user.set_password(validated_data["password"])
        user.save()
        empledo = Empleados.objects.create(
            cedula=validated_data["cedula"], numero_celular_1=validated_data["numero_celular_1"], fecha_inicio=datetime.now(), user=user)

        return empledo
