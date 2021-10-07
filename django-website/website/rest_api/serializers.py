from django.contrib.auth.models import User, Group
from rest_framework import serializers
from website.models import *


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=80)
    phoneNumber = serializers.CharField(max_length=20)
    company = serializers.CharField(max_length=120)
    password = serializers.CharField(max_length=200)

    class Meta:
        model = Users
        fields = ['__all__']


class LogSerializer(serializers.HyperlinkedModelSerializer):
    dateTime = serializers.DateTimeField()
    companyName = serializers.CharField(max_length=120)
    userName = serializers.CharField(max_length=80)
    userEmail = serializers.EmailField()
    facilityName = serializers.CharField(max_length=80)
    facilityLocation = serializers.CharField(max_length=120)

    class Meta:
        model = Logs
        fields = ['companyName', 'userName', 'dateTime', 'userEmail',
                  'facilityName', 'facilityName', 'facilityLocation']


class FacilitySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=80)
    location = serializers.CharField(max_length=120)
    owner = serializers.CharField(max_length=80)
    key = serializers.CharField(max_length=200)

    class Meta:
        model = Facilities
        fields = ['__all__']
