from django.shortcuts import render

# Create your views here.

def home(request):

    return render(request, 'home.html')

def recipe(request):
    food1 = request.POST["food1"]
    food2 = request.POST["food2"]
    food3 = request.POST["food3"]
    food4 = request.POST["food4"]
    food5 = request.POST["food5"]
    food6 = request.POST["food6"]
    food7 = request.POST["food7"]
    food8 = request.POST["food8"]
    food9 = request.POST["food9"]
    context = {
        "food1": food1,
        "food2": food2,
        "food3": food3,
        "food4": food4,
        "food5": food5,
        "food6": food6,
        "food7": food7,
        "food8": food8,
        "food9": food9,
        "recipe1": "김치전",
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