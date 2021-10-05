from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# TODO: Make id's 'auto fill' empty spaces
# TODO: Passwords should be hashed + salted
# TODO: Keys should be hashed + salted


"For Users:"


class Users(AbstractBaseUser, PermissionsMixin):
    """
    Model for users.
    """
    ID = models.AutoField(primary_key=True)

    name = models.CharField(max_length=80)
    email = models.EmailField(_('email adress'), unique=True)
    phoneNumber = models.CharField(max_length=20)
    company = models.CharField(max_length=120)
    password = models.CharField(max_length=200)

    userTypes = (
        ('Admin', 'Admin'),
        ('Office user', 'Office user'),
        ('Field user', 'Field user'))
    userType = models.CharField(max_length=30, choices=userTypes, default="Field user")

    """Next 3 fields might need deletion"""
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # set email to be the login "name"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phoneNumber', 'company']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


"For facilities:"


class Facilities(models.Model):
    """
    Model for facilities.
    """
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=80, unique=True)
    location = models.CharField(max_length=120)
    owner = models.CharField(max_length=80)
    key = models.CharField(max_length=200)

    def __str__(self):
        return self.name


"log"


class Logs(models.Model):
    """
    Model for logs.
    """
    id = models.AutoField(primary_key=True)
    facility = models.ForeignKey('Facilities', on_delete=models.DO_NOTHING, blank=True, null=True, db_constraint=False)
    user = models.ForeignKey('Users', on_delete=models.DO_NOTHING, blank=True, null=True, db_constraint=False)
    dateTime = models.DateTimeField()
    companyName = models.CharField(max_length=120)
    userName = models.CharField(max_length=80)
    userEmail = models.EmailField(null=True, blank=True)
    facilityName = models.CharField(max_length=80)
    facilityLocation = models.CharField(max_length=120, null=True, blank=True)


"Join table:"


class JoinTable(models.Model):
    """
    Model for join table.
    """
    id = models.AutoField(primary_key=True)
    facility = models.ForeignKey('Facilities', on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    timer = models.CharField(max_length=80, null=True, blank=True)
    timer_start = models.CharField(max_length=80, null=True, blank=True)


class CreateUserCode(models.Model):
    """
    Model for create user code
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
