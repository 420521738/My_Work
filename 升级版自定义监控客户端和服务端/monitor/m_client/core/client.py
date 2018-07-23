#!/usr/bin/env python 
import threading
import global_setting
import json
import time,sys
import plugin_api
import redis_connector as redis
hostname = 'alex_server'
monitor_chan = 'fm_103'

def pull_config_from_redis():
    config_data = redis.r.get("configuration::%s" % hostname)
    if config_data is not None:
        config_data = json.loads(config_data)
    else:
        sys.exit('Error: could not found any configuration data on monitor server!')
    return config_data

def run(service_config):
    service_name, interval, plugin_name = service_config
    plugin_func = getattr(plugin_api,plugin_name)
    res = plugin_func()
    
    service_data = {'hostname':hostname, 
                    'service_name':service_name,
                    'data': res}
    
    redis.r.publish(monitor_chan, json.dumps(service_data))
    
    print res
    return res
    
host_config = pull_config_from_redis()
print host_config
#for k,v in host_config.items():
#    t = threading.Thread(target=run, args=((k,v[0], v[1]), ))
#    t.start()
while True:
    for service_name,v in host_config.items():
        interval,plugin_name,last_run = v
        if (time.time() - last_run ) >= interval: #time to run monitor
            t = threading.Thread(target=run, args=((service_name,interval,plugin_name), ))
            t.start()
            #update time stamp
            host_config[service_name][2] = time.time()
        else:
            next_run_time = interval - (time.time() - last_run )
            print "\033[32;1mSerivce %s will run in next %ss..\033[0m" %(service_name, next_run_time  )
            
    time.sleep(1)
    
    
    