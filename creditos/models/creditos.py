from django.db import models
from clientes.models import Clientes
from empleados.models import Empleados
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Creditos(models.Model):

    STATUS_CHOICES = (
        (1, 'Excelente'),
        (2, 'Bueno'),
        (3, 'Regular'),
        (4, 'Malo'),
        (5, 'Muy Malo'),
    )
    
    id_credito = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    cantidad_dias = models.PositiveIntegerField(default=0, null=False)
    interes = models.IntegerField(default=20, validators=[MaxValueValidator(99)], null=False)
    fecha_inicio = models.DateField(null=False)
    valor_credito = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fecha_finalizacion_estimada = models.DateField(null=False)
    fecha_finalizacion_real = models.DateField(null=True)
    cuotas_pagadas = models.PositiveIntegerField(null=False, default=0)
    credito_finalizado = models.BooleanField (null=False, default= False)
    cuota_diaria = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    estado = models.PositiveIntegerField(choices=STATUS_CHOICES, default=2, null=False)
    
    
class Payments(models.Model):
    
    credito = models.ForeignKey(Creditos, on_delete=models.SET_NULL, related_name="payments", null=True)
    fecha_pago = models.DateField(auto_now=False, auto_now_add=False)
    responsable = models.ForeignKey(User, on_delete= models.SET_NULL, null= True)
    monto_pago = models.DecimalField( decimal_places=2, max_digits=10, null= True)
    pagado_completo = models.BooleanField(default= False, null=False)
    numero_cuota = models.PositiveIntegerField(null=False)
    cuotas_pendientes = models.PositiveIntegerField(null=False)
    fecha_actualizacion = models.DateField(auto_now_add=True, null= True)
    monto_esperado = models.DecimalField( decimal_places=2, max_digits=10)