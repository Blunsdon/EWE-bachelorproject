from django.urls import path
from . import views

# TODO: added stuff

urlpatterns = [
    path('', views.office_user_home, name="office_user_home"),
    path('office_user_info/', views.office_user_info, name="office_user_info"),
    path('office_user_access/', views.office_user_access, name="office_user_access"),
    path('office_edit_user/', views.office_edit_user, name="office_edit_user"),
    path('office_edit_user/<str:comp>', views.office_edit_user, name="office_edit_user_comp"),
    path('office_edit_user_final/', views.office_edit_user_final, name="office_edit_user_final"),
    path('office_user_final/upgrade/', views.upgrade_field_user, name="upgrade_field_user"),
    path('office_user_final/delete/', views.delete_field_user, name="delete_field_user"),
    path('logs_facility/', views.logs_facility, name="logs_facility"),
    path('logs_user/', views.logs_user, name="logs_user"),
    path('facility_access/', views.facility_access, name="facility_access"),
    path('facility_access/access_time_error/', views.access_time_error, name="access_time_error"),
    path('facility_access/facility_access_give_filter/', views.facility_access_give_filter, name="facility_access_give_filter"),
    path('facility_access/facility_access_give/', views.facility_access_give, name="facility_access_give"),
    path('facility_access/facility_access_remove/', views.facility_access_remove, name="facility_access_remove"),
    path('facility/', views.facility, name="facility"),
    path('facility/facility_edit_filter', views.facility_edit_filter, name="facility_edit_filter"),
    path('facility/facility_remove_filter', views.facility_remove_filter, name="facility_remove_filter"),
    path('facility/facility_add/', views.facility_add, name="facility_add"),
    path('facility/facility_edit/', views.facility_edit, name="facility_edit"),
    path('facility/facility_remove/', views.facility_remove, name="facility_remove"),
    path('edit_user_error/', views.edit_user_error, name="office_user_edit_error"),
    path('office_user_change_password/', views.office_user_change_password, name="office_user_change_password"),
]
