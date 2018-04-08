#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
try:
	conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
	cur = conn.cursor()	###创建游标
	cur.execute('create database if not exists Testpy')
	conn.select_db('Testpy')
	cur.execute("""
		create table myinfo(
			id int(5) not null primary key auto_increment,
			name char(20) not null,
			phone int(20) not null,
			class char(20)
		);
	""")
	info1 = ('Chenqiufei',15914200200,'Linux1')
	info2 = ('Linyanming',18914200220,'Linux2')
	cur.execute('insert into myinfo values(null,%s,%s,%s)',info1)
	cur.execute('insert into myinfo values(null,%s,%s,%s)',info2)
	conn.commit()
	cur.close()
	conn.close()
except MySQLdb.Error,e:
	print 'MySQL error Msg',e
	
