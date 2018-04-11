#!/usr/bin/env python
# --*-- coding: utf-8 --*--
###编辑登录脚本###

import os

def hosts_group():			###定义主机组
	os.system('clear')		###清屏
					###打印可选主机组
	print """			
		\033[31;1m[主机列表组]\033[0m

		1.qqandroid组

		2.qqios组

	"""

	global x_1                      ###记录选择的主机组号，应用于全局
	x_1 = raw_input('\033[31;1m请输入你要选择的主机组编号：\033[0m').strip()


def hosts():				###定义主机选择函数
	if x_1 == '1':			###如果在主机组中，选择的是1组
		os.system('clear')
		print """
		\033[31;1m[qqandroid主机组列表]\033[0m

		1.qqandroid1服

		2.qqandroid2服

		3.返回上一页

		"""
		
		global lines                    ###定义lines变量，应用于全局
		x_21 = raw_input("\033[31;1m请输入你要选择的服务器编号：\033[0m")
		f = file('/home/chenqiufei/Fortress_machine/hosts_user/qqandroid.txt','r')
		for line in f.readlines():
			line = line.strip('\n').split(' ')	###忽略掉换行符，并且已空格切割成列表
			if line[0] == x_21:			###如果选择选择的服务器与qqandroid.txt中服务器的序号相等
				lines = line[1]			###将服务器的IP赋予lines
		
		if x_21 == '3':		###如果选择返回上一页，则系统调用demo.py脚本执行
			os.system('/usr/bin/python /home/chenqiufei/Fortress_machine/script/demo.py')	
			
	else:				###如果不是选1，那就是2
		os.system('clear')	###先清屏
					###打印IOS服务器的服务器列表
                print """
                \033[31;1m[qqios主机组列表]\033[0m

                1.qqios1服

                2.qqios2服

                3.返回上一页

                """
                x_22 = raw_input("\033[31;1m请输入你要选择的服务器编号：\033[0m")
                f = file('/home/chenqiufei/Fortress_machine/hosts_user/qqios.txt','r')
                for line in f.readlines():
                        line = line.strip('\n').split(' ')      ###忽略掉换行符，并且已空格切割成列表
                        if line[0] == x_22:                     ###如果选择选择的服务器与qqios.txt中服务器的序号相等
                                lines = line[1]                 ###将服务器的IP赋予lines

                if x_22 == '3':         ###如果选择返回上一页，则系统调用demo.py脚本执行
                        os.system('/usr/bin/python /home/chenqiufei/Fortress_machine/script/demo.py')


def yh():			###定义用户选择函数
	os.system('clear')
	print """
	\033[31;1m[用户列表]\033[0m

	1.ihavecar

	2.zhangsan

	3.lisi
	
	4.返回首页

	"""
	
	global youruser         ###定义登录用户变量为全局变量，全局可调用
	xyh = raw_input("\033[31;1m请输入你要登录的用户编号：\033[0m")
	
	if xyh == '4':		###如果用户选择的是返回首页，那就重新执行demo.py脚本
		os.system('/usr/bin/python /home/chenqiufei/Fortress_machine/script/demo.py')
	elif xyh == '1' or xyh == '2' or xyh == '3':
		f = file('/home/chenqiufei/Fortress_machine/hosts_user/users.txt')
        	for line in f.readlines():
			line = line.strip('\n').split(' ')      ###忽略掉换行符，并且已空格切割成列表
			if line[0] == xyh:                      ###如果选择选择的服务器与user.txt中服务器的序号相等
				youruser = line[1]              ###将要登录的用户名赋予全局变量youruser
	else:
		print "\033[31;1m你的输入错误，请重新输入用户编号！\033[0m"
		os.system('/usr/bin/python /home/chenqiufei/Fortress_machine/script/demo.py')
