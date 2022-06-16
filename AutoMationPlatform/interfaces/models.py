from django.db import models

class Interfaces(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('接口名称', max_length=200, unique=True, help_text='接口名称')
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE, help_text='所属项目')
    tester = models.CharField('测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField('简要描述', max_length=200, null=True, blank=True, help_text='简要描述')
    create_time = models.DateTimeField(auto_now_add=True)  # auto_now_add只显示第一次创建的时间
    update_time = models.DateTimeField(auto_now=True)  # auto_now更新最后编辑的时间

    def __str__(self):
        return self.name

