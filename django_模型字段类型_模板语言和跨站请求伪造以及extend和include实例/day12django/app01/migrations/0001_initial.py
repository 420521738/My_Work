# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FirstModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('UserName', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThirdModel',
            fields=[
                ('Nid', models.AutoField(serialize=False, primary_key=True)),
                ('Name', models.CharField(default=b'qiufei', max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
