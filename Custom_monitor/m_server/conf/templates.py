#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from services import linux

### 说明
### 对函数进行编写构造函数，目的在于，实例在实例化的时候能将各自的参数独立，不互相影响，使用构造函数是可以达到这个目的。

class BaseTemplate:			### 定义基础监控类
	name = None	
	services = None
	hostname = None
	ip_address = None
	port = None
	os = None

class LinuxGeneralServices(BaseTemplate):	### 定义Linux监控类。继承基础类
	def __init__(self):			### 创建构造函数，目的在于使里面的东西独立，也就是deepcopy
		self.name = 'Linux General Services'
		self.services = {
			'cpu': linux.cpu(),
			'memory': linux.memory(),
			'load': linux.load(),
		}

class WindowsGeneralServices(BaseTemplate):	### 定义windows监控类。继承基础类
	def __init__(self):			### 创建构造函数，目的在于使里面的东西独立，也就是deepcopy
	        self.name = 'Windows General Services'
	        self.services = {
	                'cpu': linux.cpu(),
	                'memory': linux.memory(),
	                'load': linux.load(),
	        }

