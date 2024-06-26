# Generated by Django 3.2 on 2024-06-26 01:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0012_alter_walletmovement_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGoals',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('borrowed_goal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('borrowed', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('collected_goal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('collected', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('loans_finished_goal', models.IntegerField(default=0)),
                ('loans_finished', models.IntegerField(default=0)),
                ('new_customers_goal', models.IntegerField(default=0)),
                ('new_customers', models.IntegerField(default=0)),
                ('clavos_recovered_goal', models.IntegerField(default=0)),
                ('clavos_recovered', models.IntegerField(default=0)),
                ('period_closure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.periodclosures')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserGoals',
                'db_table': 'user_goals',
                'ordering': ['-id'],
            },
        ),
    ]
