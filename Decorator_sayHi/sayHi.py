#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def time_counter(func):		###函数把参数func接收，这个func是想对哪个函数进行包装
	def wrapper():		###这个是包装的过程
		start = time.time()
		func()
		end = time.time()
		print 'This fuunction costs :', end - start
	return wrapper		###把包装的函数体返回了,但是并没有执行

@time_counter
def tellYourSalary():
	print 'Allen makes 25K per month...'

@time_counter
def sayHi():
        print 'hi your sister...'
        time.sleep(0.1)
#@time_counter 其实是等于下面两句，只是这个是简写
# sayHi = time_counter(sayHi)
# sayHi()


sayHi()

tellYourSalary()
