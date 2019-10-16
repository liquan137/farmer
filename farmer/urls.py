"""farmer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from home import views as home_views
from api import views as api_views
from admin import views as admin_views

urlpatterns = [
    path('message/<str:error>', home_views.message),  # 错误信息提示页面
    path('captcha/', include('captcha.urls')),  # 验证码
    path('refresh_captcha/', admin_views.refresh_captcha),  # 验证码刷新
    path('admin/login', admin_views.login),  # 后台登录接口
    path('admin/', admin_views.index),  # 后台主页
    path('admin/setting', admin_views.setting),  # 网站设置页面
    path('admin/sysUser/<int:page>', admin_views.sysUser),  # 管理员设置页面
    path('admin/sysBind', admin_views.sysBind),  # 管理员设置接口
    path('admin/user/<int:page>', admin_views.menber),  # 用户管理
    path('admin/menber', admin_views.sysMenber),  # 用户管理接口
    path('admin/authGetMenber', admin_views.authGetMenber),  # 用户审核获取信息接口
    path('admin/authMenber', admin_views.authMenber),  # 用户审核接口
    path('admin/main', admin_views.main),  # 主类目页面
    path('admin/category', admin_views.category),  # 品种页面
    path('admin/init', admin_views.initialize),  # 初始化系统
    path('admin/sysMain', admin_views.sysMain),  # 主类目接口
    path('admin/sysCategory', admin_views.sysCategory),  # 品种接口
    path('', home_views.index),  # 主页面
    path('list/<int:page>', home_views.List),  # 主页分页
    path('search/', home_views.search),  # 搜索
    path('quote/<int:child>/<int:page>', home_views.Quote),  # 报价
    path('logout/', home_views.logout),  # 退出登录
    path('login/', home_views.login),  # 登录
    path('register/', home_views.register),  # 注册
    path('registerReg/', home_views.registerReg),  # 完善资料
    path('authReg/', home_views.authReg),  # 认证
    path('report/', home_views.report),  # 认证
    path('forget/', home_views.forget),  # 找回密码
    path('publish/', home_views.publish),  # 发布信息
    path('city/', home_views.city),  # 城市写入接口
    path('publishDetail/<int:father>/<int:child>', home_views.publishDetail),  # 发布详细信息
    path('product/<int:father>/<int:child>/<int:last>/<int:province>/<int:city>/<int:county>/<int:page>',  # 产品筛选页面
         home_views.product),
    path('manage/<int:page>', home_views.Manage),  # 个人信息管理
    path('managePrice/<int:page>', home_views.ManagePrice),  # 报价页面
    path('password/', home_views.ManagePassword),  # 修改密码页面
    path('productDetail/<int:id>', home_views.productDetail),  # 详情页
    path('api/login', api_views.login),  # 登录接口
    path('api/register', api_views.register),  # 注册接口
    path('api/verifyEmail', api_views.verifyEmail),  # 获取验证码接口
    path('api/registerReg', api_views.registerReg),  # 完善注册接口
    path('api/forget', api_views.forget),  # 找回密码接口
    path('api/publish', api_views.publish),  # 发布信息接口
    path('api/uploadImg', api_views.uploadImg),  # 上传图片接口
    path('api/updatePrice', api_views.updatePrice),  # 修改报价接口
    path('api/updatePublish', api_views.updatePublish),  # 修改信息接口
    path('api/updatePassword', api_views.updatePassword),  # 修改密码接口
    path('api/authReg', api_views.authReg),  # 提交认证接口
]
