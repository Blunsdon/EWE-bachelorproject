from django.urls import path
from . import views

# TODO: added stuff

urlpatterns = [
    path('', views.office_user_home, name="office_user_home"),
    path('office_user_info/', views.office_user_info, name="office_user_info"),
    path('office_user_access/', views.office_user_access, name="office_user_access"),
]