from django.shortcuts import render

# Create your views here.

def home(request):

    return render(request, 'home.html')

def recipe(request):
    
    return render(request, 'recipe.html')

def recipe1(request):
    
    return render(request, 'recipe1.html')