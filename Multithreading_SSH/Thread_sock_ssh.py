#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import SocketServer	###导入sochet多线程模块
import commands		###导入系统命令行模块
import time		###导入时间模块，服务端连续发信息给客户端有可能会粘包，所以需要短时间睡眠

class MySockServer(SocketServer.BaseRequestHandler):	###必须继承基类
	def handle(self):
		print "获取一个新的连接,客户端地址是:",self.client_address
		while True:
			cmd = self.request.recv(1024)	###基类中规定收信息需要加self.request
			if not cmd:break		###如果客户端传输空信息，则退出循环
			print "从客户端%s收到命令是：\033[31;1m%s\033[0m" % (self.client_address,cmd)
			cmd_result = commands.getstatusoutput(cmd)	
			self.request.send(str(len(cmd_result[1])))	###基类中规定发信息需要加self.request
			time.sleep(0.2)		###睡眠0.2秒的作用在用预防服务端连续发信息会导致客户端接收信息时出现粘包
			self.request.send(cmd_result[1])

if __name__ == '__main__':	###如果是自己执行，则执行以下
	host = '0.0.0.0'		
	port = 9001		
	s = SocketServer.ThreadingTCPServer((host,port),MySockServer)	###使用SocketServer的方法	
	s.serve_forever()	###永远侦听客户端请求

