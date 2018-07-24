#!/usr/bin/env python
import commands


def monitor(frist_invoke=1):
    shell_command = 'uptime'

    status,result = commands.getstatusoutput(shell_command)
    if status != 0: #cmd exec error
        value_dic = {'status':status}
    else:
	value_dic = {}
        uptime = result.split(',')[:1][0]
        load1,load5,load15 = result.split('load average:')[1].split(',')
        value_dic['data_value'] = {
            'uptime': uptime,
            'load1': load1,
            'load5': load5,
            'load15': load15,
            'status': status
        }
    return value_dic

if __name__ == '__main__':
	print monitor()
