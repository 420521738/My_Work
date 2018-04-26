#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import global_setting		### 导入环境变量模块，设定当前家目录为/root/py_training/day7/monitor/m_server/,根据自己的代码目录可以修改该模块
from conf import hosts		### 导入当前代码家目录下的conf下的hosts模块
import redis_connector as redis	### 导入redis连接模块
import json			### 导入json模块,后续收消息需要使用json格式


def push_configure_data_to_redis():	### 定义将客户端配置推送到redis的模块
	for h in hosts.monitored_hosts:	### monitored_hosts为hosts模块中定义好的主机列表
		config_dic = {}
		for k,v in h.services.items():	### h.services.items在hosts模块除模块大部分内容外，已经被自定义了
			config_dic[k] = [v.interval,v.plugin_name,0]	### 0代表第一次的时间戳
		print config_dic	### config_dic是每台客户端的自定义后的监控间隔、插件名、时间戳的字典

		redis.r['configuration::%s' %h.hostname] = json.dumps(config_dic) ### 将configuration::主机名这样格式key值，与其对应的config_dic字典json化后存入redis

push_configure_data_to_redis()

channel = 'fm_103'		### 定义redis的订阅频道，用于接收客户端发过来的消息

msg_queue = redis.r.pubsub()	###绑定监听实例
msg_queue.subscribe(channel)

msg_queue.parse_response()	###监听客户端发过来的消息

count = 0

while True:
	data = msg_queue.parse_response()	###持续监听客户端发过来的消息
	print 'round %s ::' % count,json.loads(data[2])
	count +=1

