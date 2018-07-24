
from rest_framework import serializers
import models
from django.utils import timezone


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = ('id','hostname','group','ip','port','status_monitor_on','template_list')
        depth = 3
class HostProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = ('id','hostname','group','ip','port','status_monitor_on','template_list','poll_interval')
        



class DateTimeTzAwareField(serializers.DateTimeField):

    def to_native(self, value):
        value = timezone.localtime(value)
        return super(DateTimeTzAwareField, self).to_native(value)           
         
class TaskCenterSerializer(serializers.ModelSerializer):
    #kick_off_at = DateTimeTzAwareField()
    class Meta:
        model = models.TaskCenter
        #fields = ('id',)
    
'''
class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Templates
        #fields = ('hostname','ip','port','status_monitor_on')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Services

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Items
class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceList
class ConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conditions
'''