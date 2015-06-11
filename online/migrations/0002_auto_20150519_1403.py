# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=50)),
                ('file_loc', models.FileField(upload_to=b'./upload/')),
                ('file_size', models.CharField(max_length=50)),
                ('file_type', models.CharField(max_length=50)),
                ('upload_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('folder_name', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField()),
                ('modify_time', models.DateTimeField()),
                ('description', models.CharField(max_length=50)),
                ('User', models.ForeignKey(to='online.User')),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=50)),
                ('User', models.ForeignKey(to='online.User')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='Folder',
            field=models.ForeignKey(to='online.Folder'),
        ),
    ]
