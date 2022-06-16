from rest_framework import serializers
from interfaces.models import Interfaces
from rest_framework import validators
from projects.models import Projects

import locale
'''
自定义调用字段校验，value是前端传入的字段，如在name字段调用此函数，value=name，如果校验失败一定使用
raise serializers.ValidationError
'''


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):

    project = serializers.StringRelatedField(label='所属项目', help_text='所属项目')

    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True)  #  添加一个不是表中的字段必须要加write_only=True

    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True)

    name = serializers.CharField(read_only=True)

    class Meta:
        model = Interfaces
        fields =('name', 'pid', 'iid', 'project')





class TestCaseSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)

    name = serializers.CharField(max_length=20,)

    author = serializers.CharField(max_length=20)

    request = serializers.CharField(max_length=5000)

    include = serializers.CharField(allow_blank=True, allow_null=True)

    interface = InterfacesProjectsModelSerializer()

    locale.setlocale(locale.LC_CTYPE, 'chinese')
    datatime_fmt = '%Y年%m月%d %H:%M:%S'
    update_time = serializers.DateTimeField(format=datatime_fmt, read_only=True)
    create_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format=datatime_fmt, read_only=True)



class EnvSerializer(serializers.Serializer):

    id = serializers.CharField()

    name = serializers.CharField()



