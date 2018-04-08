#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle,time,sys

def shopping(name):
	account_file = file('account.pkl','rb')
	account_info = pickle.load(account_file)
	account_file.close()
	###自定义购物列表
	shopping_list = {
	'1':['皮鞋','300'],
	'2':['跑步鞋','200'],
	'3':['IPhonex','9000'],
	'4':['IPadAir','4500'],
	'5':['咖啡','40'],
	'6':['小轿车','158000']
	}
	
	print "\033[32;1m商品编号      商品名字      商品价格\033[0m"
	for x,y in shopping_list.items():
		print "%s\t\t%s\t\t%s" % (x,shopping_list[x][0],shopping_list[x][1])
	try:
		choice = raw_input('\033[31;1m请选择你要购买的商品，输入商品序号:\033[0m')
		if choice == 'quit':
			print "\033[31;1m您已成功退出ATM系统，欢迎你下次继续使用！\033[0m"
			sys.exit('再见，欢迎下次使用！')
		choice = int(choice)
		if choice == 1 or choice == 2 or choice == 3 or choice == 4 or choice == 5:
			choice = str(choice)
			if float(shopping_list[choice][1]) > account_info[name][2]:
				print "\033[31;1m你没有足够的钱购买这个商品，还卡内余额为￥%s\033[0m" % account_info[name][2]
				#continue
			else:
				account_info[name][2] = float(account_info[name][2]) - float(shopping_list[choice][1])
				account_file = file('account.pkl','wb')
				pickle.dump(account_info,account_file)
				account_file.close()
				now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				record = "购物"
				f = file('user.log','a')
				f.write("%s\t%s\t%s\t-￥%.2f\t￥0\n" % (now,name,record,float(shopping_list[choice][1])))
				f.close()
				print "\033[31;1m你已成功购买%s,你的卡内余额为￥%.2f\033[0m" % (shopping_list[choice][0],account_info[name][2])
		else:
			print "\033[32;1m你输入的商品序号不存在，请输入正确的商品序号!\033[0m"
			#continue
	except ValueError:
		print "\033[32;1m你输入的商品序号不存在，请输入正确的商品序号!\033[0m"
		#break
#shopping('qiu')
