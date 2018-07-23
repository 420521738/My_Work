#!/usr/bin/env python
import commands


def monitor(frist_invoke=1):
    shell_command = 'uptime'
    status,result = commands.getstatusoutput(shell_command)
    if status != 0:
        value_dic = {'status': status}
    else:
        host_status = result 

        value_dic = {
            'host_status': host_status,
            'status': status
        }
    return value_dic

if __name__ == '__main__':
    print monitor(frist_invoke=1)
