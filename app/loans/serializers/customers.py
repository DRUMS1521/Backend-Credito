from rest_framework import serializers
from app.loans.models import Customer

class CustomerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')