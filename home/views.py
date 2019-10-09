from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *
from django.template import loader
import time

# Create your views here.

def index(request):
    template = loader.get_template('home/index.html')
    list = []
    list_data = {
        'm_title': '柑桔13886725378特早蜜桔，叶桔，蜜橘桔子',
        'm_address_belong': '1564',
        'create_time': '1564658781'
    }
    for i in range(0, 10):
        list.append(list_data)
    context = {
        'list': list
    }
    return HttpResponse(template.render(context, request))


def login(request):
    if request.userInfo != None:
        return HttpResponseRedirect(request.session.get('from'))
    template = loader.get_template('home/login.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def register(request):
    if request.userInfo != None:
        return HttpResponseRedirect(request.session.get('from'))
    template = loader.get_template('home/register.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def registerReg(request):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')
    template = loader.get_template('home/registerReg.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def logout(request):
    template = loader.get_template('home/logout.html')
    if request.userInfo != None:
        del request.session['user_id']
    context = {
    }
    return HttpResponse(template.render(context, request))

def forget(request):
    # if request.userInfo == None:
    #     return HttpResponseRedirect('/login')
    template = loader.get_template('home/forget.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def publish(request):
    if request.userInfo == None:
        return HttpResponseRedirect('/login')
    template = loader.get_template('home/publish.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
