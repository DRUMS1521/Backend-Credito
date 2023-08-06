from rest_framework import serializers
from clientes.models.clientes import Clientes

class ClienteSerializer(serializers.ModelSerializer):
    id_cliente = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(required=True)
    apellido = serializers.CharField(required=True)
    estado_cliente = serializers.IntegerField(required=False)
    estado_credito = serializers.IntegerField(required=False)
    estado_del_cliente = serializers.CharField(source='get_estado_cliente_display', read_only=True)
    estado_del_credito = serializers.CharField(source='get_estado_credito_display', read_only=True)
    direccion_2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    numero_celular_2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    class Meta:
        model = Clientes
        fields = '__all__'

    def validate(self, attrs):
        if attrs['numero_celular_1'] == attrs['numero_celular_2']:
            raise serializers.ValidationError("Los numeros de celular no pueden ser iguales")
        if attrs['direccion_1'] == attrs['direccion_2']:
            raise serializers.ValidationError("Las direcciones no pueden ser iguales")
        #validate unique email
        if attrs['email'] is not None:
            if Clientes.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError("El email ya existe")
        #validate unique numero_celular_1
        if Clientes.objects.filter(numero_celular_1=attrs['numero_celular_1']).exists():
            raise serializers.ValidationError("El numero de celular ya existe")
        return attrs
    
    def create(self, validated_data):
        return Clientes.objects.create(**validated_data)
