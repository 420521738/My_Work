import time
import hashlib
import db_conn
import django
django.setup()
import hmac,hashlib
from app01.models import ApiAuth,UserProfile

class Auth:
    def __init__(self):
        self.user_dic = {}
        self.errors = []
        
    def __build_ssig(self, string2sign, password):
        ssig = hmac.new(password, string2sign, hashlib.sha1).digest().encode('base64')[5:15]
        return ssig
    def __user_is_valid(self,username):
        try:
            user = UserProfile.objects.get(user__username=username)
            self.user_token = user.token
            print 'token:', self.user_token
            return True 
        except Exception,e:
            print e
            return False
    def __has_permission(self,url,username,method):
        permission_list = ApiAuth.objects.filter(url__startswith=url, method_type=method)
        print permission_list
        for i in permission_list: #'api/v1.0/test' also contains api/v1.0/test/second/third, so if loop matchs the first one ,will not go on .
            print '-->', i.url, i.method_type,i.users.select_related()
            for u in   i.users.select_related():
                if u.user.username == username:
                    #print 'match user,he has right..'
                    return True
        else:
            self.errors.append({'permission_denied': 'user %s has no access to %s method for this api' % (username,method)}) 
            return False  

                 
    def auth(self,url,time_stamp,username,md5_val,action):
        '''fetch user password according username,then compare the md5(username + time_stamp + password) with md5_val sent from client  '''
        #print url
        #print url.split('//')[1].split('/')[1:-2]
        clean_url =  '/'.join(url.split('//')[1].split('/')[1:-2])
        print clean_url, action

        
        expires_time = 995920 
        print '----line19'
        if time_stamp is None:
            self.errors.append({'time_stamp': 'this field is required.'})
            return False
        if username is None:
            self.errors.append({'username': 'this field is required.'})
            return False
        if md5_val is None:
            self.errors.append({'hash_val': 'this field is required.'})
            return False            
           
        if time.time() - float(time_stamp) > expires_time:
            print 'token is expired...'
            self.errors.append({'authentication': 'requested url has expired,please make sure your local time syncs with the server' })
        else:
            
            if self.__user_is_valid(username):
                token = self.user_token
                hash_string = '%s\n%s' %(time_stamp,username)
                hmac_val = self.__build_ssig(hash_string, str(token))
                print md5_val, hmac_val
                if  md5_val  ==hmac_val: 
                    print 'valid user:'
                    if self.__has_permission(clean_url, username, action):
                        return True
                    
                else:
                    self.errors.append({'authentication': 'invalid username or password'})
                    return False                    
            else:
                print 'username invalid:', username
            '''if self.user_dic.get(username) is not None:
                passwd_str,methods = self.user_dic[username]
                hash_str = '%s|%s|%s' %(username, passwd_str,time_stamp)
                hash_md5 = hashlib.md5(hash_str).hexdigest()
                print hash_str
                print hash_md5,md5_val
                if hash_md5 == md5_val:
                    print '-0---------->passed the auto token'
                    if action in methods: #has permission
                        return True ##'user valid'
                    else:
                        self.errors.append({'permission_denied': 'user %s has no access to %s method for this api' % (username,action)})
                else:
                    self.errors.append({'authentication': 'invalid username or password'})
                    return False
            else:
                self.errors.append({'username': 'invalid username %s' % username})
                return False
            '''



if __name__ == '__main__':
    test= Auth()
    test.auth(1418284311.24, 'user','308af4be3eb9c0e53976d38bf2312137')
    print test.errors
    
    