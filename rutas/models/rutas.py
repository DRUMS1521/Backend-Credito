from django.db import models
from clientes.models import Clientes



class Rutas(models.Model):

    id_ruta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    saldo_a_cobrar = models.IntegerField(null=True)
    valor_cobrado = models.IntegerField(null=True)
    
#tabla Gastos

