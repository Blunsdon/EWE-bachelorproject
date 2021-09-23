from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect

@login_required
def index(request):
    usertype = request.user.userType

    if usertype == 'Field user':
        return redirect('/field_user_home')
    elif usertype == 'Office user':
        return redirect('/office_user_home')
    elif usertype == 'Admin':
        return redirect('/admin')
    else:
        return redirect('')

def homepage(request):
    return redirect('/accounts/login')