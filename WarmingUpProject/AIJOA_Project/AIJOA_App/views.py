import sys
# sys.path.append(r'C:\Users\NA\Desktop\Workspace\AI_Warmup_Project_0921\GJAI_WarmingUpProject\AIJOA_Project\AIJOA_App')
sys.path.append(r'C:\Users\HAN\Desktop\WarmingUpProject\AIJOA_Project\wiki.ko\wiki_ko_v3.model')

from django.shortcuts import render
from django.http import HttpResponse
import json
import ft_gensim_v3 as gs
from django.conf import settings

# Create your views here.

def home(request):
    context = {
    }
    return render(request,'home.html', context)


def voice(request):
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
        print(getattr(settings, 'MODEL'))
        resultword = gs.getwordsim(data,getattr(settings, 'MODEL'))
        if resultword == -1:
            return None
        else:
            return HttpResponse(json.dumps({'message':resultword}), 'application/json')
    
    return render(request, 'menu1.html', context)


def menu1(request):
    context = {
        "select_name": '불고기버거',
        "select_count": '1',
    }
    return render(request,'menu1.html', context)


def popup(request):
    context = {
    }
    return render(request,'popup.html', context)
