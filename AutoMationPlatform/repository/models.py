from django.db import models


class Repository(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField(max_length=50, unique=True, help_text='工程名称')
    git = models.CharField(max_length=200, help_text='git仓库地址')
    server = models.CharField(max_length=200, help_text='服务器地址')  # 加 null=True是有因为有些用例不需要前置
    type = models.CharField(max_length=10, help_text='工程类型')
    address = models.CharField(max_length=500, help_text='企业微信地址')
    send = models.BooleanField(help_text='是否发送')
    build = models.TextField(help_text='构建前后步骤', null=True, blank=True)



