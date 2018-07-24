#_*_coding:utf8_*_
import global_setting
import urllib2,urllib
import json
import threading 
import time,sys
import plugin_api
import md5 
params = {'get_configuration': '/api/configuration/1/?format=json',
          'post_monitor_data': '/api/monitor_data/',
          'get_asset_id': '/api/asset/',
          'config_md5': None,
          'server': '10.168.66.29',
          'port':80,
          }

          
          
          
class server_conn(object):
    
    def __init__(self,host,port=None):
        self.host = host 
        self.port = port
        self.configurations = None
        print '==========',self.port 
        self.monitor_dic = {} #store configuration data 
    def get_assetid(self):
        pass
    
    
    def request(self,url):
        if self.port !=80:
            url_str = "http://%s:%s%s" %(self.host,self.port,url)
            
        else:
            url_str = "http://%s%s" %(self.host,url)    
        print url_str
        req = urllib2.urlopen(url_str)
        result = req.read()
        return result 
         
    def convert_config_data(self,data):     
        configs= json.loads(data) 
        monitor_list = [] 
        
        if type(configs) is dict:
            self.asset_id = configs['id']
            
            if configs.get('status_monitor_on') is True:
                for template in configs.get('template_list'):
                    monitor_list +=template['service_list']
                    
            else:
                print 'status_monitor_on field is disabled on server, will not monitor this host'
            
        else:
            print 'the configuration got from server is invaild...'
    
        for i in monitor_list:
            self.monitor_dic[i['service']['name']] = { 
                                                 'check_interval': i['check_interval'],
                                                 'plugin':i['service']['plugin']  ,
                                                 'last_run': 0,
                                                 }
        

        return True        
    def handle(self,parameters):
        
        #step 1 , get config data from server fisrt 
        data = self.request(parameters['get_configuration'])
        if self.convert_config_data(data): #valid configuration data
            print '----going to monitor services-----'
            print self.monitor_dic
            params['config_md5'] = md5.md5(json.dumps(self.monitor_dic)).hexdigest() #缁欓厤缃俊鎭敓鎴恗d5鍊�
            
            m = monitor(self.monitor_dic,self.asset_id, parameters)
            m.run_forever()
            
class  monitor(object):
    def __init__(self, monitor_list,asset_id, get_config_params):
        self.monitor_list = monitor_list
        self.asset_id = asset_id
    def run_plugin(self,service_name,monitor_item,lock_obj):
        lock_obj.acquire()
        self.monitor_list[service_name]['last_run'] = time.time()
        lock_obj.release()
        plugin_func = getattr(plugin_api,monitor_item['plugin'])
        service_status=  plugin_func()
        
        service_status['time_stamp'] = time.time()
        #report to server 
        report_data = {'client_data':service_status }
        
        self.post_data(report_data)
        print '\033[44;1m------going to send:: %s-----\033[0m' % service_name,report_data
        
        
        
    def run_forever(self):
        stop_event = False
        lock = threading.RLock() 
        update_counter = 0
        while not stop_event:
            
            for service_name,items in self.monitor_list.items(): #寰幆鐩戞帶鍒楄〃 
                if (time.time() - items['last_run']) > items['check_interval']: 
                    t = threading.Thread(target=self.run_plugin, args=(service_name, items,lock ))
                    t.start()
                    print '=======>cur thread...' ,t.ident
                else:
                    next_run = items['check_interval'] -  (time.time() - items['last_run'])
                    print '\033[32;1m------run:%s  next time:%s------\033[0m' %(service_name,next_run )
            time.sleep(3)
            update_counter +=1
            if update_counter > 3: #update config data each 300secs
                self.update_moniotr_list()
                update_counter = 0
                    
        
    def update_moniotr_list(self):
        cli_sock = server_conn(params['server'],params['port'])
        request_data = cli_sock.request(params['get_configuration'])      
        if cli_sock.convert_config_data(request_data):
            #print 'old:',params['config_md5'] 
            new_config_md5 = md5.md5(json.dumps(cli_sock.monitor_dic)).hexdigest()
            #print 'new:', new_config_md5
            if params['config_md5'] != new_config_md5:
                self.monitor_list =cli_sock.monitor_dic
                print '--=-config updated----- \033[31;1m%s\033[0m' % self.monitor_list
                params['config_md5'] = new_config_md5 #瀛樹笂鏂扮殑閰嶇疆淇℃伅
                return True
        else:
            return False
    
    def post_data(self,service_data):
        url_path = params['post_monitor_data'] 
        host = params['server']
        port = params['port']    
        if port != 80:
            url_str = "http://%s:%s%s" %(host,port,url_path)
            
        else:
            url_str = "http://%s%s" %(host,url_path)    
        #print url_str
        data = urllib.urlencode(service_data)
        req = urllib2.urlopen(url_str,data)
        result = req.read()
        print '\033[41;1m---%s---\033[0m' %result 
        return result         
        
if __name__=='__main__':
    cli_sock = server_conn(params['server'],params['port'] )
    request = cli_sock.handle(params)
    #print request 
   
    