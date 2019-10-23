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
import codecs
# 引入公共文件 中的分页class
from common.page import PageObject
from common.dedupe import Dedupe

from admin.models import p_sys

global W_title
global W_dec
global W_keyword

try:
    W_sys = p_sys.objects.get(id=1)
    W_title = W_sys.title
    W_dec = W_sys.dec
    W_keyword = W_sys.keyword
except:
    W_title = '请先初始化后台'
    W_dec = '请先初始化后台'
    W_keyword = '请先初始化后台'


# 处理信息中的城市渲染
def CitySelect(list):
    # 加载城市列表
    file_name = "static/json/city.json"
    with open(file_name) as file_obj:
        cityList = json.load(file_obj)
    LIST = list
    for item in list:
        if isinstance(item['m_address_province'], int):
            for city_i in cityList['province_list']:
                if str(item['m_address_province']) == str(city_i):
                    LIST[list.index(item)]['m_address_province'] = cityList['province_list'][city_i]
        if isinstance(item['m_address_city'], int):
            for city_x in cityList['city_list']:
                if str(item['m_address_city']) == str(city_x):
                    LIST[list.index(item)]['m_address_city'] = cityList['city_list'][city_x]
        if isinstance(item['m_address_belong'], int):
            for city_y in cityList['county_list']:
                if str(item['m_address_belong']) == str(city_y):
                    LIST[list.index(item)]['m_address_belong'] = cityList['county_list'][city_y]
    return LIST


# 处理信息中的城市渲染
def CitySelectOne(list):
    # 加载城市列表
    file_name = "static/json/city.json"
    with open(file_name) as file_obj:
        cityList = json.load(file_obj)
    LIST = list
    if isinstance(LIST['address_province'], int):
        for city_i in cityList['province_list']:
            if str(LIST['address_province']) == str(city_i):
                LIST['address_province'] = cityList['province_list'][city_i]
    if isinstance(LIST['address_city'], int):
        for city_x in cityList['city_list']:
            if str(LIST['address_city']) == str(city_x):
                LIST['address_city'] = cityList['city_list'][city_x]
    if isinstance(LIST['address_belong'], int):
        for city_y in cityList['county_list']:
            if str(LIST['address_belong']) == str(city_y):
                LIST['address_belong'] = cityList['county_list'][city_y]
    return LIST


# 处理数据库中的图片数组
def handlePhoto(list):
    for item in list:
        print('photo', item['m_photo'])
        list[list.index(item)]['m_photo'] = json.loads(item['m_photo'])
        if item['create_time'] != 0:
            list[list.index(item)]['create_time'] = time.strftime("%m-%d %H:%M",
                                                                  time.localtime(float(item['create_time'])))
        if item['update_time'] != 0:
            list[list.index(item)]['update_time'] = time.strftime("%m-%d %H:%M",

                                                                  time.localtime(float(item['update_time'])))
    list = CitySelect(list)
    return list


# 处理数据库中的图片数组
def handleLike(list):
    for item in list:
        list[list.index(item)]['m_photo'] = json.loads(item['m_photo'])
        list[list.index(item)]['create_time'] = time.strftime("%Y-%m-%d %H:%M",
                                                              time.localtime(float(item['create_time'])))
        list[list.index(item)]['update_time'] = time.strftime("%Y-%m-%d %H:%M",

                                                              time.localtime(float(item['update_time'])))

    list = CitySelect(list)
    print('create_time', list)
    return list


# 处理首页的数据
def handleIndexData(list):
    for item in list:
        now_time = time.time()
        list[list.index(item)]['m_photo'] = json.loads(item['m_photo'])
        if item['create_time'] != 0:
            time_delta = round(now_time) - round(float(item['create_time']))
            time_result = round(time_delta / 60)
            print(time_result)
            if time_result < 1:
                temp = time_result
                list[list.index(item)]['create_time'] = '刚刚'
            elif time_result < 60 and time_result > 1:
                temp = time_result
                list[list.index(item)]['create_time'] = '%s分钟前' % temp
            elif time_result > 60 and time_result < 1440:
                temp = round(time_result / 60)
                list[list.index(item)]['create_time'] = '%s小时前' % temp
            else:
                temp = round(time_result / 1440)
                list[list.index(item)]['create_time'] = '%s天前' % temp
        if item['update_time'] != 0:
            time_delta = round(now_time) - round(float(item['update_time']))
            time_result = round(time_delta / 60)
            if time_result < 60:
                temp = time_result
                list[list.index(item)]['update_time'] = '%s分钟前' % temp
            elif time_result > 60 and time_result < 1440:
                temp = round(time_result / 60)
                list[list.index(item)]['update_time'] = '%s小时前' % temp
            else:
                temp = round(time_result / 1440)
                list[list.index(item)]['update_time'] = '%s天前' % temp
            # list[list.index(item)]['update_time'] = time.strftime("%m-%d %H:%M",
            #                                                       time.localtime(float(item['update_time'])))
    list = CitySelect(list)
    return list


# Create your views here.
# objects.get()结果转换
def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state" and kk != "password"])


# 产品报价
def cdBaoJia():
    handle = PageObject()
    page = 1
    todayPY = Paginator(p_message.objects.all().values().order_by('-update_time'),
                        6)
    todayData = handle.handlePage(todayPY, page, 6)
    todayData['page_list'] = handleIndexData(todayData['page_list'])
    return todayData


# 热门产品
def hot():
    handle = PageObject()
    page = 1
    hignList = list(
        p_message.objects.all().values('m_pz', 'id', 'm_c_id').annotate(avg=Avg("m_c_id")).order_by('-num'))
    deep = Dedupe()
    hignList = list(deep.dedupe(hignList, key=lambda d: d['m_c_id']))
    print(hignList)
    for item in hignList:
        sqlChild = p_product_child.objects.get(id=item['m_c_id'])
        hignList[hignList.index(item)].update(p_id=item['m_c_id'], p_name=sqlChild.p_name)
    todayData = {
        'page_list': hignList
    }
    return todayData


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
    nav = navList()
    recPerPage = 25
    page = 1
    try:
        pagePY = Paginator(p_message.objects.all().values().order_by('-create_time'),
                           recPerPage)
    except:
        pagePY = False
    if pagePY != False:
        handle = PageObject()
        pageData = handle.handlePage(pagePY, page, recPerPage)
        pageData['page_list'] = handlePhoto(pageData['page_list'])
        todayData = cdBaoJia()
    else:
        pageData = False
    context = {
        'supply': pageData,
        'list': pageData,
        'nav': nav,
        'path': '/list/',
        'today': todayData,
        'hot': hot()
    }
    return HttpResponse(template.render(context, request))


# 首页 分页
def List(request, page):
    template = loader.get_template('home/index.html')
    nav = navList()
    recPerPage = 25
    try:
        pagePY = Paginator(p_message.objects.all().values().order_by('-create_time'),
                           recPerPage)
    except:
        pagePY = False
    if pagePY != False:
        handle = PageObject()
        pageData = handle.handlePage(pagePY, page, recPerPage)
        pageData['page_list'] = handlePhoto(pageData['page_list'])
        todayData = cdBaoJia()
    else:
        pageData = False
    context = {
        'supply': pageData,
        'list': pageData,
        'nav': nav,
        'path': '/list/',
        'today': todayData,
        'hot': hot()
    }
    return HttpResponse(template.render(context, request))


# 搜索
def search(request):
    if request.GET.get('keyword') == '' or request.GET.get('keyword') == None:
        template = loader.get_template('home/message.html')
        context = {
            'msg': urllib.parse.unquote(urllib.parse.unquote('请填写关键词'))
        }
        return HttpResponse(template.render(context, request))
    template = loader.get_template('home/search.html')
    keyword = request.GET.get('keyword')
    print()
    nav = navList()
    recPerPage = 25
    page = 1
    try:
        pagePY = Paginator(p_message.objects.filter(m_title__contains=keyword).values().order_by('-create_time'),
                           recPerPage)
    except:
        pagePY = False
    if pagePY != False:
        handle = PageObject()
        pageData = handle.handlePage(pagePY, page, recPerPage)
        pageData['page_list'] = handlePhoto(pageData['page_list'])
        todayData = cdBaoJia()
    else:
        pageData = False

    context = {
        'supply': pageData,
        'list': pageData,
        'nav': nav,
        'path': '/list/',
        'today': todayData,
        'hot': hot(),
        'search': keyword
    }
    return HttpResponse(template.render(context, request))


# 报价 分页
def Quote(request, child, page):
    template = loader.get_template('home/quote.html')
    nav = navList()
    recPerPage = 25
    try:
        if child == 0:
            pagePY = Paginator(p_message.objects.filter(type=1).values().order_by('-create_time'),
                               recPerPage)
        else:
            pagePY = Paginator(p_message.objects.filter(m_c_id=child).values().order_by('-create_time'),
                               recPerPage)
    except:
        pagePY = False
    if pagePY != False:
        handle = PageObject()
        pageData = handle.handlePage(pagePY, page, recPerPage)
        pageData['page_list'] = handleIndexData(pageData['page_list'])
        todayData = cdBaoJia()
    else:
        pageData = False
    childAll = list(p_product_child.objects.all().values().order_by('-create_time'))
    if child == 0:
        childAllList = [{
            'title': '全部',
            'link': 0,
            'active': 'on'
        }]
    else:
        childAllList = [{
            'title': '全部',
            'link': 0,
            'active': ''
        }]
    for item in childAll:
        on = ''
        if child == item['id']:
            on = 'on'
        childAllList.append({
            'title': item['p_name'],
            'link': item['id'],
            'active': on
        })
        for items in pageData['page_list']:
            print(items['m_c_id'], item['id'])
            if int(items['m_c_id']) == int(item['id']):
                pageData['page_list'][pageData['page_list'].index(items)]['m_content'] = item['p_name']

    context = {
        'supply': pageData,
        'list': pageData,
        'nav': nav,
        'path': '/quote/' + str(child) + '/',
        'today': todayData,
        'hot': hot(),
        'all': childAllList
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


# 认证
def authReg(request):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')
    template = loader.get_template('home/authReg.html')
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
    if request.admin != None:
        del request.session['admin']
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


# 产品详情页
def productDetail(request, id):
    if id != None:
        if isinstance(id, int):
            template = loader.get_template('home/productDetail.html')
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
            else:
                ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
            dataContact = []
            sqldata = p_message.objects.get(id=id)
            try:
                ipList = json.loads(sqldata.m_ip)
                for item in ipList:
                    if ip in ipList:
                        print('---', item, ip, sqldata.m_ip)
                    else:
                        sqldata.num = sqldata.num + 1
                        ipList.append(ip)
                        sqldata.m_ip = json.dumps(ipList)
                        sqldata.save()
            except:
                sqldata.m_ip = json.dumps([ip])
                sqldata.num = 1
                sqldata.save()
            try:
                data = object_to_json(sqldata)
                print(data)
                data['m_photo'] = json.loads(data['m_photo'])
                dataContact = p_message_contact.objects.get(p_id=id)
                typeF = p_product.objects.get(id=data['m_f_id'])
                typeC = p_product_child.objects.get(id=data['m_c_id'])
                dataContact = object_to_json(dataContact)
                writerList = Paginator(
                    p_message.objects.filter(username=data['username']).order_by('-update_time').values(), 6)
                handle = PageObject()
                writerList = handle.handlePage(writerList, 1, 6)
                writerList['page_list'] = handleIndexData(writerList['page_list'])
                likeList = Paginator(
                    p_message.objects.filter(m_c_id=data['m_c_id']).order_by('-create_time').values(), 6)
                likeList = handle.handlePage(likeList, 1, 6)
                likeList['page_list'] = handleLike(likeList['page_list'])
                data['create_time'] = time.strftime("%Y-%m-%d %H:%M",
                                                    time.localtime(float(data['create_time'])))
                data['update_time'] = time.strftime("%Y-%m-%d %H:%M",
                                                    time.localtime(float(data['update_time'])))
            except:
                data = {}

            context = {
                'data': data,
                'contact': CitySelectOne(dataContact),
                'typeF': typeF.p_name,
                'typeC': typeC.p_name,
                'typeFLink': '/product/' + data['m_f_id'] + '/0/0/0/0/0/1',
                'typeCLink': '/product/' + data['m_f_id'] + '/' + data['m_c_id'] + '/0/0/0/0/1',
                'typePZLink': '/product/' + data['m_f_id'] + '/' + data['m_c_id'] + '/' + str(id) + '/0/0/0/1',
                'today': cdBaoJia(),
                'hot': hot(),
                'writer': writerList,
                'like': likeList
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('页面参数错误')
    else:
        return HttpResponse('不存在参数')


# 生成一级列表
def FClist(father, child, province, city, county):
    table_nav = list(p_product_child.objects.filter(p_id=father).values())
    if child == 0:
        childData = [{
            'link': '/product/' + str(father) + '/0/0/' + str(province) + '/' + str(city) + '/' + str(county) + '/1',
            'title': '全部',
            'f_id': 0,
            'active': 'on'
        }]
    else:
        childData = [{
            'link': '/product/' + str(father) + '/0/0/' + str(province) + '/' + str(city) + '/' + str(county) + '/1',
            'title': '全部',
            'f_id': 0,
            'active': ''
        }]
    for item in table_nav:
        if item['id'] == child:
            on = 'on'
        else:
            on = ''
        if len(p_message.objects.filter(m_c_id=item['id'])) > 0:
            childData.append({
                'link': '/product/' + str(father) + '/' + str(item['id']) + '/0/' + str(province) + '/' + str(
                    city) + '/' + str(county) + '/1',
                'title': item['p_name'],
                'f_id': item['p_id'],
                'active': on
            })
    return childData


# 生成一级城市列表
def citySelect(cityList, province, city_arr, father, child, last, city, county):
    for city_id in cityList['city_list']:
        if str(province)[0:2] == str(city_id)[0:2]:
            city_sql = p_message.objects.filter(m_address_city=city_id)
            if len(city_sql) > 0:
                if int(city) == int(city_id):
                    city_arr.append({
                        'title': cityList['city_list'][city_id],
                        'link': '/product/' + str(father) + '/' + str(
                            child) + '/' + str(last) + '/' + str(province) + '/' + city_id + '/0/1',
                        'active': 'on'
                    })
                else:
                    city_arr.append({
                        'title': cityList['city_list'][city_id],
                        'link': '/product/' + str(father) + '/' + str(
                            child) + '/' + str(last) + '/' + str(province) + '/' + city_id + '/0/1',
                        'active': ''
                    })
    return city_arr


# 生成二级城市列表
def countySelect(cityList, county_arr, father, child, last, province, city, county):
    for county_id in cityList['county_list']:
        if str(city)[0:4] == str(county_id)[0:4]:
            county_sql = p_message.objects.filter(m_address_belong=county_id)
            if len(county_sql) > 0:
                if int(county) == int(county_id):
                    county_arr.append({
                        'title': cityList['county_list'][county_id],
                        'link': '/product/' + str(father) + '/' + str(
                            child) + '/' + str(last) + '/' + str(province) + '/' + str(city) + '/' + county_id + '/1',
                        'active': 'on'
                    })
                else:
                    county_arr.append({
                        'title': cityList['county_list'][county_id],
                        'link': '/product/' + str(father) + '/' + str(
                            child) + '/' + str(last) + '/' + str(province) + '/' + str(city) + '/' + county_id + '/1',
                        'active': ''
                    })
    return county_arr


# 生成二级列表
def product_selcet_child(father, child, last, province, city, county):
    threeList = list(
        p_message.objects.filter(m_f_id=father, m_c_id=child).values('m_pz', 'id', 'm_c_id').annotate(avg=Avg("m_pz")))
    deep = Dedupe()
    threeList = list(deep.dedupe(threeList, key=lambda d: d['m_pz']))
    if last == 0:
        threeAll = [{
            'link': '/product/' + str(father) + '/' + str(child) + '/0/' + str(province) + '/' + str(city) + '/' + str(
                county) + '/1',
            'title': '全部',
            'f_id': 0,
            'active': 'on'
        }]
    else:
        threeAll = [{
            'link': '/product/' + str(father) + '/' + str(child) + '/0/' + str(province) + '/' + str(city) + '/' + str(
                county) + '/1',
            'title': '全部',
            'f_id': 0,
            'active': ''
        }]
    for item in threeList:
        if last == item['id']:
            on_last = 'on'
        else:
            on_last = ''
        threeAll.append({
            'link': '/product/' + str(father) + '/' + str(child) + '/' + str(item['id']) + '/' + str(
                province) + '/' + str(city) + '/' + str(county) + '/1',
            'title': item['m_pz'],
            'f_id': 0,
            'active': on_last
        })
    return threeAll


# 产品列表
def product(request, father, child, last, province, city, county, page):
    city_arr = None
    county_arr = None
    this = p_product.objects.get(id=father)
    # 加载城市列表
    file_name = "static/json/city.json"
    with open(file_name) as file_obj:
        cityList = json.load(file_obj)

    # 默认加载省级列表，只加载存在信息的省级
    if province == 0:
        province_arr = [{
            'title': '全部',
            'link': '/product/' + str(father) + '/' + str(child) + '/0/0/0/0/1',
            'active': 'on'
        }]
    else:
        province_arr = [{
            'title': '全部',
            'link': '/product/' + str(father) + '/' + str(child) + '/0/0/0/0/1',
            'active': ''
        }]
    for province_id in cityList['province_list']:
        province_sql = p_message.objects.filter(m_address_province=province_id)
        if len(province_sql) > 0:
            if province == int(province_id):
                province_arr.append({
                    'title': cityList['province_list'][province_id],
                    'link': '/product/' + str(father) + '/' + str(child) + '/0/' + province_id + '/0/0/1',
                    'active': 'on'
                })
            else:
                province_arr.append({
                    'title': cityList['province_list'][province_id],
                    'link': '/product/' + str(father) + '/' + str(child) + '/0/' + province_id + '/0/0/1',
                    'active': ''
                })
    # 每页多少信息
    recPerPage = 8
    select = {
    }

    if len(p_message.objects.filter(m_f_id=father)) > 0:
        select['m_f_id'] = father
        titleNav = [
            {
                'title': W_title,
                'link': '/',
                'line': ' > '
            },
            {
                'title': this.p_name,
                'link': '/product/' + str(father) + '/0/0/0/0/0/1',
                'line': ''
            }
        ]
    else:
        msg = urllib.parse.quote('该栏目下没有信息！')
        return HttpResponseRedirect('/message/' + msg)

    if len(p_message.objects.filter(m_c_id=child)) > 0:
        select['m_c_id'] = child
        this2 = p_product_child.objects.get(id=child)
        titleNav = [
            {
                'title': W_title,
                'link': '/',
                'line': ' > '
            },
            {
                'title': this.p_name,
                'link': '/product/' + str(father) + '/0/0/0/0/0/1',
                'line': ' > '
            },
            {
                'title': this2.p_name,
                'link': '/product/' + str(father) + '/' + str(child) + '/0/0/0/0/1',
                'line': ''
            }
        ]
    try:
        last_name = p_message.objects.get(id=last).m_pz
        if len(p_message.objects.filter(m_pz=last_name)) > 0:
            select['m_pz'] = last_name
        this2 = p_product_child.objects.get(id=child)
        titleNav = [
            {
                'title': W_title,
                'link': '/',
                'line': ' > '
            },
            {
                'title': this.p_name,
                'link': '/product/' + str(father) + '/0/0/0/0/0/1',
                'line': ' > '
            },
            {
                'title': this2.p_name,
                'link': '/product/' + str(father) + '/' + str(child) + '/0/0/0/0/1',
                'line': ' > '
            },
            {
                'title': last_name,
                'link': '/product/' + str(father) + '/' + str(child) + '/' + str(last) + '/0/0/0/1',
                'line': ''
            }
        ]
    except:
        None

    if len(p_message.objects.filter(m_address_province=province)) > 0:
        select['m_address_province'] = province

    if len(p_message.objects.filter(m_address_city=city)) > 0:
        select['m_address_city'] = city

    if len(p_message.objects.filter(m_address_belong=county)) > 0:
        select['m_address_belong'] = county

    print('select', select)
    if father != None:
        if isinstance(father, int) and isinstance(child, int) and isinstance(last, int) and isinstance(province,
                                                                                                       int) and isinstance(
            county, int) and isinstance(city, int) and isinstance(page, int):
            threeAll = None
            template = loader.get_template('home/product.html')
            # 生成一级二级列表 判断父级、子级是否被选中,来渲染模板列表的选中状态
            childData = FClist(father, child, province, city, county)
            threeAll = product_selcet_child(father, child, last, province, city, county)
            # 如果一级列表没有被选中，就查看地址是否被选中
            if city == 0:
                city_arr = [{
                    'title': '全部',
                    'link': '/product/' + str(father) + '/' + str(child) + '/0/' + str(province) + '/0/0/1',
                    'active': 'on'
                }]
            else:
                city_arr = [{
                    'title': '全部',
                    'link': '/product/' + str(father) + '/' + str(child) + '/0/' + str(province) + '/0/0/1',
                    'active': ''
                }]
            if county == 0:
                county_arr = [{
                    'title': '全部',
                    'link': '/product/' + str(father) + '/' + str(child) + '/0/' + str(
                        province) + '/' + str(city) + '/0/1',
                    'active': 'on'
                }]
            else:
                county_arr = [{
                    'title': '全部',
                    'link': '/product/' + str(father) + '/' + str(child) + '/0/' + str(
                        province) + '/' + str(city) + '/0/1',
                    'active': ''
                }]
            city_arr = citySelect(cityList, province, city_arr, father, child, last, city, county)
            county_arr = countySelect(cityList, county_arr, father, child, last, province, city, county)
            # 使用公共函数中的分页生成器
            print('select', select)
            mgsLsit = Paginator(p_message.objects.filter(**select).values().order_by('create_time'), recPerPage)
            handle = PageObject()
            pageData = handle.handlePage(mgsLsit, page, recPerPage)
            if pageData['count'] == 0:
                msg = urllib.parse.quote('该栏目下没有信息！')
                return HttpResponseRedirect('/message/' + msg)
            pageData['page_list'] = handlePhoto(pageData['page_list'])

            context = {
                'child': childData,  # 多级导航
                'list': pageData,
                'path': '/product/' + str(father) + '/' + str(child) + '/' + str(last) + '/' + str(
                    province) + '/' + str(city) + '/' + str(county) + '/',
                'titleNav': titleNav,
                'this': this.p_name,
                'threeAll': threeAll,
                'today': cdBaoJia(),
                'hot': hot(),
                'province': province_arr,
                'city': city_arr,
                'county': county_arr
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


# 管理已经发布消息
def Manage(request, page):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')
    recPerPage = 16
    template = loader.get_template('home/manage.html')
    pageData = Paginator(
        p_message.objects.filter(username=request.userInfo['username']).values().order_by('create_time'),
        recPerPage)
    handle = PageObject()
    pageData = handle.handlePage(pageData, page, recPerPage)
    pageData['page_list'] = handlePhoto(pageData['page_list'])
    context = {
        'list': pageData,
        'path': '/manage/',
    }
    return HttpResponse(template.render(context, request))


# 举报
def report(request):
    if request.GET.get('contact') == '' or request.GET.get('contact') == None:
        template = loader.get_template('home/message.html')
        context = {
            'msg': urllib.parse.unquote(urllib.parse.unquote('请填写联系方式'))
        }
        return HttpResponse(template.render(context, request))
    if request.GET.get('content') == '' or request.GET.get('content') == None:
        template = loader.get_template('home/message.html')
        context = {
            'msg': urllib.parse.unquote(urllib.parse.unquote('请填写问题描述'))
        }
        return HttpResponse(template.render(context, request))
    if request.userInfo == None:
        newReport = p_report(contact=request.GET.get('contact'), content=request.GET.get('content'), username=0)
        newReport.save()
    else:
        newReport = p_report(contact=request.GET.get('contact'), content=request.GET.get('content'),
                             username=request.userInfo['username'])
        newReport.save()
    template = loader.get_template('home/pass.html')
    context = {
        'msg': urllib.parse.unquote(urllib.parse.unquote('请填写问题描述'))
    }
    return HttpResponse(template.render(context, request))


# 报价管理
def ManagePrice(request, page):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')
    recPerPage = 16
    template = loader.get_template('home/managePrice.html')
    pageData = Paginator(
        p_message.objects.filter(username=request.userInfo['username']).values().order_by('create_time'),
        recPerPage)
    handle = PageObject()
    pageData = handle.handlePage(pageData, page, recPerPage)
    pageData['page_list'] = handlePhoto(pageData['page_list'])
    context = {
        'list': pageData,
        'path': '/managePrice/',
    }
    return HttpResponse(template.render(context, request))


def ManagePassword(request):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')
    template = loader.get_template('home/managePassword.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


# 保存城市json
def city(request):
    if request.method == 'POST':
        # data = json.loads(request.body)
        # file = open("static/json/city.json", "w")
        # file.write(json.dumps(data, ensure_ascii=False).decode('utf-8'))
        # file.close()
        return HttpResponse('1')
    else:
        file_name = "static/json/city.json"
        with open(file_name) as file_obj:
            city = json.load(file_obj)
        return HttpResponse(json.dumps(city, ensure_ascii=False))
