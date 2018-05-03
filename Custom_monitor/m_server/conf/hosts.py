#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import templates


###for host qiufei_host1
### 首先调用templates的LinuxGeneralServices类,LinuxGeneralServices类中调用了linux的cpu,memory,load类,cpu,memory,load类调用了generic中的DefaultService基类
h1 = templates.LinuxGeneralServices()		###主机实例化
h1.hostname = 'qiufei_server1'
h1.ip_address = '192.168.1.71'
h1.port = 22612
h1.os = 'Ubuntu 12.04'
h1.services['cpu'].triggers['iowait'][1] = 80
h1.services['cpu'].triggers['steal'] = [int,70,75]


###for host qiufei_host2
h2 = templates.LinuxGeneralServices()   ###主机实例化
h2.hostname = 'qiufei_server2'
h2.ip_address = '192.168.1.74'
h2.port = 22612
h2.os = 'Centos6.5'
h2.services['load'].interval = 30


###for host qiufei_host3
h3 = templates.LinuxGeneralServices()   ###主机实例化
h3.hostname = 'qiufei_server3'
h3.ip_address = '192.168.1.19'
h3.port = 22
h3.os = 'Redhat'
h3.services['load'].interval = 90
del h3.services['memory']


monitored_hosts = [h1,h2,h3]	### 定义列表monitored_hosts为主机列表


### 下列为调试代码打印结果 ###
#print '************* h1 services:\n\n',h1.services
#print '************* h2 services:\n\n',h2.services
#print '************* h3 services:\n\n',h3.services
#
#print '************* h1 cpu triggers:\n\n',h1.services['cpu'].triggers['iowait']
#print '************* h2 cpu triggers:\n\n',h2.services['cpu'].triggers['iowait']
#print '************* h3 cpu triggers:\n\n',h3.services['cpu'].triggers['iowait']
#
#print '************* h1 cpu triggers:\n\n',h1.services['cpu'].triggers['steal']
#print '************* h2 cpu triggers:\n\n',h2.services['cpu'].triggers['steal']
#print '************* h3 cpu triggers:\n\n',h3.services['cpu'].triggers['steal']
#
#print '************* h1 interval:\n\n',h1.services['load'].interval
#print '************* h2 interval:\n\n',h2.services['load'].interval
#print '************* h3 interval:\n\n',h3.services['load'].interval
