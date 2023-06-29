from django.db import models
from clientes.models import Clientes
from empleados.models import Empleados
from django.core.validators import MaxValueValidator
# Create your models here.
class Creditos(models.Model):
            
    id_credito = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    cantidad_dias = models.IntegerField(default=0, null=False)
    interes = models.IntegerField(default=0, validators=[MaxValueValidator(99)], null=False)
    fecha_inicio = models.DateField (null=False)
