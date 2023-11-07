from app.authentication.models import User
from rest_framework import serializers
from app.accounting.models import DailyCheckout
from django.utils import timezone


class FetchUserSerializer(serializers.ModelSerializer):
    made_checkout_today = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ['password', 'created_at', 'updated_at', 'is_active', 'groups', 'failed_login_attempts', 'release_login_after', 'user_permissions', 'last_login', 'failed_recovery_attempts', 'release_recovery_after']        
    
    def get_made_checkout_today(self, obj):
        today = timezone.now().date()
        return DailyCheckout.objects.filter(user=obj, created_at__date=today).exists()