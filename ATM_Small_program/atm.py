#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,pickle
import account,login,case,shopping,repayment,query


def main(name):
	while True:
		print '''\033[32;1m
			主菜单：
		1.现金服务
		2.购物刷卡
		3.还款
		4.账单查询
		5.退出
			\033[0m'''
		try:
			choice = int(raw_input('\033[31;1m选择你要进行的操作，输入序号即可:\033[0m').strip())
			if choice == 1:
				case.case(name)
			elif choice == 2:
				shopping.shopping(name)
			elif choice == 3:
				repayment.repayment(name)
			elif choice == 4:
				query.query(name)
			elif choice == 5:
				sys.exit()
			else:
				print "\033[31;1m你的选择有误，请重新选择你要进行的操作，输入序号1/2/3/4/5，谢谢！\033[0m"
				continue
		except ValueError: 	#捕获值错误的异常，如果代码执行出现这个错误，就进行下述操作
			print "\033[31;1m你的选择有误，请重新选择你要进行的操作，输入序号1/2/3/4/5，谢谢!\033[0m"
			continue

name = login.login()	###调用一次login模块的login()方法，也就是调用登录验证的功能
main(name)		###执行main函数，这个就是一个入口程序
