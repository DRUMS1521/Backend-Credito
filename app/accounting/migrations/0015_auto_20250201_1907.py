# Generated by Django 3.2 on 2025-02-01 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0014_alter_usergoals_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergoals',
            name='different_loans_collected',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usergoals',
            name='different_loans_collected_goal',
            field=models.IntegerField(default=0),
        ),
    ]
