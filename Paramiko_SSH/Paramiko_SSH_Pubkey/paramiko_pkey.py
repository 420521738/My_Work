#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import paramiko
import sys,os

host = sys.argv[1]	###执行这个脚本后面加的IP地址
user = 'ihavecar'	###定义远程连接用户名
port = 22612		###定义远程连接端口
cmd = sys.argv[2]	###执行这个脚本后面加的命令
pkey_file = '/root/.ssh/id_rsa'	###定义好秘钥的路径在哪里
key = paramiko.RSAKey.from_private_key_file(pkey_file)	###调用RSA的验证key，私钥为刚刚定义的pkey_file

s = paramiko.SSHClient()	###绑定ssh客户端实例
s.load_system_host_keys()	###加载本机host主机文件,普通用户类似/home/xxx/.ssh/known_hosts

s.connect(host,port,user,pkey=key,timeout=5)	###连接远程主机
stdin,stdout,stderr = s.exec_command(cmd)	###执行命令，stdin是输入，stdout是输出，stderr是执行错误信息

cmd_result = stdout.read(),stderr.read()	###读取执行的结果，执行不出错，则stderr.read()为空，执行出错，则stdout.read()为空

for line in cmd_result:
	print line

s.close()