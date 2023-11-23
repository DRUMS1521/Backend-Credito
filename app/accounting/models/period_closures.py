from django.db import models

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