from django.db import models
from app.core.constants import WALLET_MOVEMENT_TYPE_CHOICES
import datetime
from django.utils import timezone

class Wallet(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, null=False, primary_key=True)
    balance = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    created_at = models.DateTimeField(default=timezone.now)
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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_balance = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    current_balance = models.DecimalField(max_digits=19, decimal_places=2, null=False, default=0)
    proof = models.ForeignKey('core.UploadedFiles', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'WalletMovements'
        db_table = 'wallet_movements'

    def save(self, *args, **kwargs):
        amount = abs(self.amount)
        self.last_balance = self.wallet.balance
        if self.type not in ['entry', 'loan_in', 'admin_charge', 'positive_delete_loan']:
            self.amount = amount * -1
        self.wallet.balance += self.amount
        self.wallet.save()
        self.current_balance = self.wallet.balance
        super(WalletMovement, self).save(*args, **kwargs)