from rest_framework import serializers
from envs.models import Envs
from rest_framework import validators
from interfaces.serializers import InterfacesSerializer


import locale


class EnvSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=100, read_only=True)

    name = serializers.CharField(max_length=20, min_length=2, validators=[validators.UniqueValidator(Envs.objects.all(), message='环境已存在')])

    base_url = serializers.URLField(max_length=200)


    desc = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)

    locale.setlocale(locale.LC_CTYPE, 'chinese')
    datatime_fmt = '%Y年%m月%d %H:%M:%S'
    update_time = serializers.DateTimeField(format=datatime_fmt, read_only=True)
    create_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format=datatime_fmt, read_only=True)



class EidtEnvSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=100, read_only=True)

    name = serializers.CharField(max_length=20, min_length=2, validators=[validators.UniqueValidator(Envs.objects.all(), message='环境已存在')])

    base_url = serializers.URLField(max_length=200)


    desc = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)

    locale.setlocale(locale.LC_CTYPE, 'chinese')
    datatime_fmt = '%Y年%m月%d %H:%M:%S'
    update_time = serializers.DateTimeField(format=datatime_fmt, read_only=True)
    create_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format=datatime_fmt, read_only=True)



class EidtEnvSerializerWithNoName(serializers.Serializer):

    id = serializers.CharField(max_length=100, read_only=True)

    name = serializers.CharField(max_length=20, min_length=2)

    base_url = serializers.URLField(max_length=200)


    desc = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)

    locale.setlocale(locale.LC_CTYPE, 'chinese')
    datatime_fmt = '%Y年%m月%d %H:%M:%S'
    update_time = serializers.DateTimeField(format=datatime_fmt, read_only=True)
    create_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format=datatime_fmt, read_only=True)

