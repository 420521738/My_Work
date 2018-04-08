#!/usr/bin/env python
import MySQLdb
try:
	conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
	cur = conn.cursor()
	#cur.execute('create database if not exists s6py')
	conn.select_db('s6py')
	cur.execute('select * from stu_info')
	#cur.execute("""
	#	create table stu_info(
	#		id int(5) not null primary key auto_increment,
	#		name char(20) not null,
	#		phone int(13) not null,
	#		class char(20));
	#""")
	#info = ('Chenqiufei','110110110','Python train 6')
	#values_list = []
	#for i in range(20):
	#	values_list.append(('Chenqiufei_%s' %i,'111222123','Linux'))
	cur.scroll(14,'absolute')
	print cur.fetchall()
	#cur.executemany('insert into stu_info values(null,%s,%s,%s)',values_list)

	#conn.commit()
	#cur.close()
	#conn.close()
		
except MySQLdb.Error,e:
	print 'MySQL Error Msg:',e
