# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelist',
            name='conditons',
            field=models.ManyToManyField(to='web.Conditions', null=True, verbose_name='\u9600\u503c\u5217\u8868', blank=True),
            preserve_default=True,
        ),
    ]
