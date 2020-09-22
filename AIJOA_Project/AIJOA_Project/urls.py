"""AIJOA_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from AIJOA_App import views
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('menu1.html/', views.voice, name='voice'),
    path('menu2.html/', views.menu2, name='menu2'),
    path('menu3.html/', views.menu3, name='menu3'),
    re_path(r'^menu\d+[.]html/$', views.get_orderlist, name='getorder'),
    path('credit.html/', views.credit, name='credit'),
    path('popup.html/', views.popup, name='popup'),
    path('home.html', views.home, name='home'),
]
