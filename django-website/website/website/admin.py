from django.contrib import admin
from .models import Users, Facilities, Logs, JoinTableFacility, JoinTableUser

admin.site.register(Users)
admin.site.register(Logs)
admin.site.register(Facilities)
admin.site.register(JoinTableUser)
admin.site.register(JoinTableFacility)

