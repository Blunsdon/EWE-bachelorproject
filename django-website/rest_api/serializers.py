from abc import ABC

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from website.models import *


class LogSerializer(serializers.HyperlinkedModelSerializer):
    dateTime = serializers.DateTimeField()
    userEmail = serializers.EmailField()
    facilityName = serializers.CharField(max_length=80)


    class Meta:
        model = Logs
        fields = ['dateTime', 'userEmail', 'facilityName']


class FacilitySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=80)

    class Meta:
        model = Facilities
        fields = ['name']


class GetKeyPostLogSerializer(serializers.Serializer):
    facility = FacilitySerializer(many=True)
    log = LogSerializer(many=True)


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    userEmail = serializers.EmailField()

    class Meta:
        model = Users
        fields = ['userEmail']
