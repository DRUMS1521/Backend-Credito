# Generated by Django 4.2.3 on 2023-10-23 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creditos', '0010_alter_payments_fecha_actualizacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='ruta',
        ),
    ]
