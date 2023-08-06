# Generated by Django 4.2.3 on 2023-08-06 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditos', '0006_alter_creditos_fecha_finalizacion_real'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditos',
            name='estado',
            field=models.PositiveIntegerField(choices=[(1, 'Excelente'), (2, 'Bueno'), (3, 'Regular'), (4, 'Malo'), (5, 'Muy Malo')], default=2),
        ),
    ]