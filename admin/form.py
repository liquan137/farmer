from django import forms
from captcha.fields import CaptchaField


# 管理后端登陆表单生成
class LoginForm(forms.Form):
    user = forms.CharField(min_length=4, max_length=16, error_messages={
        "required": "账号不能为空",
        'min_length': '账号不能少于4位',
        'max_length': '账号不能超过16位',
    }, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'user', 'placeholder': '请输入账号'}))
    password = forms.CharField(min_length=4, max_length=16, error_messages={
        "required": "密码不能为空",
        'max_length': '密码不能超过16位',
        'min_length': '账号不能少于6位'
    }, widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': '请输入密码'}))
    captcha = CaptchaField(label='验证码')


# 设置表单
class SettingForm(forms.Form):
    title = forms.CharField(required=True, min_length=4, error_messages={
        "required": "网站标题不能为空",
        'min_length': '网站标题不能少于4字'
    })
    dec = forms.CharField(required=True, max_length=200, min_length=1, error_messages={
        "required": "描述不能为空",
        'max_length': '描述不能超过200字',
        'min_length': '描述不能低于1字'
    })
    keyword = forms.CharField(required=True, max_length=200, min_length=1, error_messages={
        "required": "关键词不能为空",
        'max_length': '关键词不能超过200字',
        'min_length': '关键词不能低于1字'
    })
    url = forms.CharField(required=False, max_length=200, min_length=1, error_messages={
        "required": "域名不能为空",
        'max_length': '域名不能超过200位',
        'min_length': '域名不能低于1位'
    })
    img_limit = forms.IntegerField(required=True, error_messages={
        "required": "图片限制不能为空",
    })
    article_limit = forms.IntegerField(required=True, error_messages={
        "required": "信息限制不能为空",
    })


# 绑定普通账号表单
class BindForm(forms.Form):
    username = forms.EmailField(required=True, error_messages={
        "required": "普通账号不能为空",
    })


# 修改管理员账号表单
class UpdateForm(forms.Form):
    username = forms.EmailField(required=True, error_messages={
        "required": "普通账号不能为空",
    })
    password = forms.CharField(required=True, error_messages={
        "required": "密码不能为空",
    })


# 删除管理员账号表单
class DeleteForm(forms.Form):
    id = forms.IntegerField(required=True, error_messages={
        "required": "索引ID不能为空",
    })


# 创建管理员账号表单
class CreateForm(forms.Form):
    user = forms.CharField(required=False, max_length=16, min_length=5, error_messages={
        "required": "账号不能为空",
        'max_length': '账号不能超过16位',
        'min_length': '账号不能低于5位'
    })
    password = forms.CharField(required=False, max_length=16, min_length=5, error_messages={
        "required": "密码不能为空",
        'max_length': '密码不能超过16位',
        'min_length': '密码不能低于5位'
    })
    auth = forms.IntegerField(error_messages={
        "required": "请选择权限级别",
    })


# 封禁普通账号表单
class AuthMenberForm(forms.Form):
    id = forms.EmailField(required=True, error_messages={
        "required": "普通账号不能为空",
    })
    auth = forms.IntegerField(error_messages={
        "required": "请选择封禁操作",
    })


# 修改密码普通账号表单
class PasswordMenberForm(forms.Form):
    id = forms.EmailField(required=True, error_messages={
        "required": "ID索引不能为空",
    })
    password = forms.CharField(required=False, max_length=16, min_length=5, error_messages={
        "required": "密码不能为空",
        'max_length': '密码不能超过16位',
        'min_length': '密码不能低于5位'
    })


# 绑定普通账号表单
class CreateMainForm(forms.Form):
    p_name = forms.CharField(required=True, error_messages={
        "required": "名称不能为空",
    })
    id = forms.IntegerField(required=True, error_messages={
        "required": "索引不能为空",
    })
