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
    #get hard disk info 
    dist_dic={}
    #逻辑磁盘的信息
    logical_disk_list=[]
    for disk in c.Win32_LogicalDisk (DriveType=3):
        disk_dic={}
        disk_dic['磁盘符'.decode('utf-8')]=disk.Caption
        disk_dic['Size']=str(long(disk.Size) / (1024*1024*1024)) + " GB"
        #disk_dic['Free']=100.0*long(disk.FreeSpace)/long (disk.Size)
        logical_disk_list.append(disk_dic)
    dist_dic['LogicalDiskInfo']=logical_disk_list

    #物理硬盘的信息
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
    dist_dic['PhysicalDiskInfo']=physical_disk_list

    return dist_dic

if __name__=='__main__':

    print monitor()