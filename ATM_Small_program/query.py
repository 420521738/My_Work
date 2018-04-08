#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle,time

def query(name):
	account_file = file('account.pkl','rb')
	account_info = pickle.load(account_file)
	account_file.close()
	
	month = raw_input('\033[31;1m请输入你要查询的月份账单，格式为年份-月份，如2018-03:\033[0m').strip()
	if len(month) == 0:
		month = time.strftime('%Y-%m',time.localtime(time.time()))
	if len(month) == 7:
		print "\033[31;1m-------------------------------------------------------------------------------\033[0m"
		print "姓名：%s\t额度：%s\t余额：%.2f" % (name,account_info[name][1],account_info[name][2])
		print "账单月份：%s" % month
		print "\033[32;1m      时间\t\t姓名\t操作\t流水\t\t利息\n\033[0m"
		f = file('user.log')
		for i in f.readlines():
			logmess = i.split()
			if logmess[3] == "购物":
				print "%s %s\t%s\t\033[31;1m%s\033[0m\t%s\t%s\n" % (logmess[0],logmess[1],logmess[2],logmess[3],logmess[4],logmess[5])
			if logmess[3] != "购物" and name == logmess[2] and month in logmess[0]:
				print "%s %s\t%s\t\033[31;1m%s\033[0m\t%s\t\t%s\n" % (logmess[0],logmess[1],logmess[2],logmess[3],logmess[4],logmess[5])
	else:
		print "\033[31;1m输入的查询月份格式有误，请输入正确的账单查询月份格式，如2018-03:\033[0m"

#query('qiu')
