#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import socket	###客户端导入socket模块即可
import os	###客户端导入os模块是为了下面计算传输文件的大小
host = '192.168.1.234'
port = 9001	

c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	###创建一个socket服务
c.connect((host,port))

while True:
	user_input = raw_input("\033[31;1m请执行上传或下载操作，格式为：put/get 全路径文件名：\033[0m").strip()	###客户端输入需要执行的命令
	if len(user_input) == 0:continue	###如果客户端输入空命令，就继续返回执行循环
	user_cmd = user_input.split()		###将客户端输入的put/get操作，以及文件名切割成列表
	if user_cmd[0] == 'put':
		f = file(user_cmd[1],'rb')	###将文件以二进制读rb的方式打开
		f_size = os.stat(user_cmd[1]).st_size	###计算要上传文件的大小，然后传输给服务端
		c.send('%s %s %s' % (user_cmd[0],user_cmd[1],f_size))
		c.sendall(f.read())		###f.read()就是将文件整个读出
		print c.recv(1024)		###读取服务端发送过来的成功或失败的信息

c.close()
