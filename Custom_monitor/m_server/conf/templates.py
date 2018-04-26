#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from services import linux

class BaseTemplate:			### 定义基础监控类
	name = None	
	services = None
	hostname = None
	ip_address = None
	port = None
	os = None

class LinuxGeneralServices(BaseTemplate):	### 定义Linux监控类。继承基础类
	name = 'Linux General Services'
	services = {
		'cpu': linux.cpu(),
		'memory': linux.memory(),
		'load': linux.load(),
	}

class WindowsGeneralServices(BaseTemplate):	### 定义windows监控类。继承基础类
        name = 'Windows General Services'
	#hosts = ['localhost','www.baidu.com']
        services = {
                'cpu': linux.cpu(),
                'memory': linux.memory(),
                'load': linux.load(),
        }

