from django.db import models

# TODO: Make id's 'auto fill' empty spaces
# TODO: Passwords should be hashed + salted
# TODO: Keys should be hashed + salted


"For Users:"
class Users(models.Model):
    ID = models.AutoField(primary_key=True)

    Name = models.CharField(max_length=80)
    Email = models.CharField(max_length=120)
    PhoneNumber = models.CharField(max_length=20)
    Company = models.CharField(max_length=120)
    Password = models.CharField(max_length=200)
    UserType = models.CharField(max_length=30, default="Field user")

    def __str__(self):
        return self.Name


"For facilities:"
class Facilities(models.Model):
    ID = models.AutoField(primary_key=True)

    Name = models.CharField(max_length=80)
    Location = models.CharField(max_length=120)
    Owner = models.CharField(max_length=80)
    Key = models.CharField(max_length=200)

    def __str__(self):
        return self.Name


"log"
class Logs(models.Model):
    ID = models.AutoField(primary_key=True)
    Facility = models.ForeignKey('Facilities', on_delete=models.DO_NOTHING, blank=True, null=True, db_constraint=False)
    User = models.ForeignKey('Users', on_delete=models.DO_NOTHING, blank=True, null=True, db_constraint=False)
    DateTime = models.DateTimeField()
    UserName = models.CharField(max_length=80)
    FacilityName = models.CharField(max_length=80)


"Join tables:"
class JoinTableUser(models.Model):
    ID = models.AutoField(primary_key=True)
    Facility = models.OneToOneField(Facilities, on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    User = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)


class JoinTableFacility(models.Model):
    ID = models.AutoField(primary_key=True)
    User = models.OneToOneField(Users, on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    facility = models.ForeignKey('Facilities', on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)


