from django.urls import path
from .views import *

# TODO: added stuff

urlpatterns = [
    path('log_api/', LogsView.as_view())
]


