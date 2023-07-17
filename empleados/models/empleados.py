from django.db import models


#tabla empleados 
class Empleados(models.Model):

    id_empleado = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20, unique=True)
    contraseña = models.CharField(max_length=20,null=False)
    nombre = models.CharField(max_length=20,null=False)
    apellido = models.CharField(max_length=20,null=False)
    estado_empleado = models.BooleanField(default=True, choices=[(True, 'Activo'), (False, 'Inactivo')])
    numero_celular_1=models.CharField(max_length=10,null=False)
    email=models.EmailField(null=True)
    fecha_inicio = models.DateField(null=False)

    def __str__(self):
        return self.cedula