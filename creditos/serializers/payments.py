from rest_framework import serializers
from creditos.models.creditos import Creditos, Payments
from empleados.models import Empleados
from clientes.models import Clientes
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pdb
from decimal import Decimal

class PaymentsDetailSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    fecha_pago = serializers.DateField(read_only=True)
    monto_pago = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    pagado_completo = serializers.BooleanField(read_only=True)
    numero_cuota = serializers.IntegerField(read_only=True)
    cuotas_pendientes = serializers.IntegerField(read_only=True)
    ruta_id = serializers.IntegerField(source='ruta.id_ruta',read_only=True)
    credito_id = serializers.IntegerField(source='credito.id_credito',read_only=True)
    monto_esperado = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    finalizado = serializers.SerializerMethodField(read_only=True)
    nombre = serializers.CharField(source='credito.id_cliente.nombre', read_only=True)
    apellido = serializers.CharField(source='credito.id_cliente.apellido', read_only=True)
    direccion = serializers.CharField(source='credito.id_cliente.direccion_1', read_only=True)
    telefono = serializers.CharField(source='credito.id_cliente.telefono_1', read_only=True)
    email = serializers.CharField(source='credito.id_cliente.email', read_only=True)
    cuotas_pagadas = serializers.IntegerField(source='credito.cuotas_pagadas', read_only=True)
    total_pendiente = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Payments
        fields = ['id', 'fecha_pago', 'monto_pago', 'pagado_completo', 'numero_cuota', 'cuotas_pendientes', 'ruta_id', 'credito_id', 'monto_esperado', 'finalizado', 'nombre', 'apellido', 'direccion', 'telefono', 'email', 'cuotas_pagadas', 'total_pendiente']

    def get_finalizado(self, obj):
        if obj.monto_pago is not None:
            return True
        else:
            return False
        
    def get_total_pendiente(self, obj):
        try:
            credito = obj.credito
        except:
            return None
        #first, sum all payments
        payments = Payments.objects.filter(credito=credito)
        total_paid = 0
        for payment in payments:
            if payment.monto_pago is not None:
                total_paid += payment.monto_pago
        #second, calculate max amount to pay
        max_amount = Decimal(Decimal(credito.valor_credito)*Decimal(Decimal(1)+Decimal(Decimal(credito.interes)/100))) - Decimal(total_paid)
        return max_amount

class PaymentsSerializer(serializers.ModelSerializer):

    monto_pago = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Payments
        fields = ['monto_pago']

    def validate(self, attrs):
        if self.instance.monto_pago is not None:
            raise serializers.ValidationError("El pago ya fue realizado")
        if attrs['monto_pago'] < 0:
            raise serializers.ValidationError("El monto a pagar no puede ser menor a 0")
        #calculate max amount to pay
        credito = self.instance.credito
        #first, sum all payments
        payments = Payments.objects.filter(credito=credito)
        total_paid = 0
        for payment in payments:
            if payment.monto_pago is not None:
                total_paid += payment.monto_pago
        #second, calculate max amount to pay
        max_amount = Decimal(Decimal(credito.valor_credito)*Decimal(Decimal(1)+Decimal(Decimal(credito.interes)/100))) - Decimal(total_paid)
        if attrs['monto_pago'] > max_amount:
            raise serializers.ValidationError("El monto a pagar no puede ser mayor a {}".format(max_amount))
        #calculate if is pagado_completo
        if attrs['monto_pago'] >= self.instance.monto_esperado:
            attrs['pagado_completo'] = True
        else:
            attrs['pagado_completo'] = False
        #set responsable
        try:
            attrs['responsable'] = Empleados.objects.get(user=self.context['request'].user)
        except:
            raise serializers.ValidationError("No se puede obtener el usuario, el usuario no es un empleado")
        return attrs
    
    def update(self, instance, validated_data):
        instance.monto_pago = validated_data['monto_pago']
        instance.pagado_completo = validated_data['pagado_completo']
        instance.responsable = validated_data['responsable']
        instance.save()
        #update credito
        credito = Creditos.objects.get(id_credito = instance.credito.id_credito)
        valor_final_credito = Decimal(Decimal(credito.valor_credito)*Decimal(Decimal(1)+Decimal(Decimal(credito.interes)/100)))
        total_paid = Decimal(0)
        payments = Payments.objects.filter(credito=credito)
        for payment in payments:
            if payment.monto_pago is not None:
                total_paid += Decimal(payment.monto_pago)
        credito.cuotas_pagadas += 1
        credito.save()
        #first calculate if is the last payment and the amout satisfied the credit
        if instance.numero_cuota == credito.cantidad_dias:
            if total_paid == valor_final_credito:
                credito.credito_finalizado = True
                credito.fecha_finalizacion_real = instance.fecha_pago
                credito.save()
                cliente = credito.id_cliente
                cliente.estado_cliente = 0
                cliente.save()
            else:
                credito.cantidad_dias += 1
                credito.save()
                Payments.objects.create(
                    fecha_pago = instance.fecha_pago + timedelta(days=1),
                    monto_esperado = valor_final_credito - total_paid,
                    numero_cuota = instance.numero_cuota+1,
                    ruta = instance.ruta,
                    credito = credito,
                    monto_pago = None,
                    cuotas_pendientes = 1,
                    responsable = None
                )
        else:
            if validated_data['pagado_completo'] == False:
                next_due = Payments.objects.get(credito=credito, numero_cuota=instance.numero_cuota+1)
                next_due.monto_esperado = next_due.monto_esperado + instance.monto_esperado - validated_data['monto_pago']
                next_due.save()
            else:
                if validated_data['monto_pago']>instance.monto_esperado:
                    remaining_amount = validated_data['monto_pago'] - instance.monto_esperado
                    amount_to_finish = valor_final_credito - total_paid
                    next_due_value = Payments.objects.get(credito=credito, numero_cuota=instance.numero_cuota+1).monto_esperado
                    if remaining_amount == amount_to_finish:
                        credito.credito_finalizado = True
                        credito.fecha_finalizacion_real = instance.fecha_pago
                        credito.save()
                        cliente = credito.id_cliente
                        cliente.estado_cliente = 0
                        cliente.save()
                        #update next dues
                        next_dues = Payments.objects.filter(credito=credito, numero_cuota__gt=instance.numero_cuota)
                        for due in next_dues:
                            due.monto_pago = 0
                            due.pagado_completo = True
                            due.fecha_pago = instance.fecha_pago
                            due.save()
                    elif remaining_amount <= next_due_value:
                        next_due = Payments.objects.get(credito=credito, numero_cuota=instance.numero_cuota+1)
                        next_due.monto_esperado = next_due.monto_esperado - remaining_amount
                        if next_due.monto_esperado == 0:
                            next_due.pagado_completo = True
                            next_due.fecha_pago = instance.fecha_pago
                            next_due.monto_pago = 0
                        next_due.save()
                    else:
                        i=1
                        new_remainig_amount = remaining_amount
                        new_next_due_value = next_due_value
                        while new_remainig_amount > 0:
                            if new_remainig_amount >= new_next_due_value:
                                next_due = Payments.objects.get(credito=credito, numero_cuota=instance.numero_cuota+i)
                                next_due.monto_esperado = 0
                                next_due.pagado_completo = True
                                next_due.fecha_pago = instance.fecha_pago
                                next_due.monto_pago = 0
                                next_due.save()
                                new_remainig_amount = new_remainig_amount - new_next_due_value
                                i += 1
                                if next_due.numero_cuota == credito.cantidad_dias:
                                    credito.credito_finalizado = True
                                    credito.fecha_finalizacion_real = instance.fecha_pago
                                    credito.save()
                                    cliente = credito.id_cliente
                                    cliente.estado_cliente = 0
                                    cliente.save()
                                    break
                                else:
                                    new_next_due_value = Payments.objects.get(credito=credito, numero_cuota=instance.numero_cuota+i).monto_esperado
                            else:
                                next_due = Payments.objects.get(credito=credito, numero_cuota=instance.numero_cuota+i)
                                next_due.monto_esperado = next_due.monto_esperado - new_remainig_amount
                                if next_due.monto_esperado == 0:
                                    next_due.pagado_completo = True
                                    next_due.fecha_pago = instance.fecha_pago
                                    next_due.monto_pago = 0
                                next_due.save()
                                new_remainig_amount = 0
        return instance