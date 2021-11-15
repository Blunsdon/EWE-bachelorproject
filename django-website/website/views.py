from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect


@login_required
def index(request):
    usertype = request.user.userType

    if usertype == 'Field user':
        return redirect('field_user_home')
    elif usertype == 'Office user':
        return redirect('office_user_home')
    elif usertype == 'Admin':
        return redirect('/admin')
    else:
        return redirect('logout')


def homepage(request):
    return redirect('/accounts/login')


def logout_view(request):
    logout(request)
    response = redirect('front_page')
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response

