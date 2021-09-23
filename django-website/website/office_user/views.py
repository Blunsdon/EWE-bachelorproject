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

@login_required
def logs_facility(request):

    return render(request, "logs_facility.html")

@login_required
def logs_user(request):

    return render(request, "logs_user.html")

@login_required
def facility_access(request):

    return render(request, "facility_access.html")

@login_required
def facility_access_give(request):

    return render(request, "facility_access_give.html")

@login_required
def facility_access_remove(request):

    return render(request, "facility_access_remove.html")