from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.utils import timezone
from app.core.constants import FILES_TYPE_CHOICES

def upload_to(instance, filename):
    filename = str(instance.type+'-uploaded_at-'+str(timezone.now()).replace('.','-')).replace(' ','')+'.'+(filename[-5:].split('.'))[1]
    return 'uploads/{type}/{filename}'.format(type = instance.type, filename = filename)

class UploadedFiles(models.Model):

    id = models.AutoField(primary_key=True)
    file = models.FileField(
        _("File"),
        upload_to=upload_to,
        default = 'media/default',
        null = False
        )
    uploaded_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null = False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=255,
        choices=FILES_TYPE_CHOICES,
        default = 'other',
        null = False
        )
    class Meta:
        verbose_name_plural = 'UploadedFiles'
        db_table = 'uploaded_files'

    def __str__(self):
        return self.type

class InfoAndRules(models.Model):
    id = models.AutoField(primary_key=True)
    info = models.TextField(null=False)
    rules = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'InfoAndRules'
        db_table = 'info_and_rules'

class CustomConfig(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=255, null=False)
    value = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'CustomConfig'
        db_table = 'custom_config'

    def __str__(self):
        return self.key