from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import Users, JoinTableUser, JoinTableFacility



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

        
class EditFieldUser(ModelForm):
    class Meta:
        model = Users
        fields = ('phoneNumber', 'email')


class FacilityAccessJoinTable(ModelForm):
    class Meta:
        model = JoinTableUser
        fields = ('user', 'facility')
