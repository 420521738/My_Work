#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle,time

def repayment(name):
	account_file = file('account.pkl','rb')
	account_info = pickle.load(account_file)
	account_file.close()
	
	try:
		get_num = int(raw_input("\033[32;1m请输入你要还款的金额，本机只能识别百元钞票，请放入钞票:\033[0m"))
		if get_num % 100 == 0:
			account_info[name][2] = float(account_info[name][2]) + float(get_num)
			now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			record = "还款"
			account_file = file('account.pkl','wb')
			pickle.dump(account_info,account_file)
			account_file.close()
			
			f = file('user.log','a')
			f.write("%s\t%s\t%s\t+￥%d\t￥0\n" % (now,name,record,get_num))
			f.flush()
			f.close()
			
			print "\033[31;1m你已经还款成功,还款金额为:￥%d，你目前的账户余额为:￥%.2f\033[0m" % (get_num,account_info[name][2])
		else:
			print "\033[31;1m抱歉，本机仅支持百元钞票还款！\033[0m"
	except ValueError:
		print "\033[31;1m抱歉，本机仅支持百元钞票还款！\033[0m"

#repayment('qiu')
