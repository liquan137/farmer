from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *
from django.template import loader
import json
import time


# Create your views here.
# objects.get()结果转换
def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state" and kk != "password"])


# 首页
def index(request):
    template = loader.get_template('home/index.html')
    list = []
    list_data = {
        'm_title': '柑桔13886725378特早蜜桔，叶桔，蜜橘桔子',
        'm_address_belong': '1564',
        'create_time': '1564658781'
    }
    for i in range(0, 10):
        list.append(list_data)
    context = {
        'list': list
    }
    return HttpResponse(template.render(context, request))


# 登陆
def login(request):
    if request.userInfo != None:
        return HttpResponseRedirect(request.session.get('from'))
    template = loader.get_template('home/login.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


# 注册
def register(request):
    if request.userInfo != None:
        return HttpResponseRedirect(request.session.get('from'))
    template = loader.get_template('home/register.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


# 完善信息
def registerReg(request):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')
    template = loader.get_template('home/registerReg.html')
    userInfo = p_menber.objects.get(username=request.userInfo['username'])
    userInfo = object_to_json(userInfo)
    context = {
        'userInfo': userInfo
    }
    return HttpResponse(template.render(context, request))


# 登出操作
def logout(request):
    template = loader.get_template('home/logout.html')
    if request.userInfo != None:
        del request.session['user_id']
    context = {
    }
    return HttpResponse(template.render(context, request))


# 忘记密码
def forget(request):
    # if request.userInfo == None:
    #     return HttpResponseRedirect('/login')
    template = loader.get_template('home/forget.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


# 发布信息-选择类别
def publish(request):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')
    template = loader.get_template('home/publish.html')
    try:
        selectList = p_product.objects.all()
        list = []
        for item in selectList:
            list.append({
                'link': item.id,
                'title': item.p_name,
                'child': []
            })
        if len(list) > 0:
            for item in list:
                searchChilds = p_product_child.objects.filter(p_id=item['link'])
                for searchChild in searchChilds:
                    list[list.index(item)]['child'].append({
                        'link': searchChild.id,
                        'title': searchChild.p_name,
                        'p_id': searchChild.p_id,
                        'child': []
                    })
        else:
            None
        print(list)
    except:
        list = []
    context = {
        'list': list
    }
    return HttpResponse(template.render(context, request))


# 发布信息
def publishDetail(request, father, child):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')

    if father != None and child != None:
        if isinstance(father, int) and isinstance(child, int):
            template = loader.get_template('home/publishDetail.html')
            try:
                fatherObj = p_product.objects.get(id=father)
                childObj = p_product_child.objects.get(id=child)
                userInfo = p_menber.objects.get(username=request.userInfo['username'])
                userInfo = object_to_json(userInfo)
                nowChoose = {
                    'f_name': fatherObj.p_name,
                    'c_name': childObj.p_name
                }
            except:
                None
            context = {
                'now': nowChoose,
                'userInfo': userInfo
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('页面参数错误')
    else:
        return HttpResponse('不存在参数')
