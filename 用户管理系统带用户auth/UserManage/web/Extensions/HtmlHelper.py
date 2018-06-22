#!/usr/bin/env python
#coding:utf-8

from django.utils.safestring import mark_safe

def Pager(baseurl,currentpage,totalcount,totalpage,pagernum=11):
    currentpage = int(currentpage)
    totalpage = int(totalpage)
    if currentpage>=totalpage:
        currentpage = totalpage
    pagernum = int(pagernum)
    prev = currentpage - 1
    next = currentpage + 1
    if currentpage<=1:
        prev_str = '<li class="disabled"><a href="#">上一页</a></li>'
    else:
        prev_str = '<li><a href="#" onclick="ChangePager(%d);return false;">上一页</a></li>' %(currentpage-1,)
        
    if next>=totalpage:
        next_str = '<li class="disabled"><a href="#">下一页</a></li>'
    else:
        next_url = baseurl+str(currentpage+1)
        next_str = '<li><a href="#" onclick="ChangePager(%d);return false;">下一页</a></li>' %(currentpage+1,)
    
    first_str = '<li><a href="#" onclick="ChangePager(%d);return false;">首页</a></li>' %(1,)
    end_str = '<li><a href="#" onclick="ChangePager(%d);return false;">末页</a></li>' %(totalpage,)
    pagelist = []
    
    start =  1 if currentpage-5<1 else currentpage-5
    if start<6:
        end = 11
    else:
        end = totalpage if currentpage + 5>totalpage else currentpage + 5
    if end >totalpage:
        end = totalpage
    
    for i in range(start,end+1):
        url = baseurl + str(i)
        if currentpage == i :
            pagelist.append('<li class="active"><a href="#" onclick="ChangePager(%d);return false;">%d</a></li>' %(i,i,))
        else:
            pagelist.append('<li><a href="#" onclick="ChangePager(%d);return false;">%d</a></li>' %(i,i,))
    total_str = ('<li><a href="javascript:void(0);">共 %d 页/ %d 条数据</a></li>' %(totalpage,totalcount,))
    result = first_str + prev_str + ''.join(pagelist) + next_str + end_str +total_str
    
    return mark_safe(result)


def Pager2(baseurl,currentpage,totalcount,totalpage,pagernum=11):
    currentpage = int(currentpage)
    totalpage = int(totalpage)
    if currentpage>=totalpage:
        currentpage = totalpage
    pagernum = int(pagernum)
    prev = currentpage - 1
    next = currentpage + 1
    if currentpage<=1:
        prev_str = '<li class="disabled"><a href="#">上一页</a></li>'
    else:
        prev_url = baseurl+str(currentpage-1)
        prev_str = '<li><a href="%s">上一页</a></li>' %(prev_url,)
        
    if next>=totalpage:
        next_str = '<li class="disabled"><a href="#">下一页</a></li>'
    else:
        next_url = baseurl+str(currentpage+1)
        next_str = '<li><a href="%s">下一页</a></li>' %(next_url,)
    
    first_str = '<li><a href="%s">首页</a></li>' %(baseurl+'1',)
    end_str = '<li><a href="%s">末页</a></li>' %(baseurl+str(totalpage),)
    pagelist = []
    
    start =  1 if currentpage-5<1 else currentpage-5
    if start<6:
        end = 11
    else:
        end = totalpage if currentpage + 5>totalpage else currentpage + 5
    if end >totalpage:
        end = totalpage
    
    for i in range(start,end+1):
        url = baseurl + str(i)
        if currentpage == i :
            pagelist.append('<li class="active"><a href="%s">%d</a></li>' %(url,i,))
        else:
            pagelist.append('<li><a href="%s">%d</a></li>' %(url,i,))
    total_str = ('<li><a href="javascript:void(0);">共 %d 页/ %d 条数据</a></li>' %(totalpage,totalcount,))
    result = first_str + prev_str + ''.join(pagelist) + next_str + end_str +total_str
    
    return mark_safe(result)


def SelectOption(valueTextList,selected):

    template = '''<option value='%s'>%s</option>'''
    template_selected = '''<option value='%s'>%s</option>'''
    optionList = []
    try:
        for item in valueTextList:
            if selected == item[1]:
                content = template_selected %(item[1],item[0])
            else:
                content = template %(item[1],item[0])
            optionList.append(content)
    except Exception,e:
        return mark_safe('''<option>请求异常.</option>''')
    result = ''.join(optionList)
    return mark_safe(result)


def SelectOptionAssetType(valueTextList,selected):

    template = '''<option value='%s'>%s</option>'''
    template_selected = '''<option value='%s' selected='selected'>%s</option>'''
    optionList = []
    try:
        for item in valueTextList:
            if selected == item['type']:
                content = template_selected %(item['table']+'__'+item['type'],item['type'])
            else:
                content = template %(item['table']+'__'+item['type'],item['type'])
            optionList.append(content)
    except Exception,e:
        return mark_safe('''<option>请求异常.</option>''')
    result = ''.join(optionList)
    return mark_safe(result)

