# Generated by Django 4.2.3 on 2023-08-07 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0005_alter_empleados_id_empleado'),
        ('rutas', '0006_alter_rutas_id_empleado'),
        ('creditos', '0008_remove_creditos_id_empleado'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='ruta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='rutas.rutas'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payments',
            name='responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='empleados.empleados'),
        ),
    ]