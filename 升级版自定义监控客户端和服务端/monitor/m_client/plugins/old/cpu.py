#!/usr/bin/env python
#-*-coding:utf-8-*-
import commands
import wmi

def monitor():
    c=wmi.WMI()
    cpu_dic={}
    #cpu used
    cpu_list=[]
    for cpu in c.Win32_Processor():
	tmp_dic={}
	tmp_dic['cpu_id']=cpu.DeviceID #cpu id
	tmp_dic['cpu_name']=cpu.Name.strip() 
	tmp_dic['NumberOfCores']=cpu.NumberOfCores
        tmp_dic['NumberOfLogicalProcessors']=cpu.NumberOfLogicalProcessors
        tmp_dic['DataWidth']=cpu.DataWidth
        cpu_list.append(tmp_dic)            
	#cpu_dic[cpu.DeviceID]=tmp_dic		
        #cs=c.Win32_ComputerSystem()#用于获取计算机CPU数量,内存大小,主板相关信息
    cpu_dic['cpu_basicinfo']=cpu_list
    return cpu_dic
'''		
    shell_command = 'sar 1 3| grep "^Average:"'
    status,result = commands.getstatusoutput(shell_command)
    if status != 0:
	value_dic = {'status': status}
    else:
	user,nice,system,iowait,steal,idle = result.split()[2:]
	value_dic = {
	    'user': user,
	    'nice': nice,
	    'system': system,
	    'iowait': iowait,
	    'steal': steal,
	    'idle': idle,
	    'status': status
	}
    return value_dic
'''
if __name__ == '__main__':
	print monitor()
