from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from django.contrib import messages

# used for test
from django.http import HttpResponse

from website.forms import *
from website.models import *

# used for custom decorator
from functools import wraps


# custom decorator
def user_controller(function):
    """
    Checks the user type, and redirects if wrong type

    :param function:
    :return:
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        usertype = request.user.userType
        if usertype == "Admin" or usertype == "Office user":
            return function(request, *args, **kwargs)
        elif usertype == "Field user":
            return redirect('field_user_home')
        else:
            return redirect('front_page')

    return wrap


@login_required
@user_controller
def office_user_home(request):
    """
    Gets create user code
    :param request:

    :return:
    """
    cuc = CreateUserCode.objects.get(id=1)
    cu = cuc.code
    return render(request, "office_user_home.html", {'cu': cu})

@login_required
@user_controller
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
    dict = {'name': name, 'email': email, 'phoneNumber': phone, 'company': company}
    return render(request, "office_user_info.html", dict)


"Facility access view"
@login_required
@user_controller
def office_user_access(request):
    name = request.user.name
    fac = JoinTable.objects.filter(user__name=name)
    context = {'facility': fac}
    return render(request, "office_user_access.html", context)

@login_required
@user_controller
def office_edit_user(request):
    """
    Page for choosing a user, that shall be edited.

    :param request:
    :return:
    """
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
@user_controller
def office_edit_user_final(request):
    """
    Page for editing a chosen user.

    :param request:
    :return:
    """
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
        # Save changes to model entry, and redirect to "office_edit_user"
        if form.is_valid():
            form.save()
            return redirect('office_edit_user')
        else:
            return HttpResponseBadRequest("Couldn't save user input, because of following error/errors: " + str(form.errors))

    return render(request, "office_edit_user_final.html", {'user': user_choice})

@login_required
@user_controller
def upgrade_field_user(request):
    """
    This function is for upgrading a field user to office user.

    :param request:
    :return:
    """

    # Get user email, from "office_edit_user_final"
    data = request.GET['upgrade_user']

    # Get corresponding user entry
    user_choice = Users.objects.get(email=data)

    # Change usertype and overwrite entry
    user_choice.userType = 'Office user'
    user_choice.save()

    # return to "office_edit_user"
    return redirect('office_edit_user')

@login_required
@user_controller
def delete_field_user(request):
    """
    This function is for deleting a field user.

    :param request:
    :return:
    """

    # Get user email, from "office_edit_user_final"
    data = request.GET['delete_user']

    # Get corresponding user entry
    user = Users.objects.get(email=data)

    # Delete user entry
    user.delete()

    # return to "office_edit_user"
    return redirect('office_edit_user')

@login_required
@user_controller
def logs_facility(request):

    facility_chosen = request.GET['facilities_list']

    # Retrive data object for display
    if '&' not in facility_chosen:
        return redirect('logs_facility_filter')
    else:
        list = facility_chosen.split("&", 1)
        data = Logs.objects.all().filter(facilityLocation=list[0]).filter(facilityName=list[1])

    dict = {
        'data': data,
        'location': list[0],
        'fac': list[1]
    }
    return render(request, "logs_facility.html", dict)

@login_required
@user_controller
def logs_facility_filter(request):
    """
    This function is for choosing a facility log in the database

    :param request:
    :return:
    """

    # List's to be used:
    facility_locations = []
    facilities = {}

    # Query all unique locations in the database
    facility_locations_fq = Facilities.objects.order_by().values_list('location', flat=True).distinct()
    facility_locations_lq = Logs.objects.order_by().values_list('facilityLocation', flat=True).distinct()
    for vals in facility_locations_fq:
        facility_locations.append(vals)
    for vals in facility_locations_lq:
        if vals not in facility_locations:
            facility_locations.append(vals)


    # No facility location chosen yet, so query all facilities in the database
    facilities_fq = Facilities.objects.all()
    facilities_lq = Logs.objects.all()
    for vals in facilities_fq:
        facilities[vals.location] = vals.name
    for vals in facilities_lq:
        if vals not in facilities:
            facilities[vals.facilityLocation] = vals.facilityName

    # Location is chosen:
    if request.method == 'POST':
        data = request.POST['fac_loc_list']
        if data != "None":
            # Query database for facilities, filtered by chosen location
            facilities = {}
            try:
                facilities_fq = Facilities.objects.order_by().filter(location=data)
                for vals in facilities_fq:
                    facilities[vals.location] = vals.name
            except:
                pass
            try:
                facilities_lq = Logs.objects.order_by().filter(facilityLocation=data)
                for vals in facilities_lq:
                    facilities[vals.facilityLocation] = vals.facilityName
            except:
                pass

            # Set header text
            user_header_text = "Facilities on: " + str(data)

            # Render page with filtered facilities, instead of all facilities
            render_dict = {
                'facility_locs': facility_locations,
                'facilities': facilities,
                'param': data,
                'header_text': user_header_text}
            return render(request, "logs_facility_filter.html", render_dict)

    # Set header text
    user_header_text = "All facilities:"

    # Default render with all locations, and all facilities
    render_dict = {
        'facility_locs': facility_locations,
        'facilities': facilities,
        'header_text': user_header_text}
    return render(request, "logs_facility_filter.html", render_dict)

@login_required
@user_controller
def logs_user(request):
    """
    Display log information

    :param request:
    :return:
    """
    facility_chosen = request.GET['facility_list']

    # Retrive data object for display
    if '&' not in facility_chosen:
        data = Logs.objects.all().filter(userEmail=facility_chosen)
    else:
        list = facility_chosen.split("&", 1)
        data = Logs.objects.all().filter(userEmail=list[1]).filter(facilityName=list[0])

    return render(request, "logs_user.html", {'data': data})

@login_required
@user_controller
def logs_user_filter(request):
    """
    This function is for choosing a user log in the database

    :param request:
    :return:
    """

    # List's to be used:
    company_chosen = []
    user_chosen = {}

    # Query all unique companies in the database
    company_chosen_uq = Users.objects.order_by().values_list('company', flat=True).distinct()
    company_chosen_lq = Logs.objects.order_by().values_list('companyName', flat=True).distinct()
    for vals in company_chosen_uq:
        company_chosen.append(vals)
    for vals in company_chosen_lq:
        if vals not in company_chosen:
            company_chosen.append(vals)

    # No company chosen yet, so query all users in the database
    user_chosen_uq = Users.objects.all()
    user_chosen_lq = Logs.objects.all()
    for vals in user_chosen_uq:
        user_chosen[vals.email] = vals.name
    for vals in user_chosen_lq:
        if vals not in user_chosen:
            user_chosen[vals.userEmail] = vals.userName

    is_user_chosen = "false"

    # Company is chosen:
    if request.method == 'POST':

        if 'DC' in request.POST:
            if request.POST['company_list'] != "None":
                #no user chosen yet
                is_user_chosen = "false"

                # Query database for users, filtered by chosen company
                user_chosen = {}
                try:
                    user_chosen_uq = Users.objects.order_by().filter(company=request.POST['company_list'])
                    for vals in user_chosen_uq:
                        user_chosen[vals.email] = vals.name
                except:
                    pass
                try:
                    user_chosen_lq = Logs.objects.order_by().filter(companyName=request.POST['company_list'])
                    for vals in user_chosen_lq:
                        user_chosen[vals.userEmail] = vals.userName
                except:
                    pass

                # Set header text
                user_header_text = "Users for: " + str(request.POST['company_list'])

                # Render page with filtered users, instead of all users
                render_dict = {
                    'company_chosen': company_chosen,
                    'user_chosen': user_chosen,
                    'iuc': is_user_chosen,
                    'header_text': user_header_text}
                return render(request, "logs_user_filter.html", render_dict)

        elif 'DU' in request.POST:
            if request.POST['user_list'] != 'None':
                # user is chosen
                is_user_chosen = "true"

                # Query database for facilites, filtered by chosen user
                 # Try: query in existing user
                 # exception: query in Logs for user
                try:
                    # query for user and facility
                    user_info = Users.objects.get(email=request.POST['user_list'])
                    facility_chosen = Logs.objects.order_by().filter(userEmail=user_info.email).values_list('facilityName', flat=True).distinct()

                    # Holders for information
                    user_email = user_info.email
                    company_comp = user_info.company
                    user_header_text2 = "Facilities for: " + str(user_info.name)
                except:
                    # query for user and facility
                    user_info = Logs.objects.get(userEmail=request.POST['user_list'])
                    facility_chosen = Logs.objects.order_by().filter(userEmail=user_info.userEmail).values_list('facilityName', flat=True).distinct()

                    # Holders for information
                    user_email = user_info.userEmail
                    company_comp = user_info.companyName
                    user_header_text2 = "Facilities for: " + str(user_info.userName)

                # Get chosen user/users
                user_chosen_uq = Users.objects.order_by().filter(company=company_comp)
                user_chosen = {}
                for vals in user_chosen_uq:
                    user_chosen[vals.email] = vals.name
                if not user_chosen:
                    user_chosen_lq = Logs.objects.order_by().filter(companyName=company_comp)
                    for vals in user_chosen_lq:
                        user_chosen[vals.userEmail] = vals.userName

                # header for text
                user_header_text = "Users for: " + str(company_comp)

                # Render page with filtered users, instead of all users
                render_dict = {
                    'company_chosen': company_chosen,
                    'user_chosen': user_chosen,
                    'user_email': user_email,
                    'facility': facility_chosen,
                    'iuc': is_user_chosen,
                    'header_text': user_header_text,
                    'header_text2': user_header_text2}
                return render(request, "logs_user_filter.html", render_dict)


    # Text for a header
    user_header_text = "All Users:"

    # Default render with all companies, and all users
    render_dict = {
        'company_chosen': company_chosen,
        'user_chosen': user_chosen,
        'iuc': is_user_chosen,
        'header_text': user_header_text}
    return render(request, "logs_user_filter.html", render_dict)

@login_required
@user_controller
def facility_access(request):

    return render(request, "facility_access.html")

@login_required
@user_controller
def facility_access_give_filter(request):
    """
    Function for choosing a facility

    :param request:
    :return:
    """
    # Query all unique companies in the database
    location = Facilities.objects.order_by().values_list('location', flat=True).distinct()
    # No company chosen yet, so query all users in the database
    names = Facilities.objects.order_by()

    if request.method == 'POST':
        data = request.POST['location_list']
        if data != "None":
            # Query database for users, filtered by chosen location
            names = Facilities.objects.order_by().filter(location=data)
            user_header_text = "Facilities for: " + str(data)
            # Render page with filtered users, instead of all users
            render_dict = {
                'location': location,
                'names': names,
                'param': data,
                'header_text': user_header_text}
            return render(request, "facility_access_give_filter.html", render_dict)

    # Text for a header
    user_header_text = "All facilities:"
    # Default render with all companies, and all users
    render_dict = {
        'location': location,
        'names': names,
        'header_text': user_header_text}
    return render(request, "facility_access_give_filter.html", render_dict)


@login_required
@user_controller
def facility_access_give(request):
    """
    Function for giving a user access to a facility

    :param request:
    :return:
    """
    # Get facility chosen from "facility_access_give_filter"
    data = request.GET['names_list']
    # Query all Users in the database
    all_user = Users.objects.order_by('name')
    # If there's no user chosen, redirect back to "facility access give filter"
    if data == 'None':
        return redirect("facility_access_give_filter")
    # Make query based on chosen user from "facility_access_give_filter"
    facility_choice = Facilities.objects.get(name=data)

    if request.method == 'POST':
        access = JoinTable()
        # get User object from unique Email
        access.user = Users.objects.get(email=request.POST['user'])
        # get facility info
        access.facility = Facilities.objects.get(name=facility_choice.name)
        # get date info
        access.timer_start = request.POST['timer_start']
        access.timer = request.POST['timer']
        # check if date is ok
        if access.timer < access.timer_start:
            print("Im here in error")
            return redirect('access_time_error')
        else:
            # Try rewrite timer if the access to same user and facility is already given
            try:
                access_exist = JoinTable.objects.get(user=access.user, facility=access.facility)
                # Get object
                access_exist_obj = JoinTable.objects.get(pk=access_exist.pk)
                print(access_exist.pk)
                access_exist_obj.timer = request.POST['timer']
                access_exist_obj.timer_start = request.POST['timer_start']
                access_exist_obj.save()
                return redirect('facility_access')
            except JoinTable.DoesNotExist:
                # Save
                access.save()
                return redirect('facility_access')
    # Initial "welcome" text
    disp_text = {'': ''}

    dict = {
        'name': facility_choice,
        'disp_text': disp_text,
        'users': all_user
    }
    return render(request, "facility_access_give.html", dict)


@login_required
@user_controller
def access_time_error(request):
    """
    Return error message
    :param request:
    :return:
    """
    return render(request, "access_time_error.html")


@login_required
@user_controller
def facility_access_remove(request):
    """
        This function is for filtering the JoinTable and removing access to facility
        :param request:
        :return:
        """
    # Used for html
    facility_is_chosen = False
    user_is_chosen = False
    access_remove = False
    # No facility location chosen yet, so query all facilities in the database
    facilities = JoinTable.objects.values_list('facility__name', flat=True).distinct()
    users = JoinTable.objects.values_list('user__name', 'user__email').distinct()

    # Facility is chosen:
    if request.method == 'POST':
        if 'sel_facility' in request.POST:
            data = request.POST['facility']
            if data != "None":
                facility_is_chosen = True
                # Set header text
                user_header_text = "Facility chosen: " + str(data)
                # Query all unique users in the database that has access to chosen facility
                users = JoinTable.objects.filter(facility__name=data).values_list('user__name',
                                                                                  'user__email').distinct()
                # Render page with filtered facilities, instead of all facilities
                render_dict = {
                    'users': users,
                    'facilities': data,
                    'fc': facility_is_chosen,
                    'uc': user_is_chosen,
                    'ac': access_remove,
                    'param': data,
                    'header_text': user_header_text}
                return render(request, "facility_access_remove.html", render_dict)
            else:
                print("error no data")
                # User  is chosen
        elif 'sel_user' in request.POST:
            data = request.POST['user']
            if data != "None":
                user_is_chosen = True
                list_from_user = data.split("&", 1)
                try:
                    remove_chosen = JoinTable.objects.get(user__email=list_from_user[0],
                                                          facility__name=list_from_user[1])
                    # Delete the chosen access
                    remove_chosen.delete()
                    facility_is_chosen = False
                    user_is_chosen = False
                    access_remove = True
                    # Set header text
                    user_header_text = "Access successfully removed"
                    render_dict = {
                        'fc': facility_is_chosen,
                        'uc': user_is_chosen,
                        'ac': access_remove,
                        'header_text': user_header_text}
                    return render(request, "facility_access_remove.html", render_dict)
                except JoinTable.DoesNotExist:
                    # Something failed
                    user_header_text = "Something failed try again"
                    render_dict = {
                        'fc': facility_is_chosen,
                        'uc': user_is_chosen,
                        'ac': access_remove,
                        'header_text': user_header_text}
                    return render(request, "facility_access_remove.html", render_dict)
            else:
                print("error no data")

    # Set header text
    user_header_text = "Choose facilities:"

    # Default render with all locations, and all facilities
    render_dict = {
        'users': users,
        'facilities': facilities,
        'fc': facility_is_chosen,
        'uc': user_is_chosen,
        'ac': access_remove,
        'header_text': user_header_text}
    return render(request, "facility_access_remove.html", render_dict)


@login_required
@user_controller
def facility(request):

    return render(request, "facility.html")

@login_required
@user_controller
def facility_add(request):
    """
    This funtion is for adding a new facility to the database

    :param request:
    :return:
    """

    # Initial "welcome" text
    disp_text = {'': ''}

    if request.method == 'POST':
        form = AddFacility(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facility')
        else:
            # error text and formatting, for changing "welcome" text
            disp_text = {"Errors": ""}
            error_text = form.errors.as_data()
            for key, value in error_text.items():
                for items in value:
                    for item in items:
                        disp_text["Field " + str(key) + ":"] = item
            return render(request, "facility_add.html", {'disp_text': disp_text})

    return render(request, "facility_add.html", {'disp_text': disp_text})

@login_required
@user_controller
def facility_edit_filter(request):
    """
    Function for choosing a facility

    :param request:
    :return:
    """
    # Dummy parameter
    comp = 'comp'

    # Query all unique companies in the database
    location = Facilities.objects.order_by().values_list('location', flat=True).distinct()

    # No company chosen yet, so query all users in the database
    names = Facilities.objects.order_by()

    # Company is chosen:
    if request.method == 'POST':
        data = request.POST['location_list']
        if data != "None":
            # Query database for users, filtered by chosen company
            names = Facilities.objects.order_by().filter(location=data)
            print(data)
            user_header_text = "Facilities for: " + str(data)
            # Render page with filtered users, instead of all users
            render_dict = {
                'location': location,
                'names': names,
                'param': data,
                'header_text': user_header_text}
            return render(request, "facility_edit_filter.html", render_dict)

    # Text for a header
    user_header_text = "All facilities:"

    # Default render with all companies, and all users
    render_dict = {
        'location': location,
        'names': names,
        'param': comp,
        'header_text': user_header_text}
    return render(request, "facility_edit_filter.html", render_dict)

@login_required
@user_controller
def facility_edit(request):
    """
    This funtion is for editing facilities in the database

    :param request:
    :return:
    """

    # Get facility chosen from "facility_edit_filter"
    data = request.GET['names_list']

    # If there's no user chosen, redirect back to "office_edit_user"
    if data == 'None':
        return redirect("facility_edit_filter")

    # Make query based on chosen user from "office_edit_user"
    facility_choice = Facilities.objects.get(name=data)

    # Run if statement, if "edit button" is clicked on website
    if request.method == 'POST':
        form = AllFacilityFields(request.POST, instance=facility_choice)
        # Save changes to model entry, and redirect to "office_edit_user"
        if form.is_valid():
            form.save()
            return redirect('facility_edit_filter')
        else:
            # error text and formatting, for changing "welcome" text
            disp_text = {"Errors": ""}
            error_text = form.errors.as_data()
            for key, value in error_text.items():
                for items in value:
                    for item in items:
                        disp_text["Field " + str(key) + ":"] = item
            dict = {
                'name': facility_choice,
                'disp_text': disp_text
            }
            return render(request, "facility_edit.html", dict)

    # Initial "welcome" text
    disp_text = {'': ''}

    dict = {
        'name': facility_choice,
        'disp_text': disp_text
    }

    return render(request, "facility_edit.html", dict)

@login_required
@user_controller
def facility_remove_filter(request):
    """
    Function for choosing a facility

    :param request:
    :return:
    """
    # Dummy parameter
    comp = 'comp'

    # Query all unique companies in the database
    location = Facilities.objects.order_by().values_list('location', flat=True).distinct()

    # No company chosen yet, so query all users in the database
    names = Facilities.objects.order_by()

    # Company is chosen:
    if request.method == 'POST':
        data = request.POST['location_list']
        if data != "None":
            # Query database for users, filtered by chosen company
            names = Facilities.objects.order_by().filter(location=data)
            print(data)
            user_header_text = "Facilities for: " + str(data)
            # Render page with filtered users, instead of all users
            render_dict = {
                'location': location,
                'names': names,
                'param': data,
                'header_text': user_header_text}
            return render(request, "facility_remove_filter.html", render_dict)

    # Text for a header
    user_header_text = "All facilities:"

    # Default render with all companies, and all users
    render_dict = {
        'location': location,
        'names': names,
        'param': comp,
        'header_text': user_header_text}
    return render(request, "facility_remove_filter.html", render_dict)

@login_required
@user_controller
def facility_remove(request):
    # Get facility chosen from "facility_edit_filter"
    data = request.GET['names_list']

    # If there's no user chosen, redirect back to "office_edit_user"
    if data == 'None':
        return redirect("facility_edit_filter")

    # Make query based on chosen user from "office_edit_user"
    facility_choice = Facilities.objects.get(name=data)

    # Run if statement, if "edit button" is clicked on website
    if request.method == 'POST':
        facility_choice.delete()
        return redirect('facility_remove_filter')


    return render(request, "facility_remove.html", {'facility_choice': facility_choice})


@login_required
@user_controller
def edit_user_error(request):

    return render(request, "edit_user_error.html")


"office user password change"
@login_required
@user_controller
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
