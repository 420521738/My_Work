# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_taskcenter_kick_off_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='poll_interval',
            field=models.IntegerField(default=300),
            preserve_default=True,
        ),
    ]
