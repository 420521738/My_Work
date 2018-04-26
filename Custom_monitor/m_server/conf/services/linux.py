#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from generic import DefaultService

class cpu(DefaultService):	### 定义cpu类，继承基础服务类generic里的DefaultService
	name = 'cpu'
	interval = 60
	plugin_name = 'cpu_info'
	triggers = {
		'iowait': ['percentage',5.5,90],
		'system': ['percentage',5,90],
		'idel': ['percentage',20,10],
		'user': ['percentage',80,90],
		'steal': ['percentage',80,90],
		'nice': [None,80,90],
	}

	lt_operrator = []

class memory(DefaultService):	### 定义memory类，继承基础服务类generic里的DefaultService
        name = 'memory'
        plugin_name = 'mem_info'
        triggers = {
                'SwapUsage_p': ['percentage',66,91],
                'MemUsage_p': ['percentage',68,92],
                'MemUsage': [None,60,65],
        }

class load(DefaultService):	### 定义load类，继承基础服务类generic里的DefaultService
        name = 'load'
        interval = 120
        plugin_name = 'load_info'
        triggers = {
                'load1': [int,4,9],
                'load5': [int,3,7],
                'load15': [int,3,9],
        }

