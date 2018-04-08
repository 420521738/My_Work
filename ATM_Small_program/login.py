#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,pickle,time
import getpass		###密码隐藏输入的模块

def login():
	account_file = file('account.pkl','rb')
	account_info = pickle.load(account_file)	###将序列化的账号信息反序列化成原来的字典
	account_file.close()
	count = 0 	###设定密码输入次数初始值为0
	global name	###设置name为全局变量,方便后续的case,shopping,repayment,query模块调用name白能量
	
	while True:
		name = raw_input('\033[31;1m请输入你的名字:\033[0m').strip()
		if account_info.has_key(name):			###先判断账户字典文件中，是否有这个名字
			if account_info[name][3] == '0':	###如果这个人的账号是正常状态，正常为0，锁定为1
				count = 0
				while count < 3:		###如果密码输入错误次数未达到3次
					#pwd = raw_input('\033[31;1m请输入你的密码，输错三次密码账户就会被锁定，请谨慎输入:\033[0m').strip()
					pwd = getpass.getpass("\033[31;1m请输入你的密码，输错三次密码账户就会被锁定，请谨慎输入:\033[0m").strip() 
					if pwd == account_info[name][0]:	###如果密码是正确的
						now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))		###记录当时的时间
						logfile = file('login.log','a')
						logfile.write("[%s] %s 登录ATM系统！\n" % (now,name))
						logfile.flush()
						logfile.close()
						return name	###返回name的值继续给其他函数调用
					else:
						print "\033[31;1m密码输入错误！请输入正确密码！\033[0m"
						count = count + 1
						continue
				else:
					account_info[name][3] = 1	###密码输入错误3次，账号被锁定
					account_file = file('account.pkl','wb')
					pickle.dump(account_info,account_file)
					now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))            ###记录当时的时间
					logfile = file('login.log','a')
					logfile.write("[%s] %s 该用户连续输错三次密码，该账号已被锁定！\n" % (now,name))
					logfile.flush()
					logfile.close()
					print "\033[31;1m由于你连续输错了三次密码，你的账号已被锁定，请稍后再试！\033[0m"
					sys.exit()
			else:
				print "\033[31;1m你的账号已被锁定，请稍后再试！\033[0m"
				sys.exit()
		else:
			print "\033[31;1m系统中没有你输入的用户，请确认你输入的账号是否正确！\033[0m"
			continue
