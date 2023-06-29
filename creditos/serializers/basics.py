from rest_framework import serializers
from creditos.models.creditos import Creditos

class CreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creditos
        fields = '__all__'
