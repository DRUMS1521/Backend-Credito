from app.loans.models import Loan, Payment, Customer
from app.core.constants import *
from app.core.models import UploadedFiles
from app.authentication.models import User
from rest_framework import serializers
from app.accounting.models import PeriodClosures, UserGoals

class CustomerLoanSerializer(serializers.Serializer):
    customer_type = serializers.ChoiceField(choices=CUSTOMER_TYPE_CHOICES, required=True)
    start_date = serializers.DateField(required=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False, allow_null=True)
    document_number = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    name = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    home_address = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    business_name = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    business_address = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    cell_phone_number = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    occupation = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    alias_or_reference = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    who_referred = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False, allow_null=True)
    business_location = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    home_location = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)
    identity_document = serializers.PrimaryKeyRelatedField(queryset=UploadedFiles.objects.all(), required=False, allow_null=True)
    business_photo = serializers.PrimaryKeyRelatedField(queryset=UploadedFiles.objects.all(), required=False, allow_null=True)
    business_document = serializers.PrimaryKeyRelatedField(queryset=UploadedFiles.objects.all(), required=False, allow_null=True)
    authorized_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    amount = serializers.DecimalField(required=True, decimal_places=2, max_digits=10)
    interest_rate = serializers.DecimalField(required=True, decimal_places=2, max_digits=5)
    recurrence = serializers.ChoiceField(choices=LOAN_RECURRENCE_CHOICES, required=True)
    dues = serializers.IntegerField(required=False, allow_null=True)
    due_amount = serializers.DecimalField(required=False, decimal_places=2, max_digits=10, allow_null=True)
    photo = serializers.PrimaryKeyRelatedField(queryset=UploadedFiles.objects.all(), required=False, allow_null=True)

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
                'photo': attrs.get('photo'),
                'identity_document': attrs.get('identity_document'),
                'business_photo': attrs.get('business_photo'),
                'business_document': attrs.get('business_document'),
                'created_by': attrs.get('created_by'),
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
                'ordering': 0,
                'collector': attrs.get('debt_collector'),
            }
        }
        return new_attrs
    
    def create(self, validated_data):
        customer_type = validated_data['customer_type']
        if customer_type == 'new':
            customer = Customer.objects.create(**validated_data['new_customer'])
        else:
            customer = validated_data['old_customer']['customer']
            # check debt collector
            #update customer
            customer.home_address = validated_data['new_customer']['home_address']
            customer.business_name = validated_data['new_customer']['business_name']
            customer.business_address = validated_data['new_customer']['business_address']
            customer.cell_phone_number = validated_data['new_customer']['cell_phone_number']
            customer.occupation = validated_data['new_customer']['occupation']
            customer.alias_or_reference = validated_data['new_customer']['alias_or_reference']
            customer.photo = validated_data['new_customer']['photo'] if validated_data['new_customer']['photo'] else customer.photo
            customer.identity_document = validated_data['new_customer']['identity_document'] if validated_data['new_customer']['identity_document'] else customer.identity_document
            customer.business_photo = validated_data['new_customer']['business_photo'] if validated_data['new_customer']['business_photo'] else customer.business_photo
            customer.business_document = validated_data['new_customer']['business_document'] if validated_data['new_customer']['business_document'] else customer.business_document
            customer.save()
        loan = Loan.objects.create(customer=customer, **validated_data['loan'])
        customer.notes = None
        customer.save()
        if customer_type == 'new':
            #Update goals
            period = PeriodClosures.get_open_period()
            user_goal = UserGoals.objects.filter(user=validated_data['new_customer']['created_by'], period_closure=period).first()
            user_goal.new_customers += 1
            user_goal.save()
        return loan