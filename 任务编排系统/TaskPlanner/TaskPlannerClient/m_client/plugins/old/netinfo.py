# -*- coding: utf-8 -*-
#import
########################################################################
import platform
import commands
import wmi
########################################################################
#function
########################################################################

def monitor():
    c=wmi.WMI()
    #get network card info 
    net_dic={}
    
    net_list=[]
    for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):  
        tmp_dict = {}  
        tmp_dict["Description"] = interface.Description  
        tmp_dict["IPAddress"] = interface.IPAddress[0]  
        tmp_dict["IPSubnet"] = interface.IPSubnet[0]  
        tmp_dict["MAC"] = interface.MACAddress 
        net_list.append(tmp_dict)
    #get tcp connect
    for interfacePerfTCP in c.Win32_PerfRawData_Tcpip_TCPv4():
        net_list.append({"TCP Connect":str(interfacePerfTCP.ConnectionsEstablished)})
        #tmp_dict["TCP Connect"]=str(interfacePerfTCP.ConnectionsEstablished)
        #print '\t' + 'TCP Connect :\t' + str(interfacePerfTCP.ConnectionsEstablished) 
    net_dic['NetInfo']=net_list
    return net_dic
    
if __name__=='__main__':
    print monitor()
    