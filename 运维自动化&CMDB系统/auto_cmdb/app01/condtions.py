import db_conn
import django
django.setup()
from app01.models import *
from django.db.models import Q

import operator


keys =['windows','linux']

con = reduce(operator.or_,(Q(**{'asset__hostname__contains':x})for x in keys))


print Server.objects.filter(con)
