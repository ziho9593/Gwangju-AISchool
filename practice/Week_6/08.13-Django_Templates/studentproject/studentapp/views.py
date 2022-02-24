from django.shortcuts import render

class1_students = ['송두기', '김혜란', '김민형', '최준범', '박동호', '박승재']
# Create your views here.


def home(request):
    name = '송두기'

    return render(request, 'home.html', {'username': name})


def result(request):
    username = request.POST['username']
    is_exist = False

    if username in class1_students:
        is_exist = True

    return render(request, 'result.html', {'username': username, 'is_exist': is_exist})
