from django.shortcuts import render

# Create your views here.

def field_user_home(request):

    return render(request, "field_user_home.html")

def field_user_info(request):

    return render(request, "field_user_info.html")

def field_user_access(request):

    return render(request, "field_user_access.html")