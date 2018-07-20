import db_conn
import django
django.setup()
from app01.models import *


host_list = Asset.objects.all()

h_list = []
for h in host_list:
	h_list.append(h.hostname)


import collections

uniq = []

for i in h_list:
	if i not in uniq:
		uniq.append(i)
	else:
		print i
