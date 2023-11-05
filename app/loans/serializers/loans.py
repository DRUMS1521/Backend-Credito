from app.loans.models import Loan
from rest_framework import serializers

class LoanBasicSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')