#!/usr/bin/env python
import sys
salary = int(raw_input('Please input your salary:'))
products = [
	['Iphone',5800],
	['MacPro',12000],
	['NB',680],
	['Cigarate',48],
	['MX4',2500]
]

# create a shopping list
shopping_list = []

while True:
	for p in products:
		print products.index(p),p[0],p[1]
	choice = raw_input("\033[32;1mPlease choose sthing to by:\033[0m").strip()
	if choice == 'quit':
		print "You have bought below stuff:"
		for i in shopping_list:
			print '\t',i
		sys.exit('Goodbye')
	if len(choice) == 0:continue
	if not choice.isdigit():continue
	choice = int(choice)
	if choice > len(products): # out of range
		print "\033[31;1mCould not find this item\033[0m"
		continue
	pro = products[choice]
	
	if salary >= pro[1]: # means you can afford this
		salary = salary - pro[1]
		shopping_list.append(pro)
		print "\033[34;1mAdding %s to shopping list,you have %s left\033[0m" % (pro[0],salary)
	else:
		print 'The price of %s is %s,yet your current balance is %s,so try another one!' % (pro[0],pro[1],salary)
