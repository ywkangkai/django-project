from rest_framework import serializers
from interfaces.models import Interfaces
from rest_framework import validators
from .models import Testsuits
from projects.models import Projects

import locale
'''
自定义调用字段校验，value是前端传入的字段，如在name字段调用此函数，value=name，如果校验失败一定使用
raise serializers.ValidationError
'''



class TestsuitesSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=1000, read_only=True)

    name = serializers.CharField(max_length=200, validators=[validators.UniqueValidator(Testsuits.objects.all(), message='套件已存在', )])

    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')

    project_id = serializers.PrimaryKeyRelatedField(write_only=True, label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())  #PrimaryKeyRelatedFiel会拿到关联父表的主键，即id

    include = serializers.CharField()

    locale.setlocale(locale.LC_CTYPE, 'chinese')
    datatime_fmt = '%Y年%m月%d %H:%M:%S'
    update_time = serializers.DateTimeField(format=datatime_fmt, read_only=True)
    create_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format=datatime_fmt, read_only=True)



class EditTestsuiteSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200, validators=[validators.UniqueValidator(Testsuits.objects.all(), message='接口已存在', )])

    include = serializers.CharField()

    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')

    project_id = serializers.PrimaryKeyRelatedField(write_only=True, label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())




class EditTestsuitWithNoNameSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200)

    include = serializers.CharField()

    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')

    project_id = serializers.PrimaryKeyRelatedField(write_only=True, label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())



class TestsuitesDetailSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=1000, read_only=True)

    name = serializers.CharField(read_only=True)

    project = serializers.StringRelatedField(read_only=True)

    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())  #PrimaryKeyRelatedFiel会拿到关联父表的主键，即id

    include = serializers.CharField(read_only=True)



