from app.authentication.models import User
from rest_framework import serializers


class FetchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'created_at', 'updated_at', 'is_active', 'groups', 'failed_login_attempts', 'release_login_after', 'user_permissions', 'last_login', 'failed_recovery_attempts', 'release_recovery_after']        
    