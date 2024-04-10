from django.db import models

from app.authentication.models import User
from app.core.models import UploadedFiles
from app.loans.models.customers import Customer
from app.core.constants import LOAN_RECURRENCE_CHOICES
from app.accounting.models import Wallet, WalletMovement
from django.utils import timezone
#uuid
import uuid


def get_current_date():
    return timezone.now().date()


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
    start_date = models.DateField(null=False, default=get_current_date)
    #Balance
    interest_amount_paid = models.DecimalField(null=False, default=0, decimal_places=2, max_digits=10)
    principal_amount_paid = models.DecimalField(null=False, default=0, decimal_places=2, max_digits=10)
    dues_paid = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ordering = models.IntegerField(null=False, default=0)
    is_finished = models.BooleanField(null=False, default=False)
    finished_at = models.DateTimeField(null=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name_plural = 'Loans'
        db_table = 'loans'

    def save(self, *args, **kwargs):
        # Calculate interest amount
        self.interest_amount = self.amount * self.interest_rate
        # Create wallet movement
        if self.id == None:
            destiny_wallet = Wallet.objects.get(user=self.customer.debt_collector)
            WalletMovement.objects.create(wallet=destiny_wallet, name = 'pago de cuota', type='loan_out', amount=self.amount, reason=f'Salida por prestamo del cliente {self.customer.name} por un monto de {self.amount}')
        super(Loan, self).save(*args, **kwargs)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Payments'
        db_table = 'payments'

    
    def save(self, *args, **kwargs):
        #Check if amount goes to interest or principal, and update loan balance. First customers have to pay interest, then principal
        if self.amount > 0:
            amount = self.amount
            # first pay interest
            while amount > 0:
                resting_interests = self.loan.interest_amount - self.loan.interest_amount_paid
                resting_principal = self.loan.amount - self.loan.principal_amount_paid
                if resting_interests > 0:
                    if amount > resting_interests:
                        amount -= resting_interests
                        self.loan.interest_amount_paid += resting_interests
                    else:
                        self.loan.interest_amount_paid += amount
                        amount = 0
                elif resting_principal > 0:
                    if amount > resting_principal:
                        amount -= resting_principal
                        self.loan.principal_amount_paid += resting_principal
                    else:
                        self.loan.principal_amount_paid += amount
                        amount = 0
                else:
                    amount = 0
            self.loan.save()

        else:
            # If amount is negative, is a discount
            amount = self.amount
            # Discount from principal first if is greater than 0 and then from interest. only interests can be negative
            while amount < 0:
                if self.loan.principal_amount_paid > 0:
                    if self.loan.principal_amount_paid + amount < 0:
                        amount += self.loan.principal_amount_paid
                        self.loan.principal_amount_paid = 0
                    else:
                        self.loan.principal_amount_paid += amount
                        amount = 0
                elif self.loan.interest_amount_paid > 0:
                    if self.loan.interest_amount_paid + amount < 0:
                        amount += self.loan.interest_amount_paid
                        self.loan.interest_amount_paid = 0
                    else:
                        self.loan.interest_amount_paid += amount
                        amount = 0
                else:
                    amount = 0
            self.loan.save()
        # Updatedues paid
        total_paid = self.loan.interest_amount_paid + self.loan.principal_amount_paid
        self.loan.dues_paid = int(total_paid / self.loan.due_amount)
        self.loan.save()
        # Create wallet movement
        destiny_wallet = Wallet.objects.get(user=self.loan.customer.debt_collector)
        if self.amount>0:
            WalletMovement.objects.create(wallet=destiny_wallet, name = 'pago de cuota', type='loan_in', amount=self.amount, reason=f'Entrada por cobro de prestamo del cliente {self.loan.customer.name} por un monto de {self.amount} id de prestamo {self.loan.id}')
        else:
            WalletMovement.objects.create(wallet=destiny_wallet, name = 'pago de cuota', type='loan_out', amount=self.amount, reason=f'Descuento por error {self.loan.customer.name} por un monto de {self.amount*-1} id de prestamo {self.loan.id}')
        # Check if loan is finished
        loan_total = self.loan.interest_amount + self.loan.amount
        loan_paid = self.loan.interest_amount_paid + self.loan.principal_amount_paid
        if loan_paid >= loan_total:
            self.loan.is_finished = True
            self.loan.finished_at = timezone.now()
            self.loan.save()
        super(Payment, self).save(*args, **kwargs)

class LoanMarkdowns(models.Model):
    id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    markdown = models.BooleanField(null=False, default=False)
    apply_to_date = models.DateField(null=True)

    class Meta:
        verbose_name_plural = 'LoanMarkdowns'
        db_table = 'loan_markdowns'