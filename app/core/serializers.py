from rest_framework import serializers
from app.authentication.models import User
from app.core.models import UploadedFiles
from app.core.constants import FILES_TYPE_CHOICES

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