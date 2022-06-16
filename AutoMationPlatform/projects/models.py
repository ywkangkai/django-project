from django.db import models


class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    projectname = models.CharField(max_length=20)
    leader = models.CharField(max_length=20)
    appname = models.CharField(max_length=20)
    test = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)  # auto_now_add只显示第一次创建的时间
    update_time = models.DateTimeField(auto_now=True)  # auto_now更新最后编辑的时间

    def __str__(self):
        return f"{self.projectname}"
