#!/usr/bin/env python
import commands
import wmi

def monitor():
    c=wmi.WMI()
	#get meminfo
    mem_dic={}
    mem_list=[]
    for mem in c.Win32_PhysicalMemory():
        tmp_dic={}
        tmp_dic['Caption']=mem.Caption
        tmp_dic['Manufacturer']=mem.Manufacturer
        tmp_dic['PartNumber']=mem.PartNumber
        tmp_dic['SerialNumber']=mem.SerialNumber
        tmp_dic['Tag']=mem.Tag
        tmp_dic['Capacity']=str(long(mem.Capacity) / (1024*1024*1024)) + " GB"
        mem_list.append(tmp_dic)
	
    mem_dic['mem_basicinfo']=mem_list
    return mem_dic
'''
    monitor_dic = {
	    'SwapUsage': 'percentage',
	     'MemUsage'  : 'percentage',
    }
    shell_command ="grep 'MemTotal\|MemFree\|Buffers\|^Cached\|SwapTotal\|SwapFree' /proc/meminfo"
    
    status,result = commands.getstatusoutput(shell_command)
    if status != 0: #cmd exec error
	    value_dic = {'status':status}
    else:
	    value_dic = {'status':status}
	    for i in result.split('kB\n'):
		    key= i.split()[0].strip(':') # factor name
		    value = i.split()[1]   # factor value
		    value_dic[ key] =  value
    
	    if monitor_dic['SwapUsage'] == 'percentage':
		    value_dic['SwapUsage_p'] = 100 - int(value_dic['SwapFree']) * 100 / int(value_dic['SwapTotal'])	
	    #real SwapUsage value
	    value_dic['SwapUsage'] = int(value_dic['SwapTotal']) - int(value_dic['SwapFree'])
    
	    MemUsage = int(value_dic['MemTotal']) - (int(value_dic['MemFree']) + int(value_dic['Buffers'])  + int(value_dic['Cached']))
	    if monitor_dic['MemUsage'] == 'percentage':
		    value_dic['MemUsage_p'] = int(MemUsage) * 100 / int(value_dic['MemTotal'])
	    #real MemUsage value	
	    value_dic['MemUsage'] = MemUsage 
    return value_dic
     

    
	
	
if __name__ == '__main__':
	print monitor()
'''