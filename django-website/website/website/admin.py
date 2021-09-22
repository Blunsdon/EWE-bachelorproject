from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Users, Facilities, Logs, JoinTableFacility, JoinTableUser


class CustomUserAdmin(UserAdmin):
    """
    Make the admin use the custom forms, and define admin site
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Users

    # What is shown in the list of users
    list_display = ('email', 'is_staff')

    # What filters can be applied to the entries
    list_filter = ('email', 'is_staff')

    # What is shown when editing user
    fieldsets = (
        ('User info',
          {'fields': (
             'email',
             'name',
             'phoneNumber',
             'company',
             'userType',
             'password'
         )}),
        ('Permissions',
         {'fields': (
             'is_staff',
         )}),
    )

    # what is shown in create user
    add_fieldsets = (
        (None,
         {
            'classes': ('wide',),
            'fields': (
                'email',
                'name',
                'phoneNumber',
                'company',
                'userType',
                'password', 'password2',
                'is_staff'
            )}),
    )

    # What field can be searched by
    search_fields = ('email',)

    # What are the fields ordered by as standard
    ordering = ('email',)


"""
Makes it possible to see the different tables on the admin site
"""
# The "users" section, applies a custom class
admin.site.register(Users, CustomUserAdmin)

# These use Djangos standard templates
admin.site.register(Logs)
admin.site.register(Facilities)
admin.site.register(JoinTableUser)
admin.site.register(JoinTableFacility)

