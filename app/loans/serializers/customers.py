from rest_framework import serializers
from app.loans.models import Customer

class CustomerBasicSerializer(serializers.ModelSerializer):
    photo_url = serializers.URLField(source='photo.file.url', read_only=True)
    loans_qty_state = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_active_loans(self, obj):
        active = obj.loans.filter(is_finished=False).count()
        finished = obj.loans.filter(is_finished=True).count()
        return {'active': active, 'finished': finished}

class CustomerFullSerializer(serializers.ModelSerializer):
    identity_document_url = serializers.URLField(source='identity_document.file.url', read_only=True)
    photo_url = serializers.URLField(source='photo.file.url', read_only=True)
    business_photo_url = serializers.URLField(source='business_photo.file.url', read_only=True)
    business_document_url = serializers.URLField(source='business_document.file.url', read_only=True)
    who_referred_name = serializers.CharField(source='who_referred.name', read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CustomerAddNotesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    notes = serializers.CharField(max_length=1000)
    class Meta:
        fields = ('id', 'notes')

    def validate(self, attrs):
        # Check if customer exists
        customer = Customer.objects.filter(id=attrs['id'])
        if not customer.exists():
            raise serializers.ValidationError('Customer does not exist')
        attrs['customer'] = customer.first()
        return attrs
        
    
    def create(self, validated_data):
        # get customer
        customer = validated_data['customer']
        # update notes
        customer.notes = validated_data['notes']
        customer.save()
        return customer
