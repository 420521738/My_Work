#_*_coding:utf8_*_
import global_setting
import urllib2,urllib
import json
import threading 
import time,sys,datetime
import plugin_api
import md5 
import parms_conf
import commands



global_setting.base_dir 


def url_request(url,host,port=80):
    if port !=80:
        url_str = "http://%s:%s%s" %(host,port,url)
        
    else:
        url_str = "http://%s%s" %(host,url)    
    print url_str
    req = urllib2.urlopen(url_str)
    result = req.read()
    
    return result 


def post_data(url,host,port,post_data):
  
    if port != 80:
        url_str = "http://%s:%s%s" %(host,port,url)
        
    else:
        url_str = "http://%s%s" %(host,url)    
    #print url_str
    data = urllib.urlencode(post_data)
    req = urllib2.urlopen(url_str,data)
    result = req.read()
    print '\033[41;1m---%s---\033[0m' %result 
    return result         
        

class server_conn(object):
    def __init__(self,config_parms):
        self.config_parms = config_parms
        self.host_profile = None
        #self.last_task_id = None
        self.task_dic = {}
    def get_profile(self):
        host = self.config_parms['server']
        port = self.config_parms['port']
        url = self.config_parms['get_host_profile']
        host_profile = url_request(url, host, port)
        print host_profile
        try:
            profile_to_dic = json.loads(host_profile)
            if isinstance(profile_to_dic, dict):
                self.host_profile = profile_to_dic
        except Exception,e:
            print 'Could not get host profile',e
    def update_profile(self):
        pass 
    def get_new_tasks(self):
        host = self.config_parms['server']
        port = self.config_parms['port']
        url_raw = self.config_parms['new_tasks']
        if self.get_last_run_task_id() is True:
            
            url = '%s/%s/?format=json' %(url_raw,self.last_task_id)
            #print '====>',url 
            new_tasks = url_request(url, host, port)
            print '---new tasks---> \033[32;1m%s\033[0m' % new_tasks
            new_tasks = json.loads(new_tasks)
            #print 'last_task:',new_tasks
            assert type(new_tasks) == list #raise error if the tasks format is invalid
            return new_tasks 
        else:
            return False        
    def get_last_run_task_id(self):
        last_task_id_file = '%s/%s' %(global_setting.base_dir, self.config_parms['last_task_id'])
        f = file(last_task_id_file, 'rb')
        last_id_raw = f.read()
        
        self.last_task_id = int(last_id_raw)
        f.close()
        return True
    def update_last_task_id(self,new_id):
        last_task_id_file = '%s/%s' %(global_setting.base_dir, self.config_parms['last_task_id'])
        f = file(last_task_id_file, 'wb')
        f.write(str(new_id))
        f.close()
        #self.last_task_id = new_id 
        return True
    def handle(self):

        last_pull_time = 0
        first_run_flag = 1 #when start the program ,it will run the task first 
        poll_interval = 0 #default value ,to make sure the pull task action will run in the fisrt while loop
        while True:
            if time.time() - last_pull_time  > poll_interval: #pull profile updates
                reach_interval_flag = 1
            else:
                reach_interval_flag = 0
            
            if first_run_flag == 1 or reach_interval_flag ==1:
                self.get_profile()
                assert type(self.host_profile) == dict 
                last_pull_time = time.time()
                print '+++host profile-->',self.host_profile
                has_new_task =self.get_new_tasks()
                if has_new_task: # 
                    if self.parse_tasks(has_new_task) is True:
                        
                        #save in the latest task id into disk ,otherwise program will re-get these tasks again 
                        latest_task_id = has_new_task[-1]['id']
                        self.update_last_task_id(latest_task_id)
                first_run_flag = 0 #avoid the loop always run the task 
                poll_interval = self.host_profile['poll_interval']
                print '\033[31;1m %s \033[0m ' %self.task_dic 
            #check if the task needs to kick off each 1sec
            for task_id,task in self.task_dic.items():
                if task['kick_off_at'] is not None:
                    datetime_format = datetime.datetime.strptime( task['kick_off_at'],"%Y-%m-%dT%H:%M:%S").timetuple() #format:'2015-01-21T08:11:49Z'
                    unix_time = time.mktime(datetime_format)
                    print '======>local time:' , datetime_format
                    if time.time() > unix_time:
                        
                        task_kick_off_flag = True
                    else:
                        print 'will run task later ...'
                        task_kick_off_flag = False
                else:
                    task_kick_off_flag = True
                               
                #print task
                if task_kick_off_flag is True:
                    print 'Going to run this task....' 
                    self.run(task)

            next_run = self.host_profile['poll_interval'] - (time.time() -last_pull_time)
            print 'Next round...',next_run
            

            time.sleep(1)
    def run(self,task):
        func = getattr(self, task['task_type']) 
        result = func(task) 
        
        del self.task_dic[task['id']] # task is done,no matter success or failure , it's done, so remove it from the task list 
        
        #send the result back to server 
        if result[0] ==0:
            run_status = 'success'
        else:
            run_status = 'failed'
        res_dic = {'status':run_status,
                   'run_log': result[1],
                   'host_profile': json.dumps(self.host_profile),
                   'task': json.dumps(task)}
        post_data(self.config_parms['report_result'], 
                  self.config_parms['server'],
                  self.config_parms['port'], 
                  res_dic)
        
    def cmd(self,task):
        print 'Run comd...........',task
        res = commands.getstatusoutput(task['content'])
        
        return res
    def parse_tasks(self, new_tasks):
        print '---------parsing new tasks--------' #,new_tasks
        for task in new_tasks:
            
            if self.host_profile['id'] in task['hosts']:
                take_this_task = True
            elif set(self.host_profile['group']) &  set(task['groups']): 
                take_this_task = True
            else:
                take_this_task = False
            if take_this_task:
                self.task_dic[task['id']] = task
        return True 
    
if __name__ == '__main__':
    server = server_conn(parms_conf.params)
    server.handle()
        