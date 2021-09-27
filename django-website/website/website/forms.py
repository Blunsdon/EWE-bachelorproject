from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import Users



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'name', 'phoneNumber', 'company', 'userType')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Users
        fields = ('email', 'name', 'phoneNumber', 'company', 'userType')

class EditAllUsers(ModelForm):
    class Meta:
        model = Users
        fields = ('email', 'name', 'phoneNumber', 'company')
