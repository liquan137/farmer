from django.shortcuts import render
from django.http import HttpResponse
from home.models import models as home_model
from django.template import loader


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
