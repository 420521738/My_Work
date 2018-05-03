#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from generic import DefaultService

class cpu(DefaultService):			### 定义cpu类，继承基础服务类generic里的DefaultService
	def __init__(self):                     ### 创建构造函数，目的在于使里面的东西独>立，也就是deepcopy
		self.name = 'cpu'
		self.interval = 60
		### 定义阈值
		self.threshold_cross_times = 4
		self.plugin_name = 'cpu_info'
		self.triggers = {
			'iowait': ['percentage',5.5,90],
			'system': ['percentage',5,90],
			'idle': ['percentage',20,10],
			'user': ['percentage',80,90],
			'steal': ['percentage',80,90],
			'nice': [None,80,90],
		}
		### 如果你要修改triggers的key，必须修改下列相应的key，用于存放相应时间内相应指标N次内的数值，用于监控报警判断
                self.temp_data = {
                        'iowait': {'last_item_saving': 0, 'status_data': []},
                        'system': {'last_item_saving': 0, 'status_data': []},
                        'idle': {'last_item_saving': 0, 'status_data': []},
                        'user': {'last_item_saving': 0, 'status_data': []},
                        'steal': {'last_item_saving': 0, 'status_data': []},
                        'nice': {'last_item_saving': 0, 'status_data': []},
                }

	
		self.lt_operrator = ['idle','nice']	### 进行小于运算

class memory(DefaultService):			### 定义memory类，继承基础服务类generic里的DefaultService
	def __init__(self):                     ### 创建构造函数，目的在于使里面的东西独立，也就是deepcopy
	        self.name = 'memory'
		self.interval = 15
		self.threshold_cross_times = 3	
	        self.plugin_name = 'mem_info'
	        self.triggers = {
	                'SwapUsage_p': ['percentage',66,91],
	                'MemUsage_p': ['percentage',7,10],
	                #'MemUsage': [None,60,65],
	        }
		### 如果你要修改triggers的key，必须修改下列相应的key，用于存放相应时间内相应指标N次内的数值，用于监控报警判断
                self.temp_data = {
                        'SwapUsage_p': {'last_item_saving': 0, 'status_data': []},
                        'MemUsage_p': {'last_item_saving': 0, 'status_data': []},
                        #'MemUsage': {'time':None, 'status_data': []},
                }


class load(DefaultService):			### 定义load类，继承基础服务类generic里的DefaultService
	def __init__(self):                     ### 创建构造函数，目的在于使里面的东西独>立，也就是deepcopy
	        self.name = 'load'
	        self.interval = 120
		self.threshold_cross_times = 5
	        self.plugin_name = 'load_info'
	        self.triggers = {
	                'load1': [int,4,9],
	                'load5': [int,3,7],
	                'load15': [int,3,9],
	        }
		### 如果你要修改triggers的key，必须修改下列相应的key，用于存放相应时间内相应指标N次内的数值，用于监控报警判断
                self.temp_data = {
                        'load1': {'last_item_saving': 0, 'status_data': []},
                        'load5': {'last_item_saving': 0, 'status_data': []},
                        'load15': {'last_item_saving': 0, 'status_data': []},
                }
