from app.accounting.models import Wallet, WalletMovement
from rest_framework import serializers

class SpendSerializer(serializers.ModelSerializer):
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