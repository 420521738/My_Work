# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_fourthmodel_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorDic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ColorNmae', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=20)),
                ('Gender', models.BooleanField(default=False)),
                ('Color', models.ForeignKey(to='app01.ColorDic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
