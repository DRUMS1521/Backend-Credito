# Generated by Django 4.2.3 on 2023-08-06 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0006_alter_clientes_estado_cliente_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='estado_credito',
        ),
    ]
