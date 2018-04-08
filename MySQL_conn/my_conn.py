#!/usr/bin/env python
import MySQLdb
try:
	conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306)
	cur = conn.cursor()
	cur.execute('select user,host,password from user')
	qur_result = cur.fetchall()
	for record in qur_result:
		print record
	cur.close()
	conn.close()
except MySQLdb.Error,e:
	print 'MySQL Error Msg:',e
