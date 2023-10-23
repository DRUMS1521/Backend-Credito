# Generated by Django 4.2.3 on 2023-10-23 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('creditos', '0011_remove_payments_ruta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='credito',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='creditos.creditos'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
