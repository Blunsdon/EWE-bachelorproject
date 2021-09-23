from django.shortcuts import render
from django.http import HttpResponse

# Home for create user
def create_user(request):

    return render(request, "create_user.html")

# Create your views here.
# TODO: review

