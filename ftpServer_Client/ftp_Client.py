#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import socket	###导入socket模块
import sys,os	###导入系统sys以及os模块
import getpass	###导入密码隐藏输入模块

class FtpClient(object):
	###定义ftp命令相关函数,key为命令,values为所对应的函数
	func_dic = {
		'help':'help',
		'get':'get_file',
		'put':'put_file',
		'exit':'exit',
		'ls':'list_file',
		'cd':'switch_dir',
		'del':'delete'
	}

	###定义初始化函数，包括创建socket服务，认证auth方法调用，在认证交互里再调用交互interactive方法
	def __init__(self,host,port):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.connect((host,port))
		self.exit_flag = False
		if self.auth():
			self.interactive()
		
	###定义查看文件列表函数方法list_file
	def list_file(self,msg):
		###将字符串"list_file|文件或目录或为空"，如"list_file|/home/app"第一次发送给服务端，msg[1:]已经是去掉了命令类型，如已去掉了ls
		instruction = "list_file|%s" % (' '.join(msg[1:]))
		self.sock.send(instruction)
		###接收服务端读取文件列表的确认信息，并获取收取数据的大小
		server_confirm_msg = self.sock.recv(100)
		###判断刚刚收到的确认信息是否是服务端准备就绪的信息，预设的message_transfer::ready开头就是准备好了
		if server_confirm_msg.startswith("message_transfer::ready"):
			message_transfer_msg = server_confirm_msg.split("::")
			msg_size = int(message_transfer_msg[-1])
			###客户端第二次发消息给服务端，说客户端已经准备就绪，请发送信息
			self.sock.send("message_transfer::ready::client")
			recv_size = 0
			###开始收取服务端发送过来的信息，每次收取1024bit
			while not msg_size == recv_size:
				if msg_size - recv_size > 1024:
					data = self.sock.recv(1024)
				else:
					data = self.sock.recv(msg_size - recv_size)
				recv_size += len(data)
				sys.stdout.write(data)
	
	###定义切换目录的函数方法switch_dir
	def switch_dir(self,msg):
		switch_dir_msg = "You can only switch to YourHome(/home/youname) or /root/py_training/day6/ftpServer_Client/client_getfiles(download file dir) or /root/py_training/day6/ftpServer_Client/client_putfiles(upload file dir)"
		###将字符串如"switch_dir|cd /home/app"的发送给服务端
		self.sock.send("switch_dir|%s" % (' '.join(msg)))	
		feedback = self.sock.recv(100)
		if feedback.startswith("switch_dir::ok"):
			self.cur_path = feedback.split("::")[-1]
			print "\033[32;1mYou switch the dir %s success!" % self.cur_path
		elif feedback.startswith("You dont't have privileges"):
			print "\033[31;1m%s\n%s\033[0m" % (feedback,switch_dir_msg)
		else:
			print "\033[31;1mtarget dir %s doesn't exist!\033[0m" % feedback.split("::")[-1]

	###定义删除文件的函数方法delete	
	def delete(self,msg):
		###如果del后面加了文件名参数
		if len(msg) > 1:
			###向服务端发送字符串如"delete_file|test.txt"，msg[1:]已经将del去掉
			instruction = "delete_file|%s" % (' '.join(msg[1:]))
			self.sock.send(instruction)
		else:
			print "\033[31;1mWrong command usage...\033[0m"

	###定义用户认证auth函数方法
	def auth(self):
		retry_count = 0
		while retry_count < 3:
			username = raw_input("username:").strip()
			
			if len(username) == 0:continue
			passwd = getpass.getpass()
			###将ftp_authentication|username|password格式字符串通过sock发送给服务端
			auth_str = "ftp_authentication|%s|%s" % (username,passwd)
			self.sock.send(auth_str)
			###收取服务端第一次发回来的消息，可能会有两种结果，一种是验证通过，一种是验证失败
			auth_feedback = self.sock.recv(1024)
			###如果收到的消息是ftp_authentication::success!，那么这个预设的信息在客户端认为就是验证通过了
			if auth_feedback == "ftp_authentication::success!":
				print "\033[31;1mAuthentication Passed!\033[0m"
				self.username = username
				self.cur_path = username
				return True
			else:
				print "\033[31;1mWrong username or password!\033[0m"
				retry_count += 1
		else:
			print "\033[31;1mToo many attempts,exit!\033[0m"
		
	###定义ftp命令行交互函数方法interactive	
	def interactive(self):
		try:
			while not self.exit_flag:
				###定义命令交互时的光标以及格式，可以自由定义
				cmd = raw_input("[\033[32;1m%s:\033[0m%s]>>:" % (self.username,self.cur_path)).strip()
				if len(cmd) == 0:continue
				###先将拿到的命令以空格进行分割成列表,如['ls', '/home/app']
				cmd_parse = cmd.split()
				msg_type = cmd_parse[0]
				###调用func_dic字典查看是否有命令类型，如是否有key：ls
				if self.func_dic.has_key(msg_type):
					###如果有如ls这个key对应values，那么就获取属性给funch，如func就获取了getattr(self,list_file)
					func = getattr(self,self.func_dic[msg_type])
					###执行函数如list_file(['ls','/home/app'])
					func(cmd_parse)
				else:
					print "Invalid command,type [help] to see available command list"
		except KeyboardInterrupt:
			self.exit('Exit!')
		except EOFError:
			self.exit('Exit!')

	### 上传文件,只能从自己的家目录(如/home/jack/xxxx)上传到:/root/py_training/day6/ftpServer_Client/client_putfiles
	###msg信息如 ['put','upload.block']
	def put_file(self,msg):
		if len(msg) == 2:
			file_path = "/home/%s" % self.username 
			filename = "%s/%s" % (file_path,msg[1].split("/")[-1])
			###使用os模块查询要上传文件的大小
			file_size = os.path.getsize(filename)
			###客户端将传输信息以及文件大小信息发送给服务端,倒数第二个变量是文件名，倒数第一个变量是文件大小，单位是bit
			instruction_msg = "file_transfer|put|send_ready|%s|%s" % (filename,file_size)
			self.sock.send(instruction_msg)
			###客户端收取服务端发送过来的确认信息
			feedback = self.sock.recv(1024)
			print '==>',feedback
			progress_persent = 0
			if feedback.startswith("file_transfer::put_file::recv_ready"):
				###将要上传的文件以二进制读的方式打开
				f = file(filename,'rb')
				###循环发送数据，每次发送1024bit
				sent_size = 0
				while not sent_size == file_size:
					if file_size - sent_size <= 1024:
						data = f.read(file_size - sent_size)
						sent_size += file_size - sent_size
					else:
						data = f.read(1024)
						sent_size += 1024
					self.sock.send(data)
					###以（已发送数据/文件大小）来判断发送百分比，显示进度条
					cur_persent = int(float(sent_size) / file_size * 100)
					if cur_persent > progress_persent:
						progress_persent = cur_persent
						self.show_progress(file_size,sent_size,progress_persent)
						print file_size,sent_size,progress_persent
				else:
					print "---Send File:%s Done!" % filename
				f.close()
		else:
			print "\033[31;1mFile %s doesn't exits on local disk!\033[0m" % filename
	
	###下载文件只能从/root/py_training/day6/ftpServer_Client/client_getfiles上下载到用户的家目录下(如/home/jack/xxx)
	###msg信息是如['get','getfile.block']
	def get_file(self,msg):
		if len(msg) == 2:
			###msg为发送给服务端的字符串信息，如"file_transfer|get|getfile.block"
			msg = "file_transfer|get|%s" % msg[1]
			self.sock.send(msg)
			###客户端收取服务端的准备就绪信息，以及文件大小，以便自己循环收数据
			feedback = self.sock.recv(1024)
			if feedback.startswith("file_transfer::get_file::send_ready"):
				file_size = int(feedback.split("::")[-1])
				###指定文件下载回来只能下载到自己的家目录
				get_file_path = "/home"
				filename = "%s/%s/%s" % (get_file_path,self.username,msg.split("|")[-1].split("/")[-1])
				f = file(filename,'wb')
				###客户端告诉服务端，可以开始发数据了
				self.sock.send("file_transfer::get_file::recv_ready")
				size_recv = 0
				progress_persent = 0

				while not size_recv == file_size:
					data = self.sock.recv(file_size - size_recv)
					size_recv += len(data)
					f.write(data)
					###以（已发送数据/文件大小）来判断发送百分比，显示进度条		
					cur_percent = int(float(size_recv) / file_size *100)
					if cur_percent > progress_persent:
						progress_persent = cur_percent
						self.show_progress(file_size,size_recv,progress_persent)
				else:
					print "\033[31;1mRecieved the file %s done\033[0m" % filename
				f.close()
		else:
			print "\033[31;1mFile doesn't exist on remote server or sth else went wrong!\033[0m"
	
	###定义上传和下载进度条显示的函数方法
	def show_progress(self,total,finished,percent):
		progress_mark = "=" *(percent/2)
		sys.stdout.write("[%s/%s]%s>%s\r" % (total,finished,progress_mark,percent))
		sys.stdout.flush()
		if percent == 100:
			print '\n'
	
	###定义退出程序的函数方法
	def exit(self,msg):
		self.sock.shutdown(socket.SHUT_WR)
		sys.exit("Bye! %s" % self.username)
	
	###定义帮助函数方法
	def help(self,msg):
		print '''
			\033[31;1mhelp\033[0m    help
			\033[31;1mget\033[0m     get remote_filename
			\033[31;1mput\033[0m     put local_filename
			\033[31;1mexit\033[0m    exit the system
			\033[31;1mls\033[0m      list all the files in current directory
			\033[31;1mcd\033[0m      cd some_dir
			\033[31;1mdel\033[0m     del remote_filename
		'''

###如果是自己执行，那么则执行s = FtpClient('localhost',9000)，如果是被人调用，则不执行
if __name__ == '__main__':
	s = FtpClient('localhost',9000)
