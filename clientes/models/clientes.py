from django.db import models

class Clientes(models.Model):
    class status_cliente(models.IntegerChoices):
        OPCION_A = 1, 'activo'
        OPCION_B = 2, 'desactivado'

    class status_credito(models.IntegerChoices):
        OPCION_A = 1, 'excelente'
        OPCION_B = 2, 'bien'
        OPCION_C = 3, 'mal'
        OPCION_D = 4, 'muy_mal'

    id_cliente = models.AutoField("clientes.Clientes", primary_key=True)
    nombre = models.CharField(max_length=20, null=False)
    apellido = models.CharField(max_length=20, null=False)
    estado_cliente = models.IntegerField(choices=status_cliente.choices)
    estado_credito = models.IntegerField(choices=status_credito.choices, null=True)
    nacionalidad = models.CharField(max_length=15, null=False)
    nacimiento = models.DateField(null=False)
    direccion_1 = models.CharField(max_length=30, null=False)
    direccion_2 = models.CharField(max_length=30, null=True)
    numero_celular_1 = models.CharField(max_length=10, null=False)
    numero_celular_2 = models.CharField(max_length=10, null=True)
    email = models.EmailField(unique=True, null=True)
    ruta = models.ForeignKey("rutas.Rutas", on_delete=models.SET_NULL,null=True)