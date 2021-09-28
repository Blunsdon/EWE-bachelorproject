from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# used for test
from django.http import HttpResponse
from website.forms import *
from website.models import Users

# Create your views here.
@login_required
def office_user_home(request):

    return render(request, "office_user_home.html")

@login_required
def office_user_info(request):
    """Takes changes from user input and saves it"""
    if request.method == 'POST':
        form = EditFieldUser(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/office_user_home')
        else:
            return redirect('/office_user_home/edit_user_error')
    "Gets user information"
    name = request.user.name
    phone = request.user.phoneNumber
    email = request.user.email
    company = request.user.company
    password = request.user.password
    dict = {'name': name, 'email': email, 'phoneNumber': phone, 'company': company, 'password': password}
    return render(request, "office_user_info.html", dict)


"Facility access view"
@login_required
def office_user_access(request):
    name = request.user.name
    fac = JoinTable.objects.filter(user__name=name)
    context = {'facility': fac}
    return render(request, "office_user_access.html", context)

@login_required
def office_edit_user(request):
    # Dummy parameter
    comp = 'comp'

    # Query all unique companies in the database
    company = Users.objects.order_by().values_list('company', flat=True).distinct()

    # No company chosen yet, so query all users in the database
    users = Users.objects.order_by()

    # Company is chosen:
    if request.method == 'POST':
        data = request.POST['company_list']
        if data != "None":
            # Query database for users, filtered by chosen company
            users = Users.objects.order_by().filter(company=data)
            user_header_text = "Users for: " + str(data)
            # Render page with filtered users, instead of all users
            render_dict = {
                'company': company,
                'users': users,
                'param': data,
                'header_text': user_header_text}
            return render(request, "office_edit_user.html", render_dict)

    # Text for a header
    user_header_text = "All users:"

    # Default render with all companies, and all users
    render_dict = {
        'company': company,
        'users': users,
        'param': comp,
        'header_text': user_header_text}
    return render(request, "office_edit_user.html", render_dict)

@login_required
def office_edit_user_final(request):
    # Get user chosen from "office_edit_user"
    data = request.GET['users_list']

    # If there's no user chosen, redirect back to "office_edit_user"
    if data == 'None':
        return redirect("office_edit_user")

    # Make query based on chosen user from "office_edit_user"
    user_choice = Users.objects.get(email=data)

    # Run if statement, if "edit button" is clicked on website
    if request.method == 'POST':
        form = AllUsersFields(request.POST, instance=user_choice)
        print(form)
        # Save changes to model entry, and redirect to "office_edit_user"
        if form.is_valid():
            form.save()
            return redirect(office_edit_user)
        else:
            # TODO: Create proper error statement
            print(form.errors.values())
            return redirect('/error')

    return render(request, "office_edit_user_final.html", {'user': user_choice})

@login_required
def upgrade_field_user(request):
    data = request.GET['upgrade_user']
    print(data)
    return HttpResponse('success')

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


@login_required
def edit_user_error(request):

    return render(request, "edit_user_error.html")


"office user password change"
@login_required
def office_user_change_password(request):
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
    return render(request, "office_user_change_password.html", {'form': form})
