from app.accounting.models import PeriodClosures
from rest_framework import serializers

class PeriodClosuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodClosures
        fields = '__all__'
        read_only_fields = ('id',)