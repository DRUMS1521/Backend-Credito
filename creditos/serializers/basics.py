from rest_framework import serializers
from creditos.models.creditos import Creditos, Payments
from empleados.models import Empleados
from clientes.models import Clientes
from datetime import datetime, timedelta



class CreditoSerializer(serializers.ModelSerializer):

    id_credito = serializers.IntegerField(read_only= True)
    id_cliente = serializers.PrimaryKeyRelatedField(queryset= Clientes.objects.all(),allow_null=False, required=True)
    nombre_cliente = serializers.CharField(source='id_cliente.nombre', read_only=True)
    apellido_cliente = serializers.CharField(source='id_cliente.apellido', read_only=True)
    direccion_cliente = serializers.CharField(source='id_cliente.direccion_1', read_only=True)
    numero_celular_cliente = serializers.CharField(source='id_cliente.numero_celular_1', read_only=True)
    ruta = serializers.IntegerField(source='id_cliente.ruta.id_ruta', read_only=True)
    empleado = serializers.IntegerField(source='id_cliente.ruta.id_empleado.id_empleado', read_only=True)
    cantidad_dias = serializers.IntegerField(min_value= 5, max_value=60,allow_null=False, required=True)
    interes = serializers.IntegerField(min_value= 5, max_value=50,allow_null=False, required=True)
    fecha_inicio = serializers.DateField(allow_null=False, required=True)
    valor_credito = serializers.DecimalField(decimal_places=2, max_digits=10)
    fecha_finalizacion_estimada = serializers.DateField(read_only=True) 
    fecha_finalizacion_real =serializers.DateField(read_only=True)
    cuotas_pagadas = serializers.IntegerField(read_only=True)
    credito_finalizado = serializers.BooleanField(read_only=True)
    cuota_diaria = serializers.IntegerField(read_only=True)
    credit_details = serializers.SerializerMethodField(read_only=True)
    estado = serializers.IntegerField(read_only=True)
    status = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta: 
        model = Creditos
        fields = [
            'id_credito',
            'id_cliente',
            'nombre_cliente',
            'apellido_cliente',
            'direccion_cliente',
            'numero_celular_cliente',
            'ruta',
            'empleado',
            'cantidad_dias',
            'interes',
            'fecha_inicio',
            'valor_credito',
            'fecha_finalizacion_estimada',
            'fecha_finalizacion_real',
            'cuotas_pagadas',
            'credito_finalizado',
            'cuota_diaria',
            'estado',
            'status',
            'credit_details'
        ]
    
    def get_credit_details(self, obj):
        payments = Payments.objects.filter(credito=obj).order_by('id')
        dues_detail = []
        if len(payments) > 0:
            total_paid = 0
            dues_paid = 0
            for payment in payments:
                if payment.monto_pago is not None:
                    total_paid += payment.monto_pago
                if payment.pagado_completo:
                    dues_paid += 1
                dues_detail.append(
                    {
                        "fecha_pago": payment.fecha_pago,
                        "monto_pago": payment.monto_pago,
                        "pagado_completo": payment.pagado_completo,
                        "numero_cuota": payment.numero_cuota,
                        "cuotas_pendientes": payment.cuotas_pendientes,
                        "fecha_actualizacion": payment.fecha_actualizacion,
                        "monto_esperado": payment.monto_esperado
                    }
                )
            return {
                "total_paid": total_paid,
                "total_pending": obj.valor_credito - total_paid,
                "dues_paid": dues_paid,
                "dues_pending": obj.cantidad_dias - dues_paid,
                "dues_detail": dues_detail
            }
        else:
            return {}
        
        

    def validate(self, attrs):
        attrs["cuota_diaria"] = float(attrs["valor_credito"])*(1+(attrs["interes"]/100))/attrs["cantidad_dias"]
        attrs["fecha_finalizacion_estimada"] = attrs["fecha_inicio"]+timedelta(days=attrs["cantidad_dias"])
        return attrs
        
    def create(self, validated_data):
        obj = Creditos.objects.create(**validated_data)
        for i in range(1,validated_data["cantidad_dias"]+1):
            ruta = obj.id_cliente.ruta
            Payments.objects.create(
                credito = obj,
                fecha_pago = obj.fecha_inicio+timedelta(days = i-1),
                ruta = ruta,
                monto_pago = None, 
                pagado_completo = False,
                numero_cuota = i,
                cuotas_pendientes = obj.cantidad_dias - i,
                fecha_actualizacion = None,
                monto_esperado = obj.cuota_diaria,
                responsable = None
            )
        cliente = Clientes.objects.get(id_cliente=obj.id_cliente.id_cliente)
        cliente.estado_cliente = 1
        cliente.save()
        return obj