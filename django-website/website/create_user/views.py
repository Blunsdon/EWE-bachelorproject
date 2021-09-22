from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# TODO: review
# Home for create user
def create_user(request):

    return render(request, "create_user.html")

