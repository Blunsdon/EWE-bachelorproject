from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def field_user_home(request):

    return render(request, "field_user_home.html")

@login_required
def field_user_info(request):

    return render(request, "field_user_info.html")

@login_required
def field_user_access(request):

    return render(request, "field_user_access.html")