# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('Nid', models.AutoField(serialize=False, primary_key=True)),
                ('UserName', models.CharField(max_length=50)),
                ('PassWord', models.CharField(max_length=256)),
                ('RealName', models.CharField(max_length=256)),
                ('Email', models.EmailField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
