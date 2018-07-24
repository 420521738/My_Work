# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20150122_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcenter',
            name='created_by',
            field=models.ForeignKey(verbose_name='\u4efb\u52a1\u521b\u5efa\u8005', blank=True, to='web.UserProfile', null=True),
            preserve_default=True,
        ),
    ]
