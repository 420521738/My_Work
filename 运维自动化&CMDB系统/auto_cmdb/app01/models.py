#/usr/bin/env python
#coding:utf-8

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import default

# 最顶级的通用资产信息表
class Asset(models.Model):  
    device_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('acc_cpu', u'CPU'),
        ('acc_memory', u'内存条'),
        ('acc_disk', u'硬盘'),
        ('acc_network_adapter', u'网卡'),
        ('acc_monitor', u'显示器'),
        ('acc_others', u'其它配件'),
    )
    # 设备类型
    device_type = models.CharField(choices=device_type_choices,max_length=64, default='server')
    # 显示名称
    name = models.CharField(max_length=30)
    # 主机名，唯一
    hostname= models.CharField(max_length=32, blank=True, unique=True)
    #sn = models.CharField(u'资产SN号',max_length=64, unique=True,null=True, blank=True)
    #manufactory = models.ForeignKey('Manufactory',verbose_name=u'制造商',null=True, blank=True)
    #model = models.ForeignKey('ProductVersion', verbose_name=u'型号')
    # 跟行政部门对接的资产id，行政部门也有自己建立的资产id
    asset_op = models.CharField(max_length=32,blank=True,null=True)
    # 合同
    contract = models.ForeignKey('Contract', verbose_name=u'合同',null=True, blank=True)
    # 购买时间
    trade_time = models.DateTimeField(u'购买时间',null=True, blank=True)
    # 保修期
    warranty = models.SmallIntegerField(u'保修期',null=True, blank=True)
    # 价格
    price = models.IntegerField(u'价格',null=True, blank=True)
    # 属于的业务线
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'属于的业务线',null=True, blank=True)
    # 上面跑了什么功能
    function = models.CharField(max_length=32,blank=True,null=True)
    # 设备管理员是谁
    admin = models.ForeignKey('UserProfile', verbose_name=u'设备管理员',related_name='+',null=True, blank=True)
    # 业务使用方是谁
    client = models.ForeignKey('UserProfile', verbose_name=u'业务使用方',null=True, blank=True)
    # 在哪个机房
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房',null=True, blank=True)
    # 在哪个机柜
    cabinet_num = models.CharField(u'机柜号',max_length=30,null=True, blank=True)
    # 机柜中序号
    cabinet_order = models.SmallIntegerField(u'机柜中序号',max_length=30,null=True, blank=True)
    status_choice = (
        (1, 'Init'),
        (2, 'Standby'),
        (3, 'Online'),
        (4, 'Offline'),
        (5, 'Unreachable'),
        # 弃用，可以理解为报废了
        (6, 'Deprecated'),
        (7, 'Maintenance'),
    )
    # 设备状态
    status = models.SmallIntegerField(u'设备状态', choices=status_choice,null=True, blank=True)
    #Configuration = models.OneToOneField('Configuration',verbose_name='配置管理',blank=True,null=True)
    
    memo = models.TextField(u'备注', null=True, blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
     
    #maintain_record = models.ManyToManyField('Maintainence', verbose_name='维护变更纪录')
    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"
    def __unicode__(self):
        return 'id:%s h:%s'  %(self.id,self.hostname)        
    
class Configuration(models.Model):
    '''store all the configurations of this asset'''
    definded_raid_type = models.CharField(verbose_name=u'预定义raid类型',max_length=32,blank=True,null=True)
    primary_ip = models.ManyToManyField('NIC', verbose_name=u'网卡列表',blank=True )
    os = models.ForeignKey('Software', verbose_name='OS', blank=True,null=True)
    
    os_installed = models.BooleanField(default=1)
    puppet_installed = models.BooleanField(default=1)
    zabbix_configured = models.BooleanField(default=1)
    auditing_configured = models.BooleanField(default=1)
    approved = models.BooleanField(default=1)
    
    def __unicode__(self):
        return '%s ' % self.id
    
class Server(models.Model):
    # 资产，一对一对应，必须一一对应的
    asset = models.OneToOneField('Asset')
    # 创建这个设备，可以自动创建，可以人为创建
    created_by = models.CharField(max_length=32,default='auto') #auto: auto created,   manual:created manually 
    # 序列号，sn号是有可能重复的,所以不设置唯一
    sn = models.CharField(u'SN号',max_length=64)
    # 哪个厂商的
    manufactory = models.CharField(verbose_name=u'制造商',max_length=128,null=True, blank=True)
    # 型号
    model = models.CharField(u'型号',max_length=128,null=True, blank=True )
    # 若有多个CPU，型号应该都是一致的，故没做ForeignKey，CPU个数
    cpu_count = models.SmallIntegerField(u'cpu个数',blank=True)
    # CPU核数
    cpu_core_count = models.SmallIntegerField(u'cpu核数',blank=True)
    # CPU类型,CPU详细信息外键到CPU表中
    cpu_model = models.ForeignKey('CPU')    
    # 网卡，选择ManyToManyField是因为NIC表中可能有多张网卡属于同一台服务器
    nic = models.ManyToManyField('NIC', verbose_name=u'网卡列表')
    # 硬盘 的raid类型
    raid_type = models.TextField(u'raid类型', blank=True)
    # 硬盘
    physical_disk_driver = models.ManyToManyField('Disk', verbose_name=u'硬盘',blank=True) 
    # raid卡信息
    raid_adaptor = models.ManyToManyField('RaidAdaptor', verbose_name=u'Raid卡',blank=True) 
    # memory
    ram_size = models.IntegerField(u'内存总大小GB',blank=True)
    # 内存的配置
    ram = models.ManyToManyField('Memory', verbose_name=u'内存配置',blank=True)
    
    # software，装了什么软件
    software = models.ManyToManyField('Software', verbose_name=u'软件',null=True, blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now_add=True)  
    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"   
        index_together = ["sn", "asset"]
        
    def __unicode__(self):
        return '%s sn:%s' %(self.asset.hostname,self.sn)
class NetworkDevice(models.Model):
    # 这里的大多数跟Server里面的类似，就不多做重复说明
    asset = models.OneToOneField('Asset') 
    sn = models.CharField(u'SN号',max_length=64,unique=True)
    manufactory = models.CharField(verbose_name=u'制造商',max_length=128,null=True, blank=True)
    model = models.CharField(u'型号',max_length=128,null=True, blank=True )
    # 固件版本
    firmware = models.ForeignKey('Software')
    # 端口个数
    port_num = models.SmallIntegerField(u'端口个数')
    # 设置详细配置
    device_detail = models.TextField(u'设置详细配置')
    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"   
class Software(models.Model):
    # 软件的信息
    #sn = models.CharField(u'SN号',max_length=64, unique=True)
    os_types_choice = (
        (1, 'GNU/Linux'),
        (2, 'MS/Windows'),
        (3, 'Network Firmware'),
        (4, 'Softwares'),
    )
    types = models.SmallIntegerField(u'系统类型', choices=os_types_choice, max_length=64,help_text=u'eg. GNU/Linux')  
    version = models.CharField(u'软件/系统版本', max_length=64, help_text=u'eg. CentOS release 6.5 (Final)', unique=True)
    #version = models.CharField(u'版本号', max_length=64,help_text=u'2.6.32-431.3.1.el6.x86_64' )
      
    def __unicode__(self):
        return self.version    
    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = "软件/系统"           
class Disk(models.Model):
    # 硬盘的序号
    sn = models.CharField(u'SN号', max_length=128, blank=True)
    # 硬盘在哪个服务器上，服务器的sn号
    parent_sn = models.CharField(max_length=128,blank=True)
    slot = models.CharField(u'插槽位',max_length=32,blank=True)
    manufactory = models.CharField(u'制造商', max_length=32,default=None,blank=True)
    model = models.CharField(u'磁盘型号', max_length=128,blank=True)
    capacity = models.FloatField(u'磁盘容量GB',blank=True)
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64,choices=disk_iface_choice,blank=True)
    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)    
    class Meta:
        # parent_sn 和 slot 做一个唯一的值
        unique_together = ("parent_sn", "slot")
        verbose_name = '硬盘部件'
        verbose_name_plural = "硬盘部件"      
    def __unicode__(self):
        return 'slot:%s size:%s' % (self.slot,self.capacity)
class CPU(models.Model):
    sn = models.CharField(u'SN号',max_length=64,blank=True)
    parent_sn = models.CharField(max_length=128,blank=True, unique=True)
    manufactory = models.CharField(u'制造商', max_length=32,default=None,blank=True)
    model = models.CharField(u'CPU型号', max_length=64,blank=True)
    memo = models.TextField(u'备注', blank=True)
    class Meta:

        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"   
    def __unicode__(self):
        return self.model
class Monitor(models.Model):
    asset = models.OneToOneField('Asset') 
    sn = models.CharField(u'SN号',max_length=64, unique=True)
    manufactory = models.CharField(u'制造商', max_length=32,default=None)
    model = models.CharField(u'显示设备型号', max_length=64)
    memo = models.TextField(u'备注', blank=True)
    class Meta:
        verbose_name = '显示设备'
        verbose_name_plural = "显示设备"   
    def __unicode__(self):
        return self.model
        
class NIC(models.Model):
    name = models.CharField(u'插口',max_length=128,blank=True)
    sn = models.CharField(u'SN号',max_length=128,blank=True)
    parent_sn = models.CharField(max_length=128,blank=True)
    model = models.CharField(u'网卡型号', max_length=128,blank=True)
    manufactory = models.CharField(u'制造商', max_length=32, blank=True)
    # TODO: 如果一个网卡有多个IP，那么需要将IP独立为一个model，做ForeignKey
    ipaddr = models.IPAddressField(u'ip地址',blank=True)
    mac = models.CharField(u'网卡mac地址', max_length=64)
    netmask = models.CharField(max_length=64,blank=True)
    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
    class Meta:
        unique_together = ("name", "mac")
        verbose_name = '网卡部件'
        verbose_name_plural = "网卡部件"   
    def __unicode__(self):
        return '%s:%s' %(self.name,self.ipaddr)    
        
class RaidAdaptor(models.Model):
    sn = models.CharField(u'SN号', max_length=128,blank=True)
    name = models.CharField(u'插口',max_length=32,blank=True)
    parent_sn = models.CharField(max_length=128,blank=True)
    model = models.CharField(u'型号', max_length=64,blank=True)
    memo = models.TextField(u'备注', blank=True)
    def __unicode__(self):
        return self.name 
    class Meta:
        unique_together = ("parent_sn", "name")
    
# 10w台服务器，每个机器4条内存估算，memory表行数是40w
class Memory(models.Model):
    sn = models.CharField(u'SN号', max_length=128,blank=True)
    parent_sn = models.CharField(max_length=128,blank=True)
    model = models.CharField(u'型号', max_length=64,blank=True)
    manufactory = models.CharField(u'制造商', max_length=32,null=True,blank=True)
    slot = models.CharField(u'插槽位',max_length=32,blank=True)
    capacity =  models.FloatField(u'容量',blank=True)
    # 如果内存没有sn的话，可以用model做PK
   
    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
    class Meta:
        unique_together = ("parent_sn", "slot")
        verbose_name = '内存部件'
        verbose_name_plural = "内存部件"   
    def __unicode__(self):
        if self.capacity != 0:
            return '%s: %sGB '%( self.slot, self.capacity)   
        else:  
            return self.slot
class Contract(models.Model):
    sn = models.CharField(u'合同号', max_length=64,unique=True)
    name = models.CharField(u'合同名称', max_length=64 )
    memo = models.TextField(u'备注', blank=True)
    cost = models.IntegerField(u'合同金额')
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    license_num = models.IntegerField(u'license数量',blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"     
    def __unicode__(self):
        return self.name
        
class IDC(models.Model):
    name = models.CharField(u'机房english',max_length=30)
    display_name = models.CharField(u'中文显示名',max_length=32,default=None)
    region = models.CharField(u'区域',max_length=64,default=None)
    region_display_name = models.CharField(u'区域中文',max_length=64,default=None)
    isp = models.CharField(u'运营商',max_length=32,default=None)
    isp_display_name = models.CharField(u'运营商中文',max_length=32,default=None)
    floor = models.IntegerField(u'楼层',default=1)
    memo = models.CharField(u'备注',max_length=64)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"  
        
class Manufactory(models.Model):
    name = models.CharField(u'厂商名称',max_length=64, unique=True)
    support_num = models.CharField(u'支持电话',max_length=30,blank=True)
    memo = models.CharField(u'备注',max_length=30,blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"          
class ProductVersion(models.Model):
    name = models.CharField(u'产品型号',max_length=64, unique=True)
    version = models.CharField(u'产品版本号',max_length=64,blank=True)
    def __unicode__(self):
        return self.name    
class BusinessUnit(models.Model):
    # 业务线，比如广告线、论坛线等等
    name = models.CharField(u'业务线',max_length=64, unique=True)
    memo = models.CharField(u'备注',max_length=64, blank=True)
    def __unicode__(self):
        return self.name 
    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"  
class UserProfile(models.Model):
    # CMDB里面的所有账号，以后会延伸到运维系统的所有账号都来自于这里
    # 页面登录认证的用户
    user = models.OneToOneField(User)
    name = models.CharField(u'名字', max_length=32)
    # 可以是单点登录认证
    token = models.CharField(u'token', max_length=128)
    department = models.CharField(u'部门', max_length=32)
    business_unit = models.ManyToManyField(BusinessUnit)
    email = models.EmailField(u'邮箱')
    phone = models.CharField(u'座机', max_length=32)
    mobile = models.CharField(u'手机', max_length=32)
    # 备用联系人，如果这个人找不到，可以查这个备份联系人，self是自己表，备用联系人还是在这个表里
    backup_name = models.ForeignKey('self', verbose_name=u'备用联系人',blank=True,null=True,related_name='user_backup_name')
    leader = models.ForeignKey('self', verbose_name='上级领导',blank=True,null=True)
    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = "用户信息" 
    def __unicode__(self):
        return self.name
class Maintainence(models.Model):
    # 所有的硬件变更都会在这个表里存
    name = models.CharField(u'事件名称', max_length=100)
    change_choices = (
        (1,u'硬件更换'),
        (2,u'新增配件'),
        (3,u'设备下线'),
        (4,u'设备上线'),
        (5,u'定期维护'),
        (6,u'业务上线\更新\变更'),
        (7,u'其它'),
    )
    maintain_type = models.SmallIntegerField(u'变更类型', choices= change_choices,max_length=30)
    description = models.TextField(u'事件描述')
    # 这里一定要存一个AssetID，这个变更是谁产生的，跟谁有关系
    device_sn = models.CharField('AssetID',max_length=64,blank=True)
    event_start = models.DateTimeField(u'事件开始时间',blank=True)
    event_end = models.DateTimeField(u'事件结束时间',blank=True)
    applicant = models.ForeignKey('UserProfile',verbose_name=u'发起人',related_name='applicant_user')
    performer = models.ForeignKey('UserProfile',verbose_name=u'执行人')
    memo = models.TextField(u'备注', blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '变更纪录'
        verbose_name_plural = "变更纪录" 

class EventLog(models.Model):
    # 所有的自动汇报如果出现问题就会存在这里，异常都会抓住存这里
    uuid = models.CharField(u'请求ID', max_length=128, unique=True)
    post_data = models.TextField(u'请求Data',blank=True)
    detail = models.TextField(u'详细描述' ,blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True,null=True)
    def __unicode__(self):
        return self.uuid


class ApiAuth(models.Model):
    # 接口认证
    url = models.CharField(u'接口url',max_length=64)
    description = models.CharField(u'简介', max_length=64)
    method_choice = (
        ('GET', '允许Get(可读)'),          
        ('POST', '允许POST(可修改)') ,         
        ('PUT', '允许PUT(可 创建)') ,         
        ('HEAD', 'HEAD(暂不用)') ,         
        ('PATCH', 'PATCH(暂不用)') ,         
                     )
    method_type = models.CharField(u'可用方法',choices=method_choice,max_length=32 )
    users = models.ManyToManyField(UserProfile, null=True)
    
    class Meta:
        unique_together = ("url", "method_type")
        verbose_name = '接口权限'
        verbose_name_plural = "接口权限"    
    def __unicode__(self):
        return '%s:: %s' %(self.method_type,self.url)