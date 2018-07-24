# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_tasklog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklog',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
