#/usr/bin/env python
#coding:utf-8

from django.db import models
#from test.test_imageop import MAX_LEN
from django.contrib.auth.models import User

# Create your models here.

# bbs表
# blank=True 是说django admin里面可以为空；null=True 意思是表的这个字段可以为空
class BBS(models.Model):
    category = models.ForeignKey('Category')
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=256,blank=True,null=True)
    content = models.TextField()
    author = models.ForeignKey('BBS_user')
    # view_count 是浏览数
    view_count = models.IntegerField()
    # ranking 是排名
    ranking = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now_add = True)
    
    # 写这个函数，在使用的时候就会把内存地址所在的数据取出来，而不会展示内存地址
    def __unicode__(self):
        return self.title

# 评论表
# 不自己写了，使用django自带的评论表

# 板块表
class Category(models.Model):
    # unique 代表这一条是唯一值，但它不是主键
    name =models.CharField(max_length=32,unique=True)
    administrator = models.ForeignKey('BBS_user')
    
    # 写这个函数，在使用的时候就会把内存地址所在的数据取出来，而不会展示内存地址
    def __unicode__(self):
        return self.name

# 用户表
# 用户可能需要扩展，比如用户加个自定义头像啊什么的，所以user需要继承django的额user，再进行自定义
class BBS_user(models.Model):
    # ForeignKey是一对多，OneToOneField是一对一,OneToOneField也是外键的一种
    user = models.OneToOneField(User)
    # signature是用户个性签名
    signature = models.CharField(max_length=128,default='这个家伙很懒，什么也没留下')
    # photo 是用户头像 
    photo = models.ImageField(upload_to="upload_imgs/",default="upload_imgs/user-1.jpg")
    
    def __unicode__(self):
        return self.user.username

    
    