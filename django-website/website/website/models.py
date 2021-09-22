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
    userType = models.CharField(max_length=30, default="Field user")

    """Next 3 fields might need deletion"""
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    #set email to be the login "name"
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

    name = models.CharField(max_length=80)
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
    userName = models.CharField(max_length=80)
    facilityName = models.CharField(max_length=80)


"Join tables:"
class JoinTableUser(models.Model):
    """
    Model for join table from user->facilities.
    """
    id = models.AutoField(primary_key=True)
    facility = models.OneToOneField(Facilities, on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)


class JoinTableFacility(models.Model):
    """
    Model for join table from facility->users.
    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    facility = models.ForeignKey('Facilities', on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)


