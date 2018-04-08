#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle,time

def case(name):
	account_file = file('account.pkl','rb')
	account_info = pickle.load(account_file)
	account_file.close()

	try:
		get_num = int(raw_input("\033[32;1m请输入你要取的金额，本机只提供百元钞票，只能取百的整数:\033[0m"))
		if get_num % 100 == 0:
			if get_num > account_info[name][2]:
				print "\033[32;1m抱歉，你的卡内没有足够的钱，你目前卡内余额为￥%s" % account_info[name][2]
			else:
				poundage = get_num*0.05
				account_info[name][2] = int(account_info[name][2]) - get_num - poundage
				account_file = file('account.pkl','wb')		###将实时余额写入文件
				pickle.dump(account_info,account_file)
				account_file.close()
				now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				record = "取现"
				logfile = file('user.log','a')
				logfile.write("%s\t%s\t%s\t-￥%d\t-￥%.2f\n" % (now,name,record,get_num,poundage))
				logfile.flush()
				logfile.close()
				print "\033[31;1m取现 ￥%s 成功，利息为 ￥%.2f，你的账户余额为 ￥%s\033[0m" % (str(get_num),float(poundage),str(account_info[name][2]))
		else:
			print "\033[31;1m很抱歉，本ATM机只提供百元钞票，请你输入百的倍数取款金额\033[0m"
	except ValueError:
		print "\033[31;1m很抱歉，本ATM机只提供百元钞票，请你输入百的倍数取款金额\033[0m"

#case('qiu')
