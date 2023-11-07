from rest_framework import serializers
from app.accounting.models import DailyCheckout

class DailyCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCheckout
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')