# Generated by Django 4.2.3 on 2023-10-22 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientes', '0007_remove_clientes_estado_credito'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='ruta',
        ),
        migrations.AddField(
            model_name='clientes',
            name='empleado_responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
