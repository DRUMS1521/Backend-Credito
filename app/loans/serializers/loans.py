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
    days_in_arrears = serializers.SerializerMethodField(read_only=True)
    authorized_by_first_name = serializers.CharField(source='authorized_by.first_name', read_only=True)
    authorized_by_last_name = serializers.CharField(source='authorized_by.last_name', read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_today_have_to_pay(self, obj):
        if obj.dues_paid < self.get_dues_required_to_ontime(obj):
            return True
        else:
            return False

    def get_days_in_arrears(self, obj):
        today = datetime.now().date()
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
                days_in_arrears = dues_required_to_ontime
        else:
            days_in_arrears = 0
        return days_in_arrears

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
