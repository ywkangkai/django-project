from rest_framework import serializers
from projects.models import Projects
from rest_framework import validators
from interfaces.serializers import InterfacesSerializer


import locale
'''
自定义调用字段校验，value是前端传入的字段，如在name字段调用此函数，value=name，如果校验失败一定使用
raise serializers.ValidationError
'''
def is_name_contain_x(value):
    print(value)
    if len(value) > 20:
        raise serializers.ValidationError('项目名称不能超过20个字符')
    if value == '':
        print('xxxxxxxxxxxxx')
        raise serializers.ValidationError('请填写项目名称')

class ProjectsSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=100, read_only=True)

    projectname = serializers.CharField(max_length=20, min_length=2,validators=[is_name_contain_x], error_messages={"required": "请填写项目名称"})
                                 # validators=[validators.UniqueValidator(Projects.objects.all(), message='项目已存在',
                                 #                                        ), is_name_contain_x], error_messages={"required": "请填写项目名称"})

    leader = serializers.CharField(max_length=20)
    #leader = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)

    test = serializers.CharField(max_length=20, error_messages={"required": "请填写测试人员"})

    appname = serializers.CharField(max_length=20)

    interfaces_set = InterfacesSerializer(many=True, read_only=True)  #在接口表中有一个外键叫project，在项目父表引用时写法（子表_set）

    locale.setlocale(locale.LC_CTYPE, 'chinese')
    datatime_fmt = '%Y年%m月%d %H:%M:%S'
    update_time = serializers.DateTimeField(format=datatime_fmt, read_only=True)
    create_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format=datatime_fmt, read_only=True)

