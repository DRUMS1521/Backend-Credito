from django.db import models

class DailyCheckout(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=False)
    incomes = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    initial_balance = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    collected = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    loans = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    expenses = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    final_balance = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    not_collected = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    customers_not_collected = models.IntegerField(null=False, default=0)
    customers_collected = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'DailyCheckouts'
        db_table = 'daily_checkouts'