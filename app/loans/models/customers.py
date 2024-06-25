from django.db import models
from app.authentication.models import User
from app.core.models import UploadedFiles
from django.utils import timezone

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    document_number = models.CharField(max_length=255, null=True, unique=True)
    home_address = models.CharField(max_length=255, null=True)
    business_name = models.CharField(max_length=255, null=True)
    business_address = models.CharField(max_length=255, null=True)
    cell_phone_number = models.CharField(max_length=255, null=True, unique=True)
    notes = models.CharField(max_length=1000, null=True)
    occupation = models.CharField(max_length=255, null=True)
    alias_or_reference = models.CharField(max_length=255, null=True)
    who_referred = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    business_location = models.CharField(max_length=255, null=True)
    home_location = models.CharField(max_length=255, null=True)
    photo = models.ForeignKey(UploadedFiles, on_delete=models.CASCADE, null=True, related_name='photo')
    identity_document = models.ForeignKey(UploadedFiles, on_delete=models.CASCADE, null=True, related_name='identity_document')
    business_photo = models.ForeignKey(UploadedFiles, on_delete=models.CASCADE, null=True, related_name='business_photo')
    business_document = models.ForeignKey(UploadedFiles, on_delete=models.CASCADE, null=True, related_name='business_document')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by')
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Customers'
        db_table = 'customers'

