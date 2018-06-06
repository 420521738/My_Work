# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20180604_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='FourthModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
