from app.loans.models import Loan, Payment, Customer
from app.core.constants import *
from app.core.models import UploadedFiles
from app.authentication.models import User
from rest_framework import serializers

class CustomerLoanSerializer(serializers.Serializer):
    customer_type = serializers.ChoiceField(choices=CUSTOMER_TYPE_CHOICES, required=True)
    start_date = serializers.DateField(required=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False, allow_null=True)
    document_number = serializers.CharField(required=False, max_length=255, allow_null=True)
    name = serializers.CharField(required=False, max_length=255, allow_null=True)
    home_address = serializers.CharField(required=False, max_length=255, allow_null=True)
    business_name = serializers.CharField(required=False, max_length=255, allow_null=True)
    business_address = serializers.CharField(required=False, max_length=255, allow_null=True)
    cell_phone_number = serializers.CharField(required=False, max_length=255, allow_null=True)
    occupation = serializers.CharField(required=False, max_length=255, allow_null=True)
    alias_or_reference = serializers.CharField(required=False, max_length=255, allow_null=True)
    who_referred = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False, allow_null=True)
    business_location = serializers.CharField(required=False, max_length=255, allow_null=True)
    home_location = serializers.CharField(required=False, max_length=255, allow_null=True)
    identity_document = serializers.PrimaryKeyRelatedField(queryset=UploadedFiles.objects.all(), required=False, allow_null=True)
    business_photo = serializers.PrimaryKeyRelatedField(queryset=UploadedFiles.objects.all(), required=False, allow_null=True)
    business_document = serializers.PrimaryKeyRelatedField(queryset=UploadedFiles.objects.all(), required=False, allow_null=True)
    authorized_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    amount = serializers.DecimalField(required=True, decimal_places=2, max_digits=10)
    interest_rate = serializers.DecimalField(required=True, decimal_places=2, max_digits=5)
    recurrence = serializers.ChoiceField(choices=LOAN_RECURRENCE_CHOICES, required=True)
    dues = serializers.IntegerField(required=False, allow_null=True)
    due_amount = serializers.DecimalField(required=False, decimal_places=2, max_digits=10, allow_null=True)

    class Meta:
        fields = '__all__'

    def check_required_fields(self, customer_type, data):
        required_fields = REQUIRED_FIELDS_CUSTOMER_LOAN[customer_type]
        for field in required_fields:
            if not data.get(field):
                return False
        return True
    
    def calculate_dues_or_due_amount(self, amount, recurrence, dues, due_amount, interest_rate):
        # Check that only comes one of the two fields
        if dues or due_amount:
            amount_with_interest = amount * (1 + interest_rate)
            if dues and due_amount:
                due_amount = None
            elif dues:
                due_amount = amount_with_interest / dues
            elif due_amount:
                import math
                # Calculate dues, round up to the next integer
                dues = math.ceil(amount_with_interest / due_amount)
            else:
                due_amount = amount_with_interest
                dues = 1
            return dues, due_amount
        else:
            raise serializers.ValidationError('Faltan cuotas o monto de cuota')

    def validate(self, attrs):
        if not self.check_required_fields(attrs['customer_type'], attrs):
            raise serializers.ValidationError('Missing required fields')
        # Calculate dues and due_amount
        attrs['dues'], attrs['due_amount'] = self.calculate_dues_or_due_amount(attrs['amount'], attrs['recurrence'], attrs.get('dues'), attrs.get('due_amount'), attrs['interest_rate'])
        attrs['created_by'] = self.context['request'].user
        attrs['debt_collector'] = self.context['request'].user
        #define attrs
        new_attrs = {
            'customer_type': attrs['customer_type'],
            'new_customer': {
                'document_number': attrs.get('document_number'),
                'name': attrs.get('name'),
                'home_address': attrs.get('home_address'),
                'business_name': attrs.get('business_name'),
                'business_address': attrs.get('business_address'),
                'cell_phone_number': attrs.get('cell_phone_number'),
                'occupation': attrs.get('occupation'),
                'alias_or_reference': attrs.get('alias_or_reference'),
                'who_referred': attrs.get('who_referred'),
                'business_location': attrs.get('business_location'),
                'home_location': attrs.get('home_location'),
                'identity_document': attrs.get('identity_document'),
                'business_photo': attrs.get('business_photo'),
                'business_document': attrs.get('business_document'),
                'created_by': attrs.get('created_by'),
                'debt_collector': attrs.get('debt_collector'),
            },
            'old_customer': {
                'customer': attrs.get('customer'),
            },
            'loan': {
                'authorized_by': attrs.get('authorized_by'),
                'amount': attrs.get('amount'),
                'interest_rate': attrs.get('interest_rate'),
                'recurrence': attrs.get('recurrence'),
                'dues': attrs.get('dues'),
                'due_amount': attrs.get('due_amount'),
                'start_date': attrs.get('start_date'),
            }
        }
        return new_attrs
    
    def create(self, validated_data):
        customer_type = validated_data['customer_type']
        if customer_type == 'new':
            customer = Customer.objects.create(**validated_data['new_customer'])
        else:
            customer = validated_data['old_customer']['customer']
        loan = Loan.objects.create(customer=customer, **validated_data['loan'])
        return loan