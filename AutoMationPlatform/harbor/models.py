from django.db import models

class Harbor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    repository = models.ForeignKey('repository.Repository', on_delete=models.CASCADE, help_text='所属项目', default=123)
