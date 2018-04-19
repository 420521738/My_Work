#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import MySQLdb,os,paramiko,sys,time,getpass	###加载所需要的模块
from multiprocessing import Process,Pool	###加载进程池模块

### 数据库类 ###
class Connect_mysql:
	conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = '123456',port = 3306,db = 'manager_system')
	cur = conn.cursor()	###创建游标
	
	def __init__(self,username,password='NULL'):	###创建初始化函数，调用Connect_mysql类的都会执行这个初始化函数
		self.username = username
		self.password = password

	def login_check(self):				###创建管理员账号密码检查函数
		try:
			self.cur.execute("select * from users where username = '%s' and password = '%s'" % (self.username,self.password))
			qur_result = self.cur.fetchall()
			if qur_result == ():		###如果没有匹配传输过来的账号密码，意思就是验证失败，结果集为空
				return 0
			else:
				return 1
			self.cur.close()		###正常关闭游标
			self.conn.close()		###正常关闭数据库连接
		except MySQLdb.Error,e:			###获取数据库异常信息，并在屏幕上打印
			print '\033[31;1mMySQL Error Msg:%s\033[0m' % e

	def return_server(self):			###创建返回登录系统的管理人员所对应的服务器信息
		self.cur.execute("select * from %s_server" % self.username)
		qur_result = self.cur.fetchall()
		return qur_result

### 批量远程命令执行函数 ###
def ssh_run(host_info,cmd,sysname):
	ip,username,password,port = host_info[1],host_info[2],host_info[3],host_info[4]
	date = time.strftime('%Y_%m_%d')
	date_detial = time.strftime('%Y_%m_%d %H:%M:%S')
	f = file('./log/%s_%s_record.log' % (sysname,date),'a+')	###首先需要在当前目录执行创建log目录的命令,否则执行报错
	
	try:
		s.connect(ip,int(port),username,password,timeout=5)	###s已经在主函数中被实例化了，在这里直接连接使用即可
		stdin,stdout,stderr = s.exec_command(cmd)		###标准写法
		cmd_result = stdout.read(),stderr.read()		###标准写法
		print '\033[32;1m--------------%s--------------\033[0m' % ip

		for line in cmd_result:					###将结果打印输出
			print line
	except:								###如果上面try部分出现任何异常，就走except部分
		log = "Time:%s | Type:%s | Detial:%s | Server:%s | Result:%s\n" % (date_detial,'cmd_batch',cmd,ip,'failed')
		f.write(log)
		f.close()
		print '\033[31;1mSomething is wrong of %s\033[0m' % ip
	else:								###如果try部分没有出现异常，就走这部分
		log = "Time:%s | Type:%s | Detial:%s | Server:%s | Result:%s\n" % (date_detial,'cmd_batch',cmd,ip,'success')
                f.write(log)
                f.close()
		return 1

### 批量文件分发函数 ###
def distribute_file(host_info,file_name,sysname):
        ip,username,password,port = host_info[1],host_info[2],host_info[3],host_info[4]
        date = time.strftime('%Y_%m_%d')
        date_detial = time.strftime('%Y_%m_%d %H:%M:%S')
        f = file('./log/%s_%s_record.log' % (sysname,date),'a+')
	try:
		t = paramiko.Transport((ip,port))
		t.connect(username = username,password = password)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftp.put(file_name,'/tmp/%s' % file_name)
		t.close()
	except:
		log = "Time:%s | Type:%s | Detial:%s | Server:%s | Result:%s\n" % (date_detial,'distribute_file',file_name,ip,'failed')
                f.write(log)
                f.close()
                print '\033[31;1mSomething is wrong of %s\033[0m' % ip
	else:
                log = "Time:%s | Type:%s | Detial:%s | Server:%s | Result:%s\n" % (date_detial,'distribute_file',file_name,ip,'success')
                f.write(log)
                f.close()
                print '\033[31;1mDistribute %s to %s Successfully!\033[0m' % (file_name,ip)


os.system('clear')
print '\033[32;1mWelcome to server batch management system!\033[0m'

### 程序主程序 ###
while True:
	username = raw_input("Please input your username:").strip()		###输入账号，去掉空格
	password = getpass.getpass("Please input your password:").strip()	###输入密码，隐藏输入，去掉空格
	if len(username) <= 5 or len(password) < 5:				###判断账号密码是否符合我们的长度要求，不一定是5，看你们的规则
		print '\033[31;1mInvalid username or password,please try again later!\033[0m'
		continue
	p = Connect_mysql(username,password)					###将p实例化，传参数账号和密码
	mark = p.login_check()							###p实例调用Connect_mysql的login_check方法，判断账号密码是否与数据库中的一致
	if mark == 0:								###如果验证失败
		print '\033[31;1mUsername or password wrong, Please try again later!\033[0m'
	elif mark == 1:								###如果验证通过
		print '\033[32;1mLogin Success!\033[0m'
		print 'The server you can manager are as follow:'
		server_list = p.return_server()					###p实例调用Connect_mysql的return_server方法，获取当前登录用户所能管理的服务器列表
		for server in server_list:
			print '%s:%s' % (server[5],server[1])
		while True:
			print '''
		1.Execute the command batch
		2.Distribute files batch
		3.Exit system
		'''
			choice = raw_input('\033[32;1mPlease input your choice number:\033[0m').strip()
			choice = int(choice)
			if choice >= 1 and choice <= 3:
				pass
			else:
				continue

			### 批量执行命令 ###
			if choice == 1:
				s = paramiko.SSHClient()			###绑定ssh客户端实例
				s.load_system_host_keys()			###加载本机host主机文件,普通用户类似/home/xxx/.ssh/known_hosts
				s.set_missing_host_key_policy(paramiko.AutoAddPolicy())	###第一次远程会提示输入yes，如果不加这句，第一次通过paramiko远程处理的时候就会出错
				
				p = Pool(processes=3)				###定义进程池的进程数为3
				result_list = []				###定义一个空的列表，用于存放进程执行返回的数据

				while True:
					cmd = raw_input('\033[32;1mPlease enter the command,also you can enter quit to go back the system:\033[0m')
					if cmd == 'quit':break
					for h in server_list:
						result_list.append(p.apply_async(ssh_run,[h,cmd,username]))	###进程的调用格式就是这样，遵循就行
					for res in result_list:							###将结果循环输出
						res.get()
				s.close()					###正常关闭实例
			
			### 批量分发文件 ###
			elif choice == 2:
                                s = paramiko.SSHClient()
                                s.load_system_host_keys()
                                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                                p = Pool(processes=3)
                                result_list = []
				
				while True:
					file_name = raw_input('\033[32;1mPlease input the filename which you want to distribute,also you can enter quit to go back the system:\033[0m').strip()
					start = time.time()
					if file_name == 'quit':
						break
					file_check = os.path.isfile(file_name)	###先判断文件是否存在，指的是当前执行目录下的文件
					log_list = []
					if file_check == False:			###如果文件不存在，或者其属性不是文件，而是目录
						print '\033[31;1mThe file:%s does not exist or it is a directory!\033[0m'
						continue
					else:
						for h in server_list:
							result_list.append(p.apply_async(distribute_file,[h,file_name,username]))	###进程的调用格式
						for res in result_list:
							res.get()
						end = time.time()
						print 'Cost time:%s seconds!' % str(end - start)
				
			### 退出系统 ###
			elif choice == 3:
				sys.exit('\033[32;1mWelcome to use our system,welcome to the next time!\033[0m')