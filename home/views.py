from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *
from django.template import loader
from django.core.paginator import Paginator
from django.db.models import Avg
from django.core import serializers
import json
import time
import urllib.parse
import datetime
# 引入公共文件 中的分页class
from common.page import PageObject
from common.dedupe import Dedupe


# 处理数据库中的图片数组
def handlePhoto(list):
    for item in list:
        list[list.index(item)]['m_photo'] = json.loads(item['m_photo'])
        if item['create_time'] != 0:
            list[list.index(item)]['create_time'] = time.strftime("%m-%d %H:%M",
                                                                  time.localtime(float(item['create_time'])))
        if item['update_time'] != 0:
            list[list.index(item)]['update_time'] = time.strftime("%m-%d %H:%M",
                                                                  time.localtime(float(item['update_time'])))
    return list




# 处理首页的数据
def handleIndexData(list):
    for item in list:
        now_time = time.time()
        list[list.index(item)]['m_photo'] = json.loads(item['m_photo'])
        if item['create_time'] != 0:
            print('datatime', now_time)
            print('datatime', float(item['create_time']))
            time_delta = round(now_time) - round(float(item['create_time']))
            time_result = round(time_delta / 60)
            print('分钟', round(time_delta / 60))
            if time_result < 60:
                temp = time_result
                list[list.index(item)]['create_time'] = '%s分钟前' % temp
            elif time_result > 60 and time_result < 1440:
                temp = round(time_result / 60)
                list[list.index(item)]['create_time'] = '%s小时前' % temp
            else:
                temp = round(time_result / 1440)
                list[list.index(item)]['create_time'] = '%s天前' % temp
        if item['update_time'] != 0:
            list[list.index(item)]['update_time'] = time.strftime("%m-%d %H:%M",
                                                                  time.localtime(float(item['update_time'])))
    return list

# Create your views here.
# objects.get()结果转换
def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state" and kk != "password"])


# 查询并生成导航列表
def navList():
    try:
        p_product.objects.all()
        lists = list(p_product.objects.all().values())
        return lists
    except:
        return None


# 首页
def index(request):
    template = loader.get_template('home/index.html')
    list = []
    nav = navList()
    recPerPage = 12
    page = 1
    try:
        pagePY = Paginator(p_message.objects.all().values().order_by('-create_time'),
                  recPerPage)
        todayPY =  Paginator(p_message.objects.all().values().order_by('-create_time'),
                  6)
    except:
        pagePY = False
    if pagePY != False:
        handle = PageObject()
        pageData = handle.handlePage(pagePY, page, recPerPage)
        pageData['page_list'] = handlePhoto(pageData['page_list'])
        todayData = handle.handlePage(todayPY, page, 12)
        todayData['page_list'] = handleIndexData(todayData['page_list'])
        print(todayData)
    else:
        pageData = False
    list_data = {
        'm_title': '柑桔13886725378特早蜜桔，叶桔，蜜橘桔子',
        'm_address_belong': '1564',
        'create_time': '1564658781'
    }
    for i in range(0, 10):
        list.append(list_data)
    context = {
        'supply': pageData,
        'list': pageData,
        'nav': nav,
        'path': '/',
        'today': todayData
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
                'userInfo': userInfo,
                'id': {
                    'f': father,
                    'c': child
                }
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('页面参数错误')
    else:
        return HttpResponse('不存在参数')


# 获取m_f_id全部对应的消息
def getPMsgList(id, recPerPage):
    List = Paginator(p_message.objects.filter(m_f_id=id).values().order_by('create_time'), recPerPage)
    return List




# 产品列表详情页
def productDetail(request, id):
    if id != None:
        if isinstance(id, int):
            template = loader.get_template('home/productDetail.html')
            try:
                data = p_message.objects.get(id=id)
                data = object_to_json(data)
                data['m_photo'] = json.loads(data['m_photo'])
                dataContact = p_message_contact.objects.get(p_id=id)
                typeF = p_product.objects.get(id=data['m_f_id'])
                typeC = p_product_child.objects.get(id=data['m_c_id'])
                dataContact = object_to_json(dataContact)
                print(data)
                print(dataContact)
            except:
                data = {}
            context = {
                'data': data,
                'contact': dataContact,
                'typeF': typeF.p_name,
                'typeC': typeC.p_name
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('页面参数错误')
    else:
        return HttpResponse('不存在参数')


# 产品列表 二级
def productC(request, id, page):
    # 每页多少信息
    recPerPage = 16
    # if request.userInfo == None:
    #     return HttpResponseRedirect('/login')
    if id != None:
        if isinstance(id, int):
            template = loader.get_template('home/productC.html')
            try:
                index = p_product_child.objects.get(id=id)
                father = p_product.objects.get(id=index.p_id)
                childList = list(p_message.objects.filter(m_c_id=id).values())
                titleNav = [
                    {
                        'title': '农产品网',
                        'link': '/'
                    },
                    {
                        'title': father.p_name,
                        'link': ''
                    },
                    {
                        'title': index.p_name,
                        'link': ''
                    }
                ]
                print(titleNav)
                childData = [{
                    'link': '/product/' + str(id) + '/1',
                    'title': '全部',
                    'f_id': 0
                }]
                for item in childList:
                    childData.append({
                        'link': item['id'],
                        'title': item['m_pz'],
                        'f_id': item['m_f_id']
                    })

            except:
                childData = None
            try:
                mgsLsit = Paginator(p_message.objects.filter(m_c_id=id).values().order_by('create_time'),
                                    recPerPage)
                # 使用公共函数中的分页生成器
                handle = PageObject()
                pageData = handle.handlePage(mgsLsit, page, recPerPage)
                pageData['page_list'] = handlePhoto(pageData['page_list'])
            except:
                pageData = None
            context = {
                'child': childData,
                'list': pageData,
                'path': '/product/' + str(id) + '/',
                'titleNav': titleNav,
                'this': index.p_name
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('页面参数错误')
    else:
        return HttpResponse('不存在参数')


# 产品列表
def product(request, father, child, last, page):
    # 每页多少信息
    recPerPage = 16
    # if request.userInfo == None:
    #     return HttpResponseRedirect('/login')
    if father != None:
        if isinstance(father, int):
            threeAll = None
            template = loader.get_template('home/product.html')
            table_nav = list(p_product_child.objects.filter(p_id=father).values())
            if child == 0:
                childData = [{
                    'link': '/product/' + str(father) + '/0/0/1',
                    'title': '全部',
                    'f_id': 0,
                    'active': 'on'
                }]
            else:
                childData = [{
                    'link': '/product/' + str(father) + '/0/0/1',
                    'title': '全部',
                    'f_id': 0,
                    'active': ''
                }]
            for item in table_nav:
                if item['id'] == child:
                    on = 'on'
                else:
                    on = ''
                childData.append({
                    'link': '/product/' + str(father) + '/' + str(item['id']) + '/0/1',
                    'title': item['p_name'],
                    'f_id': item['p_id'],
                    'active': on
                })

            try:
                if child == 0:
                    mgsLsit = Paginator(p_message.objects.filter(m_f_id=father).values().order_by('create_time'),
                                        recPerPage)
                else:
                    #  查询所属二级列表下面的所有不重复的子产品！
                    threeList = list(
                        p_message.objects.filter(m_c_id=child).values('m_pz', 'id', 'm_c_id').annotate(avg=Avg("m_pz")))
                    deep = Dedupe()
                    threeList = list(deep.dedupe(threeList, key=lambda d: d['m_pz']))
                    # 检查所属二级列表下面的品种
                    if last == 0:
                        threeAll = [{
                            'link': '/product/' + str(father) + '/' +str(child) +'/0/1',
                            'title': '全部',
                            'f_id': 0,
                            'active': 'on'
                        }]
                        # 获取分页数据
                        mgsLsit = Paginator(p_message.objects.filter(m_c_id=child).values().order_by('create_time'),
                                            recPerPage)
                    else:
                        threeAll = [{
                            'link': '/product/' + str(father) + '/' +str(child) +'/0/1',
                            'title': '全部',
                            'f_id': 0,
                            'active': ''
                        }]
                        m_pz = p_message.objects.get(id=last)
                        # 获取分页数据
                        mgsLsit = Paginator(p_message.objects.filter(m_pz=m_pz.m_pz).values().order_by('create_time'),
                                            recPerPage)

                    for item in threeList:
                        if last == item['id']:
                            on_last = 'on'
                        else:
                            on_last = ''
                        threeAll.append({
                            'link': '/product/' + str(father) + '/' + str(child) + '/' + str(item['id']) + '/1',
                            'title': item['m_pz'],
                            'f_id': 0,
                            'active': on_last
                        })
                # 使用公共函数中的分页生成器
                handle = PageObject()
                pageData = handle.handlePage(mgsLsit, page, recPerPage)
                if pageData['count'] == 0:
                    msg = urllib.parse.quote('该栏目下没有信息！')
                    return HttpResponseRedirect('/message/' + msg)
                pageData['page_list'] = handlePhoto(pageData['page_list'])
            except:
                pageData = None
            this = p_product.objects.get(id=father)
            titleNav = [
                {
                    'title': '农产品网',
                    'link': '/'
                },
                {
                    'title': this.p_name,
                    'link': ''
                }
            ]
            context = {
                'child': childData,  # 多级导航
                'list': pageData,
                'path': '/product/' + str(father) + '/' + str(child) + '/' + str(last) + '/',
                'titleNav': titleNav,
                'this': this.p_name,
                'threeAll': threeAll
            }


            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('页面参数错误')
    else:
        return HttpResponse('不存在参数')


# 产品列表
def message(request, error):
    template = loader.get_template('home/message.html')
    print(urllib.parse.unquote(error))
    context = {
        'msg': urllib.parse.unquote(error)
    }
    return HttpResponse(template.render(context, request))
