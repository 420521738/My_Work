# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20150118_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u4efb\u52a1\u540d\u79f0')),
                ('description', models.TextField(null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('task_type', models.CharField(max_length=32, verbose_name='\u4efb\u52a1\u7c7b\u578b', choices=[(b'cmd', b'\xe5\x91\xbd\xe4\xbb\xa4\xe6\x89\xa7\xe8\xa1\x8c'), (b'file_transfer', b'\xe6\x96\x87\xe4\xbb\xb6\xe5\x88\x86\xe5\x8f\x91'), (b'config_allocation', b'\xe9\x85\x8d\xe7\xbd\xae\xe4\xb8\x8b\xe5\x8f\x91')])),
                ('total_hosts', models.IntegerField(verbose_name='\u4efb\u52a1\u4e3b\u673a\u6570')),
                ('content', models.TextField(verbose_name='\u4efb\u52a1\u5185\u5bb9')),
                ('memo', models.TextField(null=True, blank=True)),
                ('created_by', models.ForeignKey(verbose_name='\u4efb\u52a1\u521b\u5efa\u8005', to='web.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.CharField(max_length=32, verbose_name='\u7ed3\u679c', choices=[(b'success', '\u6210\u529f'), (b'failed', '\u5931\u8d25'), (b'unknown', '\u672a\u77e5')])),
                ('log', models.TextField(verbose_name='\u4efb\u52a1\u65e5\u5fd7')),
                ('task', models.ForeignKey(to='web.TaskCenter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
