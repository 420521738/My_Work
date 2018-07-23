from django import forms
from django.contrib import admin
import models




class TemplatesAdmin(admin.ModelAdmin):
    #form = TemplatesForm

    list_display = ('name',)

    filter_horizontal = ('service_list','graph_list')

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'monitor_type')
    filter_horizontal = ('item_list',)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name','key','data_type','enabled')

class StatusAdmin(admin.ModelAdmin):
    search_fields = ('host','host_status')
    list_display = ('host','host_status','ping_status','availability','host_uptime','breakdown_count','up_count','attempt_count')

class TriggersAdmin(admin.ModelAdmin):
    list_display = ('name','service','check_interval')
    filter_horizontal = ('conditons',)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('link_name','url','color')
class HostAdmin(admin.ModelAdmin):
    list_display = ('id','display_name','hostname','ip','port','idc','status_monitor_on')
    filter_horizontal = ('template_list','custom_services')
class CondtionAdmin(admin.ModelAdmin):
    list_display=('name','item','formula','operator','threshold')
admin.site.register(models.Idc)
admin.site.register(models.Host,HostAdmin)
admin.site.register(models.Group)
admin.site.register(models.UserProfile)
admin.site.register(models.ServerStatus,StatusAdmin)
admin.site.register(models.Templates,TemplatesAdmin)
admin.site.register(models.Services,ServicesAdmin)
admin.site.register(models.Items,ItemsAdmin)
admin.site.register(models.ServiceList,TriggersAdmin)
admin.site.register(models.Graphs)
admin.site.register(models.Operations)
admin.site.register(models.Actions)
admin.site.register(models.TrunkServers)
admin.site.register(models.Conditions,CondtionAdmin)
admin.site.register(models.Formulas)
admin.site.register(models.Operators)

