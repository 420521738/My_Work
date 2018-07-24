import os,sys

#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
base_dir = '/'.join(__file__.split('/')[:-2])
if sys.platform.startswith('win32'):
    base_dir = '\\'.join(__file__.split('\\')[:-2])

sys.path.append(base_dir)

#print base_dir

#from conf import templates


