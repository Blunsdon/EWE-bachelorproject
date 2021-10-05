from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'name', 'phoneNumber', 'company', 'userType')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Users
        fields = ('email', 'name', 'phoneNumber', 'company', 'userType')

        
class AllUsersFields(ModelForm):
    class Meta:
        model = Users
        fields = ('email', 'name', 'phoneNumber', 'company')


class AllFacilityFields(ModelForm):
    class Meta:
        model = Facilities
        fields = ('name', 'location', 'owner', 'key')

        
class EditFieldUser(ModelForm):
    class Meta:
        model = Users
        fields = ('phoneNumber', 'email')


class AddFacility(ModelForm):
    class Meta:
        model = Facilities
        fields = ('name', 'location', 'owner', 'key')


class CreateNewUserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'name', 'phoneNumber', 'company')


class CreateJoinTableForm(ModelForm):
    class Meta:
        model = JoinTable
        fields = ('user', 'facility', 'timer')
