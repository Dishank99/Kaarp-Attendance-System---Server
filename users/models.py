from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

class UserRoles(models.Model):
    role = models.CharField(max_length=15, unique=True)

    def __str__ (self):
        return self.role

    class Meta:
        verbose_name = 'User Roles'
        verbose_name_plural = 'User Roles'

class KaarpUser(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    email = models.EmailField(_('email address'), unique=True)
    mobile_no = models.CharField(max_length=15, unique=True)
    device_id = models.CharField(max_length=20, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.OneToOneField(UserRoles, on_delete=models.PROTECT, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def fullname(self):
        return f'{self.fname} {self.lname}'

    def __str__(self):
        return self.fullname if self.fullname != ' ' else self.email
