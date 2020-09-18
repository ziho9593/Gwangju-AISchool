from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.http import HttpResponse
from .modules import example
import json

# Create your views here.

def home(request):
    # classes = AiClass.objects.all()
    context = {
    }
    return render(request,'home.html', context)

def voice(request):
    # classes = AiClass.objects.all()

    example.main()#

    context = {
    }
    return render(request,'menu1.html', context)

def get_orderlist(request): # https://weejw.tistory.com/160 참고
    context = {}
    request_getdata = request.POST
    if request.is_ajax():
        data = request_getdata['getdata']
        return HttpResponse(json.dumps({'message':data}), 'application/json')
    
    return render(request, 'menu1.html', context)

def menu1(request):
    # classes = AiClass.objects.all()
    context = {
        "select_name": '불고기버거',
        "select_count": '1',
    }
    return render(request,'menu1.html', context)

def menu2(request):
    # classes = AiClass.objects.all()
    context = {
    }
    return render(request,'menu2.html', context)

def menu3(request):
    # classes = AiClass.objects.all()
    context = {
    }
    return render(request,'menu3.html', context)

def credit(request):
    # classes = AiClass.objects.all()
    context = {
    }
    return render(request,'credit.html', context)

def popup(request):
    # classes = AiClass.objects.all()
    context = {
    }
    return render(request,'popup.html', context)
