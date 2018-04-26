#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import global_setting			### 导入global_setting模块，设定代码执行家目录
from plugins import cpu,load,memory	### 从plugins中导入cpu，load，memory模块，其实就是数据采集脚本

def cpu_info():				### 定义获取cpu信息的模块
	data = cpu.monitor()
	#print data
	return data
cpu_info()

def load_info():			### 定义获取系统负载信息的模块
	data = load.monitor()
	#print data
	return data
load_info()

def mem_info():				### 定义获取系统内存信息的模块
	data = memory.monitor()
	#print data
	return data
mem_info()
