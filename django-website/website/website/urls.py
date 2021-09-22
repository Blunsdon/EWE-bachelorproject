"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"commit test"
from django.contrib import admin
from django.urls import path, include

# TODO: check if all added
urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_user/', include('create_user.urls')),
    path('field_user_home/', include('field_user.urls')),
    #path('office_user/', include('office_user.urls')),
    #path('rest_api/', include('rest_api.urls')),
]
