from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, password=None):
        if email is None:
            raise TypeError('Users should have a Email')
        user = self.model(username=self.normalize_email(email), email=self.normalize_email(email), first_name=first_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        first_name = None
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(email, first_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user