# Generated by Django 3.2 on 2024-05-03 19:46

from django.db import migrations

def create_initial_config(apps, schema_editor):
    CustomConfig = apps.get_model('core', 'CustomConfig')
    CustomConfig.objects.create(key='interest_rate', value='0.2')

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_customconfig'),
    ]

    operations = [
        migrations.RunPython(create_initial_config),
    ]
