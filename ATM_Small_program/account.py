#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle,os

if os.path.exists('account.pkl'):
	pass
else:
	account_info = {		###预设定用户名、密码等信息
		'qiu':['123','15000','15000','0'],
		'fei':['123','15000','15000','0']
}
	account_file = file('account.pkl','wb')		###打开account.pkl文件,以写二进制方式打开
	pickle.dump(account_info,account_file)		###将account_info的数据序列化到account_file中去
	account_file.close()
