from django.db import models

from app.authentication.models import User
from app.core.models import UploadedFiles
from app.loans.models.customers import Customer
from app.core.constants import LOAN_RECURRENCE_CHOICES
from app.accounting.models import Wallet, WalletMovement
import datetime

class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    authorized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    interest_rate = models.DecimalField(null=False, default=0.02, decimal_places=2, max_digits=5)
    interest_amount = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    recurrence = models.CharField(choices=LOAN_RECURRENCE_CHOICES, null=False, default='daily', max_length=255)
    dues = models.IntegerField(null=True)
    due_amount = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    start_date = models.DateField(null=False, default=datetime.date.today)
    #Balance
    interest_amount_paid = models.DecimalField(null=False, default=0, decimal_places=2, max_digits=10)
    principal_amount_paid = models.DecimalField(null=False, default=0, decimal_places=2, max_digits=10)
    dues_paid = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Loans'
        db_table = 'loans'

    def save(self, *args, **kwargs):
        # Calculate interest amount
        self.interest_amount = self.amount * self.interest_rate
        super(Loan, self).save(*args, **kwargs)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Payments'
        db_table = 'payments'

    
    def save(self, *args, **kwargs):
        #Check if amount goes to interest or principal, and update loan balance. First customers have to pay interest, then principal
        amount = self.amount
        if self.loan.interest_amount_paid < self.loan.interest_amount:
            if self.loan.interest_amount_paid + amount > self.loan.interest_amount:
                amount = self.loan.interest_amount - self.loan.interest_amount_paid
            self.loan.interest_amount_paid += amount
        else:
            if self.loan.principal_amount_paid + amount > self.loan.amount:
                amount = self.loan.amount - self.loan.principal_amount_paid
            self.loan.principal_amount_paid += amount
        self.loan.save()
        # Updatedues paid
        total_paid = self.loan.interest_amount_paid + self.loan.principal_amount_paid
        self.loan.dues_paid = int(total_paid / self.loan.due_amount)
        self.loan.save()
        # Create wallet movement
        destiny_wallet = Wallet.objects.get(user=self.loan.customer.debt_collector)
        WalletMovement.objects.create(wallet=destiny_wallet, type='deposit', amount=amount, reason=f'Entrada por cobro de prestamo del día {self.created_at} del cliente {self.loan.customer.name} por un monto de {amount} id de prestamo {self.loan.id}')
        super(Payment, self).save(*args, **kwargs)