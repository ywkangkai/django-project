from rest_framework import serializers
from projects.models import Projects
from rest_framework import validators
from interfaces.serializers import InterfacesSerializer


import locale


class DebugtalkSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=100, read_only=True)

    name = serializers.CharField(read_only=True)

    project = serializers.StringRelatedField(read_only=True)

    debugtalk = serializers.CharField()


