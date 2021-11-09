from django.urls import path
from . import views

# TODO: added stuff

urlpatterns = [
    path('', views.field_user_home, name="field_user_home"),
    path('field_user_info/', views.field_user_info, name="field_user_info"),
    path('field_user_access/', views.field_user_access, name="field_user_access"),
    path('edit_user_error/', views.edit_user_error, name="field_user_edit_error"),
    path('field_user_change_password/', views.field_user_change_password, name="field_user_change_password"),
]