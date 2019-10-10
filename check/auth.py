from home.models import p_menber, p_product


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
            'link': 'product/' + str(data[i]['id'])+'/1',
            'title': data[i]['p_name'],
            'active': active
        })
    if 'publish/' in request.path:
        nav.append({
            'link': 'publish/',
            'title': '产品发布',
            'active': 'active'
        })
    else:
        nav.append({
            'link': 'publish/',
            'title': '农产品信息发布',
            'active': ''
        })
    return nav


class menber_check(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['from'] = request.META.get('HTTP_REFERER', '/')
        user_id = request.session.get("user_id")
        request.nav = navList(request)
        if user_id:
            try:
                user = p_menber.objects.get(username=user_id)
                if user.nickname == '':
                    user.nickname = '<font><a href="/registerReg/" style="color:#F00">请完善资料</a></font>'
                else:
                    user.nickname = '<font color="#444">' + user.nickname + '</font>'
                request.userInfo = {
                    'id': user.id,
                    'nickname': user.nickname,
                    'username': user.username,
                    'type': user.type,
                    'company_name': user.company_name
                }
            except:
                request.userInfo = None
        else:
            request.userInfo = None

        response = self.get_response(request)

        return response
