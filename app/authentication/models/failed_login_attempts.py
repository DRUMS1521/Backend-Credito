from django.db import models
from app.authentication.models.users import User


class Failed_login_attempts(models.Model):
    """
    Represents a table in the database for storing failed login attempts.

    Fields:
    - id: An auto-incrementing integer field that serves as the primary key for each failed login attempt.
    - user: A foreign key field that references the User model and represents the user associated with the failed login attempt.
    - ip_address: A character field that stores the IP address from which the failed login attempt originated.
    - created_at: A date and time field that automatically records the timestamp when the failed login attempt was created.
    """
    id = models.AutoField(verbose_name="id", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_user')
    ip_address = models.CharField(verbose_name="ip_address", max_length=255)
    created_at = models.DateTimeField(verbose_name="created_at", auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Failed_login_attempts'
        db_table = 'failed_login_attempts'