import urllib2
import json
import threading 

params = {'get_configuration': '/api/configuration/1/?format=json',
          'get_asset_id': '/api/asset/'
          }

class server_conn(object):
    
    def __init__(self,host,port=None):
        self.host = host 
        self.port = port
        self.configurations = None
        self.monitor_dic = {} #store configuration data 
    def get_assetid(self):
        pass
    
    def request(self,url):
        if self.port is not None:
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
                                                 'plugin':i['service']['plugin']   }
    
        return True        
    def handle(self,parameters):
        
        #step 1 , get config data from server fisrt 
        data = self.request(parameters['get_configuration'])
        if self.convert_config_data(data): #valid configuration data
            print '----going to monitor services-----'
           
class  monitor(object):
    pass 
if __name__=='__main__':
    cli_sock = server_conn('10.168.66.29')
    request = cli_sock.handle(params)
    #print request 
   
    