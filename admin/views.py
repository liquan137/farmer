from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django import forms

from captcha.fields import CaptchaField
import json


class LoginForm(forms.Form):
    user = forms.CharField(min_length=4, error_messages={
        "required": "账号不能为空",
        'min_length': '账号不能少于6位'
    }, widget=forms.TextInput(attrs={'class': 'form-control','name': 'user','placeholder': '请输入账号'}))
    password = forms.CharField(max_length=6, error_messages={
        "required": "密码不能为空",
        'min_length': '密码不能少于6位'
    }, widget=forms.TextInput(attrs={'class': 'form-control','name': 'password','placeholder': '请输入密码'}))
    # code = forms.CharField(max_length=5, error_messages={
    #     "required": "验证码不能为空",
    #     'min_length': '验证码不能少于6位'
    # }, widget=forms.TextInput(attrs={'class': 'form-control','name': 'code','placeholder': '请输入验证码'}))
    captcha = CaptchaField(label='验证码')

# Create your views here.
def captcha():
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


def login(request):
    template = loader.get_template('admin/login.html')
    loginForm = LoginForm()
    context = {
        'form': loginForm
    }
    return HttpResponse(template.render(context, request))


def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')
