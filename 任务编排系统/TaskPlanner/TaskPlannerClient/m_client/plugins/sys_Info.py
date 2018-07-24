#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#import
########################################################################
import platform

import xml2json
import json,time
import subprocess
import os.path
import wmi
########################################################################
#function
########################################################################
def get_os_info():
    return platform.platform()
	
def getinfo():
    print platform.system()
    print platform.release()
    print platform.version()
    print platform.machine()

def getvalue():
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

def monitor():
    value_dic=getvalue()
    os_dic={}
    c=wmi.WMI()
    os_dic['SysInfo']={'MachineName':value_dic['asset'].get('DxDiag')["SystemInformation"]['MachineName'],
                                'OperatingSystem':value_dic['asset'].get('DxDiag')["SystemInformation"]['OperatingSystem'],
                                'Language':value_dic['asset'].get('DxDiag')["SystemInformation"]['Language'],
                                'SystemManufacturer':value_dic['asset'].get('DxDiag')["SystemInformation"]['SystemManufacturer'],
                                'SystemModel':value_dic['asset'].get('DxDiag')["SystemInformation"]['SystemModel'],
                                'BIOS':value_dic['asset'].get('DxDiag')["SystemInformation"]['BIOS'],
                                'Processor':value_dic['asset'].get('DxDiag')["SystemInformation"]['Processor'],
                                'Memory':value_dic['asset'].get('DxDiag')["SystemInformation"]['Memory']}	
    os_list=[]
    for os in c.Win32_OperatingSystem():
        tmp_dic={}
        #tmp_dic['Caption']=os.Caption
        #tmp_dic['NumberOfUsers']=os.NumberOfUsers
        tmp_dic['Organization']=os.Organization
        tmp_dic['RegisteredUser']=os.RegisteredUser
        tmp_dic['SN']=os.SerialNumber
        #tmp_dic['Version'] = os.Version
        os_list.append(tmp_dic)
    os_dic['OSInfo']=os_list
    
    return os_dic

if __name__ == "__main__":
    print monitor()
    getinfo()
