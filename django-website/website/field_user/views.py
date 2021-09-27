from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pytz import unicode

from website.forms import *

# Create your views here.



@login_required
def field_user_home(request):

    return render(request, "field_user_home.html")

# get user info
@login_required
def field_user_info(request):
    if request.method == 'POST':
        print('iam posting')
        form = EditFieldUser(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            print('Should be saved')
            return redirect('/field_user_home')
        else:
            return redirect('/field_user_home/edit_user_error')
    name = request.user.name
    phone = request.user.phoneNumber
    email = request.user.email
    company = request.user.company
    password = request.user.password
    dict = {'name': name, 'email': email, 'phoneNumber': phone, 'company': company, 'password': password}
    return render(request, "field_user_info.html", dict)

@login_required
def field_user_access(request):

    return render(request, "field_user_access.html")

@login_required
def edit_user_error(request):

    return render(request, "edit_user_error.html")

