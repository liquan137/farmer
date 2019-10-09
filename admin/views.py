from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django import forms
from admin.models import *

from captcha.fields import CaptchaField
import json


class LoginForm(forms.Form):
    user = forms.CharField(min_length=4, error_messages={
        "required": "账号不能为空",
        'min_length': '账号不能少于6位'
    }, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'user', 'placeholder': '请输入账号'}))
    password = forms.CharField(max_length=6, error_messages={
        "required": "密码不能为空",
        'min_length': '密码不能少于6位'
    }, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': '请输入密码'}))
    captcha = CaptchaField(label='验证码')


# Create your views here.
def captcha():
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            # 如果验证码匹配
            if get_captcha.response == captchaStr.lower():
                return True
        except:
            return False
    else:
        return False


def login(request):
    loginForm = LoginForm()
    if request.method == 'GET':
        template = loader.get_template('admin/login.html')
        context = {
            'form': loginForm
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        requestJson = request.POST
        for requestJsones in requestJson:
            print(requestJson[requestJsones])
        if jarge_captcha(requestJson.get('code'), requestJson.get('captcha_0')):
            try:
                admin = p_admin.objects.get(user=requestJson.get('user'))
                if admin.password == requestJson.get('password'):
                    data = {
                        'status': 200,
                        'msg': '登陆成功',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
                else:
                    data = {
                        'status': 200,
                        'msg': '账号或者密码错误',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
            except:
                data = {
                    'status': 200,
                    'msg': '账号或者密码错误',
                    'data': None
                }
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data = {
                'status': 400,
                'msg': '验证码错误',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


def initialize(request):
    if request.method == 'GET':
        try:
            p_admin.objects.get(user='admin')
            result = '系统当前已经初始过管理员了'
            return HttpResponse(result)
        except:
            newAdmin = p_admin(user='admin', password='123456', username='', auth=1)
            newAdmin.save()
            result = '系统管理员已经初始化完成，请联系作者获取密码'
            return HttpResponse(result)
