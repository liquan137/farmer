from django.shortcuts import render
from django.http import HttpResponse
from home.models import *
import zmail
import json
import string
import random
import time
import os
from django.conf import settings
import datetime

# Create your views here.
# 邮箱配置
server = zmail.server('1031308775@qq.com', 'vwfjwqaeftiebegb')


# 生成AES密匙以及邮箱验证码
def random_password(num):
    result = ''
    choice = '0123456789' + string.ascii_lowercase
    result += random.choice('0123456789')
    result += random.choice(string.ascii_lowercase)
    list = []
    for i in range(num - 2):
        a = random.choice(choice)
        list.append(a)
        result += a
    return result


# 登陆
def login(request):
    print(request.userInfo)
    print(request.method)
    if request.method == 'POST':
        responses = json.loads(request.body)
        for response in responses:
            print(responses[response])
            if response == 'username':
                request.session['user_id'] = responses[response]

        try:
            user = p_menber.objects.get(username=responses['username'])
            if user.password == responses['password']:
                request.session['user_id'] = responses['username']
                data = {
                    'status': 200,
                    'msg': '登录成功',
                    'data': None
                }
            else:
                data = {
                    'status': 401,
                    'msg': '密码错误',
                    'data': None
                }
        except:
            data = {
                'status': 401,
                'msg': '没有此账号',
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


# 注册
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
            try:
                userEmail = p_menber_email.objects.get(username=responses['username'], type=1)
                if userEmail.code == responses['code']:
                    newUser = p_menber(username=responses['username'], password=responses['password'], nickname='')
                    newUser.save()
                    request.session['user_id'] = responses['username']
                    data = {
                        'status': 200,
                        'msg': '注册成功',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                else:
                    data = {
                        'status': 401,
                        'msg': '邮箱验证码错误',
                        'data': None
                    }
                    print('code错误')
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
            except:
                data = {
                    'status': 401,
                    'msg': '请先获取邮箱验证码，再完成注册！',
                    'data': None
                }
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    else:
        data = {
            'status': 401,
            'msg': '请求错误',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 忘记密码
def forget(request):
    print(request.userInfo)
    print(request.method)
    if request.method == 'POST':
        responses = json.loads(request.body)
        for response in responses:
            print(responses[response])

        try:
            username = responses['username']
            user = p_menber.objects.get(username=username)
            try:
                userEmail = p_menber_email.objects.get(username=responses['username'], type=2)
                if userEmail.code == responses['code']:
                    user.password = responses['password']
                    user.save()
                    request.session['user_id'] = responses['username']
                    data = {
                        'status': 200,
                        'msg': '修改成功',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                else:
                    data = {
                        'status': 401,
                        'msg': '邮箱验证码错误',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
            except:
                data = {
                    'status': 401,
                    'msg': '请先获取邮箱验证码，再修改密码！',
                    'data': None
                }
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        except:
            data = {
                'status': 401,
                'msg': '没有此账号！',
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


# 完善资料
def registerReg(request):
    if request.userInfo == None:
        data = {
            'status': 401,
            'msg': '请登录之后，再进行操作哦',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
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
            user.address_province = responses['company_address1']
            user.address_city = responses['company_address2']
            user.address_belong = responses['company_address']
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


# 邮箱验证码 注册、忘记密码的时候发送验证码
def verifyEmail(request):
    # status为True 就发送邮件
    status = False
    if request.method == 'POST':
        responses = json.loads(request.body)
        type = responses['sendType']
        key = random_password(4)
        if int(type) == 1:
            try:
                p_menber.objects.get(username=responses['username'])
                data = {
                    'status': 401,
                    'msg': '账号已经注册过了',
                    'data': None
                }
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
            except:
                print('账号不存在，可以注册')
        # 检查该邮箱是否发送过邮件，如果发送过，就检查发送时间，如果超过60秒就设置status为True，
        try:
            sqlTime = p_menber_email.objects.get(username=responses['username'], type=type)
            oldTime = int(str(sqlTime.create_time).split('.')[0]) + 60
            nowTime = int(str(time.time()).split('.')[0])
            if nowTime < oldTime:
                status = False
            else:
                status = True
        except:
            status = True
        #     判断是否发送验证码邮件
        if status == True:
            option = ['', '注册账号', '找回密码']
            mail = {
                'subject': '验证码通知-农业网',
                'content_text': """
                    此验证码为 [ """ + option[int(type)] + """] 所用，
                    
                    您的验证码是： """ + key + """，10分钟内有效！
                                """,
            }
            server.send_mail(responses['username'], mail)
            data = {
                'status': 200,
                'msg': '发送成功',
                'data': None
            }
            try:
                sqlTime = p_menber_email.objects.get(username=responses['username'], type=type)
                sqlTime.create_time = time.time()
                sqlTime.code = key
                sqlTime.save()
            except:
                newEmail = p_menber_email(username=responses['username'], type=type, code=key, create_time=time.time())
                newEmail.save()
        else:
            data = {
                'status': 401,
                'msg': '已经发送过一封邮件了',
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


# 发布信息
def publish(request):
    if request.userInfo == None:
        data = {
            'status': 401,
            'msg': '请登录之后，再进行操作哦',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    if request.method == 'POST':
        responses = json.loads(request.body)
        try:
            p_message.objects.get(m_title=responses['m_title'])
            data = {
                'status': 400,
                'msg': '已经发表过此标题的文章了',
                'data': None
            }
        except:
            checkPz = list(p_message.objects.filter(m_pz=responses['m_pz']).values())
            for item in checkPz:
                if item['m_c_id'] != responses['m_c_id'] or item['m_f_id'] != responses['m_f_id']:
                    father = p_product.objects.get(id=item['m_f_id'])
                    child = p_product_child.objects.get(id=item['m_c_id'])
                    data = {
                        'status': 401,
                        'msg': '品种：【' + responses[
                            'm_pz'] + '】已经绑定此大类：' + '【' + father.p_name + '-' + child.p_name + '】',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
            newMessage = p_message(
                m_title=responses['m_title'],
                m_address_belong=responses['company_address'],
                m_address_province=responses['company_address1'],
                m_address_city=responses['company_address2'],
                m_address_detail=responses['address_detail'],
                m_begin=str(int(responses['m_begin'])) + '月' + responses['m_begin_size'],
                m_end=str(int(responses['m_end'])) + '月' + responses['m_end_size'],
                m_photo=responses['m_photo'],
                m_pz=responses['m_pz'],
                m_size=responses['m_size'],
                m_today_price=responses['m_today_price'],
                m_today_date=time.time(),
                m_today_size=responses['m_today_size'],
                m_content=responses['m_content'],
                m_f_id=responses['m_f_id'],
                m_c_id=responses['m_c_id'],
                create_time=time.time(),
                update_time=time.time(),
                username=request.userInfo['username'],
            )
            newMessage.save()
            newMessageContact = p_message_contact(
                p_id=newMessage.id,
                username=request.userInfo['username'],
                company_name=responses['company_name'],
                address_province=responses['company_address1'],
                address_city=responses['company_address2'],
                address_belong=responses['company_address'],
                address_detail=responses['address_detail'],
                contact_person=responses['contact_person'],
                contact_phone=responses['contact_phone'],
                contact_tel=responses['contact_tel'],
                contact_email=responses['contact_email'],
                contact_qq=responses['contact_qq'],
            )
            newMessageContact.save()
            data = {
                'status': 200,
                'msg': '发表成功',
                'data': newMessage.id
            }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        data = {
            'status': 401,
            'msg': '请求错误',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 图片上传
def uploadImg(request):
    if request.userInfo == None:
        data = {
            'status': 401,
            'msg': '请登录之后，再上传图片哦',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    img = request.FILES.get('file')
    # 判断参数是否齐全
    if not img:
        data = {
            'status': 400,
            'msg': '参数不全',
            'data': None,
            "errno": 1,
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    fix = str(round(time.time())) + '1'
    name = img.name.split('.')
    if len(name) == 1:
        name = request.POST.get('name').split('.')
        print('name', name)
    # 对 我们settings中已经配置好的路径 把文件的名称进行存入
    img_path = os.path.join(settings.UPLOADFILES_DIRS, fix + str(request.userInfo['id']) + '.' + name[len(name) - 1])
    f = open(img_path, 'wb')
    for i in img.chunks():
        f.write(i)
    f.close()

    # 入库操作
    url = '/static/upload/images/' + fix + str(request.userInfo['id']) + '.' + name[len(name) - 1]
    newFile = p_file(name=img.name, path=url, create_time=time.time())
    newFile.save()
    data = {
        'status': 200,
        'msg': '上传成功',
        'data': [url],
        'type': 'success',
        "errno": 0,
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 修改报价
def updatePrice(request):
    if request.userInfo == None:
        data = {
            'status': 401,
            'msg': '请登录之后，再进行操作哦',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    if request.method == 'POST':
        responses = json.loads(request.body)
        try:
            find = p_message.objects.get(id=responses['id'])
            find.m_today_price = responses['m_today_price']
            find.m_today_size = responses['m_today_size']
            find.update_time = time.time()
            find.save()
            data = {
                'status': 200,
                'msg': '修改报价成功',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        except:
            data = {
                'status': 401,
                'msg': '没有找到此条信息',
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


def updatePassword(request):
    if request.userInfo == None:
        data = {
            'status': 401,
            'msg': '请登录之后，再进行操作哦',
            'data': None
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    if request.method == 'POST':
        responses = json.loads(request.body)
        try:
            find = p_menber.objects.get(username=request.userInfo['username'])
            if responses['password_old'] == find.password:
                find.password = responses['password_new']
                find.save()
                data = {
                    'status': 200,
                    'msg': '修改密码成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': '原密码错误',
                    'data': None
                }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        except:
            data = {
                'status': 401,
                'msg': '没有找到此账号',
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
