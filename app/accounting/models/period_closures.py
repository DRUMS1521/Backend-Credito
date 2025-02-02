from django.db import models
from django.utils import timezone
import datetime


class PeriodClosures(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    closed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'PeriodClosures'
        db_table = 'period_closures'
        ordering = ['-id']

    def __str__(self):
        return str(self.date)
    
    def get_open_period():
        period = PeriodClosures.objects.filter(closed=False).first()
        if not period:
            #Create new period with today as start_date and start_date + 1 month as end_date
            period = PeriodClosures.objects.create(start_date=timezone.now().date(), end_date=timezone.now().date() + datetime.timedelta(days=30))
        return period
    
    def save(self, *args, **kwargs):
        # Crear un flag para saber si el objeto es nuevo
        is_new = not self.id

        # Primero guardamos el objeto para asegurar que tenga un ID
        super(PeriodClosures, self).save(*args, **kwargs)

        if is_new:
            from app.authentication.models import User  # Idealmente mover esta importación al inicio del archivo

            # Cerrar todos los períodos anteriores
            PeriodClosures.objects.filter(closed=False).exclude(id=self.id).update(closed=True)

            # Crear objetivos para todos los usuarios
            users = User.objects.all()
            for user in users:
                UserGoals.objects.create(user=user, period_closure=self)
    
class UserGoals(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    period_closure = models.ForeignKey(PeriodClosures, on_delete=models.CASCADE)
    borrowed_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    borrowed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    different_loans_collected_goal = models.IntegerField(default=0)
    different_loans_collected = models.IntegerField(default=0)
    collected_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    collected = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loans_finished_goal = models.IntegerField(default=0)
    loans_finished = models.IntegerField(default=0)
    new_customers_goal = models.IntegerField(default=0)
    new_customers = models.IntegerField(default=0)
    clavos_recovered_goal = models.IntegerField(default=0)
    clavos_recovered = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'UserGoals'
        db_table = 'user_goals'
        ordering = ['-id']
        unique_together = ('user', 'period_closure')