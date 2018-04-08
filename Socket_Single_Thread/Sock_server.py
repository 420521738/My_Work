#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import socket
###Socket服务绑定到4个0，也就是所有的IP地址段均可请求
host = '0.0.0.0'
###定义Socket绑定的端口为8000
port = 8000
###打开一个socket，使用socket.AF_INET的socket类型,也就是服务器之间进行网络通讯的类型;使用流式socket,socket.SOCK_STREAM,适用于TCP协议
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
###为打开的socket绑定IP地址和端口
s.bind((host,port))
###开始监听传入连接,1代表在拒绝连接之前,操作系统可以挂起的最大连接数量
s.listen(1)

while True:
	conn,addr = s.accept()	###s.accept()表示接受连接并返回，conn是新的套接字对象，也就是一个实例，用来接收和发送数据；addr是连接客户端的地址
	print "开始一个新的连接，客户端地址是：",addr
	while True:
		data = conn.recv(1024)	###接收套接字数据，数据以字符串形式返回，1024指的是要接收的最大数据量，1024为1K
		if not data:break	###如果没有数据进来，就跳出循环
		conn.send(data)		###将客户端发送过来的消息再传回客户端
		print "收到客户端:%s的消息：\033[31;1m%s\033[0m" % (addr,data)
s.close()	###关闭socket服务
