from app.authentication.models import User
from rest_framework import serializers

class ListAdminUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
