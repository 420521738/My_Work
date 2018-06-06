# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_fourthmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='fourthmodel',
            name='IP',
            field=models.IPAddressField(default='127.0.0.1'),
            preserve_default=False,
        ),
    ]
