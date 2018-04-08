# cat paramiko_pkey_sftp.py
#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import paramiko
import sys,os

host = sys.argv[1]		###执行这个脚本后面加的IP地址
user = 'ihavecar'
port = 22612			###定义好端口
pkey_file = '/root/.ssh/id_rsa'	###定义好秘钥的路径在哪里
key = paramiko.RSAKey.from_private_key_file(pkey_file)	###调用RSA的验证key，私钥为刚刚定义的pkey_file

t = paramiko.Transport((host,port))		###绑定传输实例t
t.connect(username=user,pkey=key)	###建立一个传输连接

sftp = paramiko.SFTPClient.from_transport(t)	###创建一个sftp实例，从t实例获取
sftp.get('/home/ihavecar/1.txt','1.new.txt')	###将远程服务器的/home/ihavecar/1.txt下载到当前路径，并重命名文件为1.new.txt
sftp.put('1.new.txt','/tmp/1.txt')		###将当前路径下的1.new.txt上传到远程服务器的/tmp/下，并重命名为1.txt

t.close()