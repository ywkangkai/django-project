# Generated by Django 3.2.13 on 2022-05-11 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testsuits',
            fields=[
                ('id', models.AutoField(help_text='id主键', primary_key=True, serialize=False, verbose_name='id主键')),
                ('name', models.CharField(help_text='套件名称', max_length=200, unique=True, verbose_name='套件名称')),
                ('include', models.TextField(help_text='包含的接口', verbose_name='包含的接口')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(help_text='所属项目', on_delete=django.db.models.deletion.CASCADE, to='projects.projects')),
            ],
        ),
    ]