from rest_framework import serializers
from app.authentication.models import User, Failed_login_attempts
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta, timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.utils import timezone


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, max_length=255, min_length=3)

    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    tokens = serializers.SerializerMethodField(read_only=True, required=False)

    user_type = serializers.SerializerMethodField(read_only=True, required=False)

    def get_user_type(self, obj):
        user = User.objects.get(email=obj['email'])

        if user.is_superuser:
            return 'admin'
        if user.is_staff:
            return 'staff'
        if user.user_type == 'client':
            return 'client'

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        
        #pdb.set_trace()
        all_tokens = OutstandingToken.objects.filter(user=user).order_by('-id')
        for element in all_tokens:
            if BlacklistedToken.objects.filter(token=element).exists():
                pass
            else:
                BlacklistedToken.objects.create(
                    token=element,
                )
        token_data = user.tokens()
        return {
            'access':{
                'token': str(token_data['access']),
                'expires_at': datetime.fromtimestamp(token_data['access']['exp'])+timedelta(hours=-5),
            }
        }

    def user_could_try_login(self, user):
        if user.release_login_after==None:
            return True
        else:
            if user.release_login_after<timezone.now():
                return True
            else:
                return False        

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        try:
            user = User.objects.get(email=email)
        except:
            raise AuthenticationFailed({'error': 'Credenciales incorrectas, por favor intente de nuevo'})
        #go to self function to explain why this is here
        if user.is_active==False:
            raise AuthenticationFailed({'error': 'Contacta a un administrador para más información'})
        if self.user_could_try_login(user)==True:
            try_login = auth.authenticate(email=email, password=password)
            try:
                
                if user != None and try_login != None:
                    pass
                else:
                    raise AuthenticationFailed({'error': 'Credenciales incorrectas, por favor intente de nuevo'})
            except:
                #import pdb;pdb.set_trace()
                ip_address = None
                ip_address = self.context['request'].META.get('HTTP_X_FORWARDED_FOR')
                if ip_address:
                    ip_address = ip_address.split(',')[0]
                else:
                    ip_address = self.context['request'].META.get('REMOTE_ADDR')
                Failed_login_attempts.objects.create(
                    user=user,
                    ip_address = ip_address,
                    )
                if user.failed_login_attempts<5:
                    user.failed_login_attempts += 1
                    user.save()
                elif user.failed_login_attempts==5:
                    user.failed_login_attempts = 0
                    user.release_login_after = timezone.now()+timedelta(minutes=10)
                    user.save()
                    AuthenticationFailed({'error': 'Credenciales incorrectas, por favor intente de nuevo'})
                raise AuthenticationFailed({'error': 'Credenciales incorrectas, por favor intente de nuevo'})
            else:
                user.last_login = timezone.now()
                user.failed_login_attempts = 0
                user.release_login_after = None
                user.save()
                return attrs
        else:
            raise AuthenticationFailed({'error': 'Espere 10 minutos para volver a intentar'})

    class Meta:
        fields = ['id',
        'email',
        'password',
        'tokens',
        'user_type'
        ]