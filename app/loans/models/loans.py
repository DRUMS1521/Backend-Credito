from django.db import models

from app.authentication.models import User
from app.core.models import UploadedFiles
from app.loans.models.customers import Customer
from app.core.constants import LOAN_RECURRENCE_CHOICES
from app.accounting.models import Wallet, WalletMovement, PeriodClosures, UserGoals
from django.utils import timezone
import datetime
import math
#uuid
import uuid


def get_current_date():
    return timezone.now().date()

def update_clavo_status(loan, days):
    if days > 60:
        loan.is_clavo = True
        loan.save()
    else:
        if loan.is_clavo:
            loan.is_clavo = False
            loan.save()
            # Update Goals
            period = PeriodClosures.get_open_period()
            user_goal = UserGoals.objects.get(user=loan.collector, period_closure=period)
            user_goal.clavos_recovered += 1
            user_goal.save()
    return loan

def get_business_days(start_date, end_date):
    current_date = start_date
    business_days = 0
    
    while current_date <= end_date:
        if current_date.weekday() != 6:  # Excluir domingos (6 es domingo en Python)
            business_days += 1
        current_date += datetime.timedelta(days=1)
    return business_days

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
    is_clavo = models.BooleanField(null=False, default=False)
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
    collector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='collector')

    class Meta:
        verbose_name_plural = 'Loans'
        db_table = 'loans'

    def save(self, *args, **kwargs):
        # Calculate interest amount
        self.interest_amount = self.amount * self.interest_rate
        # Create wallet movement
        if self.id == None:
            destiny_wallet = Wallet.objects.get(user=self.collector)
            WalletMovement.objects.create(wallet=destiny_wallet, name = 'Nuevo prestamo', type='new_loan', amount=self.amount, reason=f'Salida por prestamo del cliente {self.customer.name} por un monto de {self.amount}')
            # Update Goals
            period = PeriodClosures.get_open_period()
            user_goal = UserGoals.objects.get(user=self.collector, period_closure=period)
            user_goal.borrowed += self.amount
            user_goal.save()
        super(Loan, self).save(*args, **kwargs)

    def get_end_date(self):
        start_date = self.start_date
        dues = self.dues
        if self.recurrence == 'daily':
            end_date = start_date + datetime.timedelta(days=(dues-1))
        elif self.recurrence == 'weekly':
            end_date = start_date + datetime.timedelta(weeks=(dues-1))
        elif self.recurrence == 'biweekly':
            end_date = start_date + datetime.timedelta(weeks=(dues-1)*2)
        elif self.recurrence == 'monthly':
            end_date = start_date + datetime.timedelta(days=(dues-1)*30)
        return end_date

    def get_arrears(self):
        pending_dues = self.dues - self.dues_paid
        if pending_dues < 1:
            return 0, 0, 0
        # this function returns the days in arrears, the number of dues in arrears and the amount in arrears
        if self.recurrence == 'daily':
            # Get the simulated date of the last payment according to the dues
            if self.dues_paid == 0:
                last_payment = self.start_date
            else:
                last_payment = self.start_date + datetime.timedelta(days=(self.dues_paid-1))
            # Get the difference between the last payment and today

            days = get_business_days(last_payment, timezone.now().date())
            # check if is lower than 1
            if days < 1:
                return 0, 0, 0
            else:
                update_clavo_status(self, days)
                dues = days if days <= pending_dues else pending_dues
                return days, dues, dues*self.due_amount
        elif self.recurrence == 'weekly':
            # Get the simulated date of the last payment according to the dues
            if self.dues_paid == 0:
                last_payment = self.start_date
            else:
                last_payment = self.start_date + datetime.timedelta(weeks=(self.dues_paid-1))
            # Get the difference between the last payment and today
            days = (timezone.now().date() - last_payment).days
            update_clavo_status(self, days)
            # check if is lower than 7
            if days < 7:
                return 0, 0, 0
            else:
                dues = math.floor(days/7) if math.floor(days/7) <= pending_dues else pending_dues
                return days, dues, dues*self.due_amount
        elif self.recurrence == 'biweekly':
            # Get the simulated date of the last payment according to the dues
            if self.dues_paid == 0:
                last_payment = self.start_date
            else:
                last_payment = self.start_date + datetime.timedelta(weeks=(self.dues_paid-1)*2)
            # Get the difference between the last payment and today
            days = (timezone.now().date() - last_payment).days
            update_clavo_status(self, days)
            # check if is lower than 14
            if days < 14:
                return 0, 0, 0
            else:
                dues = math.floor(days/14) if math.floor(days/14) <= pending_dues else pending_dues
                return days, dues, dues*self.due_amount
        elif self.recurrence == 'monthly':
            # Get the simulated date of the last payment according to the dues
            if self.dues_paid == 0:
                last_payment = self.start_date
            else:
                last_payment = self.start_date + datetime.timedelta(months=(self.dues_paid-1))
            # Get the difference between the last payment and today
            days = (timezone.now().date() - last_payment).days
            update_clavo_status(self, days)
            # check if is lower than 30
            if days < 30:
                return 0, 0, 0
            else:
                dues = math.floor(days/30) if math.floor(days/30) <= pending_dues else pending_dues
                return days, dues, dues*self.due_amount
        else:
            return 0, 0, 0


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
        period = PeriodClosures.get_open_period()
        user_goal = UserGoals.objects.get(user=self.loan.collector, period_closure=period)
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
            # Update Goals
            user_goal.collected += self.amount
            # if loan not has other payments today, update goal for different loans collected
            today = timezone.now().date()
            if not Payment.objects.filter(loan=self.loan, created_at__date=today).exclude(id=self.id).exists():
                user_goal.different_loans_collected += 1


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
            # Update Goals
            user_goal.collected += self.amount
        # Updatedues paid
        total_paid = self.loan.interest_amount_paid + self.loan.principal_amount_paid
        self.loan.dues_paid = int(total_paid / self.loan.due_amount)
        self.loan.save()
        # Create wallet movement
        destiny_wallet = Wallet.objects.get(user=self.loan.collector)
        if self.amount>0:
            WalletMovement.objects.create(wallet=destiny_wallet, name = 'pago de cuota', type='loan_in', amount=self.amount, reason=f'Entrada por cobro de prestamo del cliente {self.loan.customer.name} por un monto de {self.amount} id de prestamo {self.loan.id}')
        else:
            WalletMovement.objects.create(wallet=destiny_wallet, name = 'Corrección de pago', type='loan_out', amount=self.amount, reason=f'Descuento por error {self.loan.customer.name} por un monto de {self.amount*-1} id de prestamo {self.loan.id}')
        # Check if loan is finished
        loan_total = self.loan.interest_amount + self.loan.amount
        loan_paid = self.loan.interest_amount_paid + self.loan.principal_amount_paid
        if loan_paid >= loan_total:
            self.loan.is_finished = True
            self.loan.finished_at = timezone.now()
            self.loan.save()
            # Update Goal
            user_goal.loans_finished += 1
            # Check if is clavo
            if self.loan.is_clavo:
                user_goal.clavos_recovered += 1
        user_goal.save()
        
        super(Payment, self).save(*args, **kwargs)

class LoanMarkdowns(models.Model):
    id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    markdown = models.BooleanField(null=False, default=False)
    apply_to_date = models.DateField(null=True)

    class Meta:
        verbose_name_plural = 'LoanMarkdowns'
        db_table = 'loan_markdowns'