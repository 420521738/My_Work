#!/usr/bin/env python 
#coding:utf-8
import xml2json
import json,time
import subprocess,os.path
import wmi

def monitor():
    shell_command = 'dxdiag /x d:\hard.xml'
    status = subprocess.call(shell_command,shell=True)

    #time.sleep(5);
    if status != 0:
        value_dic = {'status':stauts}
    else:
        if os.path.exists('d:\hard.xml'):
            asset_raw_data = file('d:\hard.xml').read()
            asset_to_json = xml2json.xml2json(asset_raw_data)
            asset_to_dict = json.loads(asset_to_json)
            value_dic = {
                'asset':asset_to_dict,
                'status':status
            }
        else:
            value_dic = {'status':1}


    return value_dic

def handle_info():
    monitor_info_dic={}
    value_dic=monitor()
    c=wmi.WMI()
    
    monitor_info_dic['status']=value_dic['status']
    monitor_info_dic['data_value']={"SystemInformation":{},
                              # "LogicalDisks":value_dic['asset']['DxDiag'].get("LogicalDisks"),
                               "SystemDevices":value_dic['asset'].get('DxDiag')["SystemDevices"]}      
    
    for k in monitor_info_dic['data_value'].keys():
        if k =="SystemInformation":
            monitor_info_dic['data_value'][k]={'MachineName':value_dic['asset'].get('DxDiag')["SystemInformation"]['MachineName'],
                                          'OperatingSystem':value_dic['asset'].get('DxDiag')["SystemInformation"]['OperatingSystem'],
                                          'Language':value_dic['asset'].get('DxDiag')["SystemInformation"]['Language'],
                                          'SystemManufacturer':value_dic['asset'].get('DxDiag')["SystemInformation"]['SystemManufacturer'],
                                          'SystemModel':value_dic['asset'].get('DxDiag')["SystemInformation"]['SystemModel'],
                                          'BIOS':value_dic['asset'].get('DxDiag')["SystemInformation"]['BIOS'],
                                          'Processor':value_dic['asset'].get('DxDiag')["SystemInformation"]['Processor'],
                                          'Memory':value_dic['asset'].get('DxDiag')["SystemInformation"]['Memory']}	
        '''
        elif k =="SystemDevices":
            monitor_info_dic['data_value'][k]={value_dic['asset'].get('DxDiag')["SystemDevices"]}
                                                 
        elif monitor_info_dic.get('data_value')[k] =="LogicalDisks":
            pass
        '''	 
    #get os info such:sn
    '''
    print "系统sn号：".decode('utf-8')
    for x in c.Win32_PhysicalMedia():
        print x.SerialNumber
    '''
    os_list=[]
    for os in c.Win32_OperatingSystem():
        tmp_dic={}
        '''
        tmp_dic['Caption']=os.Caption
        tmp_dic['NumberOfUsers']=os.NumberOfUsers
        tmp_dic['Organization']=os.Organization
        tmp_dic['RegisteredUser']=os.RegisteredUser
        '''
        tmp_dic['SN']=os.SerialNumber
        #tmp_dic['Version'] = os.Version
        os_list.append(tmp_dic)
    monitor_info_dic['data_value']['OSInfo']=os_list

    #cpu used，CPU的个数、型号等
    cpu_dic={}
    for cpu in c.Win32_Processor():
        tmp_dic={}
        tmp_dic['cpu_id']=cpu.DeviceID #cpu id
        tmp_dic['cpu_name']=cpu.Name.strip()
        tmp_dic['NumberOfCores']=cpu.NumberOfCores
        tmp_dic['NumberOfLogicalProcessors']=cpu.NumberOfLogicalProcessors
        tmp_dic['DataWidth']=cpu.DataWidth	
        #device=cpu.DeviceID.lower()
        #tmp_dic[device]={'used':float(cpu.LoadPercentage), 'unit':'%'}    
        cpu_dic[cpu.DeviceID]=tmp_dic
    monitor_info_dic['data_value']['CPUInfo']=cpu_dic
    
    #get hard disk info
    #hardware.write('硬盘使用情况：')
    logical_disk_list=[]
    for disk in c.Win32_LogicalDisk (DriveType=3):
        disk_dic={}
        disk_dic['磁盘符'.decode('utf-8')]=disk.Caption
        disk_dic['Size']=str(long(disk.Size) / (1024*1024*1024)) + " GB"
        #disk_dic['Free']=100.0*long(disk.FreeSpace)/long (disk.Size)
        logical_disk_list.append(disk_dic)
    monitor_info_dic['data_value']['LogicalDiskInfo']=logical_disk_list
    
    #得到物理硬盘的信息
    physical_disk_list=[]
    for disk in c.Win32_DiskDrive():
        tmp_dic={}
        tmp_dic['Caption']=disk.Caption
        tmp_dic['InterfaceType']=disk.InterfaceType
        #tmp_dic['CreationClassName']=disk.CreationClassName
        tmp_dic['SerialNumber']=disk.SerialNumber
        if disk.Size is not None:
            tmp_dic['Size']=str(long(disk.Size) / (1024*1024*1024)) + " GB"
        else:
            tmp_dic['Size']="0 GB"#disk.Size
        physical_disk_list.append(tmp_dic)

    monitor_info_dic['data_value']['PhysicalDiskInfo']=physical_disk_list
    #get meminfo获得详细的物理内存的信息。   
    '''
    cs = c.Win32_ComputerSystem()#用于获取计算机CPU数量,内存大小,主板相关信息
    os = c.Win32_OperatingSystem()#用于获取计算机运行环境信息
    pfu = c.Win32_PageFileUsage()# 获取缓冲信息   
    mem_dic["MemTotal"] = {'volume':float(cs[0].TotalPhysicalMemory) / (1024*1024), 'unit':'MB'}
    mem_dic["MemFree"] = {'volume':float(os[0].FreePhysicalMemory)/1024, 'unit':'MB'}
    mem_dic["SwapTotal"] = {'volume':float(pfu[0].AllocatedBaseSize), 'unit':'MB'}
    mem_dic["SwapFree"] = {'volume':float(pfu[0].AllocatedBaseSize - pfu[0].CurrentUsage), 'unit':'MB'} 
    monitor_info_dic['data_value']['MemInfo']={"MemTotal":mem_dic["MemTotal"],
                                             #"MemFree":mem_dic["MemFree"],
                                             "SwapTotal":mem_dic["SwapTotal"]
                                            # "SwapFree":mem_dic["SwapFree"]
                                           } 
    ''' 
    mem_list=[]
    for mem in c.Win32_PhysicalMemory():
        mem_dic={}
        mem_dic['Caption']=mem.Caption
        mem_dic['Manufacturer']=mem.Manufacturer
        mem_dic['PartNumber']=mem.PartNumber
        mem_dic['SerialNumber']=mem.SerialNumber
        mem_dic['Tag']=mem.Tag
        mem_dic['Capacity']=str(long(mem.Capacity) / (1024*1024*1024)) + " GB"
        mem_list.append(mem_dic)

    monitor_info_dic['data_value']['MemInfo']=mem_list
     
   
    #get net info form wmi.Win32_NetworkAdapterConfiguration
    tmplist=[]
    for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):  
        tmpdict = {}  
        tmpdict["Description"] = interface.Description  
        tmpdict["IPAddress"] = interface.IPAddress[0]  
        tmpdict["IPSubnet"] = interface.IPSubnet[0]  
        tmpdict["MAC"] = interface.MACAddress 
        tmplist.append(tmpdict)
    #get tcp connect
    for interfacePerfTCP in c.Win32_PerfRawData_Tcpip_TCPv4():
        tmplist.append({"TCP Connect":str(interfacePerfTCP.ConnectionsEstablished)})
        tmpdict["TCP Connect"]=str(interfacePerfTCP.ConnectionsEstablished)
        #print '\t' + 'TCP Connect :\t' + str(interfacePerfTCP.ConnectionsEstablished) 
    monitor_info_dic['data_value']['NetInfo']=tmplist
    
    return monitor_info_dic

'''

asset_raw_data = file('hardinfor.txt').read()

asset_to_json = xml2json.xml2json(asset_raw_data)

asset_to_dict = json.loads(asset_to_json)
for k,v in asset_to_dict['DxDiag'].items():
    print '\033[42;1m--- %s----\033[0m' % k
    """
    for name,info in v.items():
        if type(info) is dict:
            for n,i in info.items():
                print n,i
        else:
            print info
    """
    if k == 'SystemDevices':
        for n,i in v.items():	
            print n,'\n'
            for d in i:print d['Name']
    elif k == 'SystemInformation':
        for n,i in v.items():
            print n,i
    else:
        pass #print k
'''


if __name__ == '__main__':
    monitor_info_dic=handle_info()   
    #print monitor_info_dic
    json_monitor_dic=json.dumps(monitor_info_dic)
    #xlm_monitor_data=xml2json.json2xml(json_monitor_dic)
    '''
    for i in monitor_info_dic.keys():
        if monitor_info_dic[i] =='data_value':
            for j in monitor_info_dic[i].keys():
            if monitor_info_dic[i][j] == 'SystemDevices':
                for k in monitor_info_dic[i][j].keys():
                print monitor_info_dic[i][j][k]
    '''  
 
    print 'Window平台下的资产收集情况\n'.decode('utf-8')
    #print system information
    print '系统基本信息:'.decode('utf-8')
    for k in monitor_info_dic['data_value']['SystemInformation'].keys():
        print "\t" + k + ":" + monitor_info_dic['data_value']['SystemInformation'][k]        
    for value in monitor_info_dic['data_value']['OSInfo']:
        if type(value) is dict:
            for k in value.keys():
                print "\t" + k+":" + value[k]
                #print value[k]
    
    #print systemDevices
    '''
    print '\n系统设备信息:'.decode('utf-8')
    for k in monitor_info_dic['data_value']['SystemDevices'].keys():
        for value in monitor_info_dic['data_value']['SystemDevices'][k]:
            print "Name:"
            print value['Name']
    
    #print LogicalDisks
    print '系统逻辑磁盘信息\n'.decode('utf-8')
    for k in monitor_info_dic['data_value']['LogicalDisks'].keys():
        for value in monitor_info_dic['data_value']['LogicalDisks'][k]:
            print value
    '''  
    #print hard disk info
    print '\n逻辑磁盘信息:'.decode('utf-8')
    for value in monitor_info_dic['data_value']['LogicalDiskInfo']:
        if type(value) is dict:
            for k in value.keys():
                print k+":" 
                print value[k]
                
    print '\n物理磁盘信息:'.decode('utf-8')
    for value in monitor_info_dic['data_value']['PhysicalDiskInfo']:
        if type(value) is dict:
            for k in value.keys():
                print k+":" 
                print value[k]
    #print cupinfo
    print '\nCPU处理器的信息:'.decode('utf-8')
    for k in monitor_info_dic['data_value']['CPUInfo'].keys():
        print k + ":" 
        print monitor_info_dic['data_value']['CPUInfo'][k]    
        
    #print meminfo
    print '\n内存信息:'.decode('utf-8')
    for value in monitor_info_dic['data_value']['MemInfo']:
        if type(value) is dict:
            for k in value.keys():
                print k+":" 
                print value[k] 
    
    #print NetInfo
    print '\n网卡信息:'.decode('utf-8')
    for value in monitor_info_dic['data_value']['NetInfo']:
        if type(value) is dict:
            for k in value.keys():
                print k + ":"
                print value[k]
            #print '\t'+ k + ":" 
            #print monitor_info_dic['data_value']['NetInfo'][k]  

    file_path = open("json.txt","w")
    file_path.write(json_monitor_dic)  
    file_path.close()      
