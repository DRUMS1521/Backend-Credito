# Generated by Django 3.2 on 2024-04-08 23:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0014_custom_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]