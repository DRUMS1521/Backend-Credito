from app.loans.models import Loan, Payment, LoanMarkdowns, Customer
from app.loans.serializers.payments import PaymentSerializer
from rest_framework import serializers
from app.loans.serializers.customers import CustomerFullSerializer
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, fields
from decimal import Decimal

def calculate_due_date(start_date, recurrence, dues):
    if recurrence == 'daily':
        return start_date + timedelta(days=dues)
    elif recurrence == 'weekly':
        return start_date + timedelta(weeks=dues)
    elif recurrence == 'biweekly':
        return start_date + timedelta(weeks=2*dues)
    elif recurrence == 'monthly':
        return start_date + timedelta(days=30*dues)  # Simplificación

class LoanBasicSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    collector_first_name = serializers.CharField(source='collector.first_name', read_only=True)
    collector_last_name = serializers.CharField(source='collector.last_name', read_only=True)
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class FullLoanSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_data = CustomerFullSerializer(read_only=True, source='customer')
    due_last_date = serializers.SerializerMethodField(read_only=True)
    dues_required_to_ontime = serializers.SerializerMethodField(read_only=True)
    today_have_to_pay = serializers.SerializerMethodField(read_only=True)
    payment_today = serializers.SerializerMethodField(read_only=True)
    days_in_arrears = serializers.SerializerMethodField(read_only=True)
    authorized_by_first_name = serializers.CharField(source='authorized_by.first_name', read_only=True)
    authorized_by_last_name = serializers.CharField(source='authorized_by.last_name', read_only=True)
    who_referred_name = serializers.CharField(source='customer.who_referred.name', read_only=True)
    who_referred_phone = serializers.CharField(source='customer.who_referred.cell_phone_number', read_only=True)
    has_markdown = serializers.SerializerMethodField(read_only=True)
    payments = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_payments(self, obj):
        payments = Payment.objects.filter(loan=obj)
        serializer = PaymentSerializer(payments, many=True)
        return serializer.data

    def get_has_markdown(self, obj):
        today = timezone.now().date()
        markdowns = LoanMarkdowns.objects.filter(loan=obj, apply_to_date=today, markdown=True)
        if markdowns.exists():
            return True
        else:
            return False

    def get_today_have_to_pay(self, obj):
        if obj.dues_paid < self.get_dues_required_to_ontime(obj):
            return True
        else:
            return False

    def get_days_in_arrears(self, obj):
        today = timezone.now().date()
        start_date = obj.start_date
        dues_paid = obj.dues_paid
        dues_required_to_ontime = self.get_dues_required_to_ontime(obj)
        if dues_paid < dues_required_to_ontime:
            if obj.recurrence == 'weekly':
                days_in_arrears = (today + timedelta(weeks=dues_paid) - start_date).days
                if days_in_arrears >= 7:
                    days_in_arrears -= 7
            elif obj.recurrence == 'biweekly':
                days_in_arrears = (today + timedelta(weeks=dues_paid*2) - start_date).days
                if days_in_arrears >= 14:
                    days_in_arrears -= 14
            elif obj.recurrence == 'monthly':
                days_in_arrears = (today + relativedelta(months=+dues_paid) - start_date).days
                if days_in_arrears >= 30:
                    days_in_arrears -= 30
            elif obj.recurrence == 'daily':
                sundays = (today + timedelta(days=dues_paid) - start_date).days // 7
                days_in_arrears = (today + timedelta(days=dues_paid) - start_date).days - sundays
        else:
            days_in_arrears = 0
        return days_in_arrears

    def get_payment_today(self, obj):
        today = timezone.now().date()
        payments = Payment.objects.filter(loan=obj, created_at__date=today)
        if payments.count() > 0:
            # sum payments
            total = 0
            for payment in payments:
                total += payment.amount
            return total
        else:
            return 0

    def get_due_last_date(self, obj):
        dues = obj.dues
        created_date = obj.start_date
        # Remove sunday on daily recurrence
        if obj.recurrence == 'daily':
            days_added = 0
            due_last_date = created_date
            while days_added < dues:
                due_last_date += timedelta(days=1)
                if due_last_date.weekday() != 6:  # 6 es domingo
                    days_added += 1
        elif obj.recurrence == 'weekly':
            due_last_date = created_date + timedelta(weeks=dues)
        elif obj.recurrence == 'monthly':
            due_last_date = created_date + relativedelta(months=+dues)
        elif obj.recurrence == 'biweekly':
            due_last_date = created_date + timedelta(weeks=dues*2)
        return due_last_date
    
    def get_dues_required_to_ontime(self, obj):
        today = timezone.now().date()
        created_date = obj.start_date
        days_between = (today - created_date).days
        # Remove sunday on daily recurrence
        if obj.recurrence == 'weekly':
            dues_required_to_ontime = days_between // 7
        elif obj.recurrence == 'biweekly':
            dues_required_to_ontime = days_between // 14
        elif obj.recurrence == 'monthly':
            # Calculate months between
            months_between = (today.year - created_date.year) * 12 + today.month - created_date.month
            dues_required_to_ontime = months_between
        elif obj.recurrence == 'daily':
            # Calculate days between without sundays
            days_added = 0
            while created_date < today:
                created_date += timedelta(days=1)
                if created_date.weekday() != 6:
                    days_added += 1
            dues_required_to_ontime = days_added
        dues_left = obj.dues - obj.dues_paid
        if dues_required_to_ontime > dues_left:
            return dues_left
        else:
            return dues_required_to_ontime

class CustomerCustomSerializer(serializers.ModelSerializer):
    photo_url = serializers.URLField(source='photo.file.url', read_only=True)
    identity_document_url = serializers.URLField(source='identity_document.file.url', read_only=True)
    business_photo_url = serializers.URLField(source='business_photo.file.url', read_only=True)
    business_document_url = serializers.URLField(source='business_document.file.url', read_only=True)
    who_referred_name = serializers.CharField(source='who_referred.name', read_only=True)
    collector_first_name = serializers.CharField(source='collector.first_name', read_only=True)
    collector_last_name = serializers.CharField(source='collector.last_name', read_only=True)
    loans = serializers.SerializerMethodField(read_only=True)
    customer_score = serializers.SerializerMethodField(read_only=True)

    def get_customer_score(self, obj):
        customer = obj
        loans = Loan.objects.filter(customer=customer)
        total_score = 0

        for loan in loans:
            payments = Payment.objects.filter(loan=loan)
            total_payments = payments.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
            expected_total = loan.amount + (loan.amount * loan.interest_rate)

            # Calcular la puntualidad de pagos
            on_time_payments = 0
            for i in range(loan.dues):
                due_date = calculate_due_date(loan.start_date, loan.recurrence, i+1)
                if payments.filter(created_at__lte=due_date).exists():
                    on_time_payments += 1

            payment_timeliness_score = (on_time_payments / loan.dues * 100) if loan.dues else 100
            payment_completion_score = (total_payments / expected_total * 100) if expected_total else 100

            # Promedio ponderado de los puntajes
            loan_score = (Decimal(payment_timeliness_score) * Decimal(0.7) + Decimal(payment_completion_score * Decimal(0.3)))
            total_score += loan_score

        # Promedio de puntajes de todos los préstamos
        final_score = total_score / loans.count() if loans.count() else 0
        return final_score
        
    def get_loans(self, obj):
        loans = Loan.objects.filter(customer=obj)
        serializer = FullLoanSerializer(loans, many=True)
        return serializer.data
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')