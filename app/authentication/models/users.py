from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

from app.authentication.models.user_management import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        max_length=255,
        unique=True,
        db_index=True)
    
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True
    )
    
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    phone_number = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True,
        null = False
        )
    
    is_staff = models.BooleanField(
        default=False,
        null = False
        )
    
    is_superuser = models.BooleanField(
        default=False,
        null = False
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    last_login = models.DateTimeField(auto_now=False, null=True, blank=True)

    failed_login_attempts = models.IntegerField(default=0)

    release_login_after = models.DateTimeField(auto_now=False, null=True, blank=True)

    failed_recovery_attempts = models.IntegerField(default=0)

    release_recovery_after = models.DateTimeField(auto_now=False, null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': refresh.access_token
        }
    class Meta:
        db_table = 'users'