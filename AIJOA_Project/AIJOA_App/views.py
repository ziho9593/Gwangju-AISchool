import sys
sys.path.append(r'C:\Users\NA\Desktop\Workspace\AI_Warmup_Project_0921\GJAI_WarmingUpProject\AIJOA_Project\AIJOA_App')

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect
from .modules import example
import json
import ft_gensim_v3 as gs
from django.conf import settings
from .models import *

# Create your views here.

def home(request):
    # classes = AiClass.objects.all()
    context = {
    }
    return render(request,'home.html', context)

def voice(request):
    # classes = AiClass.objects.all()
    
    print("voice 함수 실행")
    context = {}
    order_dict = gs.order_dict_init()
    print(order_dict)
    
    return render(request, 'menu1.html', {'orderdict': order_dict})

def get_orderlist(request): # https://weejw.tistory.com/160 참고
    print("get orderlist 함수 실행")
    context = {}
    request_getdata = request.POST
    if request.is_ajax():
        data = request_getdata['getdata']
        if data == '결제':
            return render(request,'menu2.html', context)
        # print(getattr(settings, 'DATABASES'))
        print(getattr(settings, 'MODEL'))
        resultword = gs.getwordsim(data,getattr(settings, 'MODEL'))
        if resultword == -1:
            return None
        else:
            return HttpResponse(json.dumps({'message':resultword}), 'application/json')
    
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
