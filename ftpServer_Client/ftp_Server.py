#!/usr/bin/env python
# --*-- coding: utf-8 --*--
import SocketServer	###导入sochet多线程模块
import commands,os,sys	###导入系统命令行模块
import MySQLdb		###导入数据库模块

class MyTCPHandler(SocketServer.BaseRequestHandler):
	exit_flag = False
	
	def handle(self):
		while not self.exit_flag:
			###服务端收取客户端发送过来的字符串信息，各个函数均有可能
			msg = self.request.recv(1024)
			if not msg:
				break
			###用|将收到的字符串信息进行分割成列表，msg_parse是一个列表
			msg_parse = msg.split("|")
			msg_type = msg_parse[0]
			###判断是否有msg_type如ftp_authentication等方法，如果有，获取这个方法
			if hasattr(self,msg_type):
				func = getattr(self,msg_type)
				###r如果有这个方法，如ftp_authentication，那么执行ftp_authentication(['ftp_authentication', 'username', 'password'])
				func(msg_parse)
			else:
				print "\033[31;1mWrong msg type:%s.\033[0m" % msg_type

	def ftp_authentication(self,msg):
		auth_res = False
		###如果msg列表里有三个参数，分别是ftp_authentication，username，password
		if len(msg) == 3:
			msg_type,username,passwd = msg
			###以下为调用python下的MySQLdb的方法
			conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
			cur = conn.cursor()
			conn.select_db('ftpuserinfo')
			###以下两个execute执行语句是为了判断当前用户名是否存在，如果存在，其家目录从数据库这种获取出来
			cur.execute('select name from userinfo where name = %s',username)
			qur_name = cur.fetchone()[0]
			cur.execute('select home from userinfo where name = %s',username)
			qur_home = cur.fetchone()[0]
			self.qur_home = qur_home
			###判断是否存在客户端输入的用户名
			if qur_name == username:
				###如果存在客户端输入的用户名，那么从数据库中获取其密码
				cur.execute('select password from userinfo where name = %s',username)
				qur_password = str(cur.fetchone()[0])
				###把客户端输入的密码与数据库中该用户名对应的密码比较
				if qur_password == passwd:
					auth_res = True
					self.login_user = username
					self.cur_path = '%s/%s' % (os.path.dirname(__file__),qur_home)
					self.home_path = '%s/%s' % (os.path.dirname(__file__),qur_home)
				else:
					auth_res = False
			else:
				auth_res = False
				cur.close()
				conn.close()
		else:
			auth_res = False
		###如果auth_res验证结果为真，也就是客户端输入的账号密码和数据库中的相匹配	
		if not auth_res == False:
			msg = "%s::success!" % msg_type
			print "\033[32;1mUser:%s has passed authentication!\033[0m" % username
		###如果auth_res验证结果为假，也就是客户端输入的账号密码和数据库中的不匹配
		else:
			msg = "%s::failed!" % msg_type
		###账号密码验证结果第一次发送给客户端
		self.request.send(msg)
	
	###定义处理客户端的文件处理函数
	###msg的信息是如['file_transfer','get','getfile.block']
	def file_transfer(self,msg):
		###首先判断传输的类型，第二个元素就是传输的类型
		transfer_type = msg[1]
		###如果传输类型是下载文件get
		if transfer_type == 'get':
			###先定义要下载文件的路径，文件的下载只能从指定的目录下载
			get_file_path = "/root/py_training/day6/ftpServer_Client/client_getfiles"
			###预防客户端输入文件的绝对路径，所以需要进行匹配
			filename = msg[2].split("/")[-1]
			filename = "%s/%s" % (get_file_path,filename)
			###首先判断客户端要下载的文件在服务端的指定目录下是否存在
			if os.path.isfile(filename):
				file_size = os.path.getsize(filename)
				###如果该文件存在就获取文件的大小以及准备就绪信息发给客户端
				confirm_msg = "file_transfer::get_file::send_ready::%s" % file_size
				self.request.send(confirm_msg)
				###服务端收到客户端可以开始发数据的消息了
				client_confirm_msg = self.request.recv(1024)
				if client_confirm_msg == "file_transfer::get_file::recv_ready":
					###开始循环发送数据到客户端，每次1024bit
					f = file(filename,'rb')
					size_left = file_size
					while size_left > 0:
						if size_left < 1024:
							self.request.send(f.read(size_left))
							size_left = 0
						else:
							self.request.send(f.read(1024))
							size_left -= 1024
					else:
						print "Send file done!"
				else:
					err_msg = "file_transfer::get_file::error::file does not exist or is a directory!"
					self.request.send(err_msg)

		###如果文件传输类型是put上传
		elif transfer_type == 'put':
			###服务端收到的msg经过以|分隔后，倒数第2个元素是文件名，倒数第一个元素是文件大小，文件大小需要转化为int整形
			filename,file_size = msg[-2],int(msg[-1])
			###指定客户端上传文件的路径
			put_file_path = "/root/py_training/day6/ftpServer_Client/client_putfiles"
			###以/作为分隔符，预防客户端在上传文件时写的是绝对路径，文件写绝对路径和相对路径都是可以匹配到的
			filename = filename.split("/")[-1]
			filename = "%s/%s" % (put_file_path,filename)
			###先使用os模块判断是否在上传目录中有这个文件，如果有就以名字.0标志	
			if os.path.isfile(filename):
				f = file('%s.0' % filename,'wb' )
			else:
				f = file('%s' % filename,'wb' )
			###告知客户端，我服务端已经准备好了，你可以开始发数据过来了
			confirm_msg = "file_transfer::put_file::recv_ready"
			self.request.send(confirm_msg)
			###开始循环接收数据，每次接收1024bit
			recv_size = 0
			while not recv_size == file_size:
				data = self.request.recv(1024)
				recv_size += len(data)
				f.write(data)
			else:
				print "\033[32;1mReceiving file:%s done!\033[0m" % filename
				f.close()

	###定义处理客户端删除文件的函数方法delete_file
	###其中msg是已经在handle处理过的参数，如['delete_file','test.txt']
	def delete_file(self,msg):
		print "\033[31;1m-->delete:\033[0m",msg[1:]
		file_list = msg[1].split()
		for i in file_list:
			###设定当前路径，用户只能删除当前目录下的文件或目录
			abs_file_path = "%s/%s" % (self.cur_path,i)
			###调用commands模块，执行删除命令
			cmd_res = commands.getstatusoutput("rm -rf %s" % abs_file_path)[1]
	
	###定义处理客户端查看文件列表的函数方法list_file
	###其中msg是已经在handle处理过的参数，如["list_file","/home/app"]
	def list_file(self,msg):
		home_prefix = self.qur_home 
		cmd = "cd %s;ls -lh %s" % (self.cur_path,' '.join(msg[1:]))
		file_list = os.popen(cmd).read()
		###将查看列表就绪的信息发送给客户端，并告知返回数据的大小，让客户端准备接受
		confirm_msg = "message_transfer::ready::%s" % len(file_list)
		self.request.send(confirm_msg)
		###接收客户端准备就绪的消息,如果收到了确认消息就开始发送数据
		confirm_from_client = self.request.recv(100)
		if confirm_from_client == 'message_transfer::ready::client':
			self.request.sendall(file_list)
	
	###定义处理客户端切换目录的函数方法switch_dir
	###其中msg是已经在handle处理过的参数，如["switch_dir","cd /home/app"]
	def switch_dir(self,msg):
		switch_res = ''
		###获取目录路径,msg[-1]获取到的如"cd /home/app",以空格分割成列表['cd','/home/app']
		msg = msg[-1].split()
		###如果msg的元素个数为1，也就是只有cd，并没有跟着路径
		if len(msg) == 1:
			self.cur_path = "/home/%s" % self.login_user
			switch_res = "switch_dir::ok::%s" % self.cur_path
			self.request.send(switch_res)
		###如果msg的元素个数为2，也就是cd后面跟着要切换的路径
		elif len(msg) == 2:
			###禁锢用户的切换目录，只允许用户切换到家目录，或者上传文件的目录，或者下载文件的目录
			if msg[-1] == self.qur_home or msg[-1] == "/root/py_training/day6/ftpServer_Client/client_getfiles" or msg[-1] == "/root/py_training/day6/ftpServer_Client/client_putfiles":
				self.cur_path = msg[-1]
				switch_res = "switch_dir::ok::%s" % self.cur_path
				self.request.send(switch_res)
			else:
				self.request.send("You dont't have privileges to switch to the dir!")
		else:
			switch_res = "switch_dir::error::target dir doesn't exist"
			self.request.send(switch_res)

###初始化函数，如果是自己执行，不是被人只执行，if的结果为true
if __name__ == "__main__":
	###定义侦听的来源IP地址
	host = '0.0.0.0'
	###侦听在9000端口
	port = 9000
	###注意(host,port)在这里是一个元组组成的参数，并不是分开的
	server = SocketServer.ThreadingTCPServer((host,port),MyTCPHandler)
###意思是永远都工作在监听状态
server.serve_forever()
