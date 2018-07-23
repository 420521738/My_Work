#!/usr/local/src/python/bin/python
import urllib, urllib2
from subprocess import PIPE,Popen
import re
import platform
monitor_info_dic={}

def getHostInfo():
    pd ={}
    version = platform.dist()
    os_name = platform.node()
    os_release = platform.release()
    os_version = '%s %s' % (version[0],version[1])
    pd['os_name'] = os_name
    pd['os_release'] = os_release
    pd['os_version'] = os_version
    return pd

def getSysInfo():
    pd = {}
    fd = {}
    p = Popen('dmidecode',shell=True,stdout=PIPE)
    stdout, stderr = p.communicate()
    line_in = False
    for line in stdout.split('\n'):
        if line.startswith('System Information'):
            line_in = True
            continue
        if line.startswith('\t') and line_in:
            k, v  = [i.strip() for i in line.split(':')]
            pd[k] = v
        else:
            line_in = False
    name = "Manufacturer:%s ; Serial_Number:%s ; Product_Name:%s" % (pd['Manufacturer'],pd['Serial Number'],pd['Product Name'])
    for i in name.split(';'):
        k, v = [j.strip() for j in i.split(':')]
        fd[k] = v
    return fd
def getNetInfo():
    p = Popen(['ifconfig'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    device = re.compile(r'(eth\d)')
    ipaddr = re.compile(r'(inet addr:[\d.]{7,15})')
    mac = re.compile(r'(HWaddr\s[0-9A-Fa-f:]{17})')
    link = re.compile(r'(Link encap:[\w]{3,14})')
    mask = re.compile(r'(Mask:[\d.]{9,15})')
    for lines in stdout.strip().split('\n\n'):
        pd = {}
        eth_device = re.search(device,lines)
        inet_ip = re.search(ipaddr,lines)
        hw = re.search(mac,lines)
        link_encap = re.search(link,lines)
        _mask = re.search(mask,lines)
        if eth_device:
            if eth_device:
                Device = eth_device.groups()[0]
            if inet_ip:
                Ipaddr =  inet_ip.groups()[0].split(':')[1]
            if hw:
                Mac = hw.groups()[0].split()[1]
            if link_encap:
                Link = link_encap.groups()[0].split(':')[1]
            if _mask:
                Mask = _mask.groups()[0].split(':')[1]
            pd['Device'] = Device
            pd['Ipaddr'] = Ipaddr
            pd['Mac'] = Mac
            pd['Link'] = Link
            pd['Mask'] = Mask
            yield pd
            
def getMemInfo():
    p = Popen(['dmidecode'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    line_in = False
    mem_str = ''
    pd = {}
    fd = {}
    for line in stdout.strip().split('\n'):
        if line.startswith('Memory Device') and line.endswith('Memory Device'):
            line_in = True
            mem_str+='\n'
            continue
        if line.startswith('\t') and line_in:
            mem_str+=line
        else:
            line_in = False
    for i in mem_str.split('\n')[1:]:
        lines = i.replace('\t','\n').strip()
        for ln in lines.split('\n'):
            k, v = [i for i in ln.split(':')]
            pd[k.strip()] = v.strip()
        if pd['Size'] != 'No Module Installed':
            mem_info = 'Size:%s  ; Part_Number:%s ; Manufacturer:%s' % (pd['Size'],pd['Part Number'],pd['Manufacturer'])
            for line in mem_info.split('\n'):
                for word in line.split(';'):
                    k, v = [i.strip() for i in word.split(':')]
                    fd[k] = v.strip()
                yield fd
                
def getCpuInfo():
    p = Popen(['cat','/proc/cpuinfo'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    pd = {}
    model_name = re.compile(r'.*model name\s+:\s(.*)')
    vendor_id = re.compile(r'vendor_id\s+:(.*)')
    cpu_cores = re.compile(r'cpu cores\s+:\s([\d]+)')
    lines = [line for line in stdout.strip().split('\n')]
    for line in lines:
        model = re.match(model_name,line)
        vendor = re.match(vendor_id,line)
        cores = re.match(cpu_cores,line)
        if model:
            pd['Model_Name'] = model.groups()[0].strip()
        if vendor:
            pd['Vendor_Id'] = vendor.groups()[0].strip()
        if cores:
            pd['Cpu_Cores'] = cores.groups()[0]
        else:
            pd['Cpu_Cores'] = int('1')
    return pd

def getDiskInfo():
    disk_dev = re.compile(r'Disk\s/dev/[a-z]{3}')
    disk_name = re.compile(r'/dev/[a-z]{3}')
    p = Popen(['fdisk','-l'],shell=False,stdout=PIPE)
    stdout, stderr = p.communicate()
    for i in stdout.split('\n'):
        disk = re.match(disk_dev,i)
        if disk:
            dk = re.search(disk_name,disk.group()).group()
    n = Popen('smartctl -i %s' % dk,shell=True,stdout=PIPE)
    stdout, stderr = n.communicate()
    ld = []
    pd = {}
    device_model = re.compile(r'(Device Model):(\s+.*)')
    serial_number = re.compile(r'(Serial Number):(\s+[\d\w]{1,30})')
    firmware_version = re.compile(r'(Firmware Version):(\s+[\w]{1,20})')
    user_capacity = re.compile(r'(User Capacity):(\s+[\d\w, ]{1,50})')
    for line in stdout.strip().split('\n'):
        serial = re.search(serial_number,line)
        device = re.search(device_model,line)
        firmware = re.search(firmware_version,line)
        user = re.search(user_capacity,line)
        if device:
            pd['Device_Model'] = device.groups()[1].strip()
        if serial:
            pd['Serial_Number'] = serial.groups()[1].strip()
        if firmware:
            pd['Firmware_Version'] = firmware.groups()[1].strip()
        if user:
            pd['User_Capacity'] = user.groups()[1].strip()
    return pd
    
def monitor():
    monitor_info_dic={}
    monitor_info_dic['data_value']={'HostInfo':getSysInfo(),
                                'DiskInfo':getDiskInfo(),
                                ' CpuInfo':getCpuInfo(),
                                'MemInfo':getMemInfo() }
    
    monitor_info_dic['status']='1'
    
    return monitor_info_dic
'''    
def getHostTotal():
    ld = []
    cpuinfo = parserCpuInfo(getCpuInfo())
    diskinfo = parserDiskInfo(getDiskInfo())
    for i in  parserMemInfo(getMemInfo()):
        meminfo = i
    productinfo = parserDMI(getDMI())
    hostinfo = getHostInfo()
    ipaddr = parserIpaddr(getIpaddr())
    for i in ipaddr:
        ip = i
    for k in cpuinfo.iteritems():
        ld.append(k)
    for i in diskinfo.iteritems():
        ld.append(i)
    for j in meminfo.iteritems():
        ld.append(j)
    for v in productinfo.iteritems():
        ld.append(v)
    for x in hostinfo.iteritems():
        ld.append(x)
    for y in ip.iteritems():
        ld.append(y)
    return ld
def parserHostTotal(hostdata):
    pg = {}
    for i in hostdata:
        pg[i[0]] = i[1]
    return pg
def urlPost(postdata):
    data = urllib.urlencode(postdata)
    req = urllib2.Request('http://132.96.77.12:8000/api/collect',data)
    response = urllib2.urlopen(req)
    return response.read()
'''
if __name__ == '__main__':
    #hostdata = getHostTotal()
    #postdata = parserHostTotal(hostdata)
    #print urlPost(postdata)
    #print hostdata
    print monitor()