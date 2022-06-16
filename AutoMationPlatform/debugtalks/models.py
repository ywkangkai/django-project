from django.db import models

class DebugTalks(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True)
    name = models.CharField('debugtalk文件名称', max_length=200, default='debugtalk.py')
    debugtalk = models.TextField(null=True, default='#debugtalk.py')
    project = models.OneToOneField('projects.Projects', on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.debugtalk
