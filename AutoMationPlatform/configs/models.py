from django.db import models

class Configures(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('配置名称', max_length=50, help_text='配置名称')
    interface = models.ForeignKey('interfaces.Interfaces', on_delete=models.CASCADE)
    author = models.CharField('编写人员', max_length=50, help_text='编写人员')
    request = models.TextField('请求信息', help_text='请求信息')


    def __str__(self):
        return self.name