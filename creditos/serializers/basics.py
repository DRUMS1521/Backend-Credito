from rest_framework import serializers
from creditos.models.creditos import Creditos, Payments
from empleados.models import Empleados
from clientes.models import Clientes
from datetime import datetime, timedelta



class CreditoSerializer(serializers.ModelSerializer):

    id_credito = serializers.IntegerField(read_only= True)
    id_cliente = serializers.PrimaryKeyRelatedField(queryset= Clientes.objects.all(),allow_null=False, required=True)
    id_empleado = serializers.PrimaryKeyRelatedField(read_only=True)
    cantidad_dias = serializers.IntegerField(min_value= 5, max_value=60,allow_null=False, required=True)
    interes = serializers.IntegerField(min_value= 5, max_value=50,allow_null=False, required=True)
    fecha_inicio = serializers.DateField(allow_null=False, required=True)
    valor_credito = serializers.DecimalField(decimal_places=2, max_digits=10)
    fecha_finalizacion_estimada = serializers.DateField(read_only=True) 
    fecha_finalizacion_real =serializers.DateField(read_only=True)
    cuotas_pagadas = serializers.IntegerField(read_only=True)
    credito_finalizado = serializers.BooleanField(read_only=True)
    cuota_diaria = serializers.IntegerField(read_only=True)
    
    class Meta: 
        model = Creditos
        fields = [
            "id_credito",
            "id_cliente",
            "id_empleado",
            "cantidad_dias",
            "interes",
            "fecha_inicio",
            "valor_credito",
            "fecha_finalizacion_estimada",
            "fecha_finalizacion_real",
            "cuotas_pagadas",
            "credito_finalizado",
            "cuota_diaria",
        ]
    
    def validate(self, attrs):
        attrs["cuota_diaria"] = float(attrs["valor_credito"])*(1+(attrs["interes"]/100))/attrs["cantidad_dias"]
        attrs["fecha_finalizacion_estimada"] = attrs["fecha_inicio"]+timedelta(days=attrs["cantidad_dias"])
        attrs["id_empleado"]=attrs["id_cliente"].ruta.id_empleado
        return attrs
        
    def create(self, validated_data):
        obj = Creditos.objects.create(**validated_data)
        for i in range(1,validated_data["cantidad_dias"]+1):
            responsable = obj.id_cliente.ruta.id_empleado
            Payments.objects.create(
                credito = obj,
                fecha_pago = obj.fecha_inicio+timedelta(days = i-1),
                responsable = responsable,
                monto_pago = None, 
                pagado_completo = False,
                numero_cuota = i,
                cuotas_pendientes = obj.cantidad_dias - i,
                fecha_actualizacion = None,
                monto_esperado = obj.cuota_diaria
            )
        return obj