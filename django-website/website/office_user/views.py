from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def office_user_home(request):

    return render(request, "office_user_home.html")

@login_required
def office_user_info(request):

    return render(request, "office_user_info.html")

@login_required
def office_user_access(request):

    return render(request, "office_user_access.html")

@login_required
def office_edit_user(request):

    return render(request, "office_edit_user.html")

@login_required
def office_edit_user_final(request):

    return render(request, "office_edit_user_final.html")