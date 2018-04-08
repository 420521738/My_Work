#!/usr/bin/env python
import sys
username = 'chenqiufei'
password = 'chenqiufei123'
locked = 1
retry_counter = 0

while retry_counter < 3:
  user = raw_input('Username:').strip()
  if len(user) ==0:
	print '\033[31;1mUsername cannot be empty!\033[0m'
	continue
  passwd = raw_input('Password:').strip()
  if len(passwd) == 0:
	print '\033[31;1mPassword cannot be empty!\033[0m'
	continue

  ##username and password is not empty

  ##going to vertified
  if locked == 0:###means the user is locked
	print 'Your username is locked!'	
	sys.exit()
  else:
	if user == username and passwd == password:###means passwd OK
		sys.exit( 'welcome %s login to our system!' %user)
	else:
		#retry_counter = retry_counter + 1
		retry_counter += 1
		print '\033[31;1mWrong username or password,you have %s more chances!\033[0m' % (3 -retry_counter)
  
