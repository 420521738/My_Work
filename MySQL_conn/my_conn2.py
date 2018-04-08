#!/usr/bin/env python
import MySQLdb
try:
	conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
	cur = conn.cursor()
	cur.execute('create database if not exists s6py')
	conn.select_db('s6py')
	cur.execute("""
		create table stu_info(
			id int(5) not null primary key auto_increment,
			name char(20) not null,
			phone int(13) not null,
			class char(20));
	""")
	info = ('Chenqiufei','110110110','Python train 6')
	info2 = ('Chenchen','222222222','Python train 7')
	cur.execute('insert into stu_info values(null,%s,%s,%s)',info)
	cur.execute('insert into stu_info values(null,%s,%s,%s)',info2)
	conn.commit()
	cur.close()
	conn.close()
		
except MySQLdb.Error,e:
	print 'MySQL Error Msg:',e
