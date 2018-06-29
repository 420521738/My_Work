# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BBS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('summary', models.CharField(max_length=256, null=True, blank=True)),
                ('content', models.TextField()),
                ('view_count', models.IntegerField()),
                ('ranking', models.IntegerField()),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BBS_user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signature', models.CharField(default=b'\xe8\xbf\x99\xe4\xb8\xaa\xe5\xae\xb6\xe4\xbc\x99\xe5\xbe\x88\xe6\x87\x92\xef\xbc\x8c\xe4\xbb\x80\xe4\xb9\x88\xe4\xb9\x9f\xe6\xb2\xa1\xe7\x95\x99\xe4\xb8\x8b', max_length=128)),
                ('photo', models.ImageField(default=b'upload_imgs/user-1.jpg', upload_to=b'upload_imgs/')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('administrator', models.ForeignKey(to='app01.BBS_user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bbs',
            name='author',
            field=models.ForeignKey(to='app01.BBS_user'),
            preserve_default=True,
        ),
    ]
