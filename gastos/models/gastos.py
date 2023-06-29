from django.db import models

# Create your models here.
class Gastos(models.Model):
        
    id_gastos = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey( 'empleados.Empleados', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30,null=False)
    descripcion = models.CharField(max_length=200)
    fecha_gasto = models.DateField(null=False)
    valor_gasto = models.CharField(max_length=20, null=False)