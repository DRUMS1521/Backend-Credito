from rest_framework import serializers
from app.accounting.models import DailyCheckout, PeriodClosures
from django.utils import timezone

class DailyCheckoutSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField(read_only=True)
    period = serializers.PrimaryKeyRelatedField(queryset=PeriodClosures.objects.all(), required=False)
    class Meta:
        model = DailyCheckout
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_day(self, obj):
        return obj.created_at.date()
    def validate(self, attrs):
        #Get the current period
        period = PeriodClosures.get_open_period()
        attrs['period'] = period
        # Validate that the user has not already created a daily checkout today
        today = timezone.now().date()
        if DailyCheckout.objects.filter(user=attrs['user'], created_at__date=today).exists():
            raise serializers.ValidationError('Ya has hecho un cierre de caja hoy')
        return super().validate(attrs)
    
class DailyCheckoutFillerSerializer(serializers.Serializer):
    initial_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_collected = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_loans = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_spend = serializers.DecimalField(max_digits=10, decimal_places=2)
    final_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    loans_in_arrears_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    loans_in_arrears = serializers.IntegerField()
    loans_paid = serializers.IntegerField()

