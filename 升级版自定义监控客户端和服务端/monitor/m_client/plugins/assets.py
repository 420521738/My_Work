#!/usr/bin/env python 
#coding:utf-8
import subprocess,os.path
import sys
import result_deal
import json
def monitor(frist_invoke=1):
    monitor_info_dic={}
    if sys.platform.startswith("win"):
        import assetsCollect
        import pythoncom
        pythoncom.CoInitialize()
        monitor_info_dic=assetsCollect.handle_info()
    else:
        #from assetsCollect_linux import *
        import assetsCollect_linux
        monitor_info_dic = assetsCollect_linux.monitor()
    if frist_invoke:
        result_filename='../recv/assets_result.json'
        result_deal.generate_file(result_filename,monitor_info_dic)
        monitor_info_dic['change_mark']=1
    else:
        result_filename='../recv/assets_result_new.json'
        result_deal.generate_file(result_filename,monitor_info_dic)
        file_md5_old=result_deal.generate_file_md5value('../recv/assets_result.json')
        file_md5_new=result_deal.generate_file_md5value(result_filename)
        if file_md5_old == file_md5_new:
            print 'monitor result no change.....'
            monitor_info_dic={}
            monitor_info_dic['change_mark']=0
            return monitor_info_dic
        else:
            result_old_dic=result_deal.read_file('../recv/assets_result.json')
            result_change_dic=result_deal.get_monitor_data_change(json.loads(result_old_dic),monitor_info_dic)
            result_deal.generate_file('../recv/assets_result.json',monitor_info_dic)
            result_change_dic['change_mark']=1
            return result_change_dic
    return monitor_info_dic

if __name__ == '__main__':
    print monitor()