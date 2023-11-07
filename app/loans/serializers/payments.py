from app.loans.models import Payment, Loan
from rest_framework import serializers

class CreatePaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    loan = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all(), required=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, attrs):
        # TODO:check if loan is paid
        # Check amount is less than or equal to loan due and greater than 0
        loan = attrs['loan']
        amount = attrs['amount']
        loan_due = loan.interest_amount + loan.amount - loan.interest_amount_paid - loan.principal_amount_paid
        if amount > loan_due:
            raise serializers.ValidationError('Amount is greater than loan due')
        #elif amount <= 0:
        #    raise serializers.ValidationError('Amount must be greater than 0')
        return attrs
    
    def create(self, validated_data):
        # Create payment
        payment = Payment.objects.create(**validated_data)
        return payment
