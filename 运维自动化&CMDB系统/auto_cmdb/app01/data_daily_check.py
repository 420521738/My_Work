#_*_coding:utf8_*_
import datetime
import db_conn
import django
django.setup()
from app01 import models


class DailyChecks(object):
    def __init__(self):
        pass
    
    def get_unreported(self):
        last_day_time = datetime.datetime.now() -  datetime.timedelta(days=1)
        print last_day_time
        total_online_asset = models.Asset.objects.filter(device_type='server',status=3).values_list('id')
        total_updates =   models.Server.objects.filter(update_at__gt=last_day_time, asset__status=3).values_list('asset__id')
        total_updates2 =   models.Server.objects.filter(update_at__gt=last_day_time, asset__status=3)
        differ =  set(total_online_asset) -set(total_updates) #didn't receive update in last 24 hours for some reason
        unupdated_list = map(lambda x:x[0], differ)
        res_list = models.Asset.objects.filter(id__in=unupdated_list)
        print len(res_list)
        for i in  total_updates2:
            print i.id, i.update_at,i.create_at
if __name__ == '__main__':
    test = DailyChecks()
    test.get_unreported()