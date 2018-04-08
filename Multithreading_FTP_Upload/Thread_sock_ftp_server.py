#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import SocketServer	###导入sochet多线程模块
import commands		###导入系统命令行模块
import time		###导入时间模块，服务端连续发信息给客户端有可能会粘包，所以需要短时间睡眠

class MySockServer(SocketServer.BaseRequestHandler):	###必须继承基类
	
	def recv_all(self,obj,msg_length,des_file):	###定义一个边收边写的函数，以防内存被撑爆了
		while msg_length != 0:
			if msg_length <= 4096:		###每次收4K，小于4K匹配这段if
				data = obj.recv(msg_length)
				msg_length = 0		###最后一次收完数据后，重置msg_length为0
			else:
				data = obj.recv(4096)	###如果数据大于4K，匹配到这个else段，每次收4K数据
				msg_length -= 4096	###收完这次4K数据后，将数据大小减去4096
			des_file.write(data)		###不管是大于4K还是小于4K，每执行完一次，写入一次数据
		return 'Done'				###函数方法执行完后，返回Done，用于稍后的判断

	def handle(self):
		print "获取一个新的连接,客户端地址是:",self.client_address
		while True:
			cmd = self.request.recv(1024)	###基类中规定收信息需要加self.request
			if not cmd:
				print "与客户端%s失去连接了!" % self.client_address
				break		###如果客户端传输空信息，则退出循环
			
			action,filename,file_size = cmd.split()	###变量分别是动作，文件名，文件大小
			if action == 'put':	###判断动作是上传put还是其他
				f = file('recv_dir/%s' % filename,'wb')	###如果是上传操作，在当前目录recv_dir下创建同名文件，并且以二进制写wb的方式打开
				write_to_file = self.recv_all(self.request,int(file_size),f)	###获取recv_all函数方法执行的结果，用于判断是否文件写入完成，因为这里是类方法，所以需要加self，参数里self.request代表自己
				if write_to_file == 'Done':
					self.request.send('\033[31;1m文件上传成功！\033[0m')
					f.close()	###文件传输成功后，一定要记得把文件关闭，否则有些内容可能还在缓冲区

if __name__ == '__main__':	###如果是自己执行，则执行以下
	host = '0.0.0.0'		
	port = 9001		
	s = SocketServer.ThreadingTCPServer((host,port),MySockServer)	###使用SocketServer的方法	
	s.serve_forever()	###永远侦听客户端请求

