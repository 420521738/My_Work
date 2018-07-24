# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_tasklog_host_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcenter',
            name='groups',
            field=models.ManyToManyField(to='web.Group', verbose_name='\u9009\u62e9\u7ec4', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taskcenter',
            name='hosts',
            field=models.ManyToManyField(to='web.Host', verbose_name='\u9009\u62e9\u4efb\u52a1\u4e3b\u673a', blank=True),
            preserve_default=True,
        ),
    ]
