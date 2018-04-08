#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import socket	###客户端导入socket模块即可
host = '192.168.1.234'
port = 9001	

c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	###创建一个socket服务
c.connect((host,port))

def recv_all(obj,recv_size):	###定义一个循环收数据的函数，因为客户端收取数据的字节大概是36K，超出就会报错,在这里4K收取,直到收取完成
	all_return_data = ''				###先定义个数据收集器为空
	while recv_size != 0:				###如果数据大小不是0
		if recv_size <= 4096:			###如果数据没有超过4K
			data = obj.recv(recv_size)	###将数据赋值给变量data
			recv_size = 0			###将数据大小清空
		else:
			data = obj.recv(4096)		###如果数据大小超过4K了
			recv_size -= 4096		###循环收取4K数据，直到数据代销小于或等于4K的时候，执行上面的if
		all_return_data += data			###不管上面两个if或者else的结果如何，都会执行将data变量里的数据赋予到all_return_data
	return all_return_data				###让函数返回命令执行的全部结果
			

while True:
	user_input = raw_input("\033[31;1m请你输入想要发给socket服务端执行的命令：\033[0m").strip()	###客户端输入需要执行的命令
	if len(user_input) == 0:continue	###如果客户端输入空命令，就继续返回执行循环
	c.send(user_input)			###将客户端命令发送给服务端

	recv_size = int(c.recv(1024))		###先接收服务端返回的第一个值,也就是命令执行结果的字节大小是多少,1024指的是K
	print '\033[31;1m收到的返回数据的字节大小(单位是bit)：\033[0m',recv_size	###调试的时候可以打印命令执行结果字节大小,正式使用时可以不打印
	result = recv_all(c,recv_size)		###调用函数recv_all,返回的结果是命令在服务端执行的全部结果
	

	print "\033[31;1m命令执行的结果是：\033[0m\n",result	###循环收全命令执行结果后，在客户端输出
c.close()
