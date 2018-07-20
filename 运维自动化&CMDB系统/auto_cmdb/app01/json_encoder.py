import db_conn
import django
django.setup()
import json
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

from app01.models import *

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)
    
a = Server.objects.get(asset_id=57)
b=LazyEncoder()
#default(a)