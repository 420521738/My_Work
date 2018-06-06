# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_colordic_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('BookName', models.CharField(max_length=10)),
                ('Author', models.ManyToManyField(to='app01.AuthorList')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
