from rest_framework import serializers
from app.loans.models import Customer

class CustomerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CustomerFullSerializer(serializers.ModelSerializer):
    identity_document_url = serializers.URLField(source='identity_document.file.url', read_only=True)
    business_photo = serializers.URLField(source='business_photo.file.url', read_only=True)
    business_document = serializers.URLField(source='business_document.file.url', read_only=True)
    who_referred_name = serializers.CharField(source='who_referred.name', read_only=True)
    debt_collector_first_name = serializers.CharField(source='debt_collector.first_name', read_only=True)
    debt_collector_last_name = serializers.CharField(source='debt_collector.last_name', read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')