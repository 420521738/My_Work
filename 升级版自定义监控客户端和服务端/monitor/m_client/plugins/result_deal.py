#-*- coding:utf-8 -*-

#from scripts import cpu,memory,sys_Info,disk,netinfo
import time#md5,
from hashlib import md5
#import recv
import filecmp
import os,json
cur_dir=os.path.dirname(os.path.realpath(__file__))

monitor_dic={}
frist_date_flag=1
file_md5_old=0
file_md5_new=0

def generate_file_md5value(filename):
    '''以文件路径作为参数，返回对文件md5后的值
    '''
    if os.path.isfile(filename):
        m=md5()
        with open(filename,'rb') as f:
            m.update(f.read())
        return m.hexdigest()
    else:
        return None
        
def generate_file(filename,data):
    f=file(filename,'w+')
    f.write(json.dumps(data))
    f.close()

def read_file(filename):
    f = open(filename)
    context = f.read() 
    f.close()
    #print context
    return context

#print type(read_file('../recv/assets45.json'))   
'''
def get_monitor_data():
    tmp_dic={}
    tmp_dic['cpu']=cpu.monitor()
    tmp_dic['mem']=memory.monitor()
    tmp_dic['disk']=disk.monitor()
    tmp_dic['sys_info']=sys_Info.monitor()
    tmp_dic['net_info']=netinfo.monitor()
    return tmp_dic
'''
#找出client向proxy代理中发送改变的监控信息
def get_monitor_data_change(monitor_dic,monitor_new_dic):
    data_change_dic={}
    for k in monitor_new_dic.keys():
        tmp={}
        if monitor_dic.has_key(k):
            if monitor_dic[k] != monitor_new_dic[k]:
                data_change_dic[k]=monitor_new_dic[k]
            else:
                pass
            '''        
            if k == 'hostname':
                pass
            else:
                
                for t in monitor_new_dic[k].keys():
                    if monitor_dic[k].has_key(t):
                        if monitor_dic[k][t] != monitor_new_dic[k][t]:
                            data_change_dic[k][t]=monitor_new_dic[k][t]
                    else:
                        data_change_dic[k][t]=monitor_new_dic[k][t]
            '''
        else:
            data_change_dic[k]=monitor_new_dic[k]
    '''
    for k in monitor_dic.keys():
        for t in monitor_dir[k].keys():
            #不能这样比较monitor_new_dic中不一定有这些keys
            if monitor_dir[k][t] != monitor_new_dic[k][t]:
                data_change_dic[k][t]=monitor_new_dic[k][t]
    '''
    return data_change_dic

def deal_monitor_data_change(client_ip,trunk_monitor_dic,data_change_dic):
    for k in data_change_dic.keys():
        for t in data_change_dic[k].keys():
            trunk_monitor_dic[client_ip][k][t] = data_change_dic[k][t]
    #处理一个大的字典，然后发送给server端，这里通过增加ip,
    #到server端中增加所属的trunk_server,编程一个更大的字典。
    return trunk_monitor_dic
#proxy代理向server端发送监控信息。
#sender.py中使用。
def send_monitor_data():
    client_ip_list=[]
    for ip in client_ip_list:
        #get ip belongs_to trunk_server
        get_monitor_data_change(ip,trunk_monitor_dic,data_change_dic)
    #server_monitor_dic={'trunk_server':'','ip':'','monitor_services':{}}
    #trunk_monitor_dic={'ip':'','monitor_services':{}}
    #monitor_dic=
    print 'send data'
    
def main():
    #如果是第一次获取信息
    i=4
    global frist_date_flag
    while i:       
        if frist_date_flag:
            monitor_dic=get_monitor_data()
            generate_file(cur_dir+'/recv/assets_tmp.log',monitor_dic)
            file_md5_old=generate_file_md5value('recv/assets_tmp.log')
            frist_date_flag=0
        else:
            monitor_new_dic=get_monitor_data()
            generate_file(cur_dir+'/recv/assets_tmp1.log',monitor_new_dic)
            file_md5_new=generate_file_md5value('recv/assets_tmp1.log')
            #比较文件md5值是否相同,在第二次才开始比较
            #filecmp.cmp(r'e:\1.txt',r'e:\2.txt') 
            if file_md5_old == file_md5_new:
                print 'send message no change'
            else:
                #data_assets_change=get_monitor_data_change('recv/assets_tmp.log','recv/assets_tmp1.log')
                data_assets_change=get_monitor_data_change(monitor_dic,monitor_new_dic)
                generate_file(cur_dir+'/recv/assets_tmp.log',monitor_new_dic)
                print 'data_assets_change'
        
        time.sleep(2)
        i = i-1
    '''
    monitor_dic=get_monitor_data()
    generate_file(cur_dir+'/recv/assets_tmp.log',monitor_dic)
    read_file(cur_dir+'/recv/assets_tmp.log')    
    
    file_md5_1=generate_file_md5value('recv/1.txt')
    file_md5_2=generate_file_md5value('recv/2.txt')
    print file_md5_1==file_md5_2
    '''
if __name__=="__main__":
    #main()
    #print read_file('../recv/assets45'.json')
    pass
    
    #server_monitor_dic={'trunk_server':'','ip':'','monitor_services':{}}
    #trunk_monitor_dic={'ip':'','monitor_services':{}}
    #monitor_dic=
    #在处理监控项时，得到大字典，然后分发给不同的trunk_server端中，变成一个小的
    #处理一个大的字典，然后发送给server端，这里通过增加ip,
    #到server端中增加所属的trunk_server,编程一个更大的字典。
