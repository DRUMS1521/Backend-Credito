from rest_framework import serializers
from app.authentication.models import User
from app.core.models import UploadedFiles, InfoAndRules, CustomConfig
from app.core.constants import FILES_TYPE_CHOICES

class CustomConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomConfig
        fields = '__all__'

class UploadFileSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    file = serializers.ImageField(
        required = True,
        allow_null = False,
    )

    uploaded_by = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        required = True,
        allow_null = False
    )

    uploaded_at = serializers.DateTimeField(read_only=True)

    type = serializers.ChoiceField(
        choices = FILES_TYPE_CHOICES,
        required = True,
        allow_null = False
    )

    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = UploadedFiles
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at', 'type']

class InfoAndRulesSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(read_only=True)

    info = serializers.CharField(
        required = True,
        allow_null = False,
        allow_blank = False,
        max_length = 10000
    )

    rules = serializers.CharField(
        required = True,
        allow_null = False,
        allow_blank = False,
        max_length = 10000
    )

    created_at = serializers.DateTimeField(read_only=True)

    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = InfoAndRules
        fields = ['id', 'info', 'rules', 'created_at', 'updated_at']

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        # Create the object only if it doesn't exist
        if InfoAndRules.objects.count() == 0:
            return InfoAndRules.objects.create(**validated_data)
        else:
            # If it exists, update it
            info_and_rules = InfoAndRules.objects.first()
            info_and_rules.info = validated_data.get('info', info_and_rules.info)
            info_and_rules.rules = validated_data.get('rules', info_and_rules.rules)
            info_and_rules.save()
            return info_and_rules
            

