from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from .modules import example

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