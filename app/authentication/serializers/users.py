from app.authentication.models import User
from rest_framework import serializers
from app.accounting.models import Wallet, UserGoals, PeriodClosures
from app.accounting.serializers import WalletSerializer, UserGoalsSerializer

class ListAdminUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class UsersSerializer(serializers.ModelSerializer):
    wallet_info = serializers.SerializerMethodField(read_only=True)
    goals = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'is_active', 'is_superuser', 'password', 'wallet_info', 'goals']  # Include 'password'
        extra_kwargs = {'password': {'write_only': True, 'required': False, 'allow_blank': True, 'allow_null': True}}

    def get_goals(self, obj):
        period = PeriodClosures.get_open_period()
        goals = UserGoals.objects.filter(user=obj, period_closure=period)
        if goals.exists():
            serializer = UserGoalsSerializer(goals.first())
            return serializer.data
        else:
            return None
    
    def get_wallet_info(self, obj):
        wallet = Wallet.objects.filter(user=obj)
        if wallet.exists():
            serializer = WalletSerializer(wallet.first())
            return serializer.data
        else:
            return None

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        if password == '' or password is None:
            raise serializers.ValidationError({'password': 'Password cannot be empty'})
        superuser = validated_data.pop('is_superuser', False)  # Use False as default if not provided
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # Set the password directly with the raw password
        user.is_superuser = superuser
        user.is_staff = superuser  # Normally, you'd also check if is_staff is provided in validated_data
        user.save()
        return user
    
    def update(self, instance, validated_data):
        superuser = validated_data.pop('is_superuser')
        instance.is_superuser = superuser
        instance.is_staff = superuser
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        # Verify if password is not empty
        if validated_data.get('password', None) is not None:
            if validated_data.get('password', None) != '':
                instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

