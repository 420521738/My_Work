#!/usr/bin/env python
#coding:utf-8

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from app01.models import *

# Serializers define the API representation.
# 你要用Serializer去表现哪个表里的数据，跟我们的form是差不多的
# 把model里面的数据变成可序列化的，是在页面上显示的，不是我们平时说的pkile
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        #fields = ('url', 'name')
        
class AssetSerializer(serializers.HyperlinkedModelSerializer):
    #sn = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Asset
class AssetSerializer2(serializers.HyperlinkedModelSerializer):
    #id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Asset
        depth = 2
        fields = ('id','device_type','name','hostname','server','asset_op','contract','trade_time' ,'warranty','price','business_unit','admin','client', 'idc',
            'cabinet_num',
            'cabinet_order' ,
            ''
            'status',
            'memo',
            'create_at',
            'update_at')
class BusinessUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BusinessUnit
        '''fields = (
            'url',
           'name', 
        )'''
class ManufactorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufactory
class ProductVersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductVersion
class ContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contract
class IDCSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IDC
            
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    #user = UserSerializer()
    #backup_name = UserSerializer()
    #leader = UserSerializer()
    #business_unit = BusinessUnitSerializer()
    class Meta:
        model = UserProfile
#class ServerSerializer(serializers.HyperlinkedModelSerializer):
class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server 
        #depth = 2
class ServerSerializer2(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server 
        #depth = 2
class NetworkDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NetworkDevice 
class SoftwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Software 
class DiskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Disk 
class CPUSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CPU 
class MonitorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Monitor 
class NICSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NIC 
class RaidAdaptorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RaidAdaptor 
class MemorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Memory 
class MaintainenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Maintainence 