from rest_framework import serializers
from interfaces.models import Interfaces
from rest_framework import validators
from .models import Reports

import locale

def datetimes_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    datatime_fmt = '%Y年%m月%d日 %H:%M:%S'  #作用是在设置时间的时候存在中文，如果不是utf-8会报错，这样是设置为简体中文
    return datatime_fmt

class ReportsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time':{
                'format':datetimes_fmt()
            },
            'update_time': {
                'format': datetimes_fmt()
            },
        }
