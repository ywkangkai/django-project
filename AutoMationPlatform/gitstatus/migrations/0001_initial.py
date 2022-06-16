# Generated by Django 3.2.13 on 2022-06-08 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitStatus',
            fields=[
                ('id', models.AutoField(help_text='id主键', primary_key=True, serialize=False, verbose_name='id主键')),
                ('git', models.CharField(default='未开始', max_length=500)),
                ('build_before', models.CharField(default='未开始', max_length=500)),
                ('structure', models.CharField(default='未开始', max_length=500)),
                ('build_after', models.CharField(default='未开始', max_length=500)),
                ('git_status1', models.CharField(default='wait', max_length=500)),
                ('build_before_status2', models.CharField(default='wait', max_length=500)),
                ('structure_status3', models.CharField(default='wait', max_length=500)),
                ('build_after_status4', models.CharField(default='wait', max_length=500)),
                ('git_description', models.CharField(default='拉取代码', max_length=500)),
                ('build_before_description', models.CharField(default='构建前步骤', max_length=500)),
                ('structure_description', models.CharField(default='构建前步骤', max_length=500)),
                ('build_after_description', models.CharField(default='构建后步骤', max_length=500)),
                ('respository', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.repository')),
            ],
        ),
    ]
