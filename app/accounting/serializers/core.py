from app.accounting.models import Wallet, WalletMovement
from rest_framework import serializers
from app.core.models import UploadedFiles
from django.utils import timezone


class WalletMovementSerializer(serializers.ModelSerializer):
    type_tag = serializers.CharField(source='get_type_display', read_only=True)
    proof_url = serializers.URLField(source='proof.file.url', read_only=True)
    class Meta:
        model = WalletMovement
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'wallet')

class WalletSerializer(serializers.ModelSerializer):
    wallet_movements = serializers.SerializerMethodField(read_only=True)
    today_movements = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')

    def get_today_movements(self, obj):
        movements = WalletMovement.objects.filter(wallet=obj, created_at__date = timezone.now().date()).order_by('-id')
        serializer = WalletMovementSerializer(movements, many=True)
        return serializer.data
    def get_wallet_movements(self, obj):
        movements = WalletMovement.objects.filter(wallet=obj)
        serializer = WalletMovementSerializer(movements, many=True)
        return serializer.data

class SpendSerializer(serializers.ModelSerializer):
    proof = serializers.PrimaryKeyRelatedField(
        queryset = UploadedFiles.objects.all(),
        required = True,
        allow_null = False
    )
    class Meta:
        model = WalletMovement
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'wallet', 'type')

    def validate(self, attrs):
        attrs['type'] = 'exit'
        # Get request user wallet
        wallet = Wallet.objects.get(user=self.context['request'].user)
        attrs['wallet'] = wallet
        return attrs

    def create(self, validated_data):
        # Create movement
        movement = WalletMovement.objects.create(**validated_data)
        return movement
    
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletMovement
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'type')

    def validate(self, attrs):
        attrs['type'] = 'entry'
        # Get request user wallet
        return attrs

    def create(self, validated_data):
        # Create movement
        movement = WalletMovement.objects.create(**validated_data)
        return movement