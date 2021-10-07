from abc import ABC

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from website.models import *


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


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    userEmail = serializers.EmailField()

    class Meta:
        model = Users
        fields = ['userEmail']


class FacilitySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=80)

    class Meta:
        model = Facilities
        fields = ['name']


class GetKeyPostLogSerializer(serializers.Serializer):
    facility = FacilitySerializer(many=True)
    log = LogSerializer(many=True)
