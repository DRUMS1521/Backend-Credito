from app.loans.models import Loan, Payment
from rest_framework import serializers
from app.loans.serializers import CustomerFullSerializer
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class LoanBasicSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
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
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_payment_today(self, obj):
        today = datetime.now().date()
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
            due_last_date = created_date + timedelta(days=dues)
        elif obj.recurrence == 'weekly':
            due_last_date = created_date + timedelta(weeks=dues)
        elif obj.recurrence == 'monthly':
            due_last_date = created_date + relativedelta(months=+dues)
        elif obj.recurrence == 'biweekly':
            due_last_date = created_date + timedelta(weeks=dues*2)
        return due_last_date
    
    def get_dues_required_to_ontime(self, obj):
        today = datetime.now().date()
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
        return dues_required_to_ontime
