from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
# Create your views here.

#TODO: fix crsf

class LogsView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = LogSerializer(data=request.data)
        # connect User fk
        # connect facility fk
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Example for login on windows curl:
# curl -X POST -d "{\"email\": \"admin@admin.com\",\"password\": \"admin\"}" -H "Content-Type:application/json"  http://127.0.0.1:8000/api/auth/token/login/
class UserView(APIView):
    def post(self, request):
        return False


class FacilityView(APIView):
    def post(self, request):
        return False
