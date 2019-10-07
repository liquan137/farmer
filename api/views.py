from django.shortcuts import render
from django.http import HttpResponse
from home.models import *
import json


# Create your views here.

def login(request):
    print(request.userInfo)
    print(request.method)
    if request.method == 'POST':
        responses = json.loads(request.body)
        for response in responses:
            print(responses[response])
            if response == 'username':
                request.session['user_id'] = responses[response]
        data = {
            'status': 200,
            'msg': '登录成功',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        data = {
            'status': 401,
            'msg': '请求错误',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


def register(request):
    print(request.userInfo)
    print(request.method)
    if request.method == 'POST':
        responses = json.loads(request.body)
        for response in responses:
            print(responses[response])

        try:
            username = responses['username']
            user = p_menber.objects.get(username=username)
            data = {
                'status': 200,
                'msg': '账号已经存在',
                'data': None
            }
        except:
            newUser = p_menber(username=responses['username'], password=responses['password'], nickname='')
            newUser.save()
            request.session['user_id'] = responses['username']
            data = {
                'status': 200,
                'msg': '注册成功',
                'data': None
            }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        data = {
            'status': 401,
            'msg': '请求错误',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


def registerReg(request):
    print(request.userInfo)
    print(request.method)
    if request.method == 'POST':
        responses = json.loads(request.body)
        for response in responses:
            print(responses[response])
        try:
            username = request.userInfo['username']
            user = p_menber.objects.get(username=username)
            user.nickname = responses['nickname']
            user.type = responses['type']
            user.company_name = responses['company_name']
            user.address_belong = responses['company_address2']
            user.address_detail = responses['address_detail']
            user.contact_person = responses['contact_person']
            user.contact_phone = responses['contact_phone']
            user.contact_tel = responses['contact_tel']
            user.contact_email = responses['contact_email']
            user.contact_qq = responses['contact_qq']
            user.company_des = responses['company_des']
            user.save()
            data = {
                'status': 200,
                'msg': '信息完善成功',
                'data': None
            }
        except:
            print('username', request.userInfo['username'])
            data = {
                'status': 200,
                'msg': '没有此用户',
                'data': None
            }

        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        data = {
            'status': 401,
            'msg': '请求错误',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
