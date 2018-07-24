# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20150120_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcenter',
            name='kick_off_at',
            field=models.DateTimeField(null=True, verbose_name='\u6267\u884c\u65f6\u95f4', blank=True),
            preserve_default=True,
        ),
    ]
