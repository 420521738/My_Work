#!/usr/bin/env python
# --*-- coding: utf-8 --*--
from multiprocessing import Process,Pool	###导入多进程模块，以及进程池
import paramiko					###导入paramiko模块
import sys,os

global cmd					###定义全局变量cmd，用于自定义想执行的命令
cmd = raw_input("请输入你要批量执行的命令:")	###用户输入命令赋予cmd变量

host_list = (
	('192.168.1.71','ihavecar','x+y-z=71'),
	('192.168.1.74','ihavecar','x+y-z=74'),
	('192.168.1.66','abcusera','x+y-66=z')
)

s = paramiko.SSHClient()	###绑定ssh客户端实例
s.load_system_host_keys()	###加载本机host主机文件,普通用户类似/home/xxx/.ssh/known_hosts
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())	###第一次远程会提示输入yes，如果不加这句，第一次通过paramiko远程处理的时候就会出错

try:
	def ssh_run(host_info,cmd):				###定义run_ssh函数，传入两个参数，一个是主机相关参数，一个是命令相关参数
		host,user,password = host_info
		s.connect(host,22612,user,password,timeout=5)	###连接远程主机
		stdin,stdout,stderr = s.exec_command(cmd)	###执行命令，stdin是输入，stdout是输出，stderr是执行错误信息

		cmd_result = stdout.read(),stderr.read()	###读取执行的结果，执行不出错，则stderr.read()为空，执行出错，则stdout.read()为空
	
		print '\033[32;1m********%s %s*************\033[0m' % (host,user)	###命令执行结果分割

		for line in cmd_result:				###将结果按行输出打印
			print line


	p = Pool(processes=2)					###创建进程池，这个进程池里有两个进程

	result_list = []					###创建一个空的字符串

	for h in host_list:					###启动多进程运行run_ssh,并将结果存放到result_list中去
		result_list.append(p.apply_async(ssh_run,[h,cmd]))
	
	for res in result_list:
		res.get()

except Exception as e:
	print "Error Info is :%s" % e
	

s.close()
