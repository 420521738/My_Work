# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_host_poll_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklog',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
