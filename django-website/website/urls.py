from django.contrib import admin
from django.urls import path, include
from . import views


# TODO: check if all added
urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login_redirect/', views.index),
    path('create_user/', include('create_user.urls')),
    path('field_user_home/', include('field_user.urls')),
    path('', views.homepage, name="front_page"),
    path('office_user_home/', include('office_user.urls')),
    path('rest_api/', include('rest_api.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('logout_user/', views.logout_view, name="logout_user")
]
