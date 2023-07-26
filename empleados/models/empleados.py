from django.db import models
from django.contrib.auth.models import User

# tabla empleados


class Empleados(models.Model):

    id_empleado = models.AutoField("empleados.Empleados", primary_key=True)
    cedula = models.CharField(max_length=20, unique=True)
    numero_celular_1 = models.CharField(max_length=10, null=False)
    fecha_inicio = models.DateField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.cedula
