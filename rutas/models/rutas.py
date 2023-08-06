from django.db import models
from clientes.models import Clientes
from empleados.models import Empleados



class Rutas(models.Model):

    id_ruta = models.AutoField(primary_key=True)
    id_empleado = models.OneToOneField(Empleados, on_delete=models.CASCADE, default=None, null=True)
    
#tabla Gastos

