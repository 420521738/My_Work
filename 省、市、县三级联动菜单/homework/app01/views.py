# --*-- coding: utf-8 --*--

from django.shortcuts import render
from django.shortcuts import render_to_response
import json
from django.http.response import HttpResponse

data = {
        '广东':{
                    '广州':['天河区','越秀区','萝岗区','黄埔区'],
                    '深圳':['福田区','罗湖区','南山区'],
                    '茂名':['茂南区','茂港区','化州','高州']
            },
        '广西':{
                    '南宁':['青秀区','良庆区','江南区'],
                    '桂林':['象山区','叠彩区','阳朔'],
                    '贵港':['港北区','港南区','桂平','平南'],
                    '玉林':['石南','容县','陆川'],
            },
    }

def Index(request):
    return render_to_response('index.html')

###前端html过来获取的省列表
def GetProvince(request):
    result = data.keys()
    return HttpResponse(json.dumps(result))

###前端html过来获取的市列表
def GetCity(request):
    getData = request.GET
    ###前端的请求是Request('/getcity/',BindCity,{Id:provinceid})，get('Id')其实就是provinceid，也就是前端标签中的value的值
    provinceId = getData.get('Id')
    result = data.values()
    ###注意这个地方，前端发过来的数据是字符串，所以如果在后端想要用，需要将字符串int成整形
    result2 = result[int(provinceId)]
    result3 = result2.keys()
    return HttpResponse(json.dumps(result3))

###前端html过来获取的县（区）列表
def GetCounty(request):
    getData = request.GET
    provinceId = getData.get('proId')
    cityId = getData.get('cityId')
    result = data.values()
    result2 = result[int(provinceId)]
    result3 = result2.values()
    result4 = result3[int(cityId)]
    return HttpResponse(json.dumps(result4))


