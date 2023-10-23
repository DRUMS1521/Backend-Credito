from django.db import models
from django.contrib.auth.models import User

class Clientes(models.Model):
    STATUS_CHOICES = (
        (1, 'activo'),
        (0, 'inactivo')
    )
    CUSTOMER_TYPE_CHOICES = (
        ('old', 'Antiguo'),
        ('new', 'Nuevo')
    )

    id_cliente = models.AutoField("clientes.Clientes", primary_key=True)
    nombre = models.CharField(max_length=20, null=False)
    apellido = models.CharField(max_length=20, null=False)
    estado_cliente = models.IntegerField(choices=STATUS_CHOICES, default=0)
    tipo_cliente = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='new')
    nacionalidad = models.CharField(max_length=60, null=False)
    nacimiento = models.DateField(null=False)
    direccion_1 = models.CharField(max_length=30, null=False)
    direccion_2 = models.CharField(max_length=30, null=True, blank=True)
    numero_celular_1 = models.CharField(max_length=10, null=False, unique=True)
    numero_celular_2 = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    empleado_responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)