from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django import forms
from admin.models import *
from home.models import p_product, p_product_child
from captcha.fields import CaptchaField
import json
import time


# 管理后端登陆表单生成
class LoginForm(forms.Form):
    user = forms.CharField(min_length=4, error_messages={
        "required": "账号不能为空",
        'min_length': '账号不能少于6位'
    }, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'user', 'placeholder': '请输入账号'}))
    password = forms.CharField(max_length=6, error_messages={
        "required": "密码不能为空",
        'min_length': '密码不能少于6位'
    }, widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': '请输入密码'}))
    captcha = CaptchaField(label='验证码')


# Create your views here.
# 验证码生成
def captcha():
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


# 验证验证码合法性
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


# 重置验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


# 登陆
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
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
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


# 初始化管理员账号，以及菜单
def initialize(request):
    if request.method == 'GET':
        index = 0
        try:
            p_admin.objects.get(user='admin')
            index += 1
            result = str(index)+') 系统当前已经初始过管理员了<br>'
        except:
            newAdmin = p_admin(user='admin', password='123456', username='', auth=1)
            newAdmin.save()
            result = str(index) + ') 初始化管理员[admin]完毕<br>'
        p_child_1 = ['白菜', '土豆', '红薯', '西红柿']
        p_child_2 = ['葡萄', '西瓜', '苹果', '香蕉']
        p_child_3 = ['稻米', '小麦', '玉米', '棉花']
        p_child_4 = ['特种养殖', '奶牛', '肉牛', '绵羊']
        p_child_5 = ['蔬瓜种子', '果树苗', '绿化苗木', '育苗基地']
        p_child_6 = ['菇类', '禽蛋制品', '茶叶', '烟叶']
        lists = [
            {
                'title': '蔬菜',
                'item': p_child_1
            },
            {
                'title': '水果',
                'item': p_child_2
            },
            {
                'title': '粮油',
                'item': p_child_3
            },
            {
                'title': '畜禽养殖',
                'item': p_child_4
            },
            {
                'title': '种子种苗、农资',
                'item': p_child_5
            },
            {
                'title': '其它农副产品',
                'item': p_child_6
            }
        ]
        for list in lists:
            index += 1
            try:
                p_product.objects.get(p_name=list['title'])
                result += str(index)+') 已经添加过了['+list['title']+']类别<br>'
            except:
                newP = p_product(p_name=list['title'], create_time=time.time())
                newP.save()
                result += str(index)+') ['+list['title']+']类别添加完毕<br>'
                for item in list['item']:
                    index += 1
                    try:
                        p_product_child.objects.get(p_name=item)
                        result += str(index)+') 已经添加过了['+item+']类别<br>'
                    except:
                        newPchild = p_product_child(p_name=item, p_id=newP.id, create_time=time.time())
                        newPchild.save()
                        result += str(index)+') ['+item+']类别添加完毕<br>'
        try:
            index += 1
            p_sys.objects.get(id=1)
            result += str(index)+') 网站设置已经初始化过了<br>'
        except:
            index += 1
            newSys = p_sys(dec='网站初始化完毕')
            newSys.save()
            result += str(index)+') 网站设置初始化完毕,请重启django服务！<br>'
        result += "<a href='/'>登陆前台首页</a> | <a href='/admin/login'>登陆到后台首页</a>"
        result = '<div style="text-align:center;line-height:28px;font-size:12px">'+result+'</div>'
        return HttpResponse(result)
