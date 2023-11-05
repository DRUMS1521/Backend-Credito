from django.db import models
from app.core.constants import WALLET_MOVEMENT_TYPE_CHOICES

class Wallet(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, null=False, primary_key=True)
    balance = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Wallets'
        db_table = 'wallets'

class WalletMovement(models.Model):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False)
    type = models.CharField(choices=WALLET_MOVEMENT_TYPE_CHOICES, null=False, default='deposit', max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    name = models.CharField(max_length=255, null=True)
    reason = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'WalletMovements'
        db_table = 'wallet_movements'

    def save(self, *args, **kwargs):
        if self.type == 'deposit':
            self.wallet.balance += self.amount
        else:
            self.wallet.balance -= self.amount
        self.wallet.save()
        super(WalletMovement, self).save(*args, **kwargs)