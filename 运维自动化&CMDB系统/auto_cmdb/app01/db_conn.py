#Author: Alex Li
import sys,os
'''
cur_dir = os.path.split(os.path.abspath(__file__))[0].split('/')[:-1]
base_dir = '/'.join(cur_dir[:-1])
sys.path.append('%s/auto_cmdb' %base_dir)
os.environ['DJANGO_SETTINGS_MODULE'] ='auto_cmdb.settings'
#from app01.models import *
'''
#for windows platform only
cur_dir = os.path.split(os.path.abspath(__file__))[0].split('\\')[:-1]
base_dir = '\\'.join(cur_dir)
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auto_cmdb.settings")

#from app01.models import *
