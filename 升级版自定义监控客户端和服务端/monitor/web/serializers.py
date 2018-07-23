
from rest_framework import serializers
import models



class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = ('id','hostname','ip','port','status_monitor_on','template_list')
        depth = 3
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