from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from website.forms import *
from website.models import Users

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
    comp = 'comp'
    company = Users.objects.order_by().values_list('company', flat=True).distinct()
    users = Users.objects.order_by()
    if request.method == 'POST':
        data = request.POST['company_list']
        if data != "None":
            users = Users.objects.order_by().filter(company=data)
            print(users.values_list())
            return render(request, "office_edit_user.html", {'company': company, 'users': users, 'param': data})

    return render(request, "office_edit_user.html", {'company': company, 'users': users, 'param': comp})

@login_required
def office_edit_user_final(request):
    data = request.GET['users_list']
    if data == 'None':
        return redirect("office_edit_user")

    user_choice = Users.objects.get(email=data)

    if request.method == 'POST':
        print('request succes')
        form = EditAllUsers(request.POST, instance=user_choice)
        print(form)
        if form.is_valid():
            form.save()
            print("save succes")
            return redirect(office_edit_user)
        else:
            print(form.errors.values())
            return redirect('/error')

    return render(request, "office_edit_user_final.html", {'user': user_choice})

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

@login_required
def facility(request):

    return render(request, "facility.html")

@login_required
def facility_add(request):

    return render(request, "facility_add.html")

@login_required
def facility_edit(request):

    return render(request, "facility_edit.html")

@login_required
def facility_remove(request):

    return render(request, "facility_remove.html")