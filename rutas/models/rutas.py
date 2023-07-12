from django.db import models
from clientes.models import Clientes
from empleados.models import Empleados



class Rutas(models.Model):

    id_ruta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, default=1)
    saldo_a_cobrar = models.IntegerField(null=True)
    valor_cobrado = models.IntegerField(null=True)
    
#tabla Gastos

