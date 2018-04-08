# cat paramiko_username_passwd_sftp.py
#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import paramiko
import sys,os

host = sys.argv[1]	###执行这个脚本后面加的IP地址
user = 'ihavecar'	###先定义好用户名      
password = 'x+y-z=71'	###先定义好密码
port = 22612		###定义好端口

t = paramiko.Transport((host,port))		###绑定传输实例t
t.connect(username=user,password=password)	###建立一个传输连接

sftp = paramiko.SFTPClient.from_transport(t)	###创建一个sftp实例，从t实例获取
sftp.get('/home/ihavecar/1.txt','1.new.txt')	###将远程服务器的/home/ihavecar/1.txt下载到当前路径，并重命名文件为1.new.txt
sftp.put('1.new.txt','/tmp/1.txt')		###将当前路径下的1.new.txt上传到远程服务器的/tmp/下，并重命名为1.txt

t.close()