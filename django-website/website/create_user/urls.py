from django.urls import path
from . import views


# TODO: should link to login page ?

urlpatterns = [
    path('', views.create_user, name='create_user'),
]