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
from home import views as home_views
from api import views as api_views
from admin import views as admin_views

urlpatterns = [
    path('captcha/', include('captcha.urls')),
    path('refresh_captcha/', admin_views.refresh_captcha),
    path('admin/login', admin_views.login),
    path('', home_views.index),
    path('logout/', home_views.logout),
    path('login/', home_views.login),
    path('register/', home_views.register),
    path('registerReg/', home_views.registerReg),
    path('forget/', home_views.forget),
    path('publish/', home_views.publish),
    path('api/login', api_views.login),
    path('api/register', api_views.register),
    path('api/verifyEmail', api_views.verifyEmail),
    path('api/registerReg', api_views.registerReg),
    path('api/forget', api_views.forget),
]
