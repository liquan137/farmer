from home.models import p_menber, p_product,p_menber_auth
from admin.models import p_sys, p_admin

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


# 查询并生成导航列表
def navList(request):
    data = list(p_product.objects.all().values())

    if len(request.path) == 1:
        nav = [{
            'link': '',
            'title': '首页',
            'active': 'active'
        }]
    else:
        nav = [{
            'link': '',
            'title': '首页',
            'active': ''
        }]

    if len(data) > 6:
        length = range(0, 6)
    else:
        length = range(0, len(data))
    for i in length:
        if 'product/' + str(data[i]['id']) in request.path:
            active = 'active'
        else:
            active = ''
        nav.append({
            'link': 'product/' + str(data[i]['id']) + '/0/0/0/0/0/1',
            'title': data[i]['p_name'],
            'active': active
        })
    if 'publish/' in request.path:
        nav.append({
            'link': 'publish/',
            'title': '农产品信息发布',
            'active': 'active'
        })
    else:
        nav.append({
            'link': 'publish/',
            'title': '农产品信息发布',
            'active': ''
        })
    return nav


def adminAuth(request, type):
    if type == 1:
        list = [
            {
                'title': '首页',
                'child':  False,
                'active': '',
                'link': '/admin',
                'block': 'none'
            },
            {
                'title': '系统设置',
                'child': [
                    {
                        'title': '网站设置',
                        'link': '/admin/setting',
                        'active': ''
                    },
                ],
                'active': '',
                'link': '',
                'block': 'none'
            },
            {
                'title': '账户管理',
                'child': [
                    {
                        'title': '系统管理员',
                        'link': '/admin/sysUser/1',
                        'active': ''
                    },
                    {
                        'title': '用户管理',
                        'link': '/admin/user/1',
                        'active': ''
                    },
                ],
                'active': '',
                'link': '',
                'block': 'none'
            },
            {
                'title': '类目管理',
                'child': [
                    {
                        'title': '主级类目',
                        'link': '/admin/main',
                        'active': ''
                    },
                    {
                        'title': '品种管理',
                        'link': '/admin/category',
                        'active': ''
                    },
                ],
                'active': '',
                'link': '',
                'block': 'none'
            }
        ]
    else:
        list = [
            {
                'title': '首页',
                'child': False,
                'active': '',
                'link': '/admin',
                'block': 'none'
            },
            {
                'title': '账户管理',
                'child': [
                    {
                        'title': '用户管理',
                        'link': '/admin/user/1',
                        'active': ''
                    },
                ],
                'active': '',
                'link': '',
                'block': 'none'
            },
            {
                'title': '类目管理',
                'child': [
                    {
                        'title': '品种管理',
                        'link': '/admin/category',
                        'active': ''
                    },
                ],
                'active': '',
                'link': '',
                'block': 'none'
            }
        ]
    for item in list:
        if len(item['link']) == 6:
            list[list.index(item)]['active'] = 'active'
        else:
            list[list.index(item)]['active'] = 'treeview'
        if item['child']:
            for items in item['child']:
                if items['link'] in request.path:
                    list[list.index(item)]['child'][list[list.index(item)]['child'].index(items)]['active'] = 'on'
                    list[list.index(item)]['active'] = 'treeview menu-open'
                    list[list.index(item)]['block'] = 'block'
                    list[list.index(item)]['active'] =  'treeview menu-open'
                else:
                    list[list.index(item)]['child'][list[list.index(item)]['child'].index(items)]['active'] = ''
    print(list)
    return list


class menber_check(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['from'] = request.META.get('HTTP_REFERER', '/')
        user_id = request.session.get("user_id")
        admin = request.session.get("admin")
        request.nav = navList(request)
        request.web = {
            'title': W_title,
            'dec': W_dec,
            'keyword': W_keyword
        }
        if admin:
            try:
                adminSql = p_admin.objects.get(user=admin)
                request.admin = {
                    'user': adminSql.user,
                    'username': adminSql.username,
                    'auth': adminSql.auth
                }
                request.admin_list = adminAuth(request, adminSql.auth)
                print(request.admin_list)
            except:
                request.admin = None
        else:
            request.admin = None
        if user_id:
            authType = ''
            try:
                user = p_menber.objects.get(username=user_id)
                if user.nickname == '':
                    user.nickname = '<font><a href="/registerReg/" style="color:#F00">请完善资料</a></font>'
                else:
                    user.nickname = '<font color="#444">' + user.nickname + '</font>'

                try:
                    auth = p_menber_auth.objects.get(username=user_id)
                    authType = auth.auth
                except:
                    authType = 0
                request.userInfo = {
                    'id': user.id,
                    'nickname': user.nickname,
                    'username': user.username,
                    'type': user.type,
                    'company_name': user.company_name,
                    'auth': authType
                }
            except:
                request.userInfo = None
        else:
            request.userInfo = None

        response = self.get_response(request)

        return response
