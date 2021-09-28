from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from website.forms import *
from website.models import *


"Home page for field user"
@login_required
def field_user_home(request):

    return render(request, "field_user_home.html")


"Personal information page for field user"
@login_required
def field_user_info(request):
    """Takes changes from user input and saves it"""
    if request.method == 'POST':
        form = EditFieldUser(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/field_user_home')
        else:
            return redirect('/field_user_home/edit_user_error')
    'Gets user information'
    name = request.user.name
    phone = request.user.phoneNumber
    email = request.user.email
    company = request.user.company
    password = request.user.password
    dict = {'name': name, 'email': email, 'phoneNumber': phone, 'company': company, 'password': password}
    return render(request, "field_user_info.html", dict)


"field user facility access view"
@login_required
def field_user_access(request):
    name = request.user.name
    facility = JoinTable.objects.filter(user__name=name)
    context = {'facility': facility}
    return render(request, "field_user_access.html", context)

@login_required
def edit_user_error(request):

    return render(request, "edit_user_error.html")


"field user password change"
@login_required
def field_user_change_password(request):
    """ Uses Django API """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            logout(request)
            return redirect('/accounts/login/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {'form': form})
