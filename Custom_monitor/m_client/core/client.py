#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import threading
import global_setting
import json
import time
import sys
import plugin_api
import redis_connector as redis

hostname = 'qiufei_server1'		### 设定主机名，主机名唯一，每台主机都不一样的
monitor_chan = 'fm_103'			### 定义redis发布订阅消息的频道，和服务端的对应

def pull_config_from_redis():		### 定义从redis中获取对应主机名的监控配置信息方法
	config_data = redis.r.get('configuration::%s' % hostname)
	if config_data is not None:
		config_data = json.loads(config_data)
	else:
		sys.exit('Error: Could not found any configuration data on monitor server!')
	return config_data

def run(service_config):		### 运行获取到的主机监控配置信息
	service_name, interval, plugin_name = service_config
	plugin_func = getattr(plugin_api,plugin_name)
	res = plugin_func()
	service_data = {'hostname':hostname,
			'service_name':service_name,
			'data':res}
	redis.r.publish(monitor_chan,json.dumps(service_data))	###使用redis发布订阅消息，频道是monitor_chan，消息是json格式化后的service_data	

	print res
	return res

host_config = pull_config_from_redis()	### 执行pull_config_from_redis方法，获取到的就是对应主机名的监控配置信息
#print host_config


#for k,v in host_config.items():
#	t = threading.Thread(target=run, args=((k,v[0],v[1]),))
#	t.start()


while True:
	for service_name,v in host_config.items():
		interval, plugin_name, last_run = v		### 服务端就是按监控间隔、插件名、上次运行时间发送过来的
		if (time.time() - last_run) >= interval:	### 当前时间减去上次执行时间大于等于监控间隔就可以执行监控任务
			t = threading.Thread(target=run, args=((service_name,interval,plugin_name),))
			t.start()
			host_config[service_name][2] = time.time()	### 执行完监控任务后，更新当前时间戳
		else:
			next_run_time = interval - (time.time() - last_run)
			print "\033[32;1m%s service will run in %ss later...\033[0m" % (service_name,next_run_time)
	time.sleep(1)



