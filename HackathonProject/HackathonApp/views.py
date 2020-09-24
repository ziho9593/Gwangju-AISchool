from django.shortcuts import render
from .modules.check import similiar_check
import json

# Create your views here.

def home(request):

    return render(request, 'home.html')

def recipe(request):
    file_path = './HackathonApp/data/material_list.json'
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    food1 = request.POST["food1"]
    food2 = request.POST["food2"]
    food3 = request.POST["food3"]
    food4 = request.POST["food4"]
    food5 = request.POST["food5"]
    food6 = request.POST["food6"]
    food7 = request.POST["food7"]
    food8 = request.POST["food8"]
    food9 = request.POST["food9"]

    user = [food1, food2, food3, food4, food5, food6, food7, food8, food9]
    temp = ''
    for u in user:
        temp += u + ' '
    temp = temp.rstrip()
    result1, result2, result3 = similiar_check(data, temp)

    context = {
        'result1': result1,
        'result2': result2,
        'result3': result3,
    }

    return render(request, 'recipe.html', context)


def recipe1(request):
    context = {
        "recipe1": "김치전",
    }
    
    return render(request, 'recipe1.html', context)


def recipe2(request):
    
    return render(request, 'recipe2.html')


def recipe3(request):
    
    return render(request, 'recipe3.html')