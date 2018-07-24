# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20150122_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklog',
            name='host_id',
            field=models.IntegerField(default=None, verbose_name='\u6c47\u62a5\u4e3b\u673aID'),
            preserve_default=True,
        ),
    ]
