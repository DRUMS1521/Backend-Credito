from django.db import models

class Clientes(models.Model):
    STATUS_CHOICES = (
        (1, 'activo'),
        (0, 'inactivo')
    )

    LOAN_STATUS = (
        (1, 'Excelente'),
        (2, 'Bueno'),
        (3, 'Regular'),
        (4, 'Malo'),
        (5, 'Muy Malo')
    )

    id_cliente = models.AutoField("clientes.Clientes", primary_key=True)
    nombre = models.CharField(max_length=20, null=False)
    apellido = models.CharField(max_length=20, null=False)
    estado_cliente = models.IntegerField(choices=STATUS_CHOICES, default=0)
    estado_credito = models.IntegerField(choices=LOAN_STATUS, default=2)
    nacionalidad = models.CharField(max_length=15, null=False)
    nacimiento = models.DateField(null=False)
    direccion_1 = models.CharField(max_length=30, null=False)
    direccion_2 = models.CharField(max_length=30, null=True, blank=True)
    numero_celular_1 = models.CharField(max_length=10, null=False, unique=True)
    numero_celular_2 = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    ruta = models.ForeignKey("rutas.Rutas", on_delete=models.SET_NULL,null=True)