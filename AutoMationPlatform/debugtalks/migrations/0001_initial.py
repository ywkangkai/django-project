# Generated by Django 3.2.13 on 2022-05-02 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebugTalks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id主键')),
                ('name', models.CharField(default='debugtalk.py', max_length=200, verbose_name='debugtalk文件名称')),
                ('debugtalk', models.TextField(default='#debugtalk.py', null=True)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='projects.projects')),
            ],
        ),
    ]
