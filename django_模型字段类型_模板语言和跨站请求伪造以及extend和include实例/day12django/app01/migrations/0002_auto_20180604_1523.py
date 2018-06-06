# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thirdmodel',
            name='Age',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thirdmodel',
            name='CaiPiao',
            field=models.CommaSeparatedIntegerField(max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thirdmodel',
            name='Cname',
            field=models.CharField(default=b'chen', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thirdmodel',
            name='Gender',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
