from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from website.forms import *

# Create your views here.



@login_required
def field_user_home(request):

    return render(request, "field_user_home.html")

# get user info
@login_required
def field_user_info(request):
    name = request.user.name
    phone = request.user.phoneNumber
    email = request.user.email
    company = request.user.company
    password = request.user.password
    dict = {'name': name, 'email': email, 'phone': phone, 'company': company, 'password': password}
    return render(request, "field_user_info.html", dict)

@login_required
def field_user_access(request):

    return render(request, "field_user_access.html")

