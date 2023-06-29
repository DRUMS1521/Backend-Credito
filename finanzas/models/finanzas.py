from django.db import models
from gastos.models.gastos import Gastos

# Create your models here.
class Finanzas (models.Model):

    id_finanzas = models.AutoField(primary_key=True)
    id_gastos = models.ForeignKey(Gastos, on_delete=models.CASCADE)
    dinero_capital = models.IntegerField(null=True)