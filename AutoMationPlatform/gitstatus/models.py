from django.db import models


class GitStatus(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    git = models.CharField(max_length=500, default='未开始')
    build_before = models.CharField(max_length=500, default='未开始')
    structure = models.CharField(max_length=500, default='未开始')
    build_after = models.CharField(max_length=500, default='未开始')

    git_status1 = models.CharField(max_length=500, default='wait')
    build_before_status2 = models.CharField(max_length=500, default='wait')
    structure_status3 = models.CharField(max_length=500, default='wait')
    build_after_status4 = models.CharField(max_length=500, default='wait')

    git_description = models.CharField(max_length=500, default='拉取代码')
    build_before_description = models.CharField(max_length=500, default='构建前步骤')
    structure_description = models.CharField(max_length=500, default='构建前步骤')
    build_after_description = models.CharField(max_length=500, default='构建后步骤')
    respository = models.ForeignKey('repository.Repository', on_delete=models.CASCADE)