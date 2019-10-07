from home.models import p_menber


class menber_check(object):

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get("user_id")
        if user_id:
            try:
                user = p_menber.objects.get(username=user_id)
                if user.nickname == '':
                    user.nickname = '<font><a href="/registerReg/" style="color:#F00">请完善资料</a></font>'
                else:
                    user.nickname = '<font color="#444">' + user.nickname + '</font>'
                request.userInfo = {
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
