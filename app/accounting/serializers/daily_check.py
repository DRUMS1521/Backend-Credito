from rest_framework import serializers
from app.accounting.models import DailyCheckout
from django.utils import timezone

class DailyCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCheckout
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, attrs):
        # Validate that the user has not already created a daily checkout today
        today = timezone.now().date()
        if DailyCheckout.objects.filter(user=attrs['user'], created_at__date=today).exists():
            raise serializers.ValidationError('Ya has hecho un cierre de caja hoy')
        return super().validate(attrs)