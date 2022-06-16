# Generated by Django 3.2.13 on 2022-04-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('projectname', models.CharField(max_length=20)),
                ('leader', models.CharField(max_length=20)),
                ('appname', models.CharField(max_length=20)),
                ('test', models.CharField(max_length=20)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]