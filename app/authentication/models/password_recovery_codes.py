from django.db import models
from app.authentication.models.users import User

class User_recovery_codes(models.Model):
    """
    Represents recovery codes for a user.

    Fields:
    - id: An auto-incrementing primary key field for the recovery code.
    - user: A foreign key to the User model, representing the user associated with the recovery code.
    - code: A character field to store the recovery code.
    - is_used: A boolean field to track whether the recovery code has been used or not.
    - created_at: A datetime field to store the creation date of the recovery code.
    - valid_until: A datetime field to store the expiration date of the recovery code.
    - email_response: A character field to store an optional email response associated with the recovery code.
    """

    id = models.AutoField(verbose_name="recovery_code_id", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(verbose_name="recovery_code", max_length=6)
    is_used = models.BooleanField(verbose_name="is_used", default=False)
    created_at = models.DateTimeField(verbose_name="created_at", auto_now_add=True)
    valid_until = models.DateTimeField(verbose_name="valid_until", auto_now_add=True)
    email_response = models.CharField(verbose_name="email_response", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User_recovery_codes'
        db_table = 'user_recovery_codes'
