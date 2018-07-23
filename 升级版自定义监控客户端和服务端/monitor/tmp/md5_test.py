import md5
import time 
passwd = 'alex3714'
time_str = time.time()
token_str = '%s|%s' %(passwd,time_str)
 
print md5.md5(token_str).hexdigest()
print time_str
import hmac
import hashlib
a= hmac.new(token_str, passwd, hashlib.sha1(64)).hexdigest()
