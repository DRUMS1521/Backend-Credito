from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from datetime import datetime, timedelta

from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        #pdb.set_trace()
        try:
            refresh = self.token_class(attrs["refresh_token"])
        except:
            raise serializers.ValidationError(
                _("Refresh Token is invalid, expired or blacklisted"),
                code="token_not_valid",
            )
        new_access_token = refresh.access_token
        data = {"access": {}, "refresh": {}}
        data["access"]["token"] = str(new_access_token)
        data["access"]["expires_at"] = datetime.fromtimestamp(new_access_token['exp'])+timedelta(hours=-5)
        try:
            refresh.blacklist()
        except AttributeError:
            pass
        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()
        new_refresh_token = refresh
        data["refresh"]["token"] = str(refresh)
        data["refresh"]["expires_at"] = datetime.fromtimestamp(refresh['exp'])+timedelta(hours=-5)
        return data