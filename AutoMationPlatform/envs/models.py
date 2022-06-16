from django.db import models

class Envs(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField(verbose_name='环境名称', max_length=200, unique=True, help_text='环境名称')
    base_url = models.URLField(verbose_name='请求base url', max_length=200, help_text='请求base url')
    desc = models.CharField(verbose_name='简要描述', max_length=200, help_text='简要描述')
    create_time = models.DateTimeField(auto_now_add=True)  # auto_now_add只显示第一次创建的时间
    update_time = models.DateTimeField(auto_now=True)  # auto_now更新最后编辑的时间

    def __str__(self):
        return self.name
