# Generated by Django 3.2 on 2023-11-05 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_walletmovement_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walletmovement',
            name='type',
            field=models.CharField(choices=[('entry', 'entry'), ('exit', 'exit'), ('loan_out', 'loan_out'), ('loan_in', 'loan_in'), ('admin_charge', 'admin_charge')], default='deposit', max_length=255),
        ),
    ]
