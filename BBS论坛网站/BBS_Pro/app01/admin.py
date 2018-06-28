#/usr/bin/env python
#coding:utf-8

from django.contrib import admin
from app01 import models
# Register your models here.

class BBS_admin(admin.ModelAdmin):
    list_display = ('title','summary','author','signature','view_count','create_at')
    list_filter = ('create_at',)
    search_fields = ('title','author__user__username')
    def signature(self,obj):
        return obj.author.signature
    signature.short_description = '个性签名'
admin.site.register(models.BBS,BBS_admin)
admin.site.register(models.Category)
admin.site.register(models.BBS_user)
