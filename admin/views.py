import os
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from admin.models import *
from home.models import *
from django.core.paginator import Paginator
from django.db.models import Avg
import json
import time
import platform
from admin.form import *
# 引入公共文件 中的分页class
from common.page import PageObject
from common.dedupe import Dedupe


# objects.get()结果转换
def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state" and kk != "password"])


def sysInfo():
    if os.name == 'nt':
        name = 'windows'
    elif os.name == 'posix':
        name = 'linux'
    elif os.name == 'java':
        name = 'java'
    print()
    return {
        'name': platform.platform(),
        'python': platform.python_version(),
    }


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
    print(request.admin)
    loginForm = LoginForm()
    if request.method == 'GET':
        if request.admin != None:
            return HttpResponseRedirect('/admin')
        template = loader.get_template('admin/login.html')
        context = {
            'form': loginForm
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        if request.admin != None:
            data = {
                'status': 200,
                'msg': '已登录管理员账号',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        requestJson = request.POST
        for requestJsones in requestJson:
            print(requestJson[requestJsones])
        if jarge_captcha(requestJson.get('code'), requestJson.get('captcha_0')):
            try:
                admin = p_admin.objects.get(user=requestJson.get('user'))
                if admin.password == requestJson.get('password'):
                    request.session['admin'] = requestJson.get('user')
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


# 首页
def index(request):
    if request.method == 'GET':
        print('admin', request.admin)
        print('admin', request.userInfo)
        if request.admin == None:
            return HttpResponseRedirect('/admin/login')
        template = loader.get_template('admin/index.html')
        context = {
            'number': {
                'msg': p_message.objects.count(),
                'user': p_menber.objects.count(),
                'nav': p_product.objects.count(),
                'product': p_product_child.objects.count()
            },
            'os': sysInfo()
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        if request.admin != None:
            data = {
                'status': 200,
                'msg': '已登录管理员账号',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data = {
                'status': 400,
                'msg': '请求错误',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 系统设置
def setting(request):
    if request.method == 'GET':
        if request.admin == None:
            return HttpResponseRedirect('/admin/login')
        Setting = object_to_json(p_sys.objects.get(id=1))
        template = loader.get_template('admin/setting.html')
        context = {
            'sys': Setting
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        if request.admin != None:
            Form = SettingForm(request.POST)
            if Form.is_valid():
                responses = request.POST
                Setting = p_sys.objects.get(id=1)
                Setting.title = responses.get('title')
                Setting.dec = responses.get('dec')
                Setting.keyword = responses.get('keyword')
                Setting.url = responses.get('url')
                Setting.img_limit = responses.get('img_limit')
                Setting.article_limit = responses.get('article_limit')
                Setting.save()
                data = {
                    'status': 200,
                    'msg': '修改完毕,请重启服务器，才可以看到效果！',
                    'data': None
                }
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
            else:
                data = {
                    'status': 400,
                    'msg': Form.errors,
                    'data': None
                }
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data = {
                'status': 400,
                'msg': '请求错误',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 系统管理员
def sysUser(request, page):
    if request.method == 'GET':
        print('admin', request.admin)
        print('admin', request.userInfo)
        if request.admin == None:
            return HttpResponseRedirect('/admin/login')
        handle = PageObject()
        recPerPage = 20
        pageData = Paginator(p_admin.objects.all().values().order_by('id'),
                             recPerPage)
        pageData = handle.handlePage(pageData, page, recPerPage)
        template = loader.get_template('admin/sysUser.html')
        context = {
            'list': pageData
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        if request.admin != None:
            data = {
                'status': 401,
                'msg': '未查询到的操作',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data = {
                'status': 400,
                'msg': '请求错误',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 系统管理员设置 API接口
def sysBind(request):
    if request.method == 'POST':
        if request.admin == None and request.admin['auth'] != 1:
            data = {
                'status': 401,
                'msg': '未查询到的操作',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        if request.POST.get('type') == 'b':
            bind = BindForm(request.POST)
            if bind.is_valid():
                admin = p_admin.objects.get(id=request.POST.get('id'))
                try:
                    p_menber.objects.get(username=request.POST.get('username'))
                except:
                    data = {
                        'status': 400,
                        'msg': '您绑定的这个普通账号不存在！',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                admin.username = request.POST.get('username')
                admin.save()
                data = {
                    'status': 200,
                    'msg': '绑定成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'u':
            bind = UpdateForm(request.POST)
            if bind.is_valid():
                try:
                    p_menber.objects.get(username=request.POST.get('username'))
                except:
                    data = {
                        'status': 400,
                        'msg': '您绑定的这个普通账号不存在！',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                admin = p_admin.objects.get(id=request.POST.get('id'))
                admin.password = request.POST.get('password')
                admin.username = request.POST.get('username')
                admin.save()
                data = {
                    'status': 200,
                    'msg': '修改成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'd':
            bind = DeleteForm(request.POST)
            if bind.is_valid():
                admin = p_admin.objects.get(id=request.POST.get('id'))
                if admin.user == 'admin':
                    data = {
                        'status': 400,
                        'msg': '系统初始管理员无法删除',
                        'data': None
                    }
                    return HttpResponse(json.dumps(data, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                admin.delete()
                data = {
                    'status': 200,
                    'msg': '删除成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'c':
            bind = CreateForm(request.POST)
            try:
                old = p_admin.objects.get(user=request.POST.get('user'))
                data = {
                    'status': 400,
                    'msg': '该账号：' + str(old.user) + '已经存在',
                    'data': None
                }
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
            except:
                if bind.is_valid():
                    admin = p_admin(user=request.POST.get('user'), auth=request.POST.get('auth'),
                                    password=request.POST.get('password'))
                    admin.save()
                    data = {
                        'status': 200,
                        'msg': '创建成功',
                        'data': None
                    }
                else:
                    data = {
                        'status': 400,
                        'msg': bind.errors,
                        'data': None
                    }
        else:
            data = {
                'status': 401,
                'msg': '请求错误',
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


# 用户
def menber(request, page):
    if request.method == 'GET':
        print('admin', request.admin)
        print('admin', request.userInfo)
        if request.admin == None:
            return HttpResponseRedirect('/admin/login')
        handle = PageObject()
        recPerPage = 20
        pageData = Paginator(p_menber.objects.all().values().order_by('id'),
                             recPerPage)
        pageData = handle.handlePage(pageData, page, recPerPage)
        template = loader.get_template('admin/menber.html')
        context = {
            'list': pageData
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        if request.admin != None:
            data = {
                'status': 401,
                'msg': '未查询到的操作',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data = {
                'status': 400,
                'msg': '请求错误',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 用户管理 API接口
def sysMenber(request):
    if request.method == 'POST':
        if request.admin == None:
            data = {
                'status': 401,
                'msg': '未查询到的操作',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        if request.POST.get('type') == 'f':
            bind = AuthMenberForm(request.POST)
            if bind.is_valid():
                user = p_menber.objects.get(username=request.POST.get('id'))
                user.auth = request.POST.get('auth')
                user.save()
                if int(user.auth) == 1:
                    msg = '切换为正常状态'
                else:
                    msg = '切换到封禁状态'
                data = {
                    'status': 200,
                    'msg': msg,
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'u':
            bind = PasswordMenberForm(request.POST)
            if bind.is_valid():
                user = p_menber.objects.get(username=request.POST.get('id'))
                user.password = request.POST.get('password')
                user.save()
                data = {
                    'status': 200,
                    'msg': '修改密码成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'd':
            bind = DeleteForm(request.POST)
            if bind.is_valid():
                user = p_menber.objects.get(username=request.POST.get('id'))
                msg = p_message.objects.filter(username=request.POST.get('id'))
                msg_add = p_message_contact.objects.filter(username=request.POST.get('id'))
                msg_img = p_file.objects.filter(username=request.POST.get('id'))
                msg.delete()
                msg_add.delete()
                msg_img.delete()
                user.delete()
                data = {
                    'status': 200,
                    'msg': '删除成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        else:
            data = {
                'status': 401,
                'msg': '请求错误',
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


# 主类目管理
def main(request):
    if request.method == 'GET':
        print('admin', request.admin)
        print('admin', request.userInfo)
        if request.admin == None:
            return HttpResponseRedirect('/admin/login')
        data = list(p_product.objects.all().values())
        pageData = []
        for item in data:
            pageData.append({
                'p_name': item['p_name'],
                'id': item['id'],
                'child': list(p_product_child.objects.filter(p_id=item['id']).values())
            })
        print(pageData)
        template = loader.get_template('admin/main.html')
        context = {
            'list': pageData
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        if request.admin != None:
            data = {
                'status': 200,
                'msg': '已登录管理员账号',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data = {
                'status': 400,
                'msg': '请求错误',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 类目管理 API接口
def sysMain(request):
    if request.method == 'POST':
        if request.admin == None:
            data = {
                'status': 401,
                'msg': '未查询到的操作',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        if request.POST.get('type') == 'f':
            bind = CreateMainForm(request.POST)
            if bind.is_valid():
                if len(p_product.objects.filter(p_name=request.POST.get('p_name'))) > 0:
                    data = {
                        'status': 400,
                        'msg': '存在重名类目',
                        'data': None
                    }
                else:
                    newP = p_product(p_name=request.POST.get('p_name'), create_time=time.time(),
                                     update_time=time.time())
                    newP.save()
                    data = {
                        'status': 200,
                        'msg': '创建成功',
                        'data': None
                    }

            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'c':
            bind = CreateMainForm(request.POST)
            if bind.is_valid():
                if len(p_product_child.objects.filter(p_name=request.POST.get('p_name'))) > 0:
                    data = {
                        'status': 400,
                        'msg': '存在重名类目',
                        'data': None
                    }
                else:
                    newP = p_product_child(p_name=request.POST.get('p_name'), create_time=time.time(),
                                           update_time=time.time(), p_id=request.POST.get('id'))
                    newP.save()
                    data = {
                        'status': 200,
                        'msg': '创建成功',
                        'data': None
                    }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'u':
            bind = CreateMainForm(request.POST)
            if bind.is_valid():
                if len(p_product.objects.filter(p_name=request.POST.get('p_name'))) > 0:
                    data = {
                        'status': 400,
                        'msg': '存在重名类目',
                        'data': None
                    }
                else:
                    father = p_product.objects.get(id=request.POST.get('id'))
                    father.p_name = request.POST.get('p_name')
                    father.save()
                    data = {
                        'status': 200,
                        'msg': '修改成功',
                        'data': None
                    }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'u_c':
            bind = CreateMainForm(request.POST)
            if bind.is_valid():
                if len(p_product_child.objects.filter(p_name=request.POST.get('p_name'))) > 0:
                    data = {
                        'status': 400,
                        'msg': '存在重名类目',
                        'data': None
                    }
                else:
                    child = p_product_child.objects.get(id=request.POST.get('id'))
                    child.p_name = request.POST.get('p_name')
                    child.save()
                    data = {
                        'status': 200,
                        'msg': '修改成功',
                        'data': None
                    }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'd':
            bind = DeleteForm(request.POST)
            if bind.is_valid():
                D_p = p_product_child.objects.filter(id=request.POST.get('id'))
                msg = p_message.objects.filter(m_c_id=request.POST.get('id'))
                for item in msg:
                    p_message_contact.objects.filter(p_id=item.id).delete()
                msg.delete()
                D_p.delete()
                data = {
                    'status': 200,
                    'msg': '删除成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'd_f':
            bind = DeleteForm(request.POST)
            if bind.is_valid():
                D_p = p_product.objects.filter(id=request.POST.get('id'))
                p_product_child.objects.filter(p_id=request.POST.get('id')).delete()
                msg = p_message.objects.filter(m_f_id=request.POST.get('id'))
                for item in msg:
                    p_message_contact.objects.filter(p_id=item.id).delete()
                msg.delete()
                D_p.delete()
                data = {
                    'status': 200,
                    'msg': '删除成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        else:
            data = {
                'status': 401,
                'msg': '请求错误',
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


# 品种管理
def category(request):
    if request.method == 'GET':
        print('admin', request.admin)
        print('admin', request.userInfo)
        if request.admin == None:
            return HttpResponseRedirect('/admin/login')
        data = list(p_product_child.objects.all().values())
        pageData = []
        deep = Dedupe()
        for item in data:
            pageData.append({
                'p_name': item['p_name'],
                'id': item['id'],
                'child': list(
                    deep.dedupe(list(p_message.objects.filter(m_c_id=item['id']).values().annotate(avg=Avg("m_pz"))),
                                key=lambda d: d['m_pz']))
            })
        print(pageData)
        template = loader.get_template('admin/category.html')
        context = {
            'list': pageData
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        if request.admin != None:
            data = {
                'status': 200,
                'msg': '已登录管理员账号',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data = {
                'status': 400,
                'msg': '请求错误',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 品种管理 API接口
def sysCategory(request):
    if request.method == 'POST':
        if request.admin == None:
            data = {
                'status': 401,
                'msg': '未查询到的操作',
                'data': None
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        if request.POST.get('type') == 'u_pz':
            bind = CreateMainForm(request.POST)
            if bind.is_valid():

                if request.POST.get('id') == 0:
                    data = {
                        'status': 400,
                        'msg': '修改失败',
                        'data': None
                    }
                else:
                    pz = p_message.objects.get(id=request.POST.get('id'))
                    pz.m_pz = request.POST.get('p_name')
                    pz.save()
                    data = {
                        'status': 200,
                        'msg': '修改成功',
                        'data': None
                    }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'u':
            bind = CreateMainForm(request.POST)
            if bind.is_valid():
                if len(p_product_child.objects.filter(p_name=request.POST.get('p_name'))) > 0:
                    data = {
                        'status': 400,
                        'msg': '存在重名类目',
                        'data': None
                    }
                else:
                    child = p_product_child.objects.get(id=request.POST.get('id'))
                    child.p_name = request.POST.get('p_name')
                    child.save()
                    data = {
                        'status': 200,
                        'msg': '修改成功',
                        'data': None
                    }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        elif request.POST.get('type') == 'd':
            bind = DeleteForm(request.POST)
            if bind.is_valid():
                D_p = p_product_child.objects.filter(id=request.POST.get('id'))
                msg = p_message.objects.filter(m_c_id=request.POST.get('id'))
                for item in msg:
                    p_message_contact.objects.filter(p_id=item.id).delete()
                msg.delete()
                D_p.delete()
                data = {
                    'status': 200,
                    'msg': '删除成功',
                    'data': None
                }
            else:
                data = {
                    'status': 400,
                    'msg': bind.errors,
                    'data': None
                }
        else:
            data = {
                'status': 401,
                'msg': '请求错误',
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


# 初始化管理员账号，以及菜单
def initialize(request):
    if request.method == 'GET':
        index = 0
        try:
            p_admin.objects.get(user='admin')
            index += 1
            result = str(index) + ') 系统当前已经初始过管理员了<br>'
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
                result += str(index) + ') 已经添加过了[' + list['title'] + ']类别<br>'
            except:
                newP = p_product(p_name=list['title'], create_time=time.time())
                newP.save()
                result += str(index) + ') [' + list['title'] + ']类别添加完毕<br>'
                for item in list['item']:
                    index += 1
                    try:
                        p_product_child.objects.get(p_name=item)
                        result += str(index) + ') 已经添加过了[' + item + ']类别<br>'
                    except:
                        newPchild = p_product_child(p_name=item, p_id=newP.id, create_time=time.time())
                        newPchild.save()
                        result += str(index) + ') [' + item + ']类别添加完毕<br>'
        try:
            index += 1
            p_sys.objects.get(id=1)
            result += str(index) + ') 网站设置已经初始化过了<br>'
        except:
            index += 1
            newSys = p_sys(dec='网站初始化完毕')
            newSys.save()
            result += str(index) + ') 网站设置初始化完毕,请重启django服务！<br>'
        result += "<a href='/'>登陆前台首页</a> | <a href='/admin/login'>登陆到后台首页</a>"
        result = '<div style="text-align:center;line-height:28px;font-size:12px">' + result + '</div>'
        return HttpResponse(result)
