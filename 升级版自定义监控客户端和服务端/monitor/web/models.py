#_*_coding:utf-8_*_
import sys
reload(sys) 
sys.setdefaultencoding("utf-8") 
from django.db import models

from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    def __unicode__(self):
        return '%s' % self.user

class Idc(models.Model):
    name=models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50,unique=True)
    display_name = models.CharField(max_length=50)
    template_list = models.ManyToManyField('Templates')
    def __unicode__(self):
        return self.display_name

class Host(models.Model):
    hostname=models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, unique = True)
    ip = models.IPAddressField(unique=True)
    child_of = models.ForeignKey('TrunkServers', null=True,blank=True)
    idc = models.ForeignKey(Idc, null=True, blank=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    template_list = models.ManyToManyField('Templates',null=True,blank=True)
    custom_services = models.ManyToManyField('Services',null=True,blank=True)
    port = models.IntegerField(default='22')
    os = models.CharField(max_length=20, default='linux', verbose_name='Operating System')

    #snmp related
    status_monitor_on = models.BooleanField(default=True)
    snmp_on = models.BooleanField(default=True)
    snmp_version = models.CharField(max_length=10,default='2c')
    snmp_community_name = models.CharField(max_length=50,default='public')
    snmp_security_level = models.CharField(max_length=50,default='auth')
    snmp_auth_protocol = models.CharField(max_length=50,default='MD5')
    snmp_user = models.CharField(max_length=50,default='triaquae_snmp')
    snmp_pass = models.CharField(max_length=50,default='my_pass')

    def __unicode__(self):
        return self.display_name


class ServerStatus(models.Model):
    host = models.OneToOneField('Host')
    hostname = models.CharField(max_length=100)
    host_status = models.CharField(max_length=10,default='Unkown')
    ping_status = models.CharField(max_length=100,default='Unkown')
    last_check = models.CharField(max_length=100,default='N/A')
    host_uptime = models.CharField(max_length=50,default='Unkown')
    attempt_count = models.IntegerField(default=0)
    breakdown_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    snmp_alert_count = models.IntegerField(default=0)
    availability = models.CharField(max_length=20,default=0)
    def __unicode__(self):
        return self.host


class TrunkServers(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=150,blank=True)
    ip_address = models.IPAddressField()
    port = models.IntegerField(default = 9998)
    def __unicode__(self):
        return self.name

class Templates(models.Model):  #monitor template
    name = models.CharField(max_length=50, unique=True)
    service_list =  models.ManyToManyField('ServiceList')
    graph_list = models.ManyToManyField('Graphs',blank=True,null=True)
    # = models.ManyToManyField('Group',blank=True,null=True)
    
    def __unicode__(self):
        return self.name

class Services(models.Model):  #services list
    name = models.CharField(max_length=50,unique=True)
    monitor_type_list = (('agent','Agent'),('snmp','SNMP'),('wget','Wget'))
    monitor_type = models.CharField(max_length=50, choices=monitor_type_list)
    plugin = models.CharField(max_length=100) 
    item_list = models.ManyToManyField('Items')
    #trigger_list = models.ManyToManyField('triggers',blank=True)
    #trigger = models.ForeignKey('Triggers', null=True,blank=True)
    
    #flexible_intervals = 
    def __unicode__(self):
        return self.name

class Items(models.Model): # monitor item
    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=100,unique=True)
    data_type_option = (('float','Float'),('string','String'),('integer', 'Integer') ) 
    data_type = models.CharField(max_length=50, choices=data_type_option)
    unit = models.CharField(max_length=30,default='%')
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class ServiceList(models.Model): 
    name = models.CharField(max_length=50,unique=True)
    service = models.ForeignKey('Services')
    check_interval = models.IntegerField(default=300)
    conditons = models.ManyToManyField('Conditions',verbose_name=u'阀值列表',null=True,blank=True)
    #expression = models.CharField(max_length=1000)
    description = models.TextField()
    '''
    serverity_list = (('information','Information'),
                       ( 'warning' ,'Warning'),
                       ('critical', 'Critical'),
                       ('urgent','Urgent'),
                       ('disaster','Disaster') )
    serverity = models.CharField(max_length=30, choices=serverity_list)
    '''
    #dependencies 
    def __unicode__(self):
        return self.name

class Graphs(models.Model):
    name = models.CharField(max_length=50, unique=True)
    datasets = models.ManyToManyField('Items')
    graph_type = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

    
class Actions(models.Model):
    name = models.CharField(max_length=100,unique=True)
    condition_list = models.ManyToManyField('Conditions')
    operation_list = models.ManyToManyField('Operations')
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=250)
    recovery_notice = models.BooleanField(default=True)
    recovery_subject = models.CharField(max_length=100)
    recovery_message = models.CharField(max_length=250)
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return self.name
class Formulas(models.Model):
    name = models.CharField(max_length=64,unique=True)
    key = models.CharField(max_length=64,unique=True)
    memo = models.TextField()
    
    def __unicode__(self):
        return self.name 
    
class Operators(models.Model):
    name = models.CharField(max_length=32,unique=True)    
    key = models.CharField(max_length=32)    
    memo = models.TextField()
    def __unicode__(self):
        return self.name 
     
class Conditions(models.Model):
    name = models.CharField(max_length=100,unique=True)
    item = models.ForeignKey('Items', verbose_name=u'监控值')
    formula = models.ForeignKey('Formulas', verbose_name=u'运算函数',null=True,blank=True)
    operator = models.ForeignKey(Operators,verbose_name=u'运算符',null=True,blank=True)
    data_type = models.CharField(default='char',max_length=32, verbose_name=u'数据类型')
    threshold = models.CharField(max_length=64, verbose_name=u'阀值')
    def __unicode__(self):
        return self.name

class Operations(models.Model):
    send_to_users = models.ManyToManyField('UserProfile')
    send_to_groups = models.ManyToManyField('Group')
    notifier_type = (('email','Email'),('sms','SMS'))
    send_via = models.CharField(max_length=30,choices=notifier_type)
    notice_times = models.IntegerField(default=5)
    notice_interval = models.IntegerField(default=300, verbose_name='notice_interval(sec)')
"""
class plugins(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    plugin_file_name = models.CharField(max_length=150)
    def __unicode__(self):
	return self.name
"""
