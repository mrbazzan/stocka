
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import CIEmailField, CICharField

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

import os
import binascii

# Create your models here.


class UserAccountManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, phone_number, business_name, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        # This normalise turns the email to small caps
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            business_name=business_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, phone_number, business_name, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, phone_number, business_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, phone_number, business_name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, first_name, last_name, phone_number, business_name, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = CIEmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = CICharField(max_length=255, unique=True)
    business_name = CICharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'phone_number', 'business_name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name + "-" + self.business_name)
        super(UserAccount, self).save(*args, **kwargs)

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_phone_number(self):
        return self.phone_number

    def __str__(self):
        return self.email


class ResetPasswordTable(models.Model):
    email = CIEmailField(unique=True, primary_key=True)
    token = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now_add=True)

    # def x(self):
    #     return self.created > timezone.now() - datetime.timedelta(minutes=5)
    # # TODO: generate a new token every 5minutes.

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.key_generate()
        return super().save(*args, **kwargs)
    
    @classmethod
    def key_generate(cls):
        return binascii.hexlify(os.urandom(2)).decode()

    def __str__(self):
        return f"{self.email} --> {self.token}" 


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
