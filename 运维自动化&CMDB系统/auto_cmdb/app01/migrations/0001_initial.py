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
            name='ApiAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=64, verbose_name='\u63a5\u53e3url')),
                ('description', models.CharField(max_length=64, verbose_name='\u7b80\u4ecb')),
                ('method_type', models.CharField(max_length=32, verbose_name='\u53ef\u7528\u65b9\u6cd5', choices=[(b'GET', b'\xe5\x85\x81\xe8\xae\xb8Get(\xe5\x8f\xaf\xe8\xaf\xbb)'), (b'POST', b'\xe5\x85\x81\xe8\xae\xb8POST(\xe5\x8f\xaf\xe4\xbf\xae\xe6\x94\xb9)'), (b'PUT', b'\xe5\x85\x81\xe8\xae\xb8PUT(\xe5\x8f\xaf \xe5\x88\x9b\xe5\xbb\xba)'), (b'HEAD', b'HEAD(\xe6\x9a\x82\xe4\xb8\x8d\xe7\x94\xa8)'), (b'PATCH', b'PATCH(\xe6\x9a\x82\xe4\xb8\x8d\xe7\x94\xa8)')])),
            ],
            options={
                'verbose_name': '\u63a5\u53e3\u6743\u9650',
                'verbose_name_plural': '\u63a5\u53e3\u6743\u9650',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_type', models.CharField(default=b'server', max_length=64, choices=[(b'server', '\u670d\u52a1\u5668'), (b'switch', '\u4ea4\u6362\u673a'), (b'router', '\u8def\u7531\u5668'), (b'firewall', '\u9632\u706b\u5899'), (b'storage', '\u5b58\u50a8\u8bbe\u5907'), (b'acc_cpu', 'CPU'), (b'acc_memory', '\u5185\u5b58\u6761'), (b'acc_disk', '\u786c\u76d8'), (b'acc_network_adapter', '\u7f51\u5361'), (b'acc_monitor', '\u663e\u793a\u5668'), (b'acc_others', '\u5176\u5b83\u914d\u4ef6')])),
                ('name', models.CharField(max_length=30)),
                ('hostname', models.CharField(unique=True, max_length=32, blank=True)),
                ('asset_op', models.CharField(max_length=32, null=True, blank=True)),
                ('trade_time', models.DateTimeField(null=True, verbose_name='\u8d2d\u4e70\u65f6\u95f4', blank=True)),
                ('warranty', models.SmallIntegerField(null=True, verbose_name='\u4fdd\u4fee\u671f', blank=True)),
                ('price', models.IntegerField(null=True, verbose_name='\u4ef7\u683c', blank=True)),
                ('function', models.CharField(max_length=32, null=True, blank=True)),
                ('cabinet_num', models.CharField(max_length=30, null=True, verbose_name='\u673a\u67dc\u53f7', blank=True)),
                ('cabinet_order', models.SmallIntegerField(max_length=30, null=True, verbose_name='\u673a\u67dc\u4e2d\u5e8f\u53f7', blank=True)),
                ('status', models.SmallIntegerField(blank=True, null=True, verbose_name='\u8bbe\u5907\u72b6\u6001', choices=[(1, b'Init'), (2, b'Standby'), (3, b'Online'), (4, b'Offline'), (5, b'Unreachable'), (6, b'Deprecated'), (7, b'Maintenance')])),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u603b\u8868',
                'verbose_name_plural': '\u8d44\u4ea7\u603b\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u4e1a\u52a1\u7ebf')),
                ('memo', models.CharField(max_length=64, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u4e1a\u52a1\u7ebf',
                'verbose_name_plural': '\u4e1a\u52a1\u7ebf',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('definded_raid_type', models.CharField(max_length=32, null=True, verbose_name='\u9884\u5b9a\u4e49raid\u7c7b\u578b', blank=True)),
                ('os_installed', models.BooleanField(default=1)),
                ('puppet_installed', models.BooleanField(default=1)),
                ('zabbix_configured', models.BooleanField(default=1)),
                ('auditing_configured', models.BooleanField(default=1)),
                ('approved', models.BooleanField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(unique=True, max_length=64, verbose_name='\u5408\u540c\u53f7')),
                ('name', models.CharField(max_length=64, verbose_name='\u5408\u540c\u540d\u79f0')),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('cost', models.IntegerField(verbose_name='\u5408\u540c\u91d1\u989d')),
                ('start_date', models.DateTimeField(blank=True)),
                ('end_date', models.DateTimeField(blank=True)),
                ('license_num', models.IntegerField(verbose_name='license\u6570\u91cf', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u5408\u540c',
                'verbose_name_plural': '\u5408\u540c',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=64, verbose_name='SN\u53f7', blank=True)),
                ('parent_sn', models.CharField(unique=True, max_length=128, blank=True)),
                ('manufactory', models.CharField(default=None, max_length=32, verbose_name='\u5236\u9020\u5546', blank=True)),
                ('model', models.CharField(max_length=64, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': 'CPU\u90e8\u4ef6',
                'verbose_name_plural': 'CPU\u90e8\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, verbose_name='SN\u53f7', blank=True)),
                ('parent_sn', models.CharField(max_length=128, blank=True)),
                ('slot', models.CharField(max_length=32, verbose_name='\u63d2\u69fd\u4f4d', blank=True)),
                ('manufactory', models.CharField(default=None, max_length=32, verbose_name='\u5236\u9020\u5546', blank=True)),
                ('model', models.CharField(max_length=128, verbose_name='\u78c1\u76d8\u578b\u53f7', blank=True)),
                ('capacity', models.FloatField(verbose_name='\u78c1\u76d8\u5bb9\u91cfGB', blank=True)),
                ('iface_type', models.CharField(blank=True, max_length=64, verbose_name='\u63a5\u53e3\u7c7b\u578b', choices=[(b'SATA', b'SATA'), (b'SAS', b'SAS'), (b'SCSI', b'SCSI'), (b'SSD', b'SSD')])),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u786c\u76d8\u90e8\u4ef6',
                'verbose_name_plural': '\u786c\u76d8\u90e8\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=128, verbose_name='\u8bf7\u6c42ID')),
                ('post_data', models.TextField(verbose_name='\u8bf7\u6c42Data', blank=True)),
                ('detail', models.TextField(verbose_name='\u8be6\u7ec6\u63cf\u8ff0', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u673a\u623fenglish')),
                ('display_name', models.CharField(default=None, max_length=32, verbose_name='\u4e2d\u6587\u663e\u793a\u540d')),
                ('region', models.CharField(default=None, max_length=64, verbose_name='\u533a\u57df')),
                ('region_display_name', models.CharField(default=None, max_length=64, verbose_name='\u533a\u57df\u4e2d\u6587')),
                ('isp', models.CharField(default=None, max_length=32, verbose_name='\u8fd0\u8425\u5546')),
                ('isp_display_name', models.CharField(default=None, max_length=32, verbose_name='\u8fd0\u8425\u5546\u4e2d\u6587')),
                ('floor', models.IntegerField(default=1, verbose_name='\u697c\u5c42')),
                ('memo', models.CharField(max_length=64, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'verbose_name': '\u673a\u623f',
                'verbose_name_plural': '\u673a\u623f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Maintainence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u4e8b\u4ef6\u540d\u79f0')),
                ('maintain_type', models.SmallIntegerField(max_length=30, verbose_name='\u53d8\u66f4\u7c7b\u578b', choices=[(1, '\u786c\u4ef6\u66f4\u6362'), (2, '\u65b0\u589e\u914d\u4ef6'), (3, '\u8bbe\u5907\u4e0b\u7ebf'), (4, '\u8bbe\u5907\u4e0a\u7ebf'), (5, '\u5b9a\u671f\u7ef4\u62a4'), (6, '\u4e1a\u52a1\u4e0a\u7ebf\\\u66f4\u65b0\\\u53d8\u66f4'), (7, '\u5176\u5b83')])),
                ('description', models.TextField(verbose_name='\u4e8b\u4ef6\u63cf\u8ff0')),
                ('device_sn', models.CharField(max_length=64, verbose_name=b'AssetID', blank=True)),
                ('event_start', models.DateTimeField(verbose_name='\u4e8b\u4ef6\u5f00\u59cb\u65f6\u95f4', blank=True)),
                ('event_end', models.DateTimeField(verbose_name='\u4e8b\u4ef6\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u53d8\u66f4\u7eaa\u5f55',
                'verbose_name_plural': '\u53d8\u66f4\u7eaa\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manufactory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u5382\u5546\u540d\u79f0')),
                ('support_num', models.CharField(max_length=30, verbose_name='\u652f\u6301\u7535\u8bdd', blank=True)),
                ('memo', models.CharField(max_length=30, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u5382\u5546',
                'verbose_name_plural': '\u5382\u5546',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, verbose_name='SN\u53f7', blank=True)),
                ('parent_sn', models.CharField(max_length=128, blank=True)),
                ('model', models.CharField(max_length=64, verbose_name='\u578b\u53f7', blank=True)),
                ('manufactory', models.CharField(max_length=32, null=True, verbose_name='\u5236\u9020\u5546', blank=True)),
                ('slot', models.CharField(max_length=32, verbose_name='\u63d2\u69fd\u4f4d', blank=True)),
                ('capacity', models.FloatField(verbose_name='\u5bb9\u91cf', blank=True)),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u5185\u5b58\u90e8\u4ef6',
                'verbose_name_plural': '\u5185\u5b58\u90e8\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(unique=True, max_length=64, verbose_name='SN\u53f7')),
                ('manufactory', models.CharField(default=None, max_length=32, verbose_name='\u5236\u9020\u5546')),
                ('model', models.CharField(max_length=64, verbose_name='\u663e\u793a\u8bbe\u5907\u578b\u53f7')),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('asset', models.OneToOneField(to='app01.Asset')),
            ],
            options={
                'verbose_name': '\u663e\u793a\u8bbe\u5907',
                'verbose_name_plural': '\u663e\u793a\u8bbe\u5907',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(unique=True, max_length=64, verbose_name='SN\u53f7')),
                ('manufactory', models.CharField(max_length=128, null=True, verbose_name='\u5236\u9020\u5546', blank=True)),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u578b\u53f7', blank=True)),
                ('port_num', models.SmallIntegerField(verbose_name='\u7aef\u53e3\u4e2a\u6570')),
                ('device_detail', models.TextField(verbose_name='\u8bbe\u7f6e\u8be6\u7ec6\u914d\u7f6e')),
                ('asset', models.OneToOneField(to='app01.Asset')),
            ],
            options={
                'verbose_name': '\u7f51\u7edc\u8bbe\u5907',
                'verbose_name_plural': '\u7f51\u7edc\u8bbe\u5907',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u63d2\u53e3', blank=True)),
                ('sn', models.CharField(max_length=128, verbose_name='SN\u53f7', blank=True)),
                ('parent_sn', models.CharField(max_length=128, blank=True)),
                ('model', models.CharField(max_length=128, verbose_name='\u7f51\u5361\u578b\u53f7', blank=True)),
                ('manufactory', models.CharField(max_length=32, verbose_name='\u5236\u9020\u5546', blank=True)),
                ('ipaddr', models.IPAddressField(verbose_name='ip\u5730\u5740', blank=True)),
                ('mac', models.CharField(max_length=64, verbose_name='\u7f51\u5361mac\u5730\u5740')),
                ('netmask', models.CharField(max_length=64, blank=True)),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u7f51\u5361\u90e8\u4ef6',
                'verbose_name_plural': '\u7f51\u5361\u90e8\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u4ea7\u54c1\u578b\u53f7')),
                ('version', models.CharField(max_length=64, verbose_name='\u4ea7\u54c1\u7248\u672c\u53f7', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RaidAdaptor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, verbose_name='SN\u53f7', blank=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u63d2\u53e3', blank=True)),
                ('parent_sn', models.CharField(max_length=128, blank=True)),
                ('model', models.CharField(max_length=64, verbose_name='\u578b\u53f7', blank=True)),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_by', models.CharField(default=b'auto', max_length=32)),
                ('sn', models.CharField(max_length=64, verbose_name='SN\u53f7')),
                ('manufactory', models.CharField(max_length=128, null=True, verbose_name='\u5236\u9020\u5546', blank=True)),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u578b\u53f7', blank=True)),
                ('cpu_count', models.SmallIntegerField(verbose_name='cpu\u4e2a\u6570', blank=True)),
                ('cpu_core_count', models.SmallIntegerField(verbose_name='cpu\u6838\u6570', blank=True)),
                ('raid_type', models.TextField(verbose_name='raid\u7c7b\u578b', blank=True)),
                ('ram_size', models.IntegerField(verbose_name='\u5185\u5b58\u603b\u5927\u5c0fGB', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
                ('asset', models.OneToOneField(to='app01.Asset')),
                ('cpu_model', models.ForeignKey(to='app01.CPU')),
                ('nic', models.ManyToManyField(to='app01.NIC', verbose_name='\u7f51\u5361\u5217\u8868')),
                ('physical_disk_driver', models.ManyToManyField(to='app01.Disk', verbose_name='\u786c\u76d8', blank=True)),
                ('raid_adaptor', models.ManyToManyField(to='app01.RaidAdaptor', verbose_name='Raid\u5361', blank=True)),
                ('ram', models.ManyToManyField(to='app01.Memory', verbose_name='\u5185\u5b58\u914d\u7f6e', blank=True)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668',
                'verbose_name_plural': '\u670d\u52a1\u5668',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('types', models.SmallIntegerField(help_text='eg. GNU/Linux', max_length=64, verbose_name='\u7cfb\u7edf\u7c7b\u578b', choices=[(1, b'GNU/Linux'), (2, b'MS/Windows'), (3, b'Network Firmware'), (4, b'Softwares')])),
                ('version', models.CharField(help_text='eg. CentOS release 6.5 (Final)', unique=True, max_length=64, verbose_name='\u8f6f\u4ef6/\u7cfb\u7edf\u7248\u672c')),
            ],
            options={
                'verbose_name': '\u8f6f\u4ef6/\u7cfb\u7edf',
                'verbose_name_plural': '\u8f6f\u4ef6/\u7cfb\u7edf',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u540d\u5b57')),
                ('token', models.CharField(max_length=128, verbose_name='token')),
                ('department', models.CharField(max_length=32, verbose_name='\u90e8\u95e8')),
                ('email', models.EmailField(max_length=75, verbose_name='\u90ae\u7bb1')),
                ('phone', models.CharField(max_length=32, verbose_name='\u5ea7\u673a')),
                ('mobile', models.CharField(max_length=32, verbose_name='\u624b\u673a')),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('backup_name', models.ForeignKey(related_name='user_backup_name', verbose_name='\u5907\u7528\u8054\u7cfb\u4eba', blank=True, to='app01.UserProfile', null=True)),
                ('business_unit', models.ManyToManyField(to='app01.BusinessUnit')),
                ('leader', models.ForeignKey(verbose_name=b'\xe4\xb8\x8a\xe7\xba\xa7\xe9\xa2\x86\xe5\xaf\xbc', blank=True, to='app01.UserProfile', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u4fe1\u606f',
                'verbose_name_plural': '\u7528\u6237\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='server',
            name='software',
            field=models.ManyToManyField(to='app01.Software', null=True, verbose_name='\u8f6f\u4ef6', blank=True),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='server',
            index_together=set([('sn', 'asset')]),
        ),
        migrations.AlterUniqueTogether(
            name='raidadaptor',
            unique_together=set([('parent_sn', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together=set([('name', 'mac')]),
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='firmware',
            field=models.ForeignKey(to='app01.Software'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='memory',
            unique_together=set([('parent_sn', 'slot')]),
        ),
        migrations.AddField(
            model_name='maintainence',
            name='applicant',
            field=models.ForeignKey(related_name='applicant_user', verbose_name='\u53d1\u8d77\u4eba', to='app01.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maintainence',
            name='performer',
            field=models.ForeignKey(verbose_name='\u6267\u884c\u4eba', to='app01.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('parent_sn', 'slot')]),
        ),
        migrations.AddField(
            model_name='configuration',
            name='os',
            field=models.ForeignKey(verbose_name=b'OS', blank=True, to='app01.Software', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='configuration',
            name='primary_ip',
            field=models.ManyToManyField(to='app01.NIC', verbose_name='\u7f51\u5361\u5217\u8868', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='admin',
            field=models.ForeignKey(related_name='+', verbose_name='\u8bbe\u5907\u7ba1\u7406\u5458', blank=True, to='app01.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(verbose_name='\u5c5e\u4e8e\u7684\u4e1a\u52a1\u7ebf', blank=True, to='app01.BusinessUnit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='client',
            field=models.ForeignKey(verbose_name='\u4e1a\u52a1\u4f7f\u7528\u65b9', blank=True, to='app01.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ForeignKey(verbose_name='\u5408\u540c', blank=True, to='app01.Contract', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(verbose_name='IDC\u673a\u623f', blank=True, to='app01.IDC', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apiauth',
            name='users',
            field=models.ManyToManyField(to='app01.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='apiauth',
            unique_together=set([('url', 'method_type')]),
        ),
    ]
