from rest_framework import serializers
from interfaces.models import Interfaces
from rest_framework import validators
from interfaces.serializers import InterfacesSerializer
from .models import Configures

import locale

class InterfacesAnotherSerializer(serializers.Serializer):

    project = serializers.StringRelatedField(help_text='项目名称')

    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True)

    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True)

    name = serializers.CharField(read_only=True)




class ConfigSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)

    interface = InterfacesAnotherSerializer()

    name = serializers.CharField(validators=[validators.UniqueValidator(Configures.objects.all(), message='配置名称已存在',)])

    author = serializers.CharField(max_length=10)

    request = serializers.CharField(write_only=True)



class ConfigUpdateSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)

    interface = InterfacesAnotherSerializer()

    name = serializers.CharField()

    author = serializers.CharField(max_length=10)

    request = serializers.CharField(write_only=True)

