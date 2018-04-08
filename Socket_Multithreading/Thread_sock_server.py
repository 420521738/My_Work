#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import SocketServer	###socket多线程模块

class MySockServer(SocketServer.BaseRequestHandler):	###自己定义的多线程交互模块需要继承基类SocketServer.BaseRequestHandler才行
	def handle(self):
		print "获取一个新的连接,客户端地址是:",self.client_address	###基类中定义的客户端地址变量
		while True:				###写死循环，重复进行信息收发工作
			data = self.request.recv(1024)	###收据接收需要使用基类中定义好的self.request前缀
			if not data:break		###如果没有数据进来，就跳出循环
			print "从客户端%s收到消息：\033[31;1m%s\033[0m" % (self.client_address,data)
			self.request.send(data.upper())	###数据发送需要使用积累中定义好的self.request前缀,将收到的信息转化为大写再发送回去给客户端

if __name__ == '__main__':				###初始化函数，如果是自己执行，不是被人只执行，if的结果为true
	host = '0.0.0.0'				###定义侦听的来源IP地址
	port = 9001					###侦听在9001端口
	s = SocketServer.ThreadingTCPServer((host,port),MySockServer)		###注意(host,port)在这里是一个元组组成的参数，并不是分开的
	s.serve_forever()				###意思是永远都工作在监听状态	

