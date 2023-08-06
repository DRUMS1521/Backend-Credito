from rest_framework import serializers
from clientes.models.clientes import Clientes




class ClienteSerializer(serializers.ModelSerializer):
    direccion_2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    numero_celular_2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    class Meta:
        model = Clientes
        fields = '__all__'
