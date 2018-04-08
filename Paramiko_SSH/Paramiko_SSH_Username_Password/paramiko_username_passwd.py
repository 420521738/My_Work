#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import paramiko
import sys,os

host = sys.argv[1]	###执行这个脚本后面加的IP地址
user = 'ihavecar'	###先定义好用户名      
password = 'x+y-z=71'	###先定义好密码
cmd = sys.argv[2]	###执行这个脚本后面加的命令

s = paramiko.SSHClient()	###绑定ssh客户端实例
s.load_system_host_keys()	###加载本机host主机文件,普通用户类似/home/xxx/.ssh/known_hosts
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())	###第一次远程会提示输入yes，如果不加这句，第一次通过paramiko远程处理的时候就会出错

s.connect(host,22612,user,password,timeout=5)	###连接远程主机
stdin,stdout,stderr = s.exec_command(cmd)	###执行命令，stdin是输入，stdout是输出，stderr是执行错误信息

cmd_result = stdout.read(),stderr.read()	###读取执行的结果，执行不出错，则stderr.read()为空，执行出错，则stdout.read()为空

for line in cmd_result:
	print line

s.close()
