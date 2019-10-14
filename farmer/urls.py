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
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from home import views as home_views
from api import views as api_views
from admin import views as admin_views

urlpatterns = [
    path('message/<str:error>', home_views.message),
    path('captcha/', include('captcha.urls')),
    path('refresh_captcha/', admin_views.refresh_captcha),
    path('admin/login', admin_views.login),
    path('admin/', admin_views.index),
    path('admin/setting', admin_views.setting),
    path('admin/sysUser/<int:page>', admin_views.sysUser),
    path('admin/sysBind', admin_views.sysBind),
    path('admin/user/<int:page>', admin_views.menber),
    path('admin/menber', admin_views.sysMenber),
    path('admin/main', admin_views.main),
    path('admin/category', admin_views.category),
    path('admin/init', admin_views.initialize),
    path('admin/sysMain', admin_views.sysMain),
    path('admin/sysCategory', admin_views.sysCategory),
    path('', home_views.index),
    path('list/<int:page>', home_views.List),
    path('quote/<int:child>/<int:page>', home_views.Quote),
    path('logout/', home_views.logout),
    path('login/', home_views.login),
    path('register/', home_views.register),
    path('registerReg/', home_views.registerReg),
    path('forget/', home_views.forget),
    path('publish/', home_views.publish),
    path('city/', home_views.city),
    path('publishDetail/<int:father>/<int:child>', home_views.publishDetail),
    path('product/<int:father>/<int:child>/<int:last>/<int:province>/<int:city>/<int:county>/<int:page>',
         home_views.product),
    path('manage/<int:page>', home_views.Manage),
    path('managePrice/<int:page>', home_views.ManagePrice),
    path('password/', home_views.ManagePassword),
    path('productDetail/<int:id>', home_views.productDetail),
    path('api/login', api_views.login),
    path('api/register', api_views.register),
    path('api/verifyEmail', api_views.verifyEmail),
    path('api/registerReg', api_views.registerReg),
    path('api/forget', api_views.forget),
    path('api/publish', api_views.publish),
    path('api/uploadImg', api_views.uploadImg),
    path('api/updatePrice', api_views.updatePrice),
    path('api/updatePassword', api_views.updatePassword),
]
# province, county, city
