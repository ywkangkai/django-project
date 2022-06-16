from rest_framework import serializers
from interfaces.models import Interfaces
from rest_framework import validators
from projects.models import Projects

import locale
'''
自定义调用字段校验，value是前端传入的字段，如在name字段调用此函数，value=name，如果校验失败一定使用
raise serializers.ValidationError
'''

def name_count(value):
    count = Interfaces.objects.filter(name=value).count()
    if count > 1:
        raise serializers.ValidationError('')



class InterfacesSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=1000, read_only=True)

    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')  # StringRelatedField会返回model中的__str__下的值

    name = serializers.CharField(max_length=200, validators=[validators.UniqueValidator(Interfaces.objects.all(), message='接口已存在', )])

    project_id = serializers.PrimaryKeyRelatedField(write_only=True, label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())  #PrimaryKeyRelatedFiel会拿到关联父表的主键，即id

    tester = serializers.CharField(max_length=20)

    desc = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)

    locale.setlocale(locale.LC_CTYPE, 'chinese')
    datatime_fmt = '%Y年%m月%d %H:%M:%S'
    update_time = serializers.DateTimeField(format=datatime_fmt, read_only=True)
    create_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format=datatime_fmt, read_only=True)



class EditInterfacesSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200, validators=[validators.UniqueValidator(Interfaces.objects.all(), message='接口已存在', )])

    tester = serializers.CharField(max_length=20)

    desc = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)




class EditInterfacesWithNoNameSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200)

    tester = serializers.CharField(max_length=20)

    desc = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)


class EnvSerializer(serializers.Serializer):

    id = serializers.CharField()

    name = serializers.CharField()

