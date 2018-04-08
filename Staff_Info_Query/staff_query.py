#!/usr/bin/env python
staff_dic = {}
f = file('stu_info.txt')
for line in f.xreadlines(): #big file ,xreadline
	stu_id,stu_name,mail,company,title,phone = line.split()
	staff_dic[stu_id] = stu_name,mail,company,title,phone
	
while True:
	query = raw_input('\033[32;1mPlease input the query string:\033[0m').strip()
	if len(query) < 3:
		print 'You have to input at least 3 letters to query!'
		continue
	match_counter = 0
	for k,v in staff_dic.items():
		index = k.find(query)
		if k.find(query) != -1:
			print k[:index] + '\033[32;1m%s\033[0m' % query + k[index + len(query):] ,v
			match_counter += 1
		else:
			str_v = '\t'.join(v)
			index = str_v.find(query)
			if index != -1:
				print k,str_v[:index] + '\033[32;1m%s\033[0m' % query + str_v[index + len(query):]
				match_counter += 1
			#for i in v: # going to do the fuzzy matchs
			#	if i.find(query) != -1: # found item
			#		str_v = '\t'.join(v)
			#		print k,v
			#		match_counter += 1
			#		break
					
	print 'Matched \033[31;1m%s\033[0m records!' % match_counter
			
