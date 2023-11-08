from app.accounting.models import PeriodClosures
from rest_framework import serializers
from django.utils import timezone

class PeriodClosuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodClosures
        fields = '__all__'
        read_only_fields = ('id',)

class NewPeriodClosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodClosures
        fields = ['end_date']

    def validate(self, attrs):
        #Verify end_date is not in the past
        end_date = attrs.get('end_date', '')
        if end_date < timezone.now().date():
            raise serializers.ValidationError("End date cannot be in the past")
        return attrs
    
    def create(self, validated_data):
        #Close all previous periods
        PeriodClosures.objects.filter(closed=False).update(closed=True)
        #Create new period, with the start_date as the end_date of the previous period
        last_period = PeriodClosures.objects.latest('id')
        start_date = last_period.end_date
        end_date = validated_data['end_date']
        new_period = PeriodClosures.objects.create(start_date=start_date, end_date=end_date)
        return new_period

