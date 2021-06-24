from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.db.models.fields import CharField

# Create your models here.

# This will helps us to v=create user. Overriding user manager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None):
        # Error for not creating an email
        if not email:
            raise ValueError('Users must have an email address')

        # This normalise turns the email to small caps
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, phone_number=phone_number)

        # Creating and using django password ashing
        user.set_password(password)
        user.save()

        return user
    # def create_superuser()


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_phone_number(self):
        return self.phone_number

    def __str__(self):
        return self.email