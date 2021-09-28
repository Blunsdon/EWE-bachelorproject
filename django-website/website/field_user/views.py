from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from website.forms import *
from website.models import *

# Create your views here.



@login_required
def field_user_home(request):

    return render(request, "field_user_home.html")

# get user info
@login_required
def field_user_info(request):
    if request.method == 'POST':
        form = EditFieldUser(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
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

