from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

"""
cURL examples:

Login curl
curl -X POST -d "{\"email\": \"admin@admin.com\",\"password\": \"admin\"}" -H "Content-Type:application/json"  http://127.0.0.1:8000/api/auth/token/login/

Post data curl, with login token
curl -X POST -d "{\"userName\":\"Marc\",\"companyName\":\"Jan\",\"dateTime\":\"2021-10-07T08:59:52\",\"userEmail\":\"field@field2.com\",\"facilityName\":\"EVE\",\"facilityLocation\":\"Herning\"}" -H "Authorization: Token d356ad4063cba234aec952d98fa9a9500dddf08e" -H "Content-Type:application/json" http://127.0.0.1:8000/rest_api/log_api/

Logout curl
curl -X POST http://127.0.0.1:8000/api/auth/token/logout/ -H "Authorization: Token ~token-code~"
"""

class LogsView(APIView):
    def post(self, request):
        post_data = GetKeyPostLogSerializer(data=request.data)
        if post_data.is_valid():
            # Get message data
            log_userName = post_data.data['log'][0]['userName']
            log_companyName = post_data.data['log'][0]['companyName']
            log_dateTime = post_data.data['log'][0]['dateTime']
            log_userEmail = post_data.data['log'][0]['userEmail']
            log_facilityName = post_data.data['log'][0]['facilityName']
            log_facilityLocaltion = post_data.data['log'][0]['facilityLocation']
            data2 = post_data.data['facility'][0]['name']
            # make log
            make_log = Logs()
            # get User object from unique Email
            make_log.user = Users.objects.get(email=log_userEmail)
            # get facility object from unique facility name
            make_log.facility = Facilities.objects.get(name=log_facilityName)
            make_log.companyName = log_companyName
            make_log.dateTime = log_dateTime
            make_log.facilityLocation = log_facilityLocaltion
            make_log.facilityName = log_facilityName
            make_log.userEmail = log_userEmail
            make_log.userName = log_userName
            make_log.save()
            # Get key
            facility = Facilities.objects.get(name=data2)
            key = facility.key
            return Response({"status": "success", "key": key}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": post_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class FacilityView(APIView):
    def post(self, request):
        post_data = UsersSerializer(data=request.data)
        if post_data.is_valid():
            data = post_data.data['userEmail']
            pk = Users.objects.get(email=data)
            list_fac = JoinTable.objects.all().filter(user=pk).values_list("facility__name", "facility__location",
                                                                           "user__email", "user__company",
                                                                           "user__name")
            return Response({"status": "success", "list":list_fac}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": post_data.errors}, status=status.HTTP_400_BAD_REQUEST)
