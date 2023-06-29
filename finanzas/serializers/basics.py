from rest_framework import serializers
from finanzas.models import Finanzas

class FinanzasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finanzas
        fields = '__all__'
