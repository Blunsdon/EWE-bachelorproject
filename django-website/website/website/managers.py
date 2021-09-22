from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authorization instead of usernames.
    """
    def create_user(self, email, password, phoneNumber, company, name, **extra_fields):
        """
        create and save users with the given email and password.

        :param Email:
        :param password:
        :param extra_fields:
        :return:
        """

        email = self.normalize_email(email)
        user = self.model(email=email,
                          name=name,
                          phoneNumber=phoneNumber,
                          company=company,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        create and save a SuperUser with the given email and password.

        :param self:
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)