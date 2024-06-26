from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from app.accounting.models import Wallet, PeriodClosures, UserGoals


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, address, phone_number, password=None):
        if email is None:
            raise TypeError('Users should have a Email')
        user = self.model(username=self.normalize_email(email), email=self.normalize_email(email), first_name=first_name, last_name=last_name, address=address, phone_number=phone_number)
        user.set_password(password)
        user.save()
        #Create wallet
        wallet = Wallet(user=user)
        wallet.save()
        #Create user goals
        period = PeriodClosures.get_open_period()
        if not period:
            pass
        else:
            UserGoals.objects.create(user=user, period_closure=period)
        return user

    def create_superuser(self, email, password=None):
        first_name, last_name, address, phone_number = 'Admin', 'Admin', 'Admin', 'Admin'
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(email, first_name, last_name, address, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user